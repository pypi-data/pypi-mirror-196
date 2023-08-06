from laipvt.controller.service.common_service import CommonController
from laipvt.interface.serviceinterface import ServiceInterface


class EntccController(CommonController):
        def __init__(self, check_result, service_path,image_pkg_path=""):
            super(CommonController, self).__init__(check_result, service_path)
