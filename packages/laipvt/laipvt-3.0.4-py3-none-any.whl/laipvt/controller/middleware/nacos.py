import json
import logging
import os

import yaml

import nacos
import requests

from laipvt.handler.middlewarehandler import NacosConfigHandler
from laipvt.helper.errors import Helper
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.interface.middlewarek8sinterface import MiddlewareK8sInterface
from laipvt.sysutil.command import GET_NACOS_VERSION_CMD, HELM_LIST, HELM_DELETE
from laipvt.sysutil.gvalue import LAIPVT_BASE_DIR
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import status_me, ssh_obj, path_join, log, run_local_cmd


class NacosController(MiddlewareK8sInterface):
    def __init__(self, result, handler, template):
        super(NacosController, self).__init__(result, handler, template)
        host = self.master_server[0]
        self.ssh_cli = ssh_obj(ip=host.ipaddress, user=host.username, password=host.password, port=host.port)
        self.nacos_cfg = NacosConfigHandler().get_config_with_check_result()
        self.helm_path = path_join(self.template, "helm")

    def replace_suffix(self, filename):
        portion = os.path.splitext(filename)  # 分离文件名与扩展名
        newname = portion[0] + '.yml'
        return newname

    @status_me("nacos")
    def generate_config_file(self) -> bool:
        fill_bin_remote = os.path.join(self.template, "pvt_gen-linux-amd64")
        k8s_dest_path = os.path.join(self.check_result.deploy_dir, "k8s_nacos_configs")
        dest_path = os.path.join(self.check_result.deploy_dir, "nacos_configs")
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        template_folder = os.path.join(os.path.dirname(__file__), "nacos_files")
        value_path = LAIPVT_BASE_DIR
        self.render_by_go_render(file_bin_remote=fill_bin_remote,
                                 template_path=template_folder,
                                 value_path=os.path.join(value_path, "services"),
                                 dest_path=dest_path,
                                 k8s_dest_path=k8s_dest_path,
                                 files=["grpc_services"])
        self.render_by_go_render(file_bin_remote=fill_bin_remote,
                                 template_path=template_folder,
                                 value_path=os.path.join(value_path, "middleware"),
                                 dest_path=dest_path,
                                 k8s_dest_path=k8s_dest_path,
                                 files=["environment_config", "middleware"])

    def _check_port_(self):
        nacos_real_ip = self.get_nacos_real_ip()
        for i in range(len(self.master_server)):
            try:
                requests.get(
                    "http://{IP}:{PORT}/nacos".format(
                        IP=nacos_real_ip, PORT=self.nacos_cfg["nacos"].get("port", 8848)
                    )
                )
                log.info(Helper().CHECK_MIDDLEWARE_SERVICE_PORT_SUCCEED.format(nacos_real_ip,
                                                                               self.nacos_cfg["nacos"].get("port",
                                                                                                           8848)))
            except Exception as e:
                log.info(Helper().CHECK_MIDDLEWARE_SERVICE_PORT_FAILED.format(nacos_real_ip,
                                                                              self.nacos_cfg["nacos"].get("port",
                                                                                                          8848)))
                log.error(e)
                return False, "nacos", Helper().CHECK_MIDDLEWARE_SERVICE_PORT_FAILED.format(
                    nacos_real_ip,
                    self.nacos_cfg["nacos"].get("port", 8848))
        return True, "nacos", ""

    def get_nacos_real_ip(self):
        nacos_real_ip = run_local_cmd("kubectl get svc nacos -n nacos -o jsonpath={..clusterIP}")["stdout"]
        return nacos_real_ip

    @status_me("nacos")
    def create_nacos_namespace(self, client):
        nacos_data = {"customNamespaceId": "pvt", "namespaceName": "pvt", "namespaceDesc": "pvt", "namespaceId": "pvt"}
        resp = client._do_sync_req("/nacos/v1/console/namespaces", None, None, data=nacos_data,
                                   timeout=100, method="POST")
        c = resp.read()
        logging.info("create nacos namespace {} success {}".format("pvt", c))
        return c

    @status_me("nacos")
    def upload_common_config(self):
        nacos_real_ip = self.get_nacos_real_ip()
        port = self.nacos_cfg["nacos"]["port"]
        username = self.nacos_cfg["nacos"]["username"]
        password = self.nacos_cfg["nacos"]["password"]
        log.info("nacos_real_ip:{},port:{},username:{},password".format(nacos_real_ip, port, username, password))
        dest_path = os.path.join(self.check_result.deploy_dir, "nacos_configs")
        client = nacos.NacosClient("http://{}:{}".format(nacos_real_ip, port), namespace="pvt", username=username,
                                   password=password)
        self.create_nacos_namespace(client)
        for file in os.listdir(os.path.join(dest_path, "nacos_files")):
            with open(os.path.join(dest_path, "nacos_files", file), "r", encoding="utf-8") as f:
                content = f.read()
                result = client.publish_config(
                    data_id=self.replace_suffix(file),
                    group="DEFAULT_GROUP",
                    content=content,
                    timeout=100
                )
                log.info("upload nacos config namespace:{} group:{},file:{},result:{}".format("pvt", "DEFAULT_GROUP",
                                                                                              self.replace_suffix(file),
                                                                                              result))
                if result is False:
                    exit(0)

    @status_me("nacos")
    def install(self):
        check_cmd = HELM_LIST.format(
            "nacos-server"
        )
        check_results = self.ssh_cli.run_cmd(cmd=check_cmd)
        if check_results["stdout"] != "":
            chart_dict = json.loads(check_results["stdout"])
            chart_list = []
            for i in chart_dict["Releases"]:
                chart_list.append(i["Name"])
            if "nacos-server" in chart_list:
                log.warning(Helper().SERVICE_EXISTS.format("nacos"))
                return

        self.nacos_install_cmd = """helm --host=localhost:44134 install --name nacos-server --set namespace=nacos --set nacos.image.repository={harbor_address} \
        --set nacos.image.tag={tag} --set persistence.enabled=true --set persistence.data.storageClassName={storage_class_name}  --set nacos.replicaCount=1  \
        --set service.port={port} --set persistence.data.resources.requests.storage=20G {filepath} """
        tag = self.ssh_cli.run_cmd(GET_NACOS_VERSION_CMD)["stdout"].replace("\n", "").replace("\r", "")
        cmd = self.nacos_install_cmd.format(storage_class_name="rook-nfs-share1",
                                            tag=tag,
                                            harbor_address=self.registry_hub,
                                            filepath=self.helm_path,
                                            port=str(self.nacos_cfg["nacos"].get("port", 8848))
                                            )
        log.info(cmd)
        results = self.ssh_cli.run_cmd(cmd)
        log.info("start_nacos_app: stdout:{} stderr{}".format(results["stdout"], results["stderr"]))

    @status_me("nacos")
    def common_check(self) -> bool:
        self.check_max_tries = 8
        self.check_interval_fn(self._check_port_)

    def deploy(self, force=False):
        self.install()
        self.common_check()
        self.generate_config_file()
        self.upload_common_config()
