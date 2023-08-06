from __future__ import absolute_import
from __future__ import unicode_literals

import os
import traceback

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from laipvt.sysutil.util import path_join, log
from laipvt.helper.errors import Helper


class Template(object):
    def __init__(self, data: dict, file_path: str, file_dest: str):
        self.file_path = file_path
        self.file_dest = file_dest
        self.data = data

    def template_handler(self, src: str) -> str:
        pass

    def _fill(self, src, dest):
        log.debug(Helper().LOCAL_FILL.format(src, dest))
        dest_dir = os.path.dirname(dest)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        content = self.template_handler(src)
        if content == "":
            log.error("dest:{},content: {} is Empty".format(dest, content))
        with open(dest, 'w+', encoding='utf-8') as fp:
            fp.write(content)

    def fill(self, ignoreError=False):
        if os.path.isfile(self.file_path):
            file_path = self.file_path
            file_dest = self.file_dest
            self._fill(file_path, file_dest)
        elif os.path.isdir(self.file_path):
            if not os.path.exists(self.file_dest):
                os.makedirs(self.file_dest)
            self.fill_all(self.file_path, self.file_dest)
        else:
            log.error(Helper().FILL_ERROR.format(self.file_path, "filepath:{} not exists,filepath:{}".format(self.file_path,self.file_dest)))
            if not ignoreError:
                traceback.print_stack()
                exit(2)

    def fill_all(self, src, dest):
        try:
            log.debug("fill config all {}:{}".format(src, dest))
            for root, dirs, files in os.walk(src):
                for file_name in files:
                    file_path = path_join(root, file_name)
                    if len(root) == len(src):
                        file_dest = path_join(dest, file_name)
                    else:
                        new_path = root.replace("{}/".format(src), "")
                        while True:
                            if new_path.startswith("/"):
                                new_path = new_path[1:]
                            else:
                                break
                        file_dest = path_join(dest, new_path, file_name)
                    self._fill(file_path, file_dest)
        except Exception as e:
            log.error(Helper().FILL_ERROR.format(self.file_path, ""))
            exit(2)

    def run(self):
        pass


class FileTemplate(Template):
    def __init__(self, data, file_path, file_dest):
        super().__init__(data, file_path, file_dest)

    def template_handler(self, src):
        try:
            # log.info("template render: src:{},des:{},data:{}".format(self.file_path, self.file_dest, self.data))
            loader = FileSystemLoader(src)
            env = Environment(loader=loader, undefined=StrictUndefined)
            return env.get_template('').render(self.data)

        except Exception as e:
            log.debug("src:{},des:{},data:{}".format(self.file_path, self.file_dest, self.data))
            log.error(Helper().FILL_ERROR.format(src, e))
            exit(2)
