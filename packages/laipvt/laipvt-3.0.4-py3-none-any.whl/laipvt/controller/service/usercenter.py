from __future__ import absolute_import
from __future__ import unicode_literals

import os
import time

import requests
import yaml
from laipvt.controller.service.common_service import CommonController

from laipvt.helper.errors import Helper
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.gvalue import LAIPVT_BASE_DIR
from laipvt.sysutil.util import path_join, log, status_me


class UserCenterController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(UserCenterController, self).__init__(check_result, service_path)

        self.app_config_hosts = path_join(self.config, "Usercenter/entuc-config.conf")
        self.app_config_container = "/app/appsettings.json"

        self.nginx_template = path_join(self.templates_dir, "nginx/nginx-entuc/nginx-entuc.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-entuc.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-entuc.conf")

    @status_me("entuc")
    def entuc_proxy_on_nginx(self):
        self.proxy_on_nginx(self.nginx_template, self.nginx_tmp, self.nginx_file_remote)

    @status_me("entuc")
    def init_entuc_user(self, ignoreError=False):
        init_user_url = "http://{}:{}/api/tenant/install/byci".format(self.middleware_cfg.nginx.lb,
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
        while not succeed and counter < 8:
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
            if ignoreError is True:
                log.info("初始化用户有可能已经注册成功了。默认忽略.假如默认账号登录不了。请检查错误")
            else:
                log.info("初始化用户失败。请重新安装")
                exit(2)

    def run(self, force=False):
        super().run(force)
        self.entuc_proxy_on_nginx()
        if not force:
            self.project_pod_check()
        else:
            self.project_pod_check()

    def rebuild_data(self, force=True):
        super().rebuild_data(force)
        self.init_entuc_user(ignoreError=True)
