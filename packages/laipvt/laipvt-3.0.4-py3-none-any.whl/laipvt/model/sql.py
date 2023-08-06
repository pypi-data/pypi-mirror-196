from __future__ import absolute_import
from __future__ import unicode_literals
import re
import os
import pymysql
from laipvt.helper.exception import ModelError
from laipvt.model.server import runcmd
from laipvt.sysutil.util import path_join, run_local_cmd, backup_file, log


class PgSqlModule(object):
    def __init__(self, **kwargs):
        self.image = "postgres:11.9"
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.port = kwargs.get("port")
        self.host = kwargs.get("host")

        GET_PG_IMAGE = """docker image list --format "{{.Repository}}:{{.Tag}}"|grep postgres|head -n 1"""
        code, image = runcmd(GET_PG_IMAGE)
        image = image.stdout.replace("\n", "")
        if code != 0:
            log.info("code失效:执行{},返回code:{}".format(GET_PG_IMAGE, code))
            exit(2)
        self.image = image

        # 添加pg的命令
        self.pg_check_cmd = "docker run --network=host -e PGPASSWORD={} --entrypoint=/usr/bin/pg_isready " \
                            "{}  -U {} -p {} -h {}".format(self.password, self.image, self.username, self.port,
                                                           self.host)

        self.pg_cmd = "docker run  --network=host -e PGPASSWORD={} --entrypoint=/usr/bin/psql  " \
                      "{}  -U {} -p {} -h {}".format(
            self.password, self.image, self.username, self.port, self.host
        ) + " -c \"{}\""

    def isHealthy(self):
        code, result = runcmd(self.pg_check_cmd)
        log.info("execute pg cmd: {} result:{}".format(self.pg_check_cmd, result))
        if result.returncode != 0:
            return False, result.stderr
        else:
            return True, ""

    def create_db(self, db_name):
        create_db = "create database {};".format(db_name)
        code, result = runcmd(self.pg_cmd.format(create_db))
        if result.returncode == 0:
            return True, ""
        else:
            log.info("create pg database {} failed,reason:{}".format(db_name, result.stdout))
            return False, result.stdout


class SqlModule(object):
    def __init__(self, *args, **kwargs):
        self.conn = pymysql.connect(**kwargs)
        self.mysql_cmd = "mysql -h {} -u{} -p{} -P{}".format(
            kwargs.get("host"),
            kwargs.get("user"),
            kwargs.get("passwd"),
            kwargs.get("port")
        )
        self.mysqldump_cmd = "mysqldump -h {} -u{} -p{} -P{}".format(
            kwargs.get("host"),
            kwargs.get("user"),
            kwargs.get("passwd"),
            kwargs.get("port")
        )

    def use_db(self, db_name):
        self.conn.select_db(db_name)

    def _read_file(self, file_path, eof=';'):
        try:
            with open(file_path) as f:
                ret = f.read()
                ret = re.sub(r'/\*.*?\*/', "\n", ret, flags=re.S)
                ret = re.sub(r"--.*\n", "\n", ret)
                ok = ret.split(eof)
                return ok
        except Exception as e:
            raise ModelError("SqlModule._read_file, 读取文件失败，文件路径: {}, 错误信息: {}".format(file_path, e)) from None

    def _read_file_lines(self, file_path, eof=";"):
        try:
            with open(file_path) as f:
                content = f.readlines()
                result = []
                sql = ""
                for line in content:
                    if not line.strip():
                        continue
                    sql += line.strip()
                    if line.strip().find(eof) >= 0:
                        ret = re.sub(r'/\*.*?\*/', "\n", sql, flags=re.S)
                        ret = re.sub(r"--.*\n", "\n", ret)
                        result.append(ret)
                        sql = ""
                return result
        except Exception as e:
            raise ModelError("SqlModule._read_file, 读取文件失败，文件路径: {}, 错误信息: {}".format(file_path, e)) from None

    def import_from_file(self, path, file_eof=";"):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        for sql_request in self._read_file(path, file_eof):
            if sql_request.strip():
                try:
                    cursor.execute(sql_request)
                except Exception as e:
                    try:
                        new_sql = sql_request.split(file_eof)
                        for s in new_sql:
                            if len(s) > 0:
                                try:
                                    cursor.execute(s)
                                except Exception as e:
                                    raise e
                    except Exception as e:
                        raise ModelError("SqlModule.import_from_file, 错误信息: {}".format(e)) from None
        cursor.close()

    def import_from_file_commander(self, path, file_eof=";"):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        for sql_request in self._read_file_lines(path, file_eof):
            if sql_request.strip():
                try:
                    cursor.execute(sql_request)
                except Exception as e:
                    try:
                        new_sql = sql_request.split(file_eof)
                        for s in new_sql:
                            if len(s) > 0:
                                try:
                                    cursor.execute(s)
                                except Exception as e:
                                    raise e
                    except Exception as e:
                        raise ModelError("SqlModule.import_from_file, 错误信息: {}".format(e)) from None
        cursor.close()

    def insert_sql(self, sql_statements):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_statements)
            self.conn.commit()
        except Exception as e:
            raise ModelError("SqlModule.insert_sql, 错误信息: {}".format(e)) from None
        finally:
            cursor.close()

    def select(self, sql_statements):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        info = None
        try:
            cursor.execute(sql_statements)
            info = cursor.fetchall()
        except Exception as e:
            raise ModelError("SqlModule.select, 错误信息: {}".format(e)) from None
        finally:
            cursor.close()
            return info

    def run_sql(self, sql):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
        except Exception as e:
            raise ModelError("SqlModule.run_sql, 错误信息: {}".format(e)) from None
        finally:
            cursor.close()

    def import_from_dir(self, db, path):
        cmd = "for i in $(ls {}); do {} {} < {}/$i; done".format(path, self.mysql_cmd, db, path)
        run_local_cmd(cmd)

    def backup_db(self, db, target):
        target_file_path = path_join(target, db + ".sql")
        if os.path.isfile(target_file_path):
            backup_file(target_file_path)
        cmd = "{} {}".format(self.mysqldump_cmd, "{} > {}".format(
            db, target_file_path
        ))
        res = run_local_cmd(cmd)
        return True if res["code"] == 0 else False

    def close(self):
        self.conn.close()
