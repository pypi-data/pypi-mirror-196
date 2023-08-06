from __future__ import absolute_import
from __future__ import unicode_literals

import os
from laipvt.sysutil.conf import YamlConfig
from laipvt.sysutil.util import path_join, gen_pass
from laipvt.sysutil.gvalue import LAIPVT_BASE_DIR, CHECK_FILE
from laipvt.sysutil.relation import get_port
from laipvt.sysutil.wraps import check_value
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.helper.exception import UtilsError


class MiddlewareConfigHandler(object):
    def __init__(self, name: str):
        self.permit_keys_base = ("ipaddress", "is_deploy", "lb")
        self.permit_keys = ()
        self.laipvt_base_dir = LAIPVT_BASE_DIR
        self.name = name
        self.local_cfg = path_join(self.laipvt_base_dir, "middleware", "{}.yaml".format(self.name))
        self.cfg = {}
        self.cfg["name"] = self.name
        self.all_cfg = {}

    def set_deploy_type(self):
        try:
            self.cfg["deploy_type"] = "single" if len(self.cfg["ipaddress"]) <= 1 else "cluster"
        except TypeError:
            self.cfg["deploy_type"] = "single"

    @check_value
    def set(self, key, value) -> bool:
        if key in self.permit_keys or key in self.permit_keys_base:
            self.cfg[key] = value
            if key == "ipaddress":
                self.set_deploy_type()
            return True
        return False

    def get(self) -> dict:
        return self.cfg

    def get_value(self, value: str):
        return self.cfg[value]

    def get_proxy_type(self) -> str:
        d = {
            "minio": "http",
            "rabbitmq": "tcp",
            "elasticsearch": "http",
            "nsq": "tcp",
            "dgraph": "tcp",
            "identity": "http",
            "mongo": "tcp",
            "etcd": "tcp",
            "mysql": "tcp",
            "mage": "http",
            "nacos": "http",
            "postgresql": "tcp"
        }
        return d.get(self.cfg["name"], "http")

    def save(self) -> bool:
        try:
            dict_cfg = {}
            dict_cfg[self.name] = self.cfg
            dumper = YamlConfig(self.local_cfg, dict_cfg)
            dumper.write_file(backup=False)
            return True
        except Exception as e:
            print(e)
            return False

    def load(self) -> dict:
        loder = YamlConfig(self.local_cfg)
        return loder.read_file()

    def load_config_from_file(self):
        if os.path.isfile(self.local_cfg):
            self.cfg = self.load()
        return {}

    def get_config_with_check_result(self) -> dict:
        try:
            self.check_result = CheckResultHandler(CHECK_FILE)
            self.servers = self.check_result.servers
            cfg = self.load()
            cfg[self.name]["lb"] = self.check_result.lb
            cfg[self.name]["deploy_type"] = "single" if len(self.check_result.config.servers) <= 1 else "cluster"
            cfg[self.name]["nginx_harbor_proxy_port"] = get_port("harbor", "nginx_harbor_proxy_port")
            cfg[self.name]["harbor_http_port"] = get_port("harbor", "http_port")
            cfg[self.name]["harbor_ipaddress"] = self.check_result.lb
            cfg[self.name]["master_harbor_ipaddress"] = self.servers.get_role_obj("harbor")[0].ipaddress
            return cfg
        except UtilsError:
            return {}

    def get_all_config_with_check_result(self) -> dict:
        try:
            cfg_dirs = path_join(self.laipvt_base_dir, "middleware")
            self.all_cfg = YamlConfig(cfg_dirs).read_dir()
        except Exception as e:
            print(e)
            exit(0)
        return self.all_cfg

    def get_ocr_module_port(self, name: str) -> int:
        if name.endswith("_gpu"):
            n = name
        else:
            n = "{}_gpu".format(name)
        return get_port("ocr", n)


class MinioConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(MinioConfigHandler, self).__init__("minio")
        self.permit_keys = ("username", "password", "user_ro", "inner_addr", "passwd_ro", "port", "nginx_proxy_port")
        self.cfg["username"] = "laiyelaiye"
        self.cfg["password"] = gen_pass()
        self.cfg["user_ro"] = "laiyero"
        self.cfg["passwd_ro"] = self.cfg["password"]
        self.cfg["user_rw"] = "laiyerw"
        self.cfg["passwd_rw"] = self.cfg["password"]
        self.cfg["inner_addr"] = "minio.default.svc"
        self.cfg["port"] = get_port("minio", "port")
        self.cfg["nginx_proxy_port"] = get_port("minio", "nginx_proxy_port")


class MinioBigDataConfigHandler(MiddlewareConfigHandler):
    """
        commander企业版使用oss，私有部署使用minio，故此增加该配置做渲染模版区分。同步minio配置
    """

    def __init__(self):
        super(MinioBigDataConfigHandler, self).__init__("miniobigdata")
        local_cfg = path_join(self.laipvt_base_dir, "middleware", "minio.yaml")
        minio_result = YamlConfig(self.laipvt_base_dir).loader(local_cfg)
        self.permit_keys = tuple(minio_result["minio"])
        self.cfg = minio_result["minio"]
        self.cfg["name"] = "miniobigdata"
        self.save()


class BaseConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(BaseConfigHandler, self).__init__("base")
        self.permit_keys = ("account", "password")
        self.cfg["account"] = "admin"
        self.cfg["password"] = "Abc123456"
        self.cfg["usercenter"] = "entuc"
        # 只能后期改了。前期拿不到check_result
        self.cfg["lang"] = "zh-CN"
        self.cfg["scheme"] = "http"


class HarborConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(HarborConfigHandler, self).__init__("harbor")
        self.permit_keys = ("http_port", "password", "nginx_harbor_proxy_port")
        self.cfg["username"] = "admin"
        self.cfg["http_port"] = get_port("harbor", "http_port")
        self.cfg["nginx_harbor_proxy_port"] = get_port("harbor", "nginx_harbor_proxy_port")
        self.cfg["password"] = gen_pass()


class RedisConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(RedisConfigHandler, self).__init__("redis")
        self.permit_keys = ("password", "port", "port_sentinel", "master_name", "master_ip", "isslave")
        self.cfg["password"] = gen_pass()
        self.cfg["port_sentinel"] = get_port("redis", "port_sentinel")
        self.cfg["port"] = get_port("redis", "port")
        self.cfg["master_name"] = "mymaster"


class NginxConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(NginxConfigHandler, self).__init__("nginx")
        self.permit_keys = (
            "service_port",
            "entcmd_proxy_port", "commander_tenant_port", "k8s_proxy_port", "mysql_proxy_port",
            "minio_proxy_port", "identity_proxy_port", "mage_proxy_port", "chatbot_proxy_port",
            "entuc_proxy_port", "notice_proxy_port", "entfs_proxy_port", "entiap_proxy_port")
        # 为了兼容

        self.cfg["k8s_proxy_port"] = get_port("nginx", "k8s_proxy_port")
        self.cfg["entuc_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["entcmd_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["mage_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["chatbot_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["dataservice_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["rpa_collaboration_backend_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["creativity_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["license_web_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["notice_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["entfs_proxy_port"] = get_port("nginx", "entuc_proxy_port")
        self.cfg["entiap_proxy_port"] = get_port("nginx", "entuc_proxy_port")


class KeepalivedConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(KeepalivedConfigHandler, self).__init__("keepalived")
        self.permit_keys = ("ipaddress", "master_network", "slave_network", "slave2_network")


class ChronydConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(ChronydConfigHandler, self).__init__("chronyd")
        self.permit_keys = ("ipaddress",)


class NacosConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(NacosConfigHandler, self).__init__("nacos")
        self.permit_keys = ("username", "password", "inner_addr", "port")
        self.cfg["username"] = "nacos"
        self.cfg["password"] = "nacos"
        self.cfg["port"] = "8848"
        self.cfg["inner_addr"] = "nacos.nacos.svc:" + self.cfg["port"]


class PgSqlConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(PgSqlConfigHandler, self).__init__("postgresql")
        self.permit_keys = ("username", "password", "database", "ipaddress", "port", "lb", "inner_addr")
        self.cfg["username"] = "postgresql"
        self.cfg["password"] = gen_pass()
        self.cfg["database"] = "laiye_ds_redash"
        self.cfg["db"] = "laiye_ds_redash"
        self.cfg["inner_addr"] = "postgresql.default.svc"
        self.cfg["port"] = get_port("postgresql", "port")


class CloudK8sConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(CloudK8sConfigHandler, self).__init__("cloudk8s")
        # self.cfg[""]


class MysqlConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(MysqlConfigHandler, self).__init__("mysql")
        self.permit_keys = ("username", "password", "ipaddress", "port", "nginx_proxy_port", "lb", "proxysql_port")
        self.cfg["username"] = "root"
        self.cfg["password"] = gen_pass()
        self.cfg["port"] = get_port("mysql", "port")
        self.cfg["proxysql_port"] = get_port("mysql", "proxysql_port")
        self.cfg["nginx_proxy_port"] = get_port("mysql", "nginx_proxy_port")


class EsConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(EsConfigHandler, self).__init__("elasticsearch")
        self.permit_keys = ("username", "password", "ipaddress", "port", "http_port", "host_name", "master_node", "ip")
        self.cfg["http_port"] = get_port("elasticsearch", "http_port")
        self.cfg["tcp_port"] = get_port("elasticsearch", "tcp_port")
        self.cfg["username"] = "admin"
        self.cfg["password"] = gen_pass()


class RabbitmqConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(RabbitmqConfigHandler, self).__init__("rabbitmq")
        self.permit_keys = ("username", "password", "ipaddress", "port", "NODENAME", "HOSTNAME", "is_standalone")
        self.cfg["username"] = "admin"
        self.cfg["password"] = gen_pass()
        self.cfg["port"] = get_port("rabbitmq", "port")
        self.cfg["manage_port"] = get_port("rabbitmq", "manage_port")
        self.cfg["empd_port"] = get_port("rabbitmq", "empd_port")
        self.cfg["erlang_port"] = get_port("rabbitmq", "erlang_port")


class EtcdConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(EtcdConfigHandler, self).__init__("etcd")
        self.permit_keys = ("username", "password", "ipaddress", "http_port", "tcp_port")
        self.cfg["http_port"] = get_port("etcd", "http_port")
        self.cfg["tcp_port"] = get_port("etcd", "tcp_port")


class MonitorConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(MonitorConfigHandler, self).__init__("monitor")
        self.permit_keys = (
            "ipaddress", "grafana_port", "prometheus_port", "mysql_exporter_port", "redis_exporter_port",
            "rabbitmq_exporter_port", "elasticsearch_exporter_port", "node_exporter_port"
                                                                     "k8s_metrics_port", "")
        self.cfg["grafana_port"] = 3000
        self.cfg["prometheus_port"] = 9090
        self.cfg["mysql_exporter_port"] = 9104
        self.cfg["redis_exporter_port"] = 9121
        self.cfg["rabbitmq_exporter_port"] = 9419
        self.cfg["elasticsearch_exporter_port"] = 9114
        self.cfg["node_exporter_port"] = 9100
        self.cfg["k8s_metrics_port"] = 31388
        self.cfg["istio_prometheus_port"] = 31390


class SiberConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(SiberConfigHandler, self).__init__("siber")
        self.permit_keys = ("ipaddress", "port")
        self.cfg["port"] = 88


class IdentityConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(IdentityConfigHandler, self).__init__("identity")
        self.permit_keys = ("ipaddress", "port", "nginx_proxy_port")
        self.cfg["port"] = get_port("identity", "port")
        self.cfg["nginx_proxy_port"] = get_port("identity", "nginx_proxy_port")


class OcrConfigHandler(MiddlewareConfigHandler):
    def __init__(self):
        super(OcrConfigHandler, self).__init__("ocr")
        self.permit_keys = ("ocr_document_gpu", "ocr_table_gpu", "ocr_receipt_gpu",
                            "ocr_idcard_gpu", "ocr_bankcard_gpu" "ocr_vehicle_gpu",
                            "ocr_vehiclelicense_gpu", "ocr_biz_gpu", "passport_gpu")
        self.cfg["ocr_document_gpu"] = get_port("ocr", "ocr_document_gpu")
        self.cfg["ocr_table_gpu"] = get_port("ocr", "ocr_table_gpu")
        self.cfg["ocr_receipt_gpu"] = get_port("ocr", "ocr_receipt_gpu")
        self.cfg["ocr_idcard_gpu"] = get_port("ocr", "ocr_idcard_gpu")
        self.cfg["ocr_bankcard_gpu"] = get_port("ocr", "ocr_bankcard_gpu")
        self.cfg["ocr_vehicle_gpu"] = get_port("ocr", "ocr_vehicle_gpu")
        self.cfg["ocr_vehiclelicense_gpu"] = get_port("ocr", "ocr_vehiclelicense_gpu")
        self.cfg["ocr_biz_gpu"] = get_port("ocr", "ocr_biz_gpu")
        self.cfg["ocr_passport_gpu"] = get_port("ocr", "ocr_passport_gpu")

    def get_ocr_module_port(self, module_name: str) -> int:
        return get_port("ocr", module_name)
