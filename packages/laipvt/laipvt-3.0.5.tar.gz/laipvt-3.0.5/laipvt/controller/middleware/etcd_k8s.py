from laipvt.handler.middlewarehandler import NacosConfigHandler
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.interface.middlewarek8sinterface import MiddlewareK8sInterface


class EtcdK8sController(MiddlewareK8sInterface):
    def __init__(self, result, handler, template):
        super(EtcdK8sController, self).__init__(result, handler, template)
        self.nacos_cfg = NacosConfigHandler().get_config_with_check_result()

    def generate_conf_file(self) -> bool:
        pass

    def _generate_nacos_files(self):
        pass

    def _upload_files_to_nacos(self):
        pass

    def check_port(self, ip, port):
        pass

    def check(self) -> bool:
        pass

    def start(self):
        pass


