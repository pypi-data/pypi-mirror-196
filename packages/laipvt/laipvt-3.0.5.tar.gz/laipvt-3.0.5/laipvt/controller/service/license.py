from __future__ import absolute_import
from __future__ import unicode_literals
import os, json
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.handler.middlewarehandler import EtcdConfigHandler
from laipvt.sysutil.util import path_join, log, status_me
from laipvt.controller.middleware.etcd import EtcdController
from laipvt.helper.errors import Helper
from laipvt.sysutil.command import GET_LICENSE_POD_INFO, RESTART_DEPLOYMENT, RESTART_DEPLOYMENT_ALL, LICENSE_QRCODE_CMD, \
    GET_LICENSE_QRCODE_IMG
from laipvt.model.cmd import DockerModel, DockerImageModel
from laipvt.model.server import runcmd


class LicenseController(ServiceInterface):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(LicenseController, self).__init__(check_result, service_path)
        self.nginx_template = path_join(self.templates_dir, "nginx/nginx-license.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-license.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-license.conf")
        self.imagePkgPath = image_pkg_path

    @status_me("license")
    def prepare_license_data_file(self, is_renew=False, **kwargs):
        self.prepare_data(project=self.project)

    def clear_etcd(self):
        etcd = EtcdController(self.check_result, EtcdConfigHandler(), "")
        etcd.reset()

    def restart_service(self):
        get_pod_info_cmd = GET_LICENSE_POD_INFO.format("license-manager")
        res = self._exec_command_to_host(cmd=get_pod_info_cmd, server=self.harbor_hosts[0], check_res=True)
        if not (res["code"] == 0 and "Running" in res["stdout"]):
            log.error("license service not found:{}".format(get_pod_info_cmd))
            exit(2)
        restart_deployment_cmd = RESTART_DEPLOYMENT_ALL.format("license")
        self._exec_command_to_host(cmd=restart_deployment_cmd, server=self.harbor_hosts[0], check_res=True)

        restart_all_deployment_cmd = [
            RESTART_DEPLOYMENT_ALL.format("mage"),
            RESTART_DEPLOYMENT_ALL.format("rpa")
        ]
        self._exec_command_to_host(cmd=restart_all_deployment_cmd, server=self.harbor_hosts[0], check_res=True)

    def renew_license(self, license_file):
        self.prepare_license_data_file(is_renew=True, license_file=license_file)
        self.restart_service()

    @status_me("license")
    def runqrcode(self):
        path = self.imagePkgPath
        image_name = path_join(path, "license_feature.tar")
        try:
            DockerModel().load(image_name)
        except Exception as e:
            log.error(e)
        log.info(image_name)
        srcConfig = path_join(self.deploy_dir, "license_config/License/laiye-saas-license-manager.conf")
        destConfig = "/home/works/program/conf/conf.yaml"

        code, image = runcmd(GET_LICENSE_QRCODE_IMG)
        image = image.stdout

        cmd = LICENSE_QRCODE_CMD.format(
            self.harbor_hosts[0].ipaddress,
            srcConfig, destConfig, path, path, image.replace("\n", "").replace("\r", ""), path
        )
        # self._exec_command_to_host(cmd, server=self.harbor_hosts[0], check_res=True)
        log.info(cmd)
        code, res = runcmd(cmd)
        if code != 0:
            log.error("run cmd error:", res)
        headStr = res.stdout.find("QR Code")
        tailStr = res.stdout.find(".jpg") + 5
        if res.stdout[headStr:tailStr] == "":
            log.debug("未获取到QR CODE字段，请手动执行生成特征码命令查看具体原因")
            log.info(cmd)
        else:
            log.info("请将服务器中特征码照片文件下载到本地并上传至来也内部私有发货平台进行授权文件申请，特征码文件存放位置: {}".format(res.stdout[headStr:tailStr]))

    @status_me("license")
    def push_license_images(self):
        self.push_images(self.project)

    @status_me("license")
    def init_license_mysql(self):
        self.init_mysql()

    @status_me("license")
    def start_license_service(self):
        self._create_namespace(namespaces=self.namespaces, istio_injection_namespaces="")
        self.start_service(project=self.project, version=self.private_deploy_version)

    @status_me("license")
    def license_proxy_on_nginx(self):
        self.proxy_on_nginx(self.nginx_template, self.nginx_tmp, self.nginx_file_remote)

    @status_me("license")
    def deploy_license_configmap(self):
        self.deploy_all_configmap()

    @status_me("license")
    def deploy_license_istio(self):
        self.deploy_istio()

    @status_me("license")
    def init_license_entuc_clients(self):
        self.init_usercenter_clients(project="license")

    @status_me("license")
    def init_minio_license(self):
        self.init_minio()

    def run(self, force=False):
        self.push_license_images()
        self.deploy_license_configmap()
        self.init_license_mysql()
        self.init_minio_license()
        self.deploy_license_istio()
        self.middleware_cfg["base"] = self.read_base_yml()["base"]
        if self.middleware_cfg.base["usercenter"] == "entuc":
            self.runqrcode()
        self.start_license_service()
        self.prepare_license_data_file()
        self.project_pod_check()

    def rebuild_data(self):
        self.init_license_mysql.set_force(True)
        self.init_license_mysql()
        self.init_minio_license.set_force(True)
        self.init_minio_license()
        if self.middleware_cfg.base.usercenter == "entuc":
            self.runqrcode()
        self.deploy_license_istio.set_force(True)
        self.deploy_license_istio()
        self.restart_service()
        self.project_pod_check()

    def upgrade(self):
        log.info("服务开始upgrade %s", self.project)
        try:
            self.push_images("license")
            self.upgrade_service("license")
            self.project_pod_check()
        except Exception as e:
            log.error(e)
            exit(2)

    def runQrcode(self):
        self.runqrcode()
