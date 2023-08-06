from os import path
from laipvt.sysutil.util import log, path_join

from laipvt.controller.service.common_service import CommonController
from laipvt.model.sql import SqlModule
from laipvt.sysutil.util import status_me, path_join
from laipvt.sysutil.command import CLOSE_SIDECAR, CLOSE_SIDECAR_END
from laipvt.model.cmd import DockerModel, DockerImageModel
from laipvt.model.harbor import HarborModel


class IapCloudController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(IapCloudController, self).__init__(check_result, service_path)

    @status_me("iapcloud", use_project_name=True)
    def start_common_service_(self):
        self._create_namespace(namespaces=["iap-cloud-tasks"], istio_injection_namespaces=None)
        super().start_common_service_()
        self.close_sidecar_()

    @status_me("iapcloud", use_project_name=True)
    def start_iapcloud_service(self):
        self.start_service(project=self.project, version=self.private_deploy_version, tf_name="iapcloud")

    @status_me("iapcloud", use_project_name=True)
    def close_sidecar_(self):
        cmds = [CLOSE_SIDECAR.format(namespace="iap-cloud", deployment="nginx-proxy") + CLOSE_SIDECAR_END,
                CLOSE_SIDECAR.format(namespace="iap-cloud", deployment="guacd") + CLOSE_SIDECAR_END,
                CLOSE_SIDECAR.format(namespace="iap-cloud", deployment="laiye-remote") + CLOSE_SIDECAR_END]
        for cmd in cmds:
            self._exec_command_to_host(cmd=cmd, server=self.servers[0])

    # 暂时没测试
    def upgrade(self):
        super().upgrade()
        self.close_sidecar_.set_force(True)
        self.close_sidecar_()
        # 需要自动set config
        self.auto_config_set_iap()

    def run(self, force=False):
        super().run()
        self.close_sidecar_()

    def rebuild_data(self, force=False):
        super().run()
        self.close_sidecar_()
        self.auto_config_set_iap.set_force(True)

    @status_me("iapcloud", use_project_name=True)
    def refresh_configmap_set(self):
        cmd = """
        kubectl get configmap -n iap-cloud laiye-cloud -o yaml \
        |sed 's/ENV_WORKER_NUMBER=0/ENV_WORKER_NUMBER=3/g' \
        |sed 's/ENV_CREATOR_NUMBER=0/ENV_CREATOR_NUMBER=5/g' > /tmp/laiye-cloud.yaml
        kubectl apply -f /tmp/laiye-cloud.yaml
        """
        self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=True)

    def refresh_machine_key(self, machine_key):
        cmd_change = """
        kubectl get configmap -n iap-cloud laiye-cloud -o yaml \
        |sed 's/CMD_MACHINE_AUTH_KEY=.*$/CMD_MACHINE_AUTH_KEY={}/g' >/tmp/laiye-cloud.yaml  
        """.format(machine_key)
        cmd_execute = """
        kubectl apply -f /tmp/laiye-cloud.yaml
        """
        self._exec_command_to_host(cmd=cmd_change, server=self.master_host, check_res=True)
        self._exec_command_to_host(cmd=cmd_execute, server=self.master_host, check_res=True)

    @status_me("iapcloud", use_project_name=True)
    def auto_config_set_iap(self):
        mysql_host = self.middleware_cfg.mysql.ipaddress[0]
        ip = self.check_result.lb
        port = self.middleware_cfg.nginx.entuc_proxy_port
        sql = SqlModule(host=mysql_host, port=int(self.middleware_cfg.mysql.port),
                        user=self.middleware_cfg.mysql.username, passwd=self.middleware_cfg.mysql.password)
        get_machine_key = """
        select company_id,connection_key from laiye_entcmd.tbl_cmd_machine where  host_type=100 order by create_time desc limit 1;
        """
        insert_machine_key_result = sql.select(get_machine_key)
        if len(insert_machine_key_result) != 0 or insert_machine_key_result is None:
            insert_machine_key = insert_machine_key_result[0]["connection_key"]
            company_id = insert_machine_key_result[0]["company_id"]
        else:
            log.error("insert machine key cannot get ")
            exit(2)
            return
        url = "http://{}:{}".format(ip, port)
        remark_value = "'{\"CreatorUri\":\"" + url + "/iapcloud\",\"IsEnabled\":true}'"
        insert_sql_cmd = """
            INSERT INTO `laiye_entuc`.`tbl_plat_company_configuration`(`company_id`, `name`, `remark`, `key`, `value`) 
             select {}, 'CMD_DockerRPA', '{}', 'CMD_DockerRPA',  {}
             from dual where not exists (select 1 from `laiye_entuc`.`tbl_plat_company_configuration` where `name`='CMD_DockerRPA');
        """.format(company_id, insert_machine_key, remark_value)
        log.info(insert_sql_cmd)
        sql.insert_sql(insert_sql_cmd)
        self.refresh_machine_key(insert_machine_key)
