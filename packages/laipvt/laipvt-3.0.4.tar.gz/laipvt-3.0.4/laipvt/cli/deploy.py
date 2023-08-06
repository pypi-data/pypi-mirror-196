#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
import os
import re
import json
import time
from functools import reduce

import yaml

from laipvt.controller.middleware.nacos import NacosController
from laipvt.controller.middleware.pgsql import PgSqlController
from laipvt.controller.service.entbs import EntbsController
from laipvt.controller.service.entcc import EntccController
from laipvt.controller.service.entiap import EntiapController
from laipvt.controller.service.iapcloud import IapCloudController
from laipvt.controller.service.ucenter import UCenterController
from laipvt.controller.service.wep import WepController
from laipvt.helper.errors import Helper
from laipvt.sysutil.gvalue import CHECK_FILE, PROJECT_INFO_FILE, LAIPVT_LOG_PATH, LAIPVT_LOG_NAME, LAIPVT_LOG_LEVEL, \
    LOG_TO_TTY, SPECIFY_DEBUG_FILE, LAIPVT_BASE_DIR
from laipvt.sysutil.log import Logger
from laipvt.sysutil.relation import find_module_by_key, find_single_module_by_key
from laipvt.sysutil.util import find, log, run_local_cmd, path_join, get_free_disk
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.handler.packagehandler import DeployPackageHandler, ServicePackageHandler
from laipvt.controller.kubernetes.kube import KubeController
from laipvt.controller.middleware.harbor import HarborController
from laipvt.controller.middleware.nginx import NginxController
from laipvt.controller.middleware.etcd import EtcdController
from laipvt.controller.middleware.minio import MinioController
from laipvt.controller.middleware.redis import RedisController
from laipvt.controller.middleware.mysql import MysqlController
from laipvt.controller.middleware.elasticsearch import EsController
from laipvt.controller.middleware.rabbitmq import RabbitmqController
from laipvt.controller.middleware.siber import SiberController
from laipvt.controller.service.license import LicenseController
from laipvt.controller.service.mage import MageController
from laipvt.controller.service.ocr_standard import OcrStandardController
from laipvt.controller.service.nlp import NlpController
from laipvt.controller.service.seal import SealController
from laipvt.controller.service.captcha import CaptchaController
from laipvt.controller.service.commander import CommanderController
from laipvt.controller.service.ocr import OcrController
from laipvt.controller.service.chatbot import ChatbotController
from laipvt.controller.service.usercenter import UserCenterController
from laipvt.controller.service.dataservice import DataServiceController
from laipvt.controller.service.notice import NoticeController
from laipvt.controller.service.ocr_text import OcrTextController
from laipvt.controller.service.ocr_text_cpu import OcrTextCpuController
from laipvt.controller.service.ocr_table import OcrTableController
from laipvt.controller.service.ocr_idcard_server import OcrIdcardController
from laipvt.controller.service.rpa_collaboration import RpaCollaborationController
from laipvt.controller.service.ocr_layout_analysis import OcrLayoutAnalysisController
from laipvt.controller.service.ocr_bizlicense import OcrBizlicenseController
from laipvt.controller.service.nlp_layoutlm import NlpLaYouTlmController
from laipvt.controller.middleware.monitor import MonitorController
from laipvt.controller.middleware.keepalived import KeepalivedController
from laipvt.handler.middlewarehandler import EtcdConfigHandler, MysqlConfigHandler, EsConfigHandler, \
    MinioConfigHandler, RabbitmqConfigHandler, RedisConfigHandler, HarborConfigHandler, NginxConfigHandler, \
    IdentityConfigHandler, SiberConfigHandler, OcrConfigHandler, MonitorConfigHandler, KeepalivedConfigHandler, \
    NacosConfigHandler, PgSqlConfigHandler
from laipvt.sysutil.util import write_to_file, read_form_json_file, gen_https_self_signed_ca, modify_umask
from laipvt.sysutil.kube_common import wait_pod_running
from laipvt.sysutil.print_info import print_project_info
from laipvt.sysutil.check import is_pre_check, check_use_https_ca, check_https_ca_self_signed
from multiprocessing import Pool


def save_specify_lines(lines):
    with open(SPECIFY_DEBUG_FILE, "w+", encoding="utf-8") as f:
        for line in lines:
            f.write(line)


def check_package_size(pkg, pkg_dir):
    if not os.path.exists(pkg):
        log.info("安装包不存在 :{}".format(pkg))
        exit(0)
    if os.path.exists(pkg_dir):
        return
    file_size = os.path.getsize(pkg)
    free_size = get_free_disk(pkg)
    size_g = (1024 * 1024 * 1024)
    if free_size < file_size * 3:
        log.info(
            "安装包文件大小为{}G,目录大小为{}G,解压后大小不满足要求.请移动安装包".format(int(file_size / size_g), int(free_size / size_g)))
        exit(0)
    return


def deploy_main(args):
    # 获取前置检查结果

    check_result_file = CHECK_FILE
    check_result = CheckResultHandler(check_result_file)
    parse_package, pkg, id, pkg_dir = parse_args(args, check_result)
    unpack_common_first(check_result, parse_package, pkg_dir)

    if args.which == "install":
        # install kubernetes
        if args.Specify is not None and args.Specify != "":
            save_specify_lines(args.Specify.split(","))
        if not args.Force:
            if not is_pre_check():
                print(Helper().PRECHECK_FAILED)
                exit(2)
        harbor, nginx = base_process_install(check_result=check_result, parse_package=parse_package, PKG_DIR=pkg_dir)
        all_run_services, run_middlewares = get_services(check_result=check_result, parse_package=parse_package,
                                                         PKG_DIR=pkg_dir)
        install_k8s_component(check_result, parse_package)
        nginx.renew_apiserver_config()
        install_interceptor(all_run_services, run_middlewares, check_result)
        log.info("install k8s finish")

        run_services = {}
        if args.services is not None and args.services != "":
            specify_services = args.services.split(",")
            for name, service in all_run_services.items():
                if name in specify_services:
                    run_services[name] = service
        else:
            run_services = all_run_services

        log.info("安装的services {} 安装的中间件 {}".format(run_services.keys(), run_middlewares.keys()))

        for middleware in run_middlewares.values():
            middleware.deploy()
        for name, deploy_service in run_services.items():
            deploy_service.run(args.Force)
        # 先after deploy
        after_deploy_main(run_services,all_run_services)
        result_test = []

        # auto test
        if args.AutoTest is True:
            for name, deploy_service in run_services.items():
                result_test.append(deploy_service.app_test())
            resetdata_all(run_middlewares,all_run_services)
        if not wait_pod_running:
            print("kubernetes集群中有pod启动状态异常，请检查: kubectl get pod -A")
            exit(2)

    if args.which == "resetdata":
        run_services, run_middlewares = get_services(check_result=check_result, parse_package=parse_package,
                                                     PKG_DIR=pkg_dir)
        resetdata_all(run_services, run_middlewares)
    if args.which == "apptest":
        run_services, run_middlewares = get_services(check_result=check_result, parse_package=parse_package,
                                                     PKG_DIR=pkg_dir)
        apptest(args, run_services, run_middlewares)
    if args.which == "monitor":
        if args.ELK:
            add_monitor(check_result=check_result)
        if args.Keepalive:
            add_keepalive(check_result=check_result)
    if args.which == "upgrade":
        run_services, run_middlewares = get_services(check_result=check_result, parse_package=parse_package,
                                                     PKG_DIR=pkg_dir)
        services = []
        if args.services is None:
            log.info("没有设置服务项,则是所有服务")
            services = run_services
        else:
            services = args.services.split(",")
        upgrade_services = []
        upgrade_middlewares_names = []
        upgrade_middlewares = []
        for name, service in run_services.items():
            if name in services:
                upgrade_services.append(service)
                middleware = service.service_path.config.middleware
                upgrade_middlewares_names.extend(middleware)

        for middleware_name in upgrade_middlewares_names:
            upgrade_middlewares.append(run_middlewares[middleware_name])

        log.info(
            "upgrade services:{},match upgrade_services {},upgrade middlewares {}".format(services, upgrade_services,
                                                                                          upgrade_middlewares))
        upgrade(upgrade_services, upgrade_middlewares)
        after_deploy_main(run_services,run_services)


def install_interceptor(all_run_services, run_middlewares, check_result):
    for name in all_run_services:
        service = all_run_services[name]
        service.write_config_to_dir()
    update_args = {}
    if "entuc" in all_run_services:
        update_args["usercenter"] = "entuc"
    if "ucenter" in all_run_services:
        update_args["usercenter"] = "ucenter"
    update_args["lang"] = check_result.config.lang
    if check_result.config.deploy_https:
        update_args["scheme"] = "https"
    else:
        update_args["scheme"] = "http"
    update_args["laiye"] = "laiyelove"
    update_base_configs(update_args)


def update_base_configs(update_values: {}):
    base_yaml = path_join(LAIPVT_BASE_DIR, "middleware", "base.yaml")
    if os.path.exists(base_yaml):
        with open(base_yaml, "r") as f:
            base_cfg = yaml.load(f.read())
            base_cfg["base"] = {**base_cfg["base"], **update_values}
        with open(base_yaml, "w") as f:
            f.write(yaml.dump(base_cfg))


def after_deploy_main(run_services,all_run_services=None):
    # 打印帮助信息
    # 这边路由会相互干扰。所以默认以entuc的为准
    if all_run_services is None:
        all_run_services=run_services

    if "entuc" in run_services:
        deploy_service = run_services["entuc"]
        deploy_service.deploy_istio()
        deploy_service.project_pod_check_()
        deploy_service.init_entuc_user.set_force(True)
        deploy_service.init_entuc_user(True)

    if "ucenter" in run_services:
        deploy_service = run_services["ucenter"]
        deploy_service.deploy_istio()
        deploy_service.project_pod_check_()
        deploy_service.init_ucenter_user.set_force(True)
        deploy_service.init_ucenter_user(True)

    # 重启entcmd免得出问题
    if "entcmd" in run_services:
        time.sleep(10)
        deploy_service = run_services["entcmd"]
        deploy_service.restart_service()
        deploy_service.project_pod_check_()

    # 重启entcc免得注册不上
    if "entcc" in run_services:
        time.sleep(10)
        deploy_service = run_services["entcc"]
        deploy_service.restart_service()
        deploy_service.project_pod_check_()

    # 重启服务保证通过
    if "iap-cloud" in run_services:
        deploy_service = run_services["iap-cloud"]
        deploy_service.auto_config_set_iap()
        deploy_service.restart_service("iap-cloud")
        deploy_service.restart_service("iap-cloud-tasks")

    # 重启服务保证通过
    if "entiap" in run_services:
        deploy_service = run_services["entiap"]
        deploy_service.restart_service("entiap")

    if "mage_core" in run_services:
        deploy_service = run_services["mage_core"]
        deploy_service.deploy_istio()

    if "ocr_text" in run_services:
        if "mage_core" in all_run_services:
            mage_core = run_services["mage_core"]
            mage_core.patch_text_cpu_configmap("gpu")

    if "ocr_text_cpu" in run_services:
        if "mage_core" in all_run_services:
            mage_core = run_services["mage_core"]
            mage_core.patch_text_cpu_configmap("cpu")

    print_project_info()


def upgrade(upgrade_services, upgrade_middlewares):
    for middleware in upgrade_middlewares:
        middleware.deploy()
    for deploy_service in upgrade_services:
        deploy_service.upgrade()


def parse_args(args, check_result):
    # 设置umask
    modify_umask(check_result=check_result, is_set=True)
    if not check_use_https_ca():
        print(Helper().HTTPS_CERTS_ERROR)
        exit(2)

    if check_https_ca_self_signed():
        gen_https_self_signed_ca()

    pkg_path = False
    if not os.path.exists(args.tarFile):
        cwd = [os.getcwd(), check_result.deploy_dir]
        for d in cwd:
            pkg_path = find(d, args.tarFile, file=True)
            if pkg_path:
                break
    else:
        pkg_path = os.path.join(os.getcwd(), args.tarFile)
    if not pkg_path:
        print(Helper().FILE_NOT_FOUND)
        exit(2)

    PKG = os.path.dirname(pkg_path)
    ID = os.path.basename(pkg_path).split(".")[0]
    PKG_DIR = pkg_path.split(".")[0]

    check_package_size(args.tarFile, PKG_DIR)

    # 将项目ID和path写入文件缓存
    project_dict = {"PKG": PKG, "ID": ID}
    write_to_file(PROJECT_INFO_FILE, json.dumps(project_dict, indent=4))
    deploy_package = DeployPackageHandler(PKG, ID, check_result)
    if not os.path.exists(PKG_DIR):
        deploy_package.unpack()

    # 解析部署包
    parse_package = deploy_package.parse()
    return parse_package, PKG, ID, PKG_DIR


def unpack_common_first(check_result, parse_package, PKG_DIR):
    kubernetes_package = parse_package.kubernetes
    middleware_package = parse_package.middleware
    harbor_package = parse_package.harbor

    if not os.path.exists(os.path.join(PKG_DIR, "kubernetes")):
        kubernetes_package.kubernetes_unpack()
    if not os.path.exists(os.path.join(PKG_DIR, "middleware")):
        middleware_package.unpack()
    if not os.path.exists(os.path.join(PKG_DIR, "harbor")):
        harbor_package.unpack()


def base_process_install(check_result, parse_package, PKG_DIR):
    kubernetes_package = parse_package.kubernetes
    middleware_package = parse_package.middleware
    harbor_package = parse_package.harbor

    # install harbor
    harbor_path = harbor_package.parse().harbor
    harbor_config = HarborConfigHandler()
    harbor = HarborController(check_result, harbor_config, harbor_path)
    harbor.install_harbor()

    kubernetes_package.push_images()
    middleware_package.push_images()
    # solve the nginx before load

    # install nginx
    nginx_package = middleware_package.parse().nginx
    nginx_config = NginxConfigHandler()
    nginx = NginxController(check_result, nginx_config, nginx_package)
    nginx.install_nginx()

    return harbor, nginx


def install_k8s_component(check_result, parse_package):
    kubernetes_package = parse_package.kubernetes
    kube_info = kubernetes_package.parse()
    kube = KubeController(check_result, kube_info)
    kube.add_hosts()
    kube.system_prepare()
    kube.init_primary_master()
    kube.cp_kube_config()
    kube.kube_completion()
    kube.join_master()
    kube.join_node()
    kube.create_namespace()
    kube.install_network_plugin()
    kube.install_helm()
    kube.install_istio()
    kube.install_rook()
    kube.install_nvidia_device_plugin()
    kube.install_chaosblade()


def resetdata_middleware(middleware_services):
    for name, middleware in middleware_services.items():
        middleware.clean_and_reset()


def resetdata_all(run_middlewares, run_services):
    log.info("run_middleware:{} run_serviecs:{}".format(run_middlewares,run_services))
    resetdata_middleware(run_middlewares)
    resetdata_services(run_services)
    after_deploy_main(run_services)


def resetdata_services(service_package):
    for name, service in service_package.items():
        service.rebuild_data()


def get_services(check_result, parse_package, PKG_DIR):
    run_services = {}
    run_middlewares = {}
    services = {
        "license": LicenseController,
        "mage": MageController,
        "entcmd": CommanderController,
        "chatbot": ChatbotController,
        "nlp": NlpController,
        "captcha": CaptchaController,
        "ocr": OcrStandardController,
        "ocr_seal": SealController,
        "entuc": UserCenterController,
        "dataservice": DataServiceController,
        "notice": NoticeController,
        "rpa-collaboration": RpaCollaborationController,
        "entcc": EntccController,
        "entbs": EntbsController,
        "entiap": EntiapController,
        "iap-cloud": IapCloudController,
        "ucenter": UCenterController,
        "ocr_core": MageController,
        "ocr_text": OcrTextController,
        "ocr_self_text_core": OcrTextCpuController,
        "ocr_table": OcrTableController,
        "ocr_idcard": OcrIdcardController,
        "ocr_layout_analysis": OcrLayoutAnalysisController,
        "ocr_bizlicense": OcrBizlicenseController,
        "ocr_vehlicense": OcrStandardController,
        "ocr_invoice": OcrStandardController,
        "nlp_layoutlm": NlpLaYouTlmController,
        "nlp_layout_extract": NlpLaYouTlmController,
        "ocr_layout_analysis": OcrStandardController,
        "ocr_text_cpu": OcrTextCpuController,
        "nlp_address": NlpLaYouTlmController,
        "nlp_text_classifier": NlpLaYouTlmController,
        "wep": WepController,
    }
    middlewares = {
        "etcd": (EtcdConfigHandler, EtcdController),
        "minio": (MinioConfigHandler, MinioController),
        "redis": (RedisConfigHandler, RedisController),
        "mysql": (MysqlConfigHandler, MysqlController),
        "elasticsearch": (EsConfigHandler, EsController),
        "rabbitmq": (RabbitmqConfigHandler, RabbitmqController),
        "nacos": (NacosConfigHandler, NacosController),
        "postgresql": (PgSqlConfigHandler, PgSqlController)
    }
    service_package = []
    middleware_package = parse_package.middleware
    middleware_list = []

    dir_dict = {}
    for i in os.listdir(PKG_DIR):
        project_name_find = re.findall(r'(.*)_\d{0,3}\.\d{0,3}-\d{14}(.*?).tar.gz', i)
        if project_name_find:
            # 就是满足固定规则后。key为服务名称。值为i
            dir_dict[project_name_find[0][0]] = i
            service_handler = ServicePackageHandler(PKG_DIR, project_name_find[0][0])
            service_handler.unpack(package_name=i)
            service_package.append(service_handler)

    for s in service_package:
        service_parse = s.parse()
        component = service_parse.config.component
        log.info(
            "project:{} component:{} namespace:{}".format(s.project_name, component, service_parse.config.namespace))
        if component == "":
            component = service_parse.project_name
        if component in services.keys():
            deploy_service = services[component](check_result, service_parse, PKG_DIR)
            deploy_service.write_config_to_dir()
            run_services[s.project_name] = deploy_service
            middleware_list.extend(service_parse.config.middleware)
        else:
            log.info("component not found:{}".format(component))
            if "ocr" in component:
                deploy_service = OcrStandardController(check_result, service_parse, PKG_DIR)
            elif "nlp" in component:
                deploy_service = NlpController(check_result, service_parse, PKG_DIR)
            else:
                log.info("component not found:{},and exit".format(component))
            run_services[s.project_name] = deploy_service
            middleware_list.extend(service_parse.config.middleware)

    for mid in list(set(middleware_list)):
        path = middleware_package.parse()[mid]
        config = middlewares[mid][0]()
        middleware = middlewares[mid][1](check_result, config, path)
        run_middlewares[mid] = middleware

    # 还是得排序。先安装license之类的
    order_service = sorted(run_services.items(),
                           key=lambda x: int(find_single_module_by_key(x[1].component).get("id", 999)))
    run_services = {k[0]: run_services[k[0]] for k in order_service}
    return run_services, run_middlewares


def add_monitor(check_result):
    project_dict = read_form_json_file(PROJECT_INFO_FILE)
    deploy_package = DeployPackageHandler(project_dict["PKG"], project_dict["ID"], check_result)
    parse_package = deploy_package.parse()
    middleware_package = parse_package.middleware

    monitor_path = middleware_package.parse().monitor
    monitor_config = MonitorConfigHandler()
    monitor = MonitorController(check_result, monitor_config, monitor_path)
    monitor.deploy_monitor()


def add_keepalive(check_result):
    project_dict = read_form_json_file(PROJECT_INFO_FILE)
    deploy_package = DeployPackageHandler(project_dict["PKG"], project_dict["ID"], check_result)
    parse_package = deploy_package.parse()
    middleware_package = parse_package.middleware

    keepalive_path = middleware_package.parse().keepalived
    keepalive_config = KeepalivedConfigHandler()
    keepalive = KeepalivedController(check_result, keepalive_config, keepalive_path)
    keepalive.deploy_keepalived()


def apptest(args, run_services, run_middleware):
    if args.Service is not None and args.Service != "" and run_services[args.Service] is not None:
        service = run_services[args.Service]
        service.app_test()
    else:
        map(lambda x: x[1].app_test(x[1].project), run_services)
    if args.ResetData:
        resetdata_all(run_middleware,run_services)
