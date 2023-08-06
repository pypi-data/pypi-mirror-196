from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.controller.service.common_service import CommonController

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me, path_join


class RpaCollaborationController(CommonController):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(RpaCollaborationController, self).__init__(check_result, service_path)
        self.nginx_template = path_join(self.templates_dir, "nginx/nginx-rpa-collaboration.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-rpa-collaboration.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-rpa-collaboration.conf")

    @status_me("rpa_collaboration")
    def prepare_rpa_collaboration_data(self):
        self.prepare_data(project=self.project)

    def upgrade(self):
        super().upgrade()

    def run(self,force=False):
        super().run()
