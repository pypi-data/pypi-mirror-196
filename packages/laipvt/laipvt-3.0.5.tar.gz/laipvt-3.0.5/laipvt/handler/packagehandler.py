from __future__ import absolute_import
from __future__ import unicode_literals

import os

from laipvt.handler.middlewarehandler import HarborConfigHandler
from laipvt.model.cmd import DockerImageModel, DockerModel
from laipvt.model.harbor import HarborModel
from laipvt.sysutil.util import path_join, run_local_cmd, to_object, status_me, log
from laipvt.helper.exception import Forbidden, HandlerError
from laipvt.helper.errors import PackageErrors, Error, Helper
from laipvt.handler.confighandler import PvtAdminConfigHandler, ServiceConfigHandler, CheckResultHandler

"""
        目录结构
        授权id.tar.gz
          |- pvtadmin.json
          |- kubernetes.tar.gz
            |- templates/
              |- admin.tmpl
            |- plugin/
              |- network/
                  |- flannel.yaml
                  |- calico.yaml
              |- helm/
                  |- bin/
              |- istio/
                  |- bin/
                  |- istio.yaml
          |- middleware.tar.gz
            |- mysql/
                |- xxx.tmpl (docker-compose文件)
                |- nginx-xxx.tmpl
                |- config.tmpl
            |- redis/
            |- ...
          |- harbor.tar.gz
            |- install.sh
          |- mage.tar.gz
            |- config.yaml
            |- init/
              |- mysql/
            |- images/
              |- xxx.tar
            |- templates/
              |- xxx.conf
            |- charts/
          |- nlp.tar.gz
            |- config.yaml
            |- images
              |- xxx.tar
            |- data
              |- xxx
"""


class PackageHandler(object):
    def __init__(self, path: str, project_name: str, check_result: CheckResultHandler = None):
        # 存放包的目录
        self.location = path
        self.project_name = project_name
        self.component = project_name
        self.package_name = "{}.tar.gz".format(self.project_name)
        self.default_img_location = "image.tar"
        self.check_result = check_result
        # 要部署的项目名称
        self.root_dir = path_join(self.location, self.project_name)
        self.pkg = path_join(self.location, self.package_name)

    def unpack(self, nozip=False, package_name=None) -> bool:
        # print(package_name)
        if package_name:
            self.package_name = package_name
            self.root_dir = path_join(self.location, package_name.split(".tar.gz")[0])
            # 如果已经存在解压的目录则跳过解压步骤
            if os.path.exists(self.root_dir):
                return True
        log.info("unpack package: {}".format(self.package_name))
        cmd = "tar zxf {} -C {}".format(path_join(self.location, self.package_name), self.location)
        if nozip:
            cmd = "tar xf {} -C {}".format(path_join(self.location, self.package_name), self.location)
        res = run_local_cmd(cmd)
        if res.code == 0 and os.path.isdir(self.root_dir):
            return True
        raise HandlerError(PackageErrors().UNPACK_ERROR.format(res.stdout, cmd)) from None

    def pack(self, nozip=False) -> bool:
        cmd = "cd {} && tar zcvf {} {}".format(self.location, self.package_name, self.project_name)
        if nozip:
            cmd = "cd {} && tar cvf {} {}".format(self.location, self.package_name, self.project_name)
        res = run_local_cmd(cmd)
        if res.code == 0 and os.path.isdir(self.root_dir):
            return self.pkg
        raise HandlerError(PackageErrors().PACK_ERROR.format(res.stdout)) from None

    def push_images(self, img_location=None, project_name=None, base_harbor=False, ignoreExists=True):
        if img_location is None:
            img_location = self.default_img_location
        img_path = os.path.join(self.location, self.project_name, img_location)
        if not os.path.exists(img_path):
            log.info(Helper().FILE_NOT_FOUND.format(img_path))
            if not ignoreExists:
                exit(2)
            return
        log.info(Helper().PUSH_IMAGE.format(img_path))
        harbor_cfg = HarborConfigHandler().get_config_with_check_result()
        harbor_ip = harbor_cfg["harbor"]["lb"]
        registry_hub = "{}:{}".format(harbor_ip, harbor_cfg["harbor"]["nginx_harbor_proxy_port"])
        if base_harbor:
            master_ip = self.check_result.servers.get_role_ip("master")[0]
            registry_hub = "{}:{}".format(master_ip, harbor_cfg["harbor"]["http_port"])
        # print(image_path)
        # 导入的还是middleware。很好很合适
        if project_name is None:
            project_name = self.project_name
        docker = DockerImageModel(
            image=img_path, project=project_name, repo=registry_hub, tag_version=None
        )
        docker.run()

    def must_in(self, name: str, path: str) -> str:
        if name in os.listdir(path):
            return path_join(path, name)
        raise Forbidden(PackageErrors().PACKAGE_ILLEGAL.format(name)) from None

    def parse(self):
        raise HandlerError(Error().UNIMPLEMENT_ERROR.format("PackageHandler.parse"))

    def get(self):
        self.unpack()
        return self.parse()


class DeployPackageHandler(PackageHandler):
    """
    解析abcdefghi.tar.gz
    """

    def __init__(self, path: str, apply_id: str, check_result: CheckResultHandler = None):
        super(DeployPackageHandler, self).__init__(path, apply_id, check_result=check_result)
        # if len(apply_id) != 9:
        #     raise Forbidden(PackageErrors().PROJECT_ID_INCORRECT)

    def unpack(self):
        super().unpack(nozip=True)

    def parse(self):
        pvtadmin_file = "config.json"
        for i in os.listdir(self.root_dir):
            if pvtadmin_file in i:
                pvtadmin_file = i
        admin_config = PvtAdminConfigHandler(path_join(self.root_dir, pvtadmin_file))
        deploy_projects = admin_config.service_list.get()
        service_list = []
        for s in deploy_projects:
            service_list.append(ServicePackageHandler(self.root_dir, s))
        res = {
            "config": admin_config,
            "kubernetes": KubePackageHandler(self.root_dir, self.check_result),
            "middleware": MiddlewarePackageHandler(self.root_dir, self.check_result),
            "harbor": HarborPackageHandler(self.root_dir),
            "license": LicensePackageHandler(self.root_dir),
            "service": service_list
        }
        return to_object(res)


class KubePackageHandler(PackageHandler):
    def __init__(self, path: str, check_result):
        super(KubePackageHandler, self).__init__(path, "kubernetes", check_result)

    def kubernetes_unpack(self):
        if os.path.exists(os.path.join(self.location, self.package_name.split(".tar.gz")[0])):
            log.info("已经解压过了。跳过步骤")
            return
        cmd = "tar zxf {} -C {}".format(path_join(self.location, self.package_name), self.location)
        log.info("解压:{}".format(cmd))
        res = run_local_cmd(cmd)
        if res.code == 0 and os.path.isdir(self.root_dir):
            return True
        log.error(PackageErrors().UNPACK_ERROR.format(res.stdout))
        exit(2)

    def push_images(self, img_location=None):
        self._push_k8s_images()

    @status_me("basesystem")
    def _push_k8s_images(self):
        super().push_images(base_harbor=True, project_name="base_system", ignoreExists=False)

    def parse(self):
        res = {
            "templates": path_join(self.root_dir, "templates"),
            "plugin": {
                "network": path_join(self.root_dir, "plugin/network"),
                "helm": path_join(self.root_dir, "plugin/helm"),
                "istio": path_join(self.root_dir, "plugin/istio"),
                "rook": path_join(self.root_dir, "plugin/rook-ceph"),
                "chaosblade": path_join(self.root_dir, "plugin/chaosblade")
            },
            "k8s-rpms": path_join(self.root_dir, "k8s-rpms")
        }
        return to_object(res)


class MiddlewarePackageHandler(PackageHandler):
    def __init__(self, path: str, check_result):
        super(MiddlewarePackageHandler, self).__init__(path, "middleware", check_result)

    def push_images(self, img_location=None):
        self.push_middleware_images()

    @status_me("basesystem")
    def push_middleware_images(self):
        super().push_images(base_harbor=True, ignoreExists=False)

    def parse(self):
        """
        返回中间件列表
        :return: ["mysql", "redis", "minio"]
        """
        middlewares = os.listdir(self.root_dir)
        res = {}
        for m in middlewares:
            res[m] = path_join(self.root_dir, m)
        return to_object(res)


class HarborPackageHandler(PackageHandler):
    def __init__(self, path: str):
        super(HarborPackageHandler, self).__init__(path, "harbor")

    def parse(self):
        res = {
            "harbor": self.root_dir
        }
        return to_object(res)


class LicensePackageHandler(PackageHandler):
    def __init__(self, path: str):
        super(LicensePackageHandler, self).__init__(path, "license")

    def parse(self):
        config_file = ServiceConfigHandler(path_join(self.root_dir, "config.yaml"))
        res = {
            "config": config_file,
            "image": path_join(self.root_dir, "image"),
            "charts": path_join(self.root_dir, "chart"),
            "templates": path_join(self.root_dir, "templates"),
            "sqls": path_join(self.root_dir, "sqls"),
            "siber_sqls": path_join(self.root_dir, "siber_sqls"),
            "identity_sqls": path_join(self.root_dir, "identity_sqls"),
            "etcd_sign": path_join(self.root_dir, "etcd_sign.json"),
            "data": path_join(self.root_dir, "data")
        }
        return to_object(res)


class ServicePackageHandler(PackageHandler):
    def __init__(self, path: str, name: str):
        super(ServicePackageHandler, self).__init__(path, name)

    def parse(self):
        config_file = ServiceConfigHandler(path_join(self.root_dir, "config.yaml"))
        res = {
            "config": config_file,
            "image": path_join(self.root_dir, "image"),
            "charts": path_join(self.root_dir, "chart"),
            "template": path_join(self.root_dir, "template"),
            "sqls": path_join(self.root_dir, "sqls"),
            "siber_sqls": path_join(self.root_dir, "data", "siber_sqls"),
            "siber_sqls_ok": path_join(self.root_dir, "data", "siber_sqls_ok"),
            "identity_sqls": path_join(self.root_dir, "identity_sqls"),
            "data": path_join(self.root_dir, "data"),
            "tf_server_chart": path_join(self.root_dir, "chart"),
            "tf_server_data": path_join(self.root_dir, "data"),
            "test": path_join(self.root_dir, "test"),
            "project_name": self.project_name
        }
        return to_object(res)


class OcrPackageHandler(PackageHandler):
    def __init__(self, path: str, name: str):
        super(OcrPackageHandler, self).__init__(path, name)

    def parse(self):
        config_file = ServiceConfigHandler(path_join(self.root_dir, "config.yaml"))
        res = {
            "config": config_file,
            "image": path_join(self.root_dir, "image"),
            "charts": path_join(self.root_dir, "chart"),
            "templates": path_join(self.root_dir, "docker-compose.tmpl"),
            "license_file": path_join(self.root_dir, "data", "licServer.lic")
        }
        return to_object(res)


class PreCheckPackageHandler(PackageHandler):
    def __init__(self, path: str, name: str):
        super(PreCheckPackageHandler, self).__init__(path, name)

    def parse(self):
        res = {
            "checker": self.root_dir,
            "check_config": path_join(self.root_dir, "check_config.json")
        }
        return to_object(res)
