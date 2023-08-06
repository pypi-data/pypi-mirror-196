from laipvt.handler.middlewarehandler import NacosConfigHandler
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.interface.middlewarek8sinterface import MiddlewareK8sInterface


class RedisK8sController(MiddlewareK8sInterface):
    def __init__(self, result, handler, template):
        super(RedisK8sController, self).__init__(result, handler, template)

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


