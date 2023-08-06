from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.controller.service.common_service import CommonController
from laipvt.controller.service.ocr_standard import OcrStandardController

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me


class OcrTextCpuController(OcrStandardController):
    def __init__(self, check_result, service_path,image_pkg_path=""):
        super(OcrTextCpuController, self).__init__(check_result, service_path)
        self.tf_name = "ocr-text_cpu"

