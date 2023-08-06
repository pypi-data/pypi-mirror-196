from __future__ import absolute_import
from __future__ import unicode_literals

import os
import time

import requests
from laipvt.controller.service.common_service import CommonController
from minio import Minio
from hashlib import sha256

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.helper.errors import Helper
from laipvt.sysutil.command import COMMANDER_UPGRADE_INSTALL, CREATE_DB, HELM_LIST, \
    FIX_ENTCMD_SIDECAR
from laipvt.sysutil.util import log, path_join, status_me, walk_sql_path, CommanderAes


class CommanderController(CommonController):
    def __init__(self, check_result, service_path,image_pkg_path=""):
        super(CommanderController, self).__init__(check_result, service_path)

    # 临时为了commander干掉entcmd-sidecar
    def fix_sidecar(self):
        self._exec_command_to_host(cmd=FIX_ENTCMD_SIDECAR, server=self.servers[0])

    def upgrade(self):
        super(CommanderController, self).upgrade()
        self.fix_sidecar()

    def run(self, force=False):
        super(CommanderController, self).run()
        self.fix_sidecar()

    def rebuild_data(self, force=False):
        super(CommanderController, self).rebuild_data()
        self.fix_sidecar()

