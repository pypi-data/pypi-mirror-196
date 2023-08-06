from prettytable import PrettyTable
from laipvt.sysutil.gvalue import CHECK_FILE
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.handler.middlewarehandler import MiddlewareConfigHandler
from laipvt.helper.errors import Helper
from laipvt.sysutil.util import log


def print_project_info():
    try:
        log.info(Helper().PRINT_PROJECT_INFO)
        tb = PrettyTable()
        tb.field_names = ["ProJect", "Desc", "URL"]
        # tb.add_row(["Adelaide", 1295, 1158259, 600.5])

        # 获取前置检查结果
        check_result_file = CHECK_FILE
        # 获取中间件信息
        middleware_cfg = MiddlewareConfigHandler("nginx").get_all_config_with_check_result()
        desc = "首页"
        url = "http://{}:{}/".format(middleware_cfg["nginx"]["lb"], middleware_cfg["nginx"]["entuc_proxy_port"])
        tb.add_row(["首页", desc, url])
        print(tb)

    except Exception as e:

        exit(2)
