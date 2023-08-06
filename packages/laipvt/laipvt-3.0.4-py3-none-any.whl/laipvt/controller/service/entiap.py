from laipvt.controller.service.common_service import CommonController
from laipvt.interface.serviceinterface import ServiceInterface


class EntiapController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(EntiapController, self).__init__(check_result, service_path)
