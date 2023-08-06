from __future__ import absolute_import
from __future__ import unicode_literals
import time
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import path_join, log, status_me


class WepController(ServiceInterface):
    def __init__(self, check_result, service_path,image_pkg_path=""):
        super(WepController, self).__init__(check_result, service_path)
