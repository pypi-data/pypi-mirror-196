from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.controller.service.common_service import CommonController

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import path_join, log, status_me


class DataServiceController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(DataServiceController, self).__init__(check_result, service_path)
        self.middleware_cfg["postgresql"]["db"] = self.middleware_cfg["postgresql"].get("database", "pgsqldb")


