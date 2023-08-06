from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.sysutil.conf import YamlConfig
from laipvt.sysutil.gvalue import PORT_MAP, DEPLOY_LANGUAGE
from laipvt.sysutil.util import log

module_require_tfserver = ("ocr_standard", "captcha", "nlp", "ocr_seal")
tfserver_name = {
    "ocr_standard": ["ocr-ctpn-tf-server", "ocr-text-recognition-tf-server",
                     "ocr-unet-table-tf-serving", "semantic-correct"],
    "captcha": ["verification-tf-serving"],
    "nlp": ["bert-service-tf"],
    "ocr_seal": ["ocr-seal-tf-serving"]
}

tfserver_image_name = {
    "ocr_standard": "tfserving",
    "captcha": "tfserving",
    "nlp": "tfserving",
    "ocr_seal": "tfserving"
}

# service_module_relation = {
#     "commander": [x for x in range(0, 9)],
#     "usercenter": [10],
#     "dataservice": [81],
#     "mage": [x for x in range(31, 51)],
#     # "wulai": [x for x in range(11, 31)],
#     "chatbot": [x for x in range(11, 31)],
#     "nlp": [33, 34, 35],
#     "captcha": [32],
#     "ocr_text_table": [36, 37],
#     "ocr_3rd": [x for x in range(51, 80)],
#     "ocr_seal": [38, 39],
#     "ocr": [40],
#     "ocr_idcard_server": [41, 42]
# }
service_module_relation = {
    # "entcmd": [x for x in range(0, 9)],
    # "entuc": [10],
    "entcmd": [10],
    "entuc": [0],
    "notice": [6],
    "dataservice": [16],
    "mage": [x for x in range(31)],
    # "wulai": [x for x in range(11, 31)],
    "chatbot": [x for x in range(11)],
    "nlp": [34],
    "captcha": [32],
    "ocr_text": [36, 37],
    "ocr_table": [38, 39],
    "ocr_seal": [40],
    "ocr_idcard": [42],
    "ocr": [30],
    "ocr_3rd": [x for x in range(61, 104)]
}

ocr_standard = range(36, 51)
ocr = range(51, 80)
if DEPLOY_LANGUAGE == "cn":
    module_info = {
        0: ("entuc", "用户中心"),
        2: ("ucenter", "用户中心"),
        1: ("license", "License授权服务"),
        5: ("rpa-collaboration", "人机协同中心"),
        6: ("notice", "通知中心"),
        10: ("entcmd", "Commander"),
        11: ("chatbot", "ChatBot吾来对话机器人"),
        12: ("entbs", "机器人商城"),
        13: ("entiap", "门户"),
        14: ("entcc", "需求管理"),
        16: ("dataservice", "数据服务"),
        30: ("ocr", "ocr go服务"),
        38: ("mage_core", "UiBot Mage"),
        40: ("mage_core", "UiBot Mage"),
        41: ("ocr_core", "ocr_core"),
        42: ("ocr_self_text_core", "ocr_self_text_core"),
        43: ("ocr_self_table_core", "ocr_self_table_core"),
        44: ("ocr_self_seal", "ocr_self_seal"),
        45: ("ocr_self_code", "ocr_self_code"),
        46: ("ocr_self_card", "ocr_self_card"),
        47: ("ocr_self_verification", "ocr_self_verification"),
        48: ("ocr_self_invoice", "ocr_self_invoice"),
        49: ("nlp_doc_extract", "nlp_doc_extract"),
        50: ("nlp_info_extract", "nlp_info_extract"),
        51: ("nlp_text_classifier", "nlp_text_classifier"),
        52: ("doc_self_training", "doc_self_training"),
        53: ("nlp_layout_extract", "nlp_layout_extract"),
        54: ("nlp_address", "nlp_address"),
        55: ("ocr_tzlf_card", "ocr_tzlf_card"),
        56: ("field_reprocess", "field_reprocess"),
        57: ("nlp_layoutlm", "nlp_layoutlm"),
        58: ("ocr_text", "ocr_text"),
        59: ("ocr_layout_analysis", "ocr_layout_analysis"),
        60: ("ocr_idcard", "ocr_idcard"),
        61: ("ocr_bizlicense", "ocr_bizlicense"),
        62: ("ocr_vehlicense", "ocr_vehlicense"),
        63: ("captcha", "captcha"),
        64: ("ocr_seal", "ocr_seal"),
        65: ("ocr_invoice", "ocr_invoice"),
        66: ("ocr_text_cpu", "ocr_text_cpu"),
        67: ("ocr_table", "ocr_table"),
        68: ("nlp_encoder", "nlp_encoder"),
        68: ("nlp_triton_server_gpu", "nlp_triton_server_gpu"),
        69: ("nlp_triton_server_cpu", "nlp_triton_server_cpu"),
    }
else:
    module_info = {
        0: ("entuc", "Enterprise Usercenter"),
        1: ("license", "License Service"),
        5: ("rpa-collaboration", "RPA Collaboration"),
        6: ("notice", "Notice Center"),
        10: ("entcmd", "Enterprise Commander"),
        11: ("chatbot", "Conversational AI Platform"),
        12: ("entbs", "Bot Store"),
        13: ("entiap", "Portal"),
        14: ("entcc", "Bot Center"),
        16: ("dataservice", "Data Service"),
        30: ("ocr", "Ocr Go"),
        40: ("mage_core", "UiBot Mage"),
        41: ("ocr_core", "ocr_core"),
        42: ("ocr_self_text_core", "ocr_self_text_core"),
        43: ("ocr_self_table_core", "ocr_self_table_core"),
        44: ("ocr_self_seal", "ocr_self_seal"),
        45: ("ocr_self_code", "ocr_self_code"),
        46: ("ocr_self_card", "ocr_self_card"),
        47: ("ocr_self_verification", "ocr_self_verification"),
        48: ("ocr_self_invoice", "ocr_self_invoice"),
        49: ("nlp_doc_extract", "nlp_doc_extract"),
        50: ("nlp_info_extract", "nlp_info_extract"),
        51: ("nlp_text_classifier", "nlp_text_classifier"),
        52: ("nlp_doc_classifier", "nlp_doc_classifier"),
        53: ("doc_self_training", "doc_self_training"),
        54: ("nlp_layout_extract", "nlp_layout_extract"),
        55: ("nlp_address", "nlp_address"),
        51: ("nlp_text_classifier", "nlp_text_classifier"),
        51: ("nlp_doc_classifier", "nlp_doc_classifier"),
        52: ("doc_self_training", "doc_self_training"),
        53: ("nlp_layout_extract", "nlp_layout_extract"),
        54: ("nlp_address", "nlp_address"),
        55: ("ocr_tzlf_card", "ocr_tzlf_card"),
        56: ("field_reprocess", "field_reprocess"),
        57: ("nlp_layoutlm", "nlp_layoutlm"),
        58: ("ocr_text", "ocr_text"),
        59: ("ocr_layout_analysis", "ocr_layout_analysis"),
        60: ("ocr_idcard", "ocr_idcard"),
        61: ("ocr_bizlicense", "ocr_bizlicense"),
        62: ("ocr_vehlicense", "ocr_vehlicense"),
        63: ("captcha", "captcha"),
        64: ("ocr_seal", "ocr_seal"),
        65: ("ocr_invoice", "ocr_invoice"),
        66: ("ocr_text_cpu", "ocr_text_cpu"),
        67: ("ocr_table", "ocr_table"),
        68: ("nlp_encoder", "nlp_encoder"),
        68: ("nlp_triton_server_gpu", "nlp_triton_server_gpu"),
        69: ("nlp_triton_server_cpu", "nlp_triton_server_cpu"),
    }

menu_relation = {
    1001: {
        36: 100101,
        37: 100102,
        51: 100103,
        52: 100104
    }
}

middleware_port_relation = {
    "minio": {
        "port": 9000,
        "nginx_proxy_port": 10000
    },
    "harbor": {
        "http_port": 8888,
        "nginx_harbor_proxy_port": 8889
    },
    "redis": {
        "port": 6379,
        "port_sentinel": 26379
    },
    "nginx": {
        "service_port": 8084,
        "k8s_proxy_port": 6444,
        "entcmd_proxy_port": 8084,
        "commander_tenant_port": 8084,
        "mage_proxy_port": 8084,
        "chatbot_proxy_port": 8084,
        "entuc_proxy_port": 8084,
        "dataservice_proxy_port": 8084,
        "notice_proxy_port": 8084,
        "license_web_proxy_port": 8084,
        "rpa_collaboration_backend_proxy_port": 8084,
        "creativity_proxy_port": 8084,
        "entfs_proxy_port": 8084,
        "entiap_proxy_port": 8084
    },
    "mysql": {
        "port": 3306,
        "proxysql_cluster_port": 6032,
        "proxysql_port": 6033,
        "nginx_proxy_port": 6034
    },
    "elasticsearch": {
        "http_port": 9200,
        "tcp_port": 9300
    },
    "rabbitmq": {
        "port": 5672,
        "manage_port": 15672,
        "empd_port": 4369,
        "erlang_port": 25672
    },
    "etcd": {
        "http_port": 12379,
        "tcp_port": 12380
    },
    "identity": {
        "port": 6060,
        "nginx_proxy_port": 6061
    },
    "monitor": {
        "grafana_port": 3000,
        "prometheus_port": 9090,
        "mysql_exporter_port": 9104,
        "redis_exporter_port": 9121,
        "rabbitmq_exporter_port": 9419,
        "elasticsearch_exporter_port": 9114,
        "node_exporter_port": 9100,
        "k8s_metrics_port": 31388,
        "istio_prometheus_port": 31390
    },
    "siber": {
        "port": 88
    },
    "postgresql": {
        "port": 5432
    },
    "ocr": {
        "ocr_document_gpu": 30006,
        "ocr_table_gpu": 30007,
        "ocr_receipt_gpu": 30008,
        "ocr_idcard_gpu": 30009,
        "ocr_bankcard_gpu": 30013,
        "ocr_vehicle_gpu": 30010,
        "ocr_vehiclelicense_gpu": 30011,
        "ocr_biz_gpu": 30012,
        "ocr_passport_gpu": 30014
    },
    "chronyd": {
        "port": 123,
        "cmdport": 323
    },
}


def init_port_config():
    conf = YamlConfig(PORT_MAP, data=middleware_port_relation)
    conf.write_file(backup=False)


def find_module_by_key(module: str) -> list:
    l = []
    for id in module_info:
        if module_info[id][0] == module:
            res = {}
            res['id'] = id
            res['module'] = module
            res['description'] = module_info[id][1]
            l.append(res)
    return l


def find_single_module_by_key(module: str) -> list:
    l = []
    for id in module_info:
        if module_info[id][0] == module:
            res = {}
            res['id'] = id
            res['module'] = module
            res['description'] = module_info[id][1]
            return res
    res = {}
    res['id'] = 999
    res['module'] = module
    res['description'] = "未知模块"
    return res


def get_module_description(module_id: int) -> str:
    if module_id not in module_info:
        return "未知模块"
    return module_info[module_id][1]


def get_module_key(module_id: int) -> str:
    if module_id not in module_info:
        return "未知模块"
    return module_info[module_id][0]


def get_module_keys(module_ids: list) -> list:
    return [get_module_key(x) for x in module_ids]


def get_all_ports(middleware="") -> list:
    ''':return list[str]'''
    l = []
    try:
        relation = YamlConfig(PORT_MAP).read_file()
    except Exception:
        relation = middleware_port_relation
    if middleware:
        try:
            for k in relation[middleware]:
                l.append(str(relation[middleware][k]))
        except KeyError:
            pass
    else:
        for mid in relation:
            for k in relation[mid]:
                l.append(str(relation[mid][k]))
    return l


def get_port(middleware: str, key: str) -> int:
    try:
        relation = YamlConfig(PORT_MAP).read_file()
    except Exception:
        relation = middleware_port_relation

    try:
        return relation[middleware][key]
    except KeyError:
        for k in relation[middleware].keys():
            if key in k:
                return relation[middleware][k]
        return 0
