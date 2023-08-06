from __future__ import absolute_import
from __future__ import unicode_literals

import functools
import os
import traceback
import json
import time

import nacos
import requests
import yaml
from requests.adapters import HTTPAdapter
from minio import Minio
from laipvt.model.cmd import DockerImageModel, DockerModel
from laipvt.model.harbor import HarborModel
from laipvt.helper.exception import UtilsError
from laipvt.handler.confighandler import CheckResultHandler, ServerHandler, PvtAdminConfigHandler
from laipvt.handler.middlewarehandler import HarborConfigHandler
from laipvt.sysutil.gvalue import LAIPVT_BASE_DIR
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, ssh_obj, to_object, walk_sql_path
from laipvt.handler.middlewarehandler import MiddlewareConfigHandler
from laipvt.model.cmd import ComposeModel, KubeModel
from laipvt.model.sql import SqlModule, PgSqlModule
from laipvt.model.server import runcmd
from laipvt.helper.errors import Helper
from laipvt.sysutil.command import HELM_UPGRADE_INSTALL_CPU, HELM_UPGRADE_INSTALL_GPU, CREATE_NS, ISTIO_INJECTION_NS, \
    KUBECTL_APPLY, MKDIR_DIR, CHMOD_777, \
    HELM_LIST, HELM_INSTALL_CPU, HELM_INSTALL_GPU, CREATE_DB, INIT_IDENTITY_USER, HELM_INSTALL_TF_SERVICE, \
    HELM_UPGRADE_INSTALL, GET_PVC_VOLUMENAME_CMD, RESTART_DEPLOYMENT, TEST_SERVICE_CMD, GET_NFS_NODE_IP_CMD


class ServiceInterface:
    def __init__(self, check_result: CheckResultHandler, service_path):
        """
        check_result: 对象，前置检查结果
        service_path: 对象，服务进程详情
        """
        self.istio_injection_namespaces = []
        self.check_result = check_result
        self.service_path = service_path

        self.admin_config_dir = os.path.dirname(os.path.dirname(self.service_path.template))
        self.admin_config_name = list(filter(lambda x: x.endswith("config.json"), os.listdir(self.admin_config_dir)))
        self.admin_config = PvtAdminConfigHandler(path_join(self.admin_config_dir, self.admin_config_name[0]))

        self.middleware_servers = self.check_result.servers
        self.middleware_server_list = self.middleware_servers.get_role_ip("master")

        self.middleware_cfg = to_object(MiddlewareConfigHandler("mysql").get_all_config_with_check_result())
        for k, v in self.middleware_cfg.items():
            if "str" in str(type(self.middleware_cfg[k])):
                # log.info("middleware cfg {} not exists".format(k))
                continue
            ipaddress = self.middleware_cfg[k].get("ipaddress", "")
            if ipaddress is not None and ipaddress != "":
                self.middleware_cfg[k]["ipaddress"] = self.middleware_server_list
        self.__update_middleware_cfg_checkresult__()
        self.servers = check_result.servers.get()
        self.service_info = service_path.config
        self.private_deploy_version = self.service_info.tag
        self.namespace = self.service_path.config.namespace

        self.service_namespaces = self.service_path.config.namespaces
        self.namespaces = [self.namespace, "proxy", *list(self.service_namespaces.keys())]
        self.project = self.namespace

        self.project_name = self.service_path.project_name

        self.templates_dir = self.service_path.template
        self.data_dir = self.service_path.data
        self.deploy_dir = self.check_result.deploy_dir

        self.service_charts_remote = path_join(self.deploy_dir, "chart")
        self.harbor_cfg = HarborConfigHandler().get_config_with_check_result()
        try:

            harbor_ip = self.harbor_cfg["harbor"]["lb"]
        except IndexError:
            harbor_ip = self.check_result.servers.get_role_ip("harbor")[0]
        self.registry_hub = "{}:{}".format(harbor_ip, self.harbor_cfg["harbor"]["nginx_harbor_proxy_port"])

        self.etcd_servers = self.check_result.servers.get_role_ip("master")
        self.etcd_endpoint = "\,".join(
            ["{}:{}".format(server, self.middleware_cfg.etcd.http_port) for server in self.etcd_servers]
        )

        self.env_k8s_config_src = path_join(self.templates_dir, "routes")
        self.env_k8s_config_dest = path_join(self.templates_dir, "routes_dest")
        self.env_k8s_config_remote = path_join(self.deploy_dir, "routes_dest")

        self.nginx_compose_file = path_join(self.deploy_dir, "nginx", "docker-compose.yml")

        self.servers = self.check_result.servers.get()
        self.middleware_cfg["k8s_hosts"] = [x.ipaddress for x in self.servers]
        self.master_hosts = self.check_result.servers.get_role_obj("master")
        self.middleware_cfg["k8s_masters"] = [x.ipaddress for x in self.master_hosts]

        self.replicas = 1
        self.nodes = self.check_result.servers.get_role_obj("node")
        self.master_host = self.check_result.servers.get_role_obj("master")[0]
        self.harbor_hosts = self.check_result.servers.get_role_obj("harbor")

        self.rabbitmq_init_file_template_path = path_join(self.templates_dir, "init_rabbitmq.tmpl")
        self.rabbitmq_init_file_path = path_join(self.templates_dir, "init_rabbitmq.sh")

        self.redis_init_file_template_path = path_join(self.templates_dir, "init_redis.tmpl")
        self.redis_init_file_path = path_join(self.templates_dir, "init_redis.sh")

        self.component = self.service_path.config.component
        self.init = self.service_path.config.init

        # bin
        self.fill_bin_src = path_join(self.templates_dir, "pvt_gen-linux-amd64")
        self.fill_bin_remote = path_join(self.deploy_dir, "pvt_gen-linux-amd64")
        # valuePath
        self.templates_src = path_join(self.templates_dir, "values")
        self.common_dest = path_join("/tmp", "{}_values".format(self.project))
        self.common_remote = path_join(self.deploy_dir, "{}_values".format(self.project))
        # tmplPath
        # self.config_templates = path_join(self.templates_dir,
        #                                   "{}_conf_templates".format(self.component),
        #                                   self.component.capitalize())
        #
        # self.config_remote = path_join(self.deploy_dir,
        #                                "{}_conf_templates".format(self.component),
        #                                self.component.capitalize())
        self.config_templates = path_join(self.templates_dir, "templates", self.component.capitalize())

        # self.config_remote = path_join(self.deploy_dir, "{}_conf_templates".format(self.component))
        self.config_remote = path_join(self.deploy_dir, "templates", self.component.capitalize())
        # if self.component == "license":
        #     self.config_templates = path_join(self.templates_dir, "templates", "Mid")
        #     self.config_remote = path_join(self.deploy_dir, "templates", "Mid")

        # self.config_target = path_join(self.deploy_dir, "{}_configmap".format(self.component))
        self.config_target = path_join(self.deploy_dir, "configmap")
        # config原生配置
        # self.config = path_join(self.deploy_dir, "{}_config".format(self.component))
        self.config = path_join(self.deploy_dir, "{}_config".format(self.component))

        # configmap
        self.configmap = path_join(self.config_target, self.component.capitalize())
        self.configmap_remote = path_join(self.deploy_dir, self.component.capitalize())

        self.specify_configs()

    def __update_middleware_cfg_checkresult__(self):
        self.middleware_cfg.update(self.check_result.__dict__)
        if "lang" in self.check_result.__dict__["config"]:
            self.middleware_cfg["lang"] = self.check_result.__dict__["config"]["lang"]

        if "deploy_https" in self.check_result.__dict__["config"]:
            if self.check_result.__dict__["config"]["deploy_https"]:
                self.middleware_cfg["scheme"] = "https"
            else:
                self.middleware_cfg["scheme"] = "http"
        if "jwt" in self.check_result.__dict__["config"]:
            self.middleware_cfg["jwt"] = self.check_result.__dict__["config"]["jwt"]
        if "processing_unit" in self.check_result.__dict__["config"]:
            self.middleware_cfg["processing_unit"] = self.check_result.__dict__["config"]["processing_unit"]
        if "postgresql" not in self.middleware_cfg:
            self.middleware_cfg["postgresql"] = {}
            self.middleware_cfg["postgresql"]["database"] = ""
            self.middleware_cfg["postgresql"]["db"] = ""
            self.middleware_cfg["postgresql"]["inner_addr"] = ""

    def specify_configs(self):
        self.istio_injection_namespaces = [self.namespace, "proxy", ]
        self.middleware_cfg["tzlf_url"] = ""
        if self.namespace == "license":
            self.istio_injection_namespaces.remove("license")

    def _fill_item_file(self, force=False):
        log.info(Helper().LOCAL_FILL.format(self.templates_src, self.common_dest))
        try:
            FileTemplate(self.middleware_cfg, self.templates_src, self.common_dest).fill(ignoreError=force)
        except UtilsError as e:
            log.error(e.msg)
            traceback.print_stack()
            exit(e.code)

        return True if os.path.isdir(self.common_dest) else False

    def upload_nacos(self):
        if not os.path.exists(os.path.join(self.templates_dir, "nacos")):
            return
        files = os.listdir(os.path.join(self.templates_dir, "nacos"))
        if len(files) == 0:
            return

        nacos_get_ip_cmd = "kubectl get svc nacos -n nacos -o jsonpath={..clusterIP}"
        nacos_real_ip = self._exec_command_to_host(cmd=nacos_get_ip_cmd, server=self.servers[0], check_res=True)[
            "stdout"]
        nacos_folder = os.path.join(self.templates_dir, "nacos")
        port = self.middleware_cfg["nacos"]["port"]
        username = self.middleware_cfg["nacos"].username
        password = self.middleware_cfg["nacos"].password
        nacos_addr = "http://{}:{}".format(nacos_real_ip, port)
        client = nacos.NacosClient(nacos_addr, namespace="pvt", username=username, password=password)
        for file in os.listdir(nacos_folder):
            log.info("upload nacos config namespace:{},file:{},folder:{}".format(self.namespace, file, nacos_folder))
            client.publish_config(
                data_id=file,
                group=self.namespace.capitalize(),
                content=open(os.path.join(nacos_folder, file), 'r').read(),
                timeout=6000
            )

    def _generic_configmap(self, genProjects="", force=False):
        """
        """
        if self._fill_item_file(force):
            self._send_file(src=self.fill_bin_src, dest=self.fill_bin_remote)
            self._send_file(src=self.common_dest, dest=self.common_remote)
            if os.path.exists(self.config_templates):
                self._send_file(src=self.config_templates, dest=self.config_remote)
            # 检查是否存在 生成指定服务配置
            if genProjects:
                genProjects = "-genProjects={}".format(genProjects)

            cmd = [
                "chmod +x {}".format(self.fill_bin_remote),
                "{} -tmplPath={} -valuePath={} -targetPath={} -configTargetPath={} {}".format(
                    self.fill_bin_remote,
                    self.config_remote,
                    self.common_remote,
                    self.config_target,
                    self.config,
                    genProjects
                )
            ]
            self._exec_command_to_host(cmd=cmd, server=self.servers[0], check_res=not force)

    def read_base_yml(self) -> dict:
        base_yaml = path_join(LAIPVT_BASE_DIR, "middleware", "base.yaml")
        base_cfg = {}
        if os.path.exists(base_yaml):
            with open(base_yaml, "r") as f:
                base_cfg = yaml.load(f.read())
        return base_cfg

    def deploy_all_configmap(self, force=False):
        try:
            service_list = []
            for i in self.service_path.config.services:
                service_list.append(i)

            # 屎山代码。先不改。默认规则文件应该是service对应service.yaml
            # 但实际上entuc->entuc-config....entbs
            service_list.append("{}-config".format(self.component))

            gen_projects = ",".join(service_list)
            # 更新了一個bug.關於程序的的配置文件必须每次最新的
            self.middleware_cfg["base"] = self.read_base_yml()["base"]

            self._generic_configmap(genProjects=gen_projects, force=force)
            self._create_namespace(namespaces=self.namespaces,
                                   istio_injection_namespaces=self.istio_injection_namespaces)
            if os.path.exists(self.configmap):
                self._send_file(src=self.configmap, dest=self.configmap_remote)
                cmd = "kubectl apply -f {}".format(self.configmap_remote)
                self._exec_command_to_host(cmd=cmd, server=self.harbor_hosts[0])
            else:
                log.info("configmap not found:not copy {}".format(self.configmap))
            log.info("configmap:{},configmap_remote:{}".format(self.configmap, self.configmap_remote))
        except Exception as e:
            log.error("configmap error: {}".format(e))
            if not force:
                exit(0)

    def check_interval_fn(self, fn):
        succeed = False
        counter = 1
        while not succeed and counter < self.check_max_tries:
            time.sleep(self.check_sleep_seconds * counter)
            result, name, msg = fn()
            if result is False:
                succeed = False
                counter = counter + 1
                log.debug("{} check failed,times:{},msg:{}".format(name, counter, msg))
            else:
                log.info(Helper().COMMON_CHECK_FILE_SUCCEED.format(name))
                return True
        log.error(Helper().COMMON_CHECK_FILE_FAILED.format(name, msg))
        exit(2)

    def push_images(self, project):
        harbor = HarborModel(username="admin", host=self.registry_hub,
                             password=self.middleware_cfg["harbor"]["password"])
        if project not in harbor.list_project():
            harbor.create_project(project)
        if os.path.exists(self.service_path.image):
            for image in os.listdir(self.service_path.image):
                image_path = path_join(self.service_path.image, image)
                log.info(Helper().PUSH_IMAGE.format(image_path))
                docker = DockerImageModel(
                    image=image_path, project=project, repo=self.registry_hub, tag_version=self.private_deploy_version
                )
                docker.run()

    def _send_file(self, src, dest, servers=None, force=False):
        l = []
        if servers:
            if isinstance(servers, list):
                l = servers
            else:
                l.append(servers)
        else:
            l = self.servers
        for server in l:
            log.info(Helper().SEND_FILE.format(src, server.ipaddress, dest))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                ssh_cli.run_cmd("mkdir -p {}||true".format(os.path.dirname(dest)))
                ssh_cli.put(src, dest)
            except Exception as e:
                log.error(e)
                traceback.print_stack()
                if force is False:
                    exit(2)
            finally:
                ssh_cli.close()

    def _exec_command_to_host(self, cmd, server: ServerHandler, check_res=True) -> dict:
        log.info(Helper().EXCUTE_COMMAND.format(server.ipaddress, cmd))
        if isinstance(cmd, list):
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            res_list = ssh_cli.run_cmdlist(cmd)
            ssh_cli.close()
            for res in res_list:
                if res["code"] != 0:
                    log.error("{} {}".format(res["stdout"], res["stderr"]))
                    traceback.print_stack()
                    if check_res:
                        exit(2)
            return res_list
        if isinstance(cmd, str):
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            res = ssh_cli.run_cmd(cmd)
            ssh_cli.close()
            if check_res:
                if res["code"] != 0:
                    log.error("{} {}".format(res["stdout"], res["stderr"]))
                    traceback.print_stack()
                    log.info(res["stdout"])
                    exit(2)
            return res
        else:
            traceback.print_stack()
            log.error(Helper().COMMAND_ERROR.format(cmd))
            exit(2)

    def _create_namespace(self, namespaces, istio_injection_namespaces=None):
        if namespaces:
            for ns in namespaces:
                log.info(Helper().CREATE_NAMESPACE.format(ns))
                cmd = CREATE_NS.format(ns)
                self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=False)
        if istio_injection_namespaces:
            for ns in istio_injection_namespaces:
                inject_cmd = ISTIO_INJECTION_NS.format(ns)
                self._exec_command_to_host(cmd=inject_cmd, server=self.master_host, check_res=False)

    def deploy_istio(self):
        # 渲染istio配置
        log.info(path_join(self.env_k8s_config_src, "istio"))
        log.info(path_join(self.env_k8s_config_dest, "istio"))
        FileTemplate(
            self.middleware_cfg,
            path_join(self.env_k8s_config_src),
            path_join(self.env_k8s_config_dest)
        ).fill()
        self._send_file(src=self.env_k8s_config_dest, dest=self.env_k8s_config_remote)
        # 临时解决entuc istio路由x-forwarded-proto: https问题
        sed_cmds = [
            "sed -i '/headers/,+3d' {}".format(path_join(self.env_k8s_config_remote, "*.yaml")),
        ]
        for sed_cmd in sed_cmds:
            self._exec_command_to_host(cmd=sed_cmd, server=self.master_host, check_res=False)

        # 临时解决license从mid迁移到license的问题
        sed_cmd = "sed -i 's/mid.svc.cluster/license.svc.cluster/g' {}".format(
            path_join(self.env_k8s_config_remote, "*"))
        log.info("临时license方案解决")
        self._exec_command_to_host(cmd=sed_cmd, server=self.master_host, check_res=False)

        cmd = KUBECTL_APPLY.format(path_join(self.env_k8s_config_remote))
        self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=False)

    def _create_logs_dir(self, project):
        log_path = os.path.join(self.deploy_dir, "Logs", project)
        log.info(Helper().CREATE_LOG_PATH.format(log_path))
        cmd = [
            MKDIR_DIR.format(log_path),
            CHMOD_777.format(log_path)
        ]
        for server in self.servers:
            self._exec_command_to_host(cmd=cmd, server=server)

    def _get_data_pvc_name(self, project, pvc_name):
        # 获取pvc的volumeName
        counter = 0
        succeed = False
        retry_count = 6
        retry_time_interval = 10
        pvc_volume_name = ""
        while not succeed and counter < retry_count:
            namespace = project
            cmd = GET_PVC_VOLUMENAME_CMD.format(namespace, pvc_name)
            res = self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=True)

            pvc_volume_name = res["stdout"].strip()
            if not pvc_volume_name:
                succeed = False
                counter += 1
            succeed = True
            time.sleep(retry_time_interval)

        return succeed, pvc_volume_name

    def _get_nfs_pvc_path(self):
        # 获取local-path pvc的volumeName
        namespace = "rook-nfs"
        local_pvc_name = "nfs-default-claim"
        cmd = GET_PVC_VOLUMENAME_CMD.format(namespace, local_pvc_name)
        res = self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=True)
        if res["code"] != 0:
            log.error(Helper().GET_LOCAL_PATH_PVC_ERROR.format(res["stdout"]))
            exit(2)
        local_pvc_volume_name = res["stdout"].strip()
        if not local_pvc_volume_name:
            log.error(Helper().GET_LOCAL_PATH_PVC_ERROR.format(res["stdout"]))
            exit(2)
        # 返回拼接目录
        return "{}_{}_{}".format(local_pvc_volume_name, namespace, local_pvc_name)

    def _get_nfs_node(self):
        cmd = GET_NFS_NODE_IP_CMD
        res = self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=True)
        if res["code"] != 0:
            log.error(Helper().GET_NFS_NODE_IP_ERROR.format(res["stdout"]))
            exit(2)
        nfs_node_ip = res["stdout"].strip()
        if not nfs_node_ip:
            log.error(Helper().GET_NFS_NODE_IP_ERROR.format(res["stdout"]))
            exit(2)
        return nfs_node_ip

    def unique_data(self, mount_datas):
        mount_data_map = {}
        get_data = lambda single_data: single_data["data_name"] + single_data["model_name"] + single_data[
            "process_name"]
        for mount_data in mount_datas:
            if get_data(mount_data) not in mount_data_map:
                mount_data_map[get_data(mount_data)] = mount_data
        return mount_data_map.values()

    def prepare_data(self, project=None):
        chown_cmd = "chown -R 5000:5000 {}"
        if project is None:
            project = self.project
        if self.service_path.config.mount_data:
            for data_info in self.unique_data(self.service_path.config.mount_data):
                data_src_dir = path_join(self.service_path.data, data_info["data_name"])
                if len(data_info["relative_path"]) == 0:
                    data_info["relative_path"] = "model"
                try:
                    pvc_name = "{}-{}-{}-claim".format(data_info["service_name"], data_info["process_name"],
                                                       data_info["relative_path"])
                    succeed, pvc_volume_name = self._get_data_pvc_name(project=project, pvc_name=pvc_name)
                except:
                    pvc_name = "{}-{}-claim".format(data_info["service_name"], data_info["relative_path"])
                    succeed, pvc_volume_name = self._get_data_pvc_name(project=project, pvc_name=pvc_name)
                if not succeed:
                    log.error(Helper().CREATE_PVC_ERROR)
                    exit(2)

                if self.check_result.use_external_disk:
                    # rook-ceph远程位置
                    use_nfs = False
                    data_remote = path_join(
                        "/var/lib/kubelet/plugins/kubernetes.io/csi/pv",
                        pvc_volume_name, "globalmount"
                    )
                else:
                    # rook-nfs远程位置
                    use_nfs = True
                    local_pvc_path = self._get_nfs_pvc_path()
                    data_remote = path_join(
                        self.deploy_dir, "nfs",
                        local_pvc_path,
                        "{}-{}-{}".format(project, pvc_name, pvc_volume_name)
                    )
                # 发送文件
                for model_dir in os.listdir(data_src_dir):
                    for i in os.listdir(path_join(data_src_dir, model_dir)):
                        model_dir_path = path_join(data_src_dir, model_dir, i)
                        data_remote_path = path_join(data_remote, i)
                        if use_nfs:
                            # nfs_node_ip = self._get_nfs_node()
                            for s in self.servers:
                                # if s.ipaddress == nfs_node_ip:
                                self._send_file(src=model_dir_path, dest=data_remote_path, servers=s)
                        else:
                            self._send_file(src=model_dir_path, dest=data_remote_path)

                # 重新启动
                # 解决挂载属主属组权限问题
                if use_nfs:
                    for s in self.servers:
                        chown_cmd = "chown -R 5000:5000 {}".format(data_remote)
                        self._exec_command_to_host(cmd=chown_cmd, server=s, check_res=True)
                time.sleep(60)
                namespace = project
                restart_deployment_cmd = RESTART_DEPLOYMENT.format(namespace, data_info["process_name"])
                self._exec_command_to_host(cmd=restart_deployment_cmd, server=self.master_host, check_res=True)

    # 安装了才有效的
    def write_config_to_dir(self):
        component = self.component.replace("-", "_")
        writefolder = os.path.join(LAIPVT_BASE_DIR, "services")
        if not os.path.exists(writefolder):
            os.makedirs(writefolder)
        writepath = os.path.join(writefolder, component + ".yaml")
        with open(writepath, "w+") as f:
            config_yaml = {component: {
                "Namespace": self.namespace
            }}
            f.write(yaml.dump(config_yaml))

    def get_dynamic_image(self, process, version, process_config):
        process_unit = process_config.get("ProcessingUnit", "cpu")
        image_name = "tfserving"
        tag = "2.8.0-cpu-encrypted-jemalloc" if process_unit == "cpu" else "2.8.0-gpu-encrypted"
        return image_name, tag

    def start_service(self, project, version, namespace=""):
        if namespace == "":
            namespace = project
        self._send_file(src=self.service_path.charts, dest=self.service_charts_remote, force=True)
        if self.check_result.use_external_disk:
            external_storageclass_name = "rook-cephfs"
        else:
            external_storageclass_name = "rook-nfs-share1"

        if self.service_path.config.services:
            for service, processes in self.service_path.config.services.items():
                for process in processes:
                    log.info(Helper().DEPLOY_SERVICE.format(process))
                    process_config = self.service_path.config.process.get(process, {})
                    processUnit = process_config.get("ProcessingUnit", "cpu")

                    check_cmd = HELM_LIST.format(process)
                    check_results = self._exec_command_to_host(cmd=check_cmd, server=self.master_host, check_res=False)
                    is_exist = False
                    file_path = os.path.join(self.service_charts_remote, process)
                    if check_results["stdout"]:
                        chart_dict = json.loads(check_results["stdout"])
                        chart_list = []
                        for i in chart_dict["Releases"]:
                            chart_list.append(i["Name"])
                        if process in chart_list:
                            log.warning(Helper().SERVICE_EXISTS.format(process))
                            is_exist = True
                    if is_exist:
                        self.upgrade_service(project)

                    if not is_exist:
                        self._create_logs_dir(service)
                        cmd_prefix = ""
                        lm_client_service_id = ""
                        if process in self.admin_config.license_service:
                            lm_client_service_id = self.admin_config.license_service[process]
                        registry_hub = path_join(self.registry_hub, namespace)
                        workload_type = ""
                        logpath = "/home/works/program/logs"
                        resources = ""
                        if self.namespace == "mage" or self.namespace == "ocr":
                            resources = "{}"
                        tag = version
                        if processUnit == "cpu":
                            cmd_prefix = HELM_INSTALL_CPU
                        elif processUnit == "gpu":
                            cmd_prefix = HELM_INSTALL_GPU

                        if project == "ocr_seal":
                            project = "ocr"
                        # 当标注是cpu但优势trfserver的时候.修改镜像为
                        if "tf" in process:
                            image_name, tag = self.get_dynamic_image(process, version, process_config)
                            registry_hub = path_join(self.registry_hub, "middleware")
                        elif process == "layout-idp-ext-eval" or process == "layout-idp-ext-train":
                            image_name = "layout-idp-ext"
                        else:
                            log.info("标准程序安装。非tfserver")
                            resources = ""
                            if self.namespace == "mage" or self.namespace == "ocr":
                                resources = "{}"
                            tag = version
                            image_name = process

                        cmd = cmd_prefix.format(
                            process=process,
                            process_name=process,
                            project_name=service,
                            namespace=self.namespace,
                            component=self.component,
                            logpath=logpath,
                            external_storageclass_name=external_storageclass_name,
                            replicas=self.replicas,
                            registry_hub=registry_hub,
                            image_name=image_name,
                            image_tag=tag,
                            pvt_work_dir=self.deploy_dir,
                            etcd_endpoint=self.etcd_endpoint,
                            nacos_host=self.middleware_cfg["nacos"].get("inner_addr", "nacos.nacos.svc:8848"),
                            lm_client_service_id=lm_client_service_id,
                            workload_type=workload_type,
                            resources=resources,
                            file_path=file_path
                        )
                        self._exec_command_to_host(cmd=cmd, server=self.master_host)

    def upgrade_service(self, project, namespace=""):
        if namespace == "":
            namespace = project
        for service, processes in self.service_path.config.services.items():
            for process in processes:
                log.info(Helper().DEPLOY_SERVICE.format(process))
                process_config = self.service_path.config.process.get(process, {})
                processUnit = process_config.get("ProcessingUnit", "cpu")
                if self.check_result.use_external_disk:
                    external_storageclass_name = "rook-cephfs"
                else:
                    external_storageclass_name = "rook-nfs-share1"
                log.info(Helper().DEPLOY_SERVICE.format(process))
                self._create_logs_dir(service)
                file_path = os.path.join(self.service_path.charts, process)
                if not os.path.exists(file_path):
                    log.info("chart file not find {}".format(file_path))
                lm_client_service_id = ""
                if process in self.admin_config.license_service:
                    lm_client_service_id = self.admin_config.license_service[process]
                registry_hub = path_join(self.registry_hub, namespace)
                workload_type = ""
                logpath = "/home/works/program/logs"
                resources = ""
                if self.namespace == "ocr" or self.namespace == "mage":
                    resources = "{}"
                process_config = self.service_path.config.process.get(process, {})
                image_name = process
                tag = self.private_deploy_version
                if "tf" in process:
                    image_name, tag = self.get_dynamic_image(process, self.private_deploy_version, process_config)
                    registry_hub = path_join(self.registry_hub, "middleware")
                elif process == "layout-idp-ext-eval" or process == "layout-idp-ext-train":
                    image_name = "layout-idp-ext"
                cmd_prefix = ""
                if processUnit == "cpu":
                    cmd_prefix = HELM_UPGRADE_INSTALL_CPU
                elif processUnit == "gpu":
                    cmd_prefix = HELM_UPGRADE_INSTALL_GPU
                if project == "ocr_seal":
                    project = "ocr"
                cmd = cmd_prefix.format(
                    process=process,
                    process_name=process,
                    project_name=service,
                    namespace=self.namespace,
                    component=self.component,
                    logpath=logpath,
                    external_storageclass_name=external_storageclass_name,
                    replicas=self.replicas,
                    registry_hub=registry_hub,
                    image_name=image_name,
                    image_tag=tag,
                    pvt_work_dir=self.deploy_dir,
                    etcd_endpoint=self.etcd_endpoint,
                    nacos_host=self.middleware_cfg["nacos"].get("inner_addr", "nacos.nacos.svc:8848"),
                    lm_client_service_id=lm_client_service_id,
                    workload_type=workload_type,
                    resources=resources,
                    file_path=file_path
                )
                self._exec_command_to_host(cmd=cmd, server=self.master_host)

    def proxy_on_nginx(self, nginx_template, nginx_tmp, nginx_file_remote):
        FileTemplate(self.middleware_cfg, nginx_template, nginx_tmp).fill()
        self._send_file(src=nginx_tmp, dest=nginx_file_remote)
        compose_cmd = ComposeModel(self.nginx_compose_file)
        for server in self.servers:
            self._exec_command_to_host(cmd=compose_cmd.restart(), server=server, check_res=True)

    def init_identity_user(self):
        init_user_cmd = INIT_IDENTITY_USER
        self._exec_command_to_host(cmd=init_user_cmd, server=self.servers[0], check_res=False)

    def deploy_tf_service(self, module_name, tf_image_name):
        # self._send_file(src=self.service_path.charts, dest=self.service_charts_remote)
        log.info(Helper().DEPLOY_SERVICE.format(module_name))
        check_cmd = HELM_LIST.format(
            module_name, module_name
        )
        check_results = self._exec_command_to_host(cmd=check_cmd, server=self.master_host, check_res=False)
        if check_results["code"] == 0:
            log.warning(Helper().SERVICE_EXISTS.format(module_name))
        else:
            file_path = os.path.join(self.service_charts_remote, module_name)
            # print(file_path)
            tag = "2.4.0-cpu" if self.service_path.config.machine_type == "cpu" else "2.8.0-gpu-encrypted"
            cmd = HELM_INSTALL_TF_SERVICE.format(
                process=module_name, replicas=self.replicas,
                registry_hub=path_join(self.registry_hub, "middleware"),
                image_name=tf_image_name, image_tag=tag,
                pvt_work_dir=self.deploy_dir,
                etcd_endpoint=self.etcd_endpoint,
                file_path=file_path)

            self._exec_command_to_host(cmd=cmd, server=self.master_host)

    def project_pod_check(self):
        counter = 0
        succeed = False
        kube = KubeModel()

        # 每10秒重试一次，重试 10 次，如果还是不成功就报错...好像有问题。。因为公用到同一个pod后。就不会走下一步了
        while not succeed and counter < 6:
            time.sleep(10 * counter)
            pod_info = kube.get_all_pod_status(namespace=self.project)
            pod_status = []
            for pod in pod_info:
                pod_status.append(pod["status"])
            if set(pod_status) == {'Running', 'Succeeded'} or set(pod_status) == {'Running'}:
                succeed = True
            else:
                succeed = False
                counter = counter + 1
                log.info("检查项目 {} 的 Pod 状态，第 {} 次重试".format(self.project, counter))
        if succeed:
            log.info(Helper().PROJECT_POD_CHECK_SUCCEED.format(self.project))
        else:
            log.info(Helper().PROJECT_POD_CHECK_FAILED.format(self.project))

    def app_test(self):
        log.info("Begin app test project:%s service_path %s", self.project, self.service_path.test)
        if os.path.exists(self.service_path.test):
            # 导入测试镜像
            test_images_path = path_join(self.service_path.test, "images")
            for image in os.listdir(test_images_path):
                image_path = path_join(test_images_path, image)
                log.info(Helper().PUSH_IMAGE.format(image_path))
                # print(image_path)
                docker = DockerImageModel(image=image_path, project=self.project,
                                          repo=self.registry_hub, tag_version=self.private_deploy_version)
                docker.run()

            # 渲染测试配置文件
            config_path_src = path_join(self.service_path.test, "templates")
            config_path_dest = path_join(self.deploy_dir, "{}_test_config".format(self.project))
            # log.info("渲染填充项文件{}到{}".format(config_path_src, config_path_dest))
            try:
                FileTemplate(self.middleware_cfg, config_path_src, config_path_dest).fill()
            except Exception as e:
                log.error(Helper().FILL_ERROR.format(config_path_src, e))
                log.error(e)

            # 运行测试命令
            host_config = os.path.join(config_path_dest, "test.conf")
            container_config = "/home/works/program/conf/test.conf"
            host_logs = path_join(self.deploy_dir, "{}_test_report".format(self.project))
            container_logs = "/home/works/program/logs"
            image_name = path_join(self.registry_hub, self.project, "{}-apptest".format(self.project))

            cmd = TEST_SERVICE_CMD.format(
                self.middleware_cfg.mysql.lb,
                host_config, container_config,
                host_logs, container_logs,
                image_name, self.private_deploy_version
            )

            counter = 0
            succeed = False

            # 如果自动化测试失败，重试1次，如果还是不成功就报错
            while not succeed and counter == 0:
                time.sleep(10)
                log.info(cmd)
                code, res = runcmd(cmd)
                if code != 0:
                    filepath = os.path.join(self.deploy_dir, "test", self.project + "-test-output.txt")
                    if not os.path.exists(os.path.dirname(filepath)):
                        os.makedirs(os.path.dirname(filepath))
                    with open(filepath, "w+") as file:
                        file.write(res.stdout)
                        log.info("请查看: {}".format(filepath))

                # 判断测试结果
                res_json_file = path_join(host_logs, "results.json")
                log.info("check_result:\r" + res_json_file)

                with open(res_json_file, "r") as fp:
                    res = json.load(fp)
                if res["code"] != 0:
                    counter = counter + 1
                    succeed = False
                    log.error(Helper().APPTEST_FAILED.format(self.project, res["msg"]))
                else:
                    succeed = True
                    log.info(Helper().APPTEST_SUCCEED.format(self.project, res["msg"]))
            return succeed, self.project, host_logs

    def init_pgsql(self):
        log.info("Init pgsql %s", self.project)
        if self.init:
            if self.init["pgsql_db"]:
                pgsql_host = self.middleware_cfg.postgresql.ipaddress[0]
                sql = PgSqlModule(host=pgsql_host, port=int(self.middleware_cfg.postgresql.port),
                                  user=self.middleware_cfg.postgresql.username,
                                  passwd=self.middleware_cfg.postgresql.password)
                for db in self.init["pgsql_db"]:
                    sql.create_db(db)

    def init_mysql(self):
        log.info("Init mysql %s", self.project)
        if self.init:
            if self.init["mysql_db"]:
                if self.middleware_cfg.mysql.is_deploy:
                    mysql_host = self.master_host.ipaddress
                else:
                    mysql_host = self.middleware_cfg.mysql.ipaddress[0]
                if len(self.master_hosts) == 1:
                    port = self.middleware_cfg.mysql.port
                else:
                    port = self.middleware_cfg.mysql.proxysql_port
                sql = SqlModule(host=mysql_host, port=int(port),
                                user=self.middleware_cfg.mysql.username, passwd=self.middleware_cfg.mysql.password)
                for db in self.init["mysql_db"]:
                    create_db = CREATE_DB.format(db_name=db)
                    sql.insert_sql(create_db)
                    log.info("execute insert mysql:{}".format(create_db))

    def init_minio(self):
        if self.init:
            if "minio_bucket_public" in self.init:
                endpoint = "{}:{}".format(self.middleware_cfg.minio.lb,
                                          self.middleware_cfg.minio.nginx_proxy_port)
                cli = Minio(
                    endpoint,
                    self.middleware_cfg.minio.username,
                    self.middleware_cfg.minio.password,
                    secure=False
                )
                for bucket in self.init["minio_bucket_public"]:
                    if not cli.bucket_exists(bucket):
                        cli.make_bucket(bucket)
                    log.info("{} Init minio private {} bucket".format(self.project, bucket))
                    policy_read_write = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": [
                                    "s3:GetObject"
                                ],
                                "Effect": "Allow",
                                "Principal": "*",
                                "Resource": [
                                    "arn:aws:s3:::{}/*".format(bucket)
                                ],
                                "Sid": ""
                            }
                        ]
                    }
                    cli.set_bucket_policy(bucket, json.dumps(policy_read_write))
            if "minio_bucket_private" in self.init:
                endpoint = "{}:{}".format(self.middleware_cfg.minio.lb,
                                          self.middleware_cfg.minio.nginx_proxy_port)
                cli = Minio(
                    endpoint,
                    self.middleware_cfg.minio.username,
                    self.middleware_cfg.minio.password,
                    secure=False
                )
                for bucket in self.init["minio_bucket_private"]:
                    log.info("{} Init minio private {} bucket".format(self.project, bucket))
                    bucket = bucket.replace("_", "-")
                    if not cli.bucket_exists(bucket):
                        cli.make_bucket(bucket)
                    policy_read_write = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": [
                                    "s3:GetObject"
                                ],
                                "Effect": "Allow",
                                "Principal": "*",
                                "Resource": [
                                    "arn:aws:s3:::{}/*".format(bucket)
                                ],
                                "Sid": ""
                            }
                        ]
                    }
                    cli.set_bucket_policy(bucket, json.dumps(policy_read_write))

    def init_rabbitmq(self):
        if self.init:
            if self.init["rabbitmq_vhost"]:
                for vhost in self.init["rabbitmq_vhost"]:
                    rabbitmq_api_vhosts = "http://{}:{}/api/vhosts/{}".format(self.master_host.ipaddress,
                                                                              self.middleware_cfg.rabbitmq.manage_port,
                                                                              vhost)
                    res = requests.put(url=rabbitmq_api_vhosts, auth=(self.middleware_cfg.rabbitmq.username,
                                                                      self.middleware_cfg.rabbitmq.password))
                    if res.status_code > 204:
                        log.error("rabbitmq vhost error.")
                        exit(2)

    def restart_service(self, namespace="all_namespaces"):
        log.info("Restart service %s", self.project)
        kube = KubeModel()
        kube.restart_deploy(namespace=namespace)

    def run(self, force=False):
        pass

    def upgrade(self):
        log.info("服务开始upgrade %s", self.project)
        try:
            self.push_images(self.namespace)
            self.upgrade_service(self.namespace)
            self.project_pod_check()
        except Exception as e:
            log.error(e)
            exit(2)

    def rebuild_data(self, force=False):
        log.info("Rebuild Service %s", self.project)
        try:
            self.init_mysql()
            self.init_minio()
            self.init_pgsql()
            self.restart_service(namespace=self.namespace)
            self.project_pod_check()
        except Exception as e:
            log.info("rebuild failed", e)
