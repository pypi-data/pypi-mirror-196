from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.controller.service.common_service import CommonController

from laipvt.sysutil.ssh import SSHConnect
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import path_join, log, status_me


def ssh_obj(ip, user, password, port=22) -> SSHConnect:
    return SSHConnect(hostip=ip, username=user, password=password, port=port)


class ChatbotController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(ChatbotController, self).__init__(check_result, service_path)

        self.chatbot_app_config_hosts = path_join(self.config, "Chatbot/laiye-chatbot-app.conf")
        self.chatbot_app_config_container = "/home/works/program/conf/online.conf"

        self.nginx_template = path_join(self.templates_dir, "nginx/nginx-chatbot.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-chatbot.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-chatbot.conf")

    @status_me("chatbot")
    def init_common_mysql_(self):
        super().init_common_mysql_()
        log.info("初始化mysql数据")
        # version = self.private_deploy_version.split("-")[0]
        mysql_real_ip = self.master_host.ipaddress
        if not self.middleware_cfg.mysql.is_deploy:
            mysql_real_ip = self.middleware_cfg.mysql.ipaddress[0]

        # docker run -t {进程：chatbot-app} --init
        cmd = "docker run --add-host mysql.default.svc:{} -t -v {}:{} {}/{}/chatbot-app:{} --init".format(
            mysql_real_ip,
            self.chatbot_app_config_hosts, self.chatbot_app_config_container,
            self.registry_hub, self.project, self.private_deploy_version
        )
        res = self._exec_command_to_host(cmd=cmd, server=self.servers[0], check_res=True)
        if res["code"] != 0:
            log.error("初始化mysql数据失败")
            log.error(res["stdout"])
            exit(2)
        log.info("初始化mysql数据完成")

    def run(self, force=False):
        super().run()


