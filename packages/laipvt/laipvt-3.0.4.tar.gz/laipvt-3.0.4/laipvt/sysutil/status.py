#!/bin/env python
# -*- encoding: utf-8 -*-
import json
import os
import pathlib

from laipvt.sysutil.conf import status_file
from laipvt.sysutil.conf import specify_debug_file
import re

dict_tmpl = {
    "basesystem": {
        "kubernetes_unpack": 0,
        "install_harbor": 0,
        "install_nginx": 0,
        "add_hosts": 0,
        "system_prepare": 0,
        "init_primary_master": 0,
        "cp_kube_config": 0,
        "kube_completion": 0,
        "install_network_plugin": 0,
        "join_master": 0,
        "join_node": 0,
        "install_helm": 0,
        "install_istio": 0,
        "install_rook": 0,
        "install_nvidia_device_plugin": 0,
        "install_chaosblade": 0,
        "create_namespace": 0
    },
    "nginx": {
        "renew_apiserver_config": 0
    },
    "middleware": {
        "deploy_etcd": 0,
        "deploy_license": 0,
        "deploy_minio": 0,
        "deploy_mysql": 0,
        "deploy_redis": 0,
        "deploy_es": 0,
        "deploy_rabbitmq": 0,
        "deploy_identity": 0,
        "deploy_commander_identity": 0,
        "deploy_monitor": 0,
        "deploy_keepalived": 0,
        "deploy_siber": 0
    }
}


class Status:
    def __init__(self):
        self.status_file = status_file
        self.specify_file = specify_debug_file
        self.STATUS_SUCCESS = 1
        self.STATUS_FAILED = 2
        self.STATUS_NOT_RUNNING = 0
        self.status_dicts = [self.STATUS_NOT_RUNNING, self.STATUS_SUCCESS, self.STATUS_FAILED]
        self.specify_list = self.get_specify_list()
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as fp:
                self.status = json.load(fp)
        else:
            with open(self.status_file, 'a') as fp:
                fp.write(json.dumps(dict_tmpl, indent=4))
            self.status = dict_tmpl

    def reset_status(self):
        status = json.loads(json.dumps(dict_tmpl))
        with open(self.status_file, "w") as sf:
            json.dump(status, sf, indent=4)

    def _reload(self):
        with open(self.status_file) as sf:
            self.status = json.load(sf)

    def _update(self):
        with open(self.status_file, "w") as sf:
            json.dump(self.status, sf, indent=4)
        self._reload()

    def get_status_failed(self, project_name):
        step_list = []
        proj = self.status[project_name]
        for step in proj:
            if proj[step] == self.STATUS_FAILED:
                step_list.append(step)
        return step_list

    def get_status(self, project, step):
        try:
            self._reload()
            return self.status_dicts[self.status[project][step]]
        except KeyError:
            self.update_status(project, step, 0)
            self._reload()
            return self.status_dicts[self.status[project][step]]

    def get_specify_list(self):
        try:
            if not os.path.exists(self.specify_file):
                pathlib.Path(self.specify_file).touch(mode=0o444)
                return []
            with open(self.specify_file) as sf:
                return sf.readlines()
        except Exception:
            self.specify_list = []

    # 设置执行某项固定的操作
    def is_specify_action(self, project, step):
        if len(self.specify_list) == 0:
            return True
        for specify_line in self.specify_list:
            action = "%s_%s".format(project, step)
            if len(re.findall(specify_line, action)) >= 1:
                return True
        return False

    def update_status_proj(self, project, value):
        for line, va in self.status[project].items():
            self.update_status(project, line, value)

    def update_status(self, project, step, value):
        try:
            if project not in self.status.keys():
                self.status[project] = {}
            if step not in self.status[project].keys():
                self.status[project][step] = 0
            self.status[project][step] = int(self.status_dicts[value])
            self._update()
            return True
        except IndexError:
            return False
