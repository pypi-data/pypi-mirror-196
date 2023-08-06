#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from laipvt.sysutil.args import Args


def main():
    args = Args().parse_args()
    func = args.which
    os.environ["HELM_HOST"] = "localhost:44134"
    if func == "delete":
        from laipvt.cli.delete import delete_main
        delete_main(args)
    else:
        from laipvt.cli.deploy import deploy_main
        deploy_main(args)
    # write dict to file
