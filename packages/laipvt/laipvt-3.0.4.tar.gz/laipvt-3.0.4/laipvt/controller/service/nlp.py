from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from laipvt.controller.service.common_service import CommonController

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me, path_join, log


class NlpController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(NlpController, self).__init__(check_result, service_path)
        self.config_templates = path_join(self.templates_dir, "templates", self.namespace.capitalize())
        self.config_remote = path_join(self.deploy_dir, "templates", self.namespace.capitalize())
        self.config_target = path_join(self.deploy_dir, "configmap")
        self.config = path_join(self.deploy_dir, "{}_config".format(self.namespace))
        self.configmap = path_join(self.config_target, self.namespace.capitalize())
        self.configmap_remote = path_join(self.deploy_dir, self.namespace.capitalize())

    @status_me("nlp", use_project_name=True)
    def prepare_nlp_data(self):
        self.prepare_data(self.project)

    @status_me("nlp", use_project_name=True)
    def apply_ocr_model_svc(self):
        try:
            model_svc_src = path_join(self.templates_dir, "model-svc")
            model_svc_dest = path_join(self.deploy_dir, "model-svc")
            self._send_file(src=model_svc_src, dest=model_svc_dest, force=True)
            cmd = "kubectl apply -R -f {}".format(model_svc_dest)
            self._exec_command_to_host(cmd=cmd, server=self.harbor_hosts[0])
        except:
            log.info("no model service found for {}".format(self.project_name))
            pass

    def run(self, force=False):
        self.push_common_images_()
        self.deploy_configmap()
        self.apply_ocr_model_svc()
        self.start_common_service_()
        self.prepare_nlp_data()

    def upgrade(self):
        self.apply_ocr_model_svc.set_force(True)
        self.apply_ocr_model_svc()
        self.deploy_configmap.set_force(True)
        self.deploy_configmap()
        self.push_common_images_.set_force(True)
        self.push_common_images_()
        self.upgrade_service(project=self.project,namespace=self.namespace)
        self.prepare_nlp_data.set_force(True)
        self.prepare_nlp_data()
