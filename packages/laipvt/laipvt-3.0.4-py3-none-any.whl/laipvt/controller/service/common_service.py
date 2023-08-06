from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me, log


class CommonController(ServiceInterface):
    def __init__(self, check_result, service_path, image_pkg_path=""):
        super(CommonController, self).__init__(check_result, service_path)

    @status_me("common", use_project_name=True)
    def deploy_configmap(self, force=True):
        self.deploy_all_configmap(force=force)

    @status_me("common", use_project_name=True)
    def deploy_istio_(self):
        self.deploy_istio()

    @status_me("common", use_project_name=True)
    def init_common_mysql_(self):
        self.init_mysql()

    @status_me("common", use_project_name=True)
    def init_common_rabbitmq_(self):
        self.init_rabbitmq()

    @status_me("common", use_project_name=True)
    def init_common_redis_(self):
        self.init_redis()

    @status_me("common", use_project_name=True)
    def init_common_minio_(self):
        self.init_minio()

    @status_me("common", use_project_name=True)
    def push_common_images_(self):
        self.push_images(self.project)

    def restart_service(self, namespace=""):
        if namespace != "":
            return super().restart_service(namespace)
        else:
            return super().restart_service(self.namespace)

    @status_me("common", use_project_name=True)
    def start_common_service_(self):
        self.start_service(project=self.project, version=self.private_deploy_version)

    @status_me("common", use_project_name=True)
    def common_apptest_(self):
        self.app_test(project=self.project)

    @status_me("common", use_project_name=True)
    def project_pod_check_(self):
        self.project_pod_check()

    @status_me("common", use_project_name=True)
    def upload_nacos_file(self):
        self.upload_nacos()

    def run_apptest(self):
        self.app_test(project=self.project)

    def upgrade(self):
        self.upload_nacos_file.set_force(True)
        self.upload_nacos_file()
        self.deploy_configmap.set_force(True)
        self.deploy_configmap()
        self.push_common_images_.set_force(True)
        self.push_common_images_()
        self.upgrade_service(project=self.project, namespace=self.namespace)
        self.prepare_data(self.project)
        self.project_pod_check_.set_force(True)
        self.project_pod_check_()

    def run(self, force=False):
        self.upload_nacos_file()
        self.init_common_mysql_()
        self.init_common_rabbitmq_()
        self.init_common_minio_()
        self.deploy_configmap()
        self.push_common_images_()
        self.start_common_service_()
        self.prepare_data(self.project)
        self.project_pod_check_()

    def app_test(self):
        super().app_test()

    def rebuild_data(self, force=False):
        self.init_common_mysql_.set_force(True)
        self.init_common_mysql_()
        self.init_common_rabbitmq_.set_force(True)
        self.init_common_rabbitmq_()
        self.init_common_minio_.set_force(True)
        self.init_common_minio_()
        self.restart_service(self.namespace)
        self.project_pod_check_.set_force(True)
        self.project_pod_check_()

