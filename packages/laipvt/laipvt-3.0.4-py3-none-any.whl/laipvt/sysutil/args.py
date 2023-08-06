# -*- encoding: utf-8 -*-
import argparse


def Args():
    parser = argparse.ArgumentParser(description='Process some integers.')

    subparsers = parser.add_subparsers(title='laipvt', description='命令模块分组', help='命令模块分组')

    install_parser = subparsers.add_parser('install', help="软件部署")
    install_parser.add_argument('--force', dest="Force", action="store_true", default=False, help="前置检查效验")
    install_parser.add_argument("--specify", dest="Specify", default=None, help="指定安装的基础组件,比如 basesystem:helm")
    install_parser.add_argument('-f', '--tar-file', dest="tarFile", type=str, help="指定部署压缩包")
    install_parser.add_argument("--auto-test", dest="AutoTest", type=bool, default=False, help="默认执行压测")
    install_parser.add_argument("--services", dest="services", type=str, default=None, help="指定安装的服务")
    install_parser.set_defaults(which='install')

    action_parser = subparsers.add_parser('run', help="执行单个命令")
    action_parser.add_argument('--force', dest="Force", action="store_true", default=False, help="前置检查效验")
    action_parser.add_argument('-f', '--tar-file', dest="tarFile", type=str, help="指定部署压缩包")
    action_parser.add_argument("--service", dest="service", type=str, default=None, help="指定安装的服务")
    action_parser.add_argument("--action", dest="action", type=str, default=None, help="指定的操作")
    action_parser.set_defaults(which='run')


    upgrade_parser = subparsers.add_parser('upgrade', help="软件部署")
    upgrade_parser.add_argument('-f', '--tar-file', dest="tarFile", type=str, help="指定部署压缩包")
    upgrade_parser.add_argument("--services", dest="services", type=str, default=None, help="升级相應的服務,分割符號為逗號")
    upgrade_parser.set_defaults(which='upgrade')



    license_parser = subparsers.add_parser('license', help='授权功能相关参数')
    license_parser.add_argument('--license-file', dest="LicenseFile",
                                type=str, help="指定需要更新的授权文件")
    license_parser.add_argument('--ocr-license-file', dest="OcrLicenseFile",
                                type=str, help="指定需要更新的ocr授权文件")
    license_parser.set_defaults(which='license')

    monitor_parser = subparsers.add_parser('monitor', help='部署额外功能相关参数')
    monitor_parser.add_argument('-f', '--tar-file', dest="tarFile", type=str, help="指定部署压缩包")
    monitor_parser.add_argument('--elk', dest="ELK", action="store_true",
                                default=False, help="部署监控功能")
    monitor_parser.add_argument('--keepalive', dest="Keepalive", action="store_true",
                                default=False, help="部署keepalive服务")
    monitor_parser.set_defaults(which='monitor')

    delete_parser = subparsers.add_parser('delete', help='删除功能相关参数')
    delete_parser.add_argument("--docker", dest="Docker", action="store_true",
                               default=False, help="删除docker服务")
    delete_parser.add_argument("--services", dest="services", action="store_true", default=False, help="删除相应的服务")
    delete_parser.add_argument('--kubernetes', dest="Kubernetes", action="store_true",
                               default=False, help="删除kubernetes服务")
    delete_parser.add_argument('--middleware', dest="Middleware", action="store_true",
                               default=False, help="删除middleware中间件服务")
    delete_parser.add_argument('--all', dest="All", action="store_true",
                               default=False, help="删除所有服务")
    delete_parser.add_argument("--servie", dest="Service", type=str, help="指定服务")
    delete_parser.set_defaults(which='delete')




    reset_parser = subparsers.add_parser('resetdata', help='重置中间件数据')
    reset_parser.add_argument("--service", dest="Service", type=str, help="指定需要自动化测试的项目")
    reset_parser.add_argument('-f', '--tar-file', dest="tarFile", type=str, help="指定部署压缩包")
    reset_parser.set_defaults(which='resetdata')

    apptest_parser = subparsers.add_parser('apptest', help='自动化功能相关参数')
    apptest_parser.add_argument("--service", dest="Service", type=str, help="指定需要自动化测试的项目")
    apptest_parser.add_argument('-f', '--tar-file', dest="tarFile", type=str, help="指定部署压缩包")
    apptest_parser.add_argument('--reset', dest='ResetData', default=True, type=bool, help="自動清空數據")
    apptest_parser.set_defaults(which='apptest')

    return parser


if __name__ == '__main__':
    args = Args().parse_args()
    print(args)
