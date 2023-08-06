from __future__ import absolute_import
from __future__ import unicode_literals

import time
import os
import socket

from laipvt.helper.errors import Helper
from laipvt.handler.middlewarehandler import MiddlewareConfigHandler, HarborConfigHandler
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.model.cmd import ComposeModel
from laipvt.sysutil.util import path_join, ssh_obj, log
from laipvt.sysutil.gvalue import CHECK_INTERVAL
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.command import RM, MKDIR_DIR, CHMOD_777


class MiddlewareK8sInterface(MiddlewareInterface):
    def __init__(self, result: CheckResultHandler, handler: MiddlewareConfigHandler, template: str):
        super(MiddlewareK8sInterface, self).__init__(result=result, handler=handler, template=template)
        self.stand_install = """
    helm --host=localhost:44134 install --name={name} --set global.env=pvt \
                    --set namespace={namespace} \
                    --set image.repository={}\
    """

    def run(self, force=False):
        self.start()
        self.check()

    def reset(self):
        pass

    def check_port(self, ip, port):
        super().check_port(ip, port)

    def init(self, path) -> bool:
        pass

    def info(self):
        pass

    def start(self):
        pass

    def deploy(self, force=False):
        pass
