from __future__ import absolute_import
from __future__ import unicode_literals

import os
import json
from minio import Minio
from laipvt.helper.exception import UtilsError
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, status_me
from laipvt.sysutil.command import CREATE_DB
from laipvt.sysutil.conf import AccountIdConfig
from laipvt.model.sql import SqlModule
from laipvt.sysutil.command import HIDE_MENU_SQL


class MageController(ServiceInterface):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(MageController, self).__init__(check_result, service_path)

        self.nginx_template = path_join(self.templates_dir, "nginx/http/nginx-mage.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-mage.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-mage.conf")
        self.minio_data_list = [
            path_join(self.data_dir, "mage_minio_data"),
            path_join(self.data_dir, "siber_minio_data")
        ]

    @status_me("mage", use_project_name=True)
    def deploy_configmap(self):
        self.deploy_all_configmap()

    @status_me("mage", use_project_name=True)
    def deploy_mage_istio(self):
        self.deploy_istio()

    @status_me("mage")
    def init_minio_data(self):
        self.init_minio()

    def create_mage_db_if_exist(self):
        if self.middleware_cfg.mysql.is_deploy:
            mysql_host = self.master_host.ipaddress
        else:
            mysql_host = self.middleware_cfg.mysql.ipaddress[0]
        sql = SqlModule(host=mysql_host, port=int(self.middleware_cfg.mysql.port),
                        user=self.middleware_cfg.mysql.username, passwd=self.middleware_cfg.mysql.password)
        if not sql.select("show databases like '%_saas_docuds';"):
            create_db = CREATE_DB.format(db_name="laiye_saas_docuds")
            sql.insert_sql(create_db)

    @status_me("mage")
    def upgrade_mage_mysql(self):
        log.info("升级mage mysql")
        version = self.private_deploy_version.split("-")[0]

    @status_me("mage")
    def init_mage_mysql(self):
        log.info("初始化mage mysql")
        version = self.private_deploy_version.split("-")[0]

        self.create_mage_db_if_exist()
        cmd = "docker run --rm --entrypoint /home/works/program/mageTool \
        {}/{}/document-mining-innerservice:{} --operateMode dbnew \
        --host {} --user {} --password {} --port {} --toVersion {}".format(
            self.registry_hub, self.project, self.private_deploy_version,
            self.middleware_cfg.mysql.ipaddress[0], self.middleware_cfg.mysql.username,
            self.middleware_cfg.mysql.password, self.middleware_cfg.mysql.port,
            version
        )
        res = self._exec_command_to_host(cmd=cmd, server=self.servers[0], check_res=True)
        if res["code"] != 0:
            log.error("初始化mage mysql失败")
            log.error(res["stdout"])
            exit(2)
        log.info("初始化mage mysql完成")
        # self.init_mysql(sql_path=self.service_path.sqls)
        # 渲染siber sqls目录
        # FileTemplate(self.middleware_cfg, self.service_path.siber_sqls, self.service_path.siber_sqls_ok).fill()
        # self.init_mysql(sql_path=self.service_path.siber_sqls_ok)

    @status_me("mage")
    def mage_transfer_data(self):
        src_dir_path = path_join(self.service_path.data, "mage_transfer_data")
        dest_dir_path = path_join(self.deploy_dir, "mage_transfer_data")
        image = "{}/{}/document-mining-innerservice:{}".format(self.registry_hub, self.project,
                                                               self.private_deploy_version)
        version = self.private_deploy_version.split("-")[0]

        cmd = "docker run --rm --entrypoint /home/works/program/mageTool {image} \
         --operateMode datatransfer --dataMode 2 --minioAddr http://{minio_host}:{minio_port} \
          --host {mysql_host} --user {mysql_user} --password {mysql_password} --port {mysql_port} \
          --toVersion {version}".format(
            image=image, minio_host=self.middleware_cfg.minio.lb, minio_port=self.middleware_cfg.minio.port,
            mysql_host=self.middleware_cfg.mysql.ipaddress[0], mysql_user=self.middleware_cfg.mysql.username,
            mysql_password=self.middleware_cfg.mysql.password, mysql_port=self.middleware_cfg.mysql.port,
            version=version
        )
        self._send_file(src=src_dir_path, dest=dest_dir_path)
        res = self._exec_command_to_host(cmd=cmd, server=self.servers[0], check_res=True)
        log.info("userid: {}".format(res["stdout"].split("\n")[-1]))
        AccountIdConfig().save(res["stdout"].split("\n")[-1])

    @status_me("mage")
    def hide_menu(self):
        if self.middleware_cfg.mysql.is_deploy:
            mysql_host = self.master_host.ipaddress
        else:
            mysql_host = self.middleware_cfg.mysql.ipaddress[0]
        hide_menu_id = ",".join(map(lambda x: str(x), self.admin_config.hide_menu_id))
        if len(self.admin_config.siber_tags) == 0:
            self.admin_config.siber_tags.append("AI_ENGINE_OCR_GENERAL_TEXT_GPU")
        image = "{}/{}/document-mining-innerservice:{}".format(self.registry_hub, self.project,
                                                               self.private_deploy_version)
        version = self.private_deploy_version.split("-")[0]
        action_cmd_prefix = "docker run --rm --entrypoint /home/works/program/mageTool {image} \
                     --operateMode recordauthorize --toVersion {version}  --fromVersion v2.1 \
                      --host {mysql_host} --user {mysql_user} --password {mysql_password} --port {mysql_port} --name " \
                            "laiye_saas_docuds --engineStrs {siber_tag} --menuUids {hide_menu_id}"
        for siber_tag in self.admin_config.siber_tags:
            cmd = action_cmd_prefix.format(
                image=image, minio_host=self.middleware_cfg.minio.lb, minio_port=self.middleware_cfg.minio.port,
                mysql_host=mysql_host, mysql_user=self.middleware_cfg.mysql.username,
                mysql_password=self.middleware_cfg.mysql.password, mysql_port=self.middleware_cfg.mysql.port,
                siber_tag=siber_tag, version=version, hide_menu_id=hide_menu_id
            )
            log.debug("mageTools执行命令:{}".format(cmd))
            # 这边配置的hide_menu_id为空就不执行
            if hide_menu_id == "":
                log.error("部署mage时，hide_menu_id为空，不执行.请特别注意这个问题。默认是必须有的")
                return

            res = self._exec_command_to_host(cmd=cmd, server=self.servers[0], check_res=True)
            log.info("userid: {}".format(res["stdout"].split("\n")[-1]))
            log.info(res["code"])

    @status_me("mage", use_project_name=True)
    def push_mage_images(self):
        self.push_images(self.project)

    @status_me("mage", use_project_name=True)
    def start_mage_service(self):
        self.start_service(project=self.project, version=self.private_deploy_version, namespace=self.namespace)

    @status_me("mage", use_project_name=True)
    def prepare_nlp_data(self):
        self.prepare_data(project=self.project)

    @status_me("mage", use_project_name=True)
    def apply_mage_model_svc(self):
        model_svc_src = path_join(self.templates_dir, "model-svc")
        model_svc_dest = path_join(self.deploy_dir, "model-svc")
        if not os.path.exists(model_svc_src):
            log.info("package not found svc {}".format(self.project))
            return

        self._send_file(src=model_svc_src, dest=model_svc_dest)
        cmd = "kubectl apply -R -f {}".format(model_svc_dest)
        self._exec_command_to_host(cmd=cmd, server=self.harbor_hosts[0])

    @status_me("mage", use_project_name=True)
    def upgrade_mage_service(self):
        self.upgrade_service(project=self.project, namespace=self.namespace)

    @status_me("mage", use_project_name=True)
    def patch_text_cpu_configmap(self, machine_type):
        if self.project_name == "mage_core" or self.project_name == "mage":
            log.info("patch text_cpu configmap")
            if os.path.exists(self.config_templates):
                sed_cmd = "sed -i 's/ocr_self_text_machine=.*$/ocr_self_text_machine=\"{}\"/' {}".format(
                    path_join(self.config_templates, machine_type), "document-mining-backend.conf")
                self._exec_command_to_host(cmd=sed_cmd, server=self.master_host, check_res=False)
                log.info("临时修改mage_core为:{}".format(machine_type))
                self.deploy_configmap.set_force(True)
                self.deploy_configmap()
                self.restart_service(self.namespace)

    def upgrade(self):
        self.push_mage_images.set_force(True)
        self.push_mage_images()
        self.deploy_configmap.set_force(True)
        self.deploy_configmap()
        if self.project_name == "mage_core" or self.project_name == "mage":
            self.hide_menu.set_force(True)
            self.hide_menu()
        self.upgrade_mage_service.set_force(True)
        self.upgrade_mage_service()
        self.prepare_nlp_data.set_force(True)
        self.prepare_nlp_data()

    def run(self, force=False):
        self.push_mage_images()
        # 默认数据库初始化.只有mage_core才能做这一步
        if self.project_name == "mage_core" or self.project_name == "mage":
            self.init_mage_mysql()
        self.init_minio_data()
        self.deploy_configmap()
        self.deploy_mage_istio()
        self.start_mage_service()
        self.prepare_nlp_data()
        if not force:
            self.project_pod_check()
        if self.project_name == "mage_core" or self.project_name == "mage":
            self.hide_menu()
        self.apply_mage_model_svc()
