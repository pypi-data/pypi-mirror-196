from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.controller.service.common_service import CommonController

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me, path_join, log


class OcrStandardController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(OcrStandardController, self).__init__(check_result, service_path)
        self.tf_name = "ocr"

    @status_me("ocr", use_project_name=True)
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

    @status_me("ocr", use_project_name=True)
    def common_prepare_data(self, project):
        super().prepare_data(project)

    def upgrade(self):
        self.push_common_images_.set_force(True)
        self.push_common_images_()
        self.deploy_configmap.set_force(True)
        self.deploy_configmap(force=True)
        self.upgrade_service(project=self.project_name, namespace=self.namespace)
        self.common_prepare_data.set_force(True)
        self.common_prepare_data(self.project)
        self.apply_ocr_model_svc.set_force(True)
        self.apply_ocr_model_svc()

    def run(self, force=False):
        self.push_common_images_()
        self.deploy_configmap(force=True)
        self.start_common_service_()
        self.common_prepare_data(self.project)
        self.apply_ocr_model_svc()
