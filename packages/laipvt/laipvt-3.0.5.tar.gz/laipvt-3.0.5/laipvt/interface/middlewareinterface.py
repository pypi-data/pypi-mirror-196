from __future__ import absolute_import
from __future__ import unicode_literals

import time
import os
import socket
import traceback

from laipvt.helper.errors import Helper
from laipvt.handler.middlewarehandler import MiddlewareConfigHandler, HarborConfigHandler
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.model.cmd import ComposeModel
from laipvt.sysutil.util import path_join, ssh_obj, log
from laipvt.sysutil.gvalue import CHECK_INTERVAL
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.command import RM, MKDIR_DIR, CHMOD_777


class MiddlewareInterface():
    def __init__(self, result: CheckResultHandler, handler: MiddlewareConfigHandler, template: str):
        self.check_result = result
        self.handler = handler
        self.template = template

        self.deploy_dir = self.check_result.deploy_dir
        self.middleware_name = self.handler.get_value("name")
        self.check_interval = CHECK_INTERVAL
        self.compose_template = path_join(self.template, "{}.tmpl".format(self.middleware_name))
        self.nginx_template = path_join(self.template, "nginx-{}.tmpl".format(self.middleware_name))
        self.servers = self.check_result.servers
        self.server_list = self.servers.get_role_ip("master")
        self.master_server = self.servers.get_role_obj("master")
        self.harbor_server = self.servers.get_role_obj("harbor")
        self.handler.set("ipaddress", self.server_list)
        self.all_server = self.servers.get()
        self.base_dir = path_join(self.deploy_dir, self.middleware_name)
        self.docker_compose_file_tmp = path_join("/tmp", "docker-compose-{}.yaml".format(self.middleware_name))
        self.nginx_config_tmp = path_join("/tmp", "nginx-{}.conf".format(self.middleware_name))

        self.docker_compose_file = path_join(self.base_dir, "docker-compose.yml")
        self.nginx_config_file = path_join(self.deploy_dir, "nginx", self.handler.get_proxy_type(),
                                           "{}.conf".format(self.middleware_name))
        self.nginx_compose_file = path_join(self.deploy_dir, "nginx", "docker-compose.yml")
        self.harbor_cfg = HarborConfigHandler().load()
        self.handler.set("harbor_http_port", self.harbor_cfg["harbor"]["http_port"])
        self.handler.set("harbor_ipaddress", [self.harbor_server[0].ipaddress, ])
        self.registry_hub = "{}:{}".format([self.harbor_server[0].ipaddress, ][0],
                                           self.harbor_cfg["harbor"]["nginx_harbor_proxy_port"])
        self.check_max_tries = 10
        self.check_sleep_seconds = 15

    def info(self):
        return self.handler.cfg

    def wait_for_service_start(self):
        time.sleep(self.check_interval)

    def check_is_deploy(self, cfg):
        return False if cfg[self.middleware_name]["is_deploy"] == False else True

    def generate_docker_compose_file(self, data_dict) -> bool:
        FileTemplate(data_dict, self.compose_template, self.docker_compose_file_tmp).fill()
        return True if os.path.isfile(self.docker_compose_file_tmp) else False

    def send_docker_compose_file(self):
        for server in self.master_server:
            log.info(
                Helper().SEND_FILE.format(self.docker_compose_file_tmp, server.ipaddress, self.docker_compose_file))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                ssh_cli.put(self.docker_compose_file_tmp, self.docker_compose_file)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def send_docker_compose_file_hosts(self, host):
        log.info(Helper().SEND_FILE.format(self.docker_compose_file_tmp, host.ipaddress, self.docker_compose_file))
        ssh_cli = ssh_obj(ip=host.ipaddress, user=host.username, password=host.password, port=host.port)
        try:
            ssh_cli.put(self.docker_compose_file_tmp, self.docker_compose_file)
        except Exception as e:
            log.error(e)
            exit(2)
        finally:
            ssh_cli.close()

    def send_config_file(self, server, src, dest, ignore='', ignoreError=False):
        log.info(Helper().SEND_FILE.format(src, server.ipaddress, dest))
        ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
        try:
            ssh_cli.put(src, dest, ignore)
        except Exception as e:
            log.error(e)
            if not ignoreError:
                log.info("忽略错误")
                exit(2)
        finally:
            ssh_cli.close()

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

    def start(self):
        compose_cmd = ComposeModel(self.docker_compose_file)
        for server in self.master_server:
            log.info(Helper().START_MIDDLEWARE_SERVICE.format(server.ipaddress, self.middleware_name))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                res = ssh_cli.run_cmd(compose_cmd.up())
                if res["code"] != 0:
                    log.error(Helper().START_MIDDLEWARE_SERVICE_ERROR.format(res["stderr"], res["stdout"]))
                    exit(2)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def start_all_node(self):
        compose_cmd = ComposeModel(self.docker_compose_file)
        for server in self.all_server:
            log.info(Helper().START_MIDDLEWARE_SERVICE.format(server.ipaddress, self.middleware_name))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                res = ssh_cli.run_cmd(compose_cmd.up())
                if res["code"] != 0:
                    log.error(Helper().START_MIDDLEWARE_SERVICE_ERROR.format(res["stderr"], res["stdout"]))
                    exit(2)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def restart(self):
        compose_cmd = ComposeModel(self.docker_compose_file)
        for server in self.master_server:
            log.info(Helper().RESTART_MIDDLEWARE_SERVICE.format(server.ipaddress, self.middleware_name))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                res = ssh_cli.run_cmd(compose_cmd.restart())
                if res["code"] != 0:
                    log.error(Helper().START_MIDDLEWARE_SERVICE_ERROR.format(res["stderr"], res["stdout"]))
                    exit(2)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def clean_and_reset(self):
        self.remove(force=True)
        self.deploy(force=True)

    def reset(self):
        compose_cmd = ComposeModel(self.docker_compose_file)
        for server in self.master_server:
            log.info(Helper().RESET_MIDDLEWARE_SERVICE.format(server.ipaddress, self.middleware_name))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                res = ssh_cli.run_cmd(compose_cmd.down())
                res = ssh_cli.run_cmd(compose_cmd.up())
                if res["code"] != 0:
                    log.error(Helper().START_MIDDLEWARE_SERVICE_ERROR.format(res["stderr"], res["stdout"]))
                    exit(2)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def create_logs_dir(self, log_path):
        log.info(Helper().CREATE_LOG_PATH.format(log_path))
        cmd = [
            MKDIR_DIR.format(log_path),
            CHMOD_777.format(log_path)
        ]
        for server in self.master_server:
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username,
                              password=server.password, port=server.port)
            ssh_cli.run_cmdlist(cmd)

    def check(self) -> bool:
        pass

    def deploy(self, force=False):
        pass

    def check_port(self, ip, port):
        try:
            if int(port) > 65536:
                return False
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = s.connect_ex((ip, port))
                if result == 0:
                    return True
                s.close()
        except Exception as e:
            log.error(e)
            return False

    def init(self, path) -> bool:
        FileTemplate(self.handler.cfg, self.nginx_template, self.nginx_config_tmp).fill()
        return True if os.path.isfile(self.nginx_config_tmp) else False

    def update_nginx_config(self):
        compose_cmd = ComposeModel(self.nginx_compose_file)
        for server in self.master_server:
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                ssh_cli.put(self.nginx_config_tmp, self.nginx_config_file)
                ssh_cli.run_cmd(compose_cmd.restart())
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def remove(self, force=False):
        log.info("remove package: {} basedir:{}".format(self.docker_compose_file, self.base_dir))
        compose_cmd = ComposeModel(self.docker_compose_file)
        for server in self.master_server:
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                ssh_cli.run_cmd(compose_cmd.down())
                ssh_cli.run_cmd(RM.format(self.base_dir))
            except Exception as e:
                log.error(e)
                if not force:
                    exit(2)
            finally:
                ssh_cli.close()

    def render_by_go_render(self, file_bin_remote, template_path, value_path, k8s_dest_path, dest_path, files=[]):
        try:
            master = self.master_server[0]
            ssh_cli = ssh_obj(ip=master.ipaddress, user=master.username, password=master.password, port=master.port)
            render_cmd = "{} -tmplPath={} -valuePath={} -targetPath={}  -configTargetPath={} -genProjects={}".format(
                file_bin_remote,
                template_path,
                value_path,
                k8s_dest_path,
                dest_path,
                ",".join(files),
            )
            cmds = [
                "chmod +x {}".format(file_bin_remote),
                render_cmd
            ]
            for cmd in cmds:
                result = ssh_cli.run_cmd(cmd)
                log.info("render nacos file {},result:{}".format(render_cmd, result))
        except Exception as e:
            log.info("nacos stand file generate error:{}".format(e))
            traceback.print_exc()
            exit(0)

    def run(self, force=False):
        log.info("install middleware {}".format(self.middleware_name))
        self.generate_docker_compose_file({})
        self.send_docker_compose_file()
        self.start()
        self.check()
        self.update_nginx_config()
