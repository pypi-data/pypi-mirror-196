from laipvt.handler.confighandler import CheckResultHandler
from laipvt.handler.middlewarehandler import PgSqlConfigHandler
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.model.server import ServerModel
from laipvt.model.sql import PgSqlModule
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import status_me, ssh_obj, log, path_join


class PgSqlController(MiddlewareInterface):
    def __init__(self, result: CheckResultHandler, handler: PgSqlConfigHandler, template: str):
        super(PgSqlController, self).__init__(result, handler, template)
        self.pgsql_cfg = PgSqlConfigHandler().get_config_with_check_result()
        self.master_host = self.master_server[0].ipaddress
        self.username = self.pgsql_cfg["postgresql"]["username"]
        self.password = self.pgsql_cfg["postgresql"]["password"]
        self.database = self.pgsql_cfg["postgresql"]["database"]
        self.port = self.pgsql_cfg["postgresql"]["port"]
        self.pgsql_cfg["postgresql"]["ipaddress"] = self.handler.cfg["ipaddress"]
        self.pgsql_cmd = PgSqlModule(
            host=self.master_host,
            username=self.username,
            password=self.password,
            port=self.port
        )
        self.pgsql_service_file_template = path_join(self.template, "postgresql_service.tmpl")
        self.pgsql_service_file_dest = path_join("/tmp", "postgresql.yaml")
        self.pgsql_service_file_remote = path_join(self.base_dir, "svc", "postgresql_service.yaml")

    def _generic_config(self):
        self.generate_docker_compose_file(self.pgsql_cfg)

    def create_pgsql_service_kubernetes(self):
        server = ServerModel(self.harbor_server)
        FileTemplate(self.pgsql_cfg, self.pgsql_service_file_template, self.pgsql_service_file_dest).fill()
        server.send_file(self.pgsql_service_file_dest, self.pgsql_service_file_remote)

        cmd = "kubectl apply -f {}".format(self.pgsql_service_file_remote)
        ssh_cli = ssh_obj(ip=self.harbor_server[0].ipaddress, user=self.harbor_server[0].username,
                          password=self.harbor_server[0].password, port=self.harbor_server[0].port)
        results = ssh_cli.run_cmd(cmd)
        if results["code"] != 0:
            log.error("{} {}".format(results["stdout"], results["stderr"]))
            exit(2)

    def _check(self):
        success, reason = self.pgsql_cmd.isHealthy()
        if success:
            return True, "pgsql", reason
        return False, "pgsql", reason

    def create_db(self):
        self.pgsql_cmd.create_db(self.database)

    def send_pg_compose(self):
        self.send_docker_compose_file()

    def start_(self):
        self.start()

    @status_me("pgsql")
    def deploy_pgsql(self, force):
        self._generic_config()
        self.send_pg_compose()
        self.start_()
        self.create_pgsql_service_kubernetes()
        self.check_interval_fn(self._check)
        self.create_db()

    def deploy(self, force=False):
        self.deploy_pgsql.set_force(True)
        self.deploy_pgsql(force)
