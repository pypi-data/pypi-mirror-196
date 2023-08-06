from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.controller.service.nlp import NlpController
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me


class NlpLaYouTlmController(NlpController):
	def __init__(self, check_result, service_path,image_pkg_path=""):
		super(NlpLaYouTlmController, self).__init__(check_result, service_path)
		self.tf_name = "nlp-layoutlm"

	def run(self, force=False):
	   self.push_common_images_()
	   self.start_common_service_()
	   self.prepare_nlp_data()



