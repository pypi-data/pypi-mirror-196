import json
import os

import requests
import time

import yaml

from laipvt.controller.service.common_service import CommonController
from laipvt.helper.errors import Helper
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.model.cmd import ComposeModel
from laipvt.sysutil.gvalue import LAIPVT_BASE_DIR
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, status_me, log


class UCenterController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(UCenterController, self).__init__(check_result, service_path)

    @status_me("usercenter", use_project_name=True)
    def init_ucenter_user(self, force=False):
        init_user_url = "http://{}:{}/admin-console/api/install/byci".format(self.middleware_cfg.nginx.lb,
                                                                             self.middleware_cfg.nginx.entuc_proxy_port)
        log.info(init_user_url)
        headers = {
            # 'Content-Type': 'application/json',
        }
        json_data = {'username': self.middleware_cfg["base"].get("account"),
                     'password': self.middleware_cfg["base"].get("password"), 'tenantName': 'Laiye Tech', }
        counter = 0
        succeed = False
        msg = ""

        log.info("curl -v --trace --request POST --data:{} {}".format(json.dumps(json_data), init_user_url))
        while not succeed and counter < 5:
            try:
                response = requests.post(init_user_url, headers=headers, json=json_data, timeout=100)
                if response.json()["code"] == 102 or response.json()["code"] == 0:
                    succeed = True
                    msg = response.json()
                    log.info(Helper().INIT_ENTUC_USER_SUCCEED.format(msg))
                else:
                    counter = counter + 1
                    msg = response.json()
                    log.error(Helper().INIT_ENTUC_USER_FAILED.format(msg))
            except Exception as e:
                counter = counter + 1
                msg = "Access Error: {}".format(e)
                log.error(Helper().INIT_ENTUC_USER_FAILED.format(msg))
                time.sleep(20 * counter)
        if succeed:
            log.info(Helper().INIT_ENTUC_USER_SUCCEED.format(msg))
        else:
            log.error(Helper().INIT_ENTUC_USER_FAILED.format(msg))
            if force is True:
                log.info("初始化用户有可能已经注册成功了。默认忽略.假如默认账号登录不了。请检查错误")
            else:
                log.info("初始化用户失败。请重新安装")
                exit(2)

    # main方法主要开始初始化ucenter的方法
    @status_me("usercenter", use_project_name=True)
    def generate_master_nginx_config(self):
        template_folder = os.path.join(os.path.dirname(__file__), "templates")
        template_file = os.path.join(template_folder, "master-nginx.tmpl")
        master_nginx_conf_tmp = path_join("/tmp", "master-nginx.conf")
        nginx_file_remote = path_join(self.deploy_dir, "nginx/http/master-nginx-service.conf")
        FileTemplate(self.middleware_cfg, template_file, master_nginx_conf_tmp).fill()
        self._send_file(src=master_nginx_conf_tmp, dest=nginx_file_remote)
        compose_cmd = ComposeModel(self.nginx_compose_file)
        for server in self.servers:
            self._exec_command_to_host(cmd=compose_cmd.restart(), server=server, check_res=True)
        time.sleep(30)


    def run(self, force=False):
        super().run()
        self.deploy_istio()
        self.generate_master_nginx_config()
        self.project_pod_check()
        self.restart_service(namespace=self.namespace)
