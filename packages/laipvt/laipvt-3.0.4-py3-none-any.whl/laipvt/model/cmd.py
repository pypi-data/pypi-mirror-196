from __future__ import absolute_import
from __future__ import unicode_literals

import docker
import datetime

from kubernetes import client, config
from kubernetes.config.kube_config import KUBE_CONFIG_DEFAULT_LOCATION
from kubernetes.client.rest import ApiException
from laipvt.helper.exception import ModelError
from laipvt.sysutil.util import log, path_join
from laipvt.handler.middlewarehandler import HarborConfigHandler
from laipvt.helper.errors import Helper


class DockerModel:
    def __init__(self, url=None):
        self.client = docker.APIClient(base_url=url, timeout=300)

    def _image_generator_parse(self, gen: any) -> str:
        image_name = []
        # log.info(image_name)
        for imageName in gen:
            image_name.append(imageName["stream"].split(" ")[-1].replace("\n", ""))
        # image_name = next(gen)["stream"].split(" ")[-1].replace("\n", "")
        # exit()
        return image_name

    def _parse_tag(self, image: str) -> dict:
        """
        :param image: tfserver:2.2.0-gpu
        :return: {"image_name": tfserver, "image_tag": 2.2.0-gpu}
        """
        try:
            t = image.split(":")
            return {"image_name": t[0], "image_tag": t[1]}
        except AttributeError as e:
            log.error("镜像{}导入失败：{}".format(image, e))
        return {"image_name": "", "image_tag": "t[1]"}

    def load(self, image: str) -> str:
        with open(image, "rb") as f:
            try:
                r = self.client.load_image(f, quiet=True)
            except Exception as e:
                log.error(e)
        try:
            return self._image_generator_parse(r)
        except Exception as e:
            log.error("导入镜像{}失败".format(image))
            log.error(e)

    def tag(self, old_image_withtag: str, new_image: str, new_image_tag: str, force=True) -> bool:
        try:
            return self.client.tag(old_image_withtag, new_image, new_image_tag, force=force)
        except Exception as e:
            log.error(e)

    def getImage(self, docker_name):
        try:
            self.client.containers().list()
        except Exception as e:
            log.error(e)

    def push(self, image: str, tag: str, auth_config=None) -> bool:
        res = list(self.client.push(image, tag, stream=True, decode=True, auth_config=auth_config))[-1]
        if "progressDetail" in res:
            return True
        if "errorDetail" in res:
            raise ModelError("DockerModel.push %s" % res.get("error")) from None
        raise ModelError("DockerModel.push %s" % res) from None

    def pull(self, image: str, tag: str, auth_config=None) -> bool:
        res = list(self.client.pull(image, tag, stream=True, decode=True, auth_config=auth_config))[-1]
        if "progressDetail" in res:
            return True
        if "errorDetail" in res:
            raise ModelError("DockerModel.push %s" % res.get("error")) from None
        raise ModelError("DockerModel.push %s" % res) from None


class DockerImageModel(DockerModel):
    def __init__(self, image: str, project: str, repo: str, tag_version: str):
        """
        :param image: /tmp/etcd.tar
        :param project: middleware
        :param repo: 1.1.1.1:8080
        docker load < /tmp/etcd.tar
        docker tag registry.cn-beijing.aliyuncs.com/laiye_poc/etcd:latest 1.1.1.1:8080/middleware/etcd:latest
        docker push 1.1.1.1:8080/middleware/etcd:latest
        """
        super(DockerImageModel, self).__init__()
        self.image = image  # 要导入的镜像文件路径
        self.repo = repo
        self.repo_path = "{}/{}".format(repo, project)
        self.new_image_addr = None
        self.tag_version = tag_version
        try:
            harbor_cfg = HarborConfigHandler().get_config_with_check_result()
            self.auth_config = {
                "username": "admin",
                "password": harbor_cfg["harbor"]["password"]
            }
        except Exception as e:
            log.error(e)
            self.auth_config = None

    def _parse_tag(self, image: str) -> dict:
        """
        :param image: tfserver:2.2.0-gpu
        :return: {"image_name": tfserver, "image_tag": 2.2.0-gpu}
        """
        try:
            t = image.split(":")
            version = self.tag_version
            if self.tag_version is None:
                version = t[1]
            return {"image_name": t[0], "image_tag": version}
        except AttributeError as e:
            log.error(Helper().PUSH_IMAGE_ERROR.format(image, e))
            exit(2)
        return {"image_name": "", "image_tag": self.tag_version}

    def __tag_and_push__(self, image, new_image_name, new_tag):
        log.info(Helper().TAG_IMAGE.format(
            image,
            path_join(self.repo_path, new_image_name),
            new_tag
        ))
        if self.tag(image, path_join(self.repo_path, new_image_name), new_tag):
            self.new_image_addr = path_join(self.repo_path, new_image_name)
            self.push(path_join(self.repo_path, new_image_name), new_tag,
                      auth_config=self.auth_config)

    # todo 改造成pool方式安裝
    def run(self) -> bool:
        if self.image is None:
            log.error(Helper().PUSH_IMAGE_ERROR.format(self.image, "镜像已经失败"))
            return False
        image_name_withtag = self.load(self.image)
        if image_name_withtag is None:
            log.error(Helper().PUSH_IMAGE_ERROR.format(self.image, "导入镜像失败,直接忽略继续执行"))
            return
        # pool来并发执行代码
        for image in image_name_withtag:
            image_name = self._parse_tag(image)
            new_image_name = image_name["image_name"].split("/")[-1]
            new_tag = image_name["image_tag"]
            self.__tag_and_push__(image, new_image_name, new_tag)
        log.info("push images finish")
        return True


class ComposeModel(object):
    """
    :return string
    """

    def __init__(self, compose_file: str, compose_cmd="/usr/bin/docker-compose"):
        """

        :param compose_file: string docker-compose路径
        """
        # try:
        #     if get_yaml_config(compose_file):
        self.compose_file = compose_file
        #     else:
        #         raise ModelError("ComposeModel.init %s 不是一个合法的docker-compose文件" % compose_file) from None
        # except UtilsError:
        #     raise ModelError("ComposeModel.init %s 不是一个合法的docker-compose文件" % compose_file) from None

        # try:
        #     if file_run_able(compose_cmd):
        self.compose = compose_cmd
        #     else:
        #         raise ModelError("ComposeModel.init %s 不是一个可执行文件" % compose_cmd)
        # except UtilsError as e:
        #     raise ModelError("ComposeModel.init %s" % e.msg) from None

    def up(self) -> str:
        return "%s -f %s up -d" % (self.compose, self.compose_file)

    def down(self) -> str:
        return "%s -f %s down" % (self.compose, self.compose_file)

    def restart(self) -> str:
        return "%s -f %s restart" % (self.compose, self.compose_file)


class KubeModel:
    def __init__(self, config_file=KUBE_CONFIG_DEFAULT_LOCATION):
        config.load_kube_config(config_file=config_file)
        self.cli = client.CoreV1Api()

    def create_namespace(self, namespace: str) -> dict:
        """

        :param namespace: string namespace名称
        :return: {name: namespace, status: Active}
        """
        body = client.V1Namespace()
        body.metadata = client.V1ObjectMeta(name=namespace)
        try:
            info = {}
            res = self.cli.create_namespace(body)
            info["name"] = namespace
            info["status"] = res.status.phase
            return info
        except client.exceptions.ApiException as apierror:
            raise ModelError("KubeModel.create_namespce API错误: %s" % apierror.reason) from None

    def get_node_status(self) -> list:
        """

        :return: [{node_name: "name", node_status: "Ready"}]
        """
        all_nodes = self.cli.list_node(pretty='true')
        node_info = []
        for node in all_nodes.items:
            info = {'name': node.metadata.name}
            for st in node.status.conditions:
                if st.reason == "KubeletReady":
                    info["status"] = st.type
            node_info.append(info)
        return node_info

    def get_all_pod_status(self, namespace="all_namespaces") -> list:
        """
        获取所有命令空间下的pod状态
        : return list

        [{
            "pod_ip":"10.244.0.19",
            "namespace":"mage",
            "pod_name":"ocr-text-recognition-tf-server-76d9c59d97-nt7lh",
            "status":"Running"
        },
        {
            "pod_ip":"10.244.0.25",
            "namespace":"mid",
            "pod_name":"license-manager-7d56c5f687-nsmzx",
            "status":"Running"
        }]
        """
        if namespace == "all_namespaces":
            ret = self.cli.list_pod_for_all_namespaces(watch=False, pretty='true')
        else:
            ret = self.cli.list_namespaced_pod(namespace=namespace)

        pod_info = []
        for item in ret.items:
            pod_info.append(
                {
                    "pod_ip": item.status.pod_ip,
                    "namespace": item.metadata.namespace,
                    "pod_name": item.metadata.name,
                    "status": item.status.phase
                }
            )
        return pod_info

    def get_all_deploy(self, namespace="all_namespaces"):
        apis_api = client.AppsV1Api()
        resp = apis_api.list_namespaced_deployment(namespace=namespace)
        return resp.items

    def restart_deploy(self, namespace="all_namespaces"):
        now = datetime.datetime.utcnow()
        now = str(now.isoformat("T") + "Z")
        body = {
            'spec': {
                'template': {
                    'metadata': {
                        'annotations': {
                            'kubectl.kubernetes.io/restartedAt': now
                        }
                    }
                }
            }
        }
        v1_apps = client.AppsV1Api()
        for i in self.get_all_deploy(namespace=namespace):
            try:
                v1_apps.patch_namespaced_deployment_with_http_info(i.metadata.name, namespace, body, pretty='true')
            except ApiException as e:
                print(e)
