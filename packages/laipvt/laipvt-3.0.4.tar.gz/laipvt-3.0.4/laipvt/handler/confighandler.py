from __future__ import absolute_import
from __future__ import unicode_literals

from functools import reduce
from laipvt.sysutil.util import get_yaml_obj, get_json_obj, get_yaml_config, to_object
from laipvt.handler import ListHandler, DictHandler
from laipvt.sysutil.relation import service_module_relation, get_module_key


class ProjectsHandler(ListHandler):
    def __init__(self, projects):
        super(ProjectsHandler, self).__init__(projects)
        self.mage = self.check("mage")
        self.commander = self.check("commander")
        self.wulai = self.check("wulai")


class RoleHandler(ListHandler):
    def __init__(self, role):
        super(RoleHandler, self).__init__(role)
        self.master = self.check("master")
        self.node = self.check("node")
        self.harbor = self.check("harbor")
        self.licserver = self.check("licserver")


class ServerHandler(DictHandler):
    """返回服务器信息"""

    def __init__(self, server):
        super(ServerHandler, self).__init__(server)
        self.ipaddress = self.d.ipaddress
        self.username = self.d.username
        self.password = self.d.password
        self.port = self.d.port
        self.role = RoleHandler(self.d.role)


class ServersHandler(ListHandler):
    """返回服务器列表"""

    def __init__(self, servers):
        super(ServersHandler, self).__init__(servers)
        try:
            self.servers = self.get()
        except KeyError:
            self.servers = to_object(self.l)

    def get(self) -> list:
        """

        :return: list[ServerHandler]
        """
        l = []
        for server in self.l:
            l.append(ServerHandler(server))
        return l

    def get_role_ip(self, role: str) -> list:
        """根据角色获取匹配该角色的ip地址列表"""
        l = []
        for server in self.servers:
            if server.role.check(role):
                l.append(server.ipaddress)
        return l

    def get_all_ip(self) -> list:
        """根据角色获取匹配该角色的ip地址列表"""
        l = []
        for server in self.servers:
            l.append(server.ipaddress)
        return l

    def get_role_obj(self, role: str) -> list:
        l = []
        for server in self.servers:
            if server.role.check(role):
                l.append(server)
        return l

    def search_server(self, key: str, value: str) -> list:
        l = []
        for server in self.servers:
            if server.__dict__[key] == value:
                l.append(server)
        return l


class CheckResultHandler():
    def __init__(self, config_file: str):
        self.config = get_yaml_obj(config_file)
        self.deploy_dir = self.config.deploy_dir
        self.lb = self.config.lb
        self.deploy_projects = ProjectsHandler(self.config.deploy_projects)
        self.servers = ServersHandler(self.config.servers)
        self.licserver = self.config.licserver
        self.use_external_disk = self.config.use_external_disk


class DeployServiceHandler():
    """
    处理要部署的项目，返回字典
    service: 自研的项目
    ocr: ocr相关
    """

    def __init__(self, deploy_service: list):
        res = []
        for id in sorted(deploy_service):
            if id in service_module_relation["ocr"]:
                res.append("ocr")
            elif id in service_module_relation["ocr_3rd"]:
                res.append("ocr_3rd")
            else:
                res.append(get_module_key(id))
            # for srv in service_module_relation:
            #     if int(id) in service_module_relation[srv]:
            #         res.append(srv)
        self.service_id = sorted(deploy_service)
        self.service_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] + res)

    def get(self) -> list:
        return self.service_list

    #已经弃用了。
    def parse(self, l: list) -> dict:
        return {
            "cpu": [],
            "gpu": []
        }


class PvtAdminConfigHandler():
    """解析私有部署授权平台传递配置
    {
        "code_version": 01,
        "deploy_type": simple/ha
        "project_name": "项目名称",
        "project_id": "abcde",
        "start_time": 1606199550,
        "end_time": 1608791570,
        "license_file_name": "abcde.lcs",
        "deploy_service": [0, 1, 2, 3, 4, 5]
    }
    {
            "commander": ["commander"],
            "mage": ["mage", "nlp", "captcha", "laiye_ocr", "hehe_ocr"],
            "wulai": ["wulai"],
            "laiye_ocr"li: ["laiye_document_cpu", "laiye_document_gpu", "laiye_table_cpu", "laiye_table_gpu"],
            "hehe_ocr": ["hehe_document_cpu", "hehe_document_gpu", "hehe_table_cpu", "hehe_table_gpu"],
    }
    """

    def __init__(self, config: str):
        self.config = get_json_obj(config)
        self.project_name = self.config.project_name
        self.project_id = self.config.project_id
        self.license_service = self.config.license_service
        self.service_list = DeployServiceHandler(self.config.deploy_service)
        self.hide_menu_id = self.config.menu_id
        if self.hide_menu_id is None or self.hide_menu_id == "":
            self.hide_menu_id = []
        self.siber_tags = self.config.get("siber_tags", [])
        if self.siber_tags is None or self.siber_tags == "":
            self.siber_tags = []
        # try:
        #     self.siber_tags = self.config.siber_tags
        # except Exception:
        #     pass


class ServiceConfigHandler:
    """
    middleware:
      - mysql
      - redis
      - minio
    services:
      document-mining-backend:
        - document-mining-rpc
        - document-mining-auth
        - document-mining-openapi
      file-analyze:
        - file-analyze
      ocr-server-dispatch:
        - ocr-server-dispatch
    """

    def __init__(self, conf: str):
        self.conf = get_yaml_config(conf)
        self.middleware = self.conf.get("middleware", [])
        self.services = self.conf.get("services", [])
        self.process = self.conf.get("process", {})
        self.tag = self.conf.get("tag", "")
        self.cfg = to_object({})
        self.buckets = self.conf.get("buckets", [])
        self.require_tfserver = self.conf.get("require_tfserver", False)
        self.machine_type = self.conf.get("machine_type", "cpu")
        self.mount_data = self.conf.get("mount_data", "")
        self.component = self.conf.get("component", "")
        # 整个component的namespace
        self.namespace = self.conf.get("namespace", "")
        self.init = self.conf.get("init", "")
        # 每个进程的namespace
        self.namespaces = self.conf.get("namespaces", {})
        if len(self.namespace) == 0:
            for service in self.services:
                self.namespaces.update({service: self.namespace})

    def get_process(self, service: str) -> list:
        return self.services.get(service)
