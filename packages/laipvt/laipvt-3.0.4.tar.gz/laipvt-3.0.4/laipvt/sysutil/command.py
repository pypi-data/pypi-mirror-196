## gen certs command
gen_server_secure_key_cmd = "openssl genrsa -des3 -passout pass:laiye -out {} 2048"
gen_server_key_cmd = "openssl rsa -in {} -passin pass:laiye -out {}"
gen_server_csr_cmd = "openssl req -new -key {} -out {} -subj '/C=CN/ST=BeiJing/L=BeiJing/O=LaiYe Security/OU=IT Department/CN=*'"
gen_ca_crt_cmd = "openssl req -new -x509 -key {} -out {} -days 3650 -subj '/C=CN/ST=BeiJing/L=BeiJing/O=LaiYe Security/OU=IT Department/CN=*'"
gen_server_crt_cmd = "openssl x509 -req -days 3650 -in {} -CA {} -CAkey {} -CAcreateserial -out {}"

SET_UMASK = "sed -i '$aumask 0022 #laiye' /etc/bashrc"
UNSET_UMASK = "sed -i '/^umask\s0022\s#laiye/d' /etc/bashrc"

## kubenetes command
BASH_RUN = "/bin/bash {}"
CP_KUBEADM = "\cp -f {}/kubeadm /usr/bin/kubeadm"
KUBE_INIT = "kubeadm init --config {}"
KUBE_RESET = "kubeadm reset -f"
CREATE_KUBE_DIR = "mkdir ~/.kube"
CP_KUBE_CONFIG = "\cp /etc/kubernetes/admin.conf ~/.kube/config"
KUBECTL_COMPLETION = "echo 'source <(kubectl completion bash)' >> ~/.bashrc"
KUBECTL_APPLY = "kubectl apply -f {}"
KUBECTL_CREATE = "kubectl create -f {}"
KUBEADM_TOKEN_CREATE = "kubeadm token create --print-join-command --config {}"
TAR_KUBE_CRETS = """tar -C /etc/kubernetes -zcvf {} \
        admin.conf pki/ca.crt pki/ca.key pki/sa.key pki/sa.pub pki/front-proxy-ca.crt \
        pki/front-proxy-ca.key pki/etcd/ca.crt pki/etcd/ca.key"""
UNTAR_KUBE_CRETS = "tar -zxvf {} -C /etc/kubernetes/"
ADD_MASTER_SUFFIX = "{} --control-plane --node-name {}"
TAINT_MASTER = "kubectl taint nodes {} node-role.kubernetes.io/master-"
HELM_PATH = "/usr/bin/helm"
TILLER_PATH = "/usr/bin/tiller"
TILLER_SERVICE_PATH = "/usr/lib/systemd/system/tiller.service"
CHMOD_EXECUTE = "chmod +x {}"
SYSTEMCTL_DAEMON_RELOAD = "systemctl daemon-reload"
SYSTEMCTL_START = "systemctl start {}"
SYSTEMCTL_ENABLE = "systemctl enable {}"
ISTIOCTL_PATH = "/usr/bin/istioctl"
ISTIOCTL_INSTALL = "istioctl install -f {}"
CHECK_ISTIO = "kubectl get crds | grep 'istio.io' | wc -l"
GET_LICENSE_POD_INFO = "kubectl -n license get pod |grep {}"
RESTART_DEPLOYMENT = "kubectl -n {} rollout restart deployment {}"
RESTART_DEPLOYMENT_ALL = "kubectl -n {} rollout restart deployment"
CREATE_NS = "kubectl create ns {}"
ISTIO_INJECTION_NS = "kubectl label namespace {} istio-injection=enabled"

CHECK_RUNNING_CMD = "kubectl -n {} get pod -l 'app={}' -o jsonpath='{{..status.phase}}'"
GET_ROOK_CEPH_DASHBOARD_PASSWORD_CMD = "kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath=\"{['data']['password']}\" | base64 --decode && echo"
GET_PVC_VOLUMENAME_CMD = "kubectl -n {} get pvc {} -o jsonpath='{{..spec.volumeName}}'"
GET_NFS_NODE_IP_CMD = "kubectl -n rook-nfs get pod -l app=rook-nfs -o jsonpath='{..status.hostIP}'"

# harbor command
TARGZ_DECOMPRESSION = "tar -zxmf {} -C {}"
CHMOD_USER_GROUP = "chown -R {}:{} {} {}"
ENABLE_HARBOR_SERVICE = "systemctl enable harbor.service"

# middleware command
RM = "rm -fr {}"
###
CREATE_DB = "create database If Not Exists `{db_name}` DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci"

MKDIR_DIR = "mkdir -p {}"
CHMOD_777 = "chmod -R 777 {}"

CREATE_LICENSE_CONFIGMAP = "kubectl -n mid create configmap license-manager-config --from-literal=signature='{signature}' --from-literal=publicKey='{publicKey}'"

HELM_LIST = "helm --host=localhost:44134 list --all --chart-name {} --output=json"
HELM_DELETE = "helm --host=localhost:44134 delete {} --purge"

FIX_ENTCMD_SIDECAR = """
   kubectl patch deploy laiye-entcmd-connector -n entcmd -p '{"spec": {"template":{"metadata":{"annotations":{"sidecar.istio.io/inject":"false"}}}} }'
"""
CLOSE_SIDECAR = """kubectl patch deploy {deployment} -n {namespace} -p """
CLOSE_SIDECAR_END = """'{"spec": {"template":{"metadata":{"annotations":{"sidecar.istio.io/inject":"false"}}}} }'"""

# HELM_INSTALL = """helm --host=localhost:44134 install --name={process} --set global.env=pvt \
#                     --set replicaCount={replicas} \
#                     --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
#                     --set pvtWorkDir={pvt_work_dir} \
#                     --set global.LM_LOG_DEBUG=1 \
#                     --set global.LM_ETCD_ENDPOINT="{etcd_endpoint}" \
#                     --set global.LM_APPLY_LICENSE_PATH='/home/works/program/data/license.lcs' \
#                     {file_path}"""

HELM_INSTALL_CPU = """helm --host=localhost:44134 install --name={process} --set global.env=pvt \
                    --set global.namespace={namespace} \
                    --set affinity=""\
                    --set global.component={component} \
                    --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=license-manager.license:19080 \
                    --set global.LM_CLIENT_LICENSE_MANAGER_SSL_HOST=license-manager.mid \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.logPath={logpath} \
                    --set global.processName={process_name} \
                    --set global.projectName={project_name} \
                    --set externalStorageClassName={external_storageclass_name} \
                    --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set pvtWorkDir={pvt_work_dir} \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.LM_ETCD_ENDPOINT="{etcd_endpoint}" \
                    --set global.LM_APPLY_LICENSE_PATH='/home/works/program/data/license.lcs' \
                    --set global.LM_CLIENT_SERVICE_ID="{lm_client_service_id}" \
                    --set global.NACOS_HOST={nacos_host} \
                    --set global.NACOS_NAMESPACE="pvt" \
                    --set workloadType="{workload_type}" \
                    --set resources="{resources}" \
                    {file_path}"""

HELM_INSTALL_GPU = """helm --host=localhost:44134 install --name={process} --set global.env=pvt \
                    --set global.namespace={namespace} \
                    --set affinity=""\
                    --set global.component={component} \
                    --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=license-manager.license:19080 \
                    --set global.LM_CLIENT_LICENSE_MANAGER_SSL_HOST=license-manager.mid \
                    --set global.logPath={logpath} \
                    --set global.processName={process_name} \
                    --set global.projectName={project_name} \
                    --set externalStorageClassName={external_storageclass_name} \
                    --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set pvtWorkDir={pvt_work_dir} \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.LM_ETCD_ENDPOINT="{etcd_endpoint}" \
                    --set global.LM_APPLY_LICENSE_PATH='/home/works/program/data/license.lcs' \
                    --set global.LM_CLIENT_SERVICE_ID="{lm_client_service_id}" \
                    --set global.NACOS_HOST={nacos_host} \
                    --set global.NACOS_NAMESPACE="pvt" \
                    --set workloadType="{workload_type}" \
                    --set resources.limits.nvidia\\\.com/gpu="1" \
                    --set resources.requests.nvidia\\\.com/gpu="1" \
                    {file_path}"""

INIT_IDENTITY_USER = "docker exec ids-server dotnet /opt/tool/idsadmin.dll -a add -u admin -p 123456"

HELM_INSTALL_TF_SERVICE = """helm --host=localhost:44134 install \
            --name={process} \
            --set affinity="" \
            --set global.env=pvt \
            --set global.namespace={namespace} \
            --set externalStorageClassName={external_storageclass_name} \
            --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
            --set pvtWorkDir={pvt_work_dir} \
            {file_path}"""

COMMANDER_UPGRADE_INSTALL = """helm --host=localhost:44134 upgrade --install --force --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=license-manager.license:19080 --set pvtWorkDir={pvt_work_dir} \
                    --set global.LM_CLIENT_LICENSE_MANAGER_SSL_HOST=license-manager.mid \
                    --set config.server="{config_server}" --set config.passwd={config_server_passwd} --set affinity="" \
                    --set mysql.host={mysql_host} --set mysql.port={mysql_port} --set mysql.user={mysql_user} \
                    --set mysql.password={mysql_password} --set mysql.database={mysql_database} --set mysql.charset={mysql_charset} \
                    --set oidc.authority={oidc_authority} --set oidc.secret={oidc_secret} \
                    --set global.LM_CLIENT_SERVICE_ID=200001  \
                    {process} {file_path}"""

HELM_UPGRADE_INSTALL = """helm --host=localhost:44134 upgrade --install --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set pvtWorkDir={pvt_work_dir} --set affinity="" \
                    --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=license-manager.license:19080 \
                    --set global.LM_CLIENT_LICENSE_MANAGER_SSL_HOST=license.mid \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.NACOS_HOST={nacos_host} \
                    --set global.NACOS_NAMESPACE="pvt" \
                    --set externalStorageClassName={external_storageclass_name} \
                    --set global.LM_ETCD_ENDPOINT="{etcd_endpoint}" \
                    --set global.LM_APPLY_LICENSE_PATH='/home/works/program/data/license.lcs' \
                    {process} {file_path}"""

HELM_UPGRADE_INSTALL_CPU = """helm --host=localhost:44134 upgrade --install --set global.env=pvt \
                    --set global.namespace={namespace} \
                    --set affinity=""\
                    --set global.component={component} \
                    --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=license-manager.license:19080 \
                    --set global.LM_CLIENT_LICENSE_MANAGER_SSL_HOST=license-manager.mid \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.logPath={logpath} \
                    --set global.processName={process_name} \
                    --set global.projectName={project_name} \
                    --set externalStorageClassName={external_storageclass_name} \
                    --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set pvtWorkDir={pvt_work_dir} \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.LM_ETCD_ENDPOINT="{etcd_endpoint}" \
                    --set global.LM_APPLY_LICENSE_PATH='/home/works/program/data/license.lcs' \
                    --set global.LM_CLIENT_SERVICE_ID="{lm_client_service_id}" \
                    --set global.NACOS_HOST={nacos_host} \
                    --set global.NACOS_NAMESPACE="pvt" \
                    --set workloadType="{workload_type}" \
                    --set resources="{resources}" \
                    {process} {file_path}"""

HELM_UPGRADE_INSTALL_GPU  = """helm --host=localhost:44134 upgrade --install --set global.env=pvt \
                    --set global.namespace={namespace} \
                    --set affinity=""\
                    --set global.component={component} \
                    --set global.LM_CLIENT_LICENSE_MANAGER_ADDR=license-manager.license:19080 \
                    --set global.LM_CLIENT_LICENSE_MANAGER_SSL_HOST=license.mid \
                    --set global.logPath={logpath} \
                    --set global.processName={process_name} \
                    --set global.projectName={project_name} \
                    --set externalStorageClassName={external_storageclass_name} \
                    --set replicaCount={replicas} \
                    --set image.hub={registry_hub} --set image.name={image_name} --set image.tag={image_tag} \
                    --set pvtWorkDir={pvt_work_dir} \
                    --set global.LM_LOG_DEBUG=1 \
                    --set global.LM_ETCD_ENDPOINT="{etcd_endpoint}" \
                    --set global.LM_APPLY_LICENSE_PATH='/home/works/program/data/license.lcs' \
                    --set global.LM_CLIENT_SERVICE_ID="{lm_client_service_id}" \
                    --set global.NACOS_HOST={nacos_host} \
                    --set global.NACOS_NAMESPACE="pvt" \
                    --set workloadType="{workload_type}" \
                    --set resources.limits.nvidia\\\.com/gpu="1" \
                    --set resources.requests.nvidia\\\.com/gpu="1" \
                    {process} {file_path}"""

# HIDE_MENU_SQL = "update laiye_saas_docuds.tbl_docuds_menu set is_deleted = 1 where menu_key in (9001, 9002, 900201, 900202, 900203);"
HIDE_MENU_SQL = "update laiye_saas_docuds.tbl_docuds_menu h join (select distinct f.menu_key, f.menu_name,f.menu_parent from laiye_saas_docuds.tbl_docuds_menu f join ( select distinct d.menu_key, d.menu_name, d.menu_parent from laiye_saas_docuds.tbl_docuds_menu d join (select distinct b.menu_key, b.menu_name, b.menu_parent from laiye_saas_docuds.tbl_docuds_menu b join (select menu_key, menu_name, menu_parent from laiye_saas_docuds.tbl_docuds_menu where menu_key in ({hide_menu_id})) a on b.menu_key = a.menu_key or b.menu_key = a.menu_parent) c on d.menu_key = c.menu_key or d.menu_key = c.menu_parent ) e on f.menu_key = e.menu_key or f.menu_key = e.menu_parent) g on h.menu_key = g.menu_key set is_deleted = 0;"
TEST_SERVICE_CMD = "docker run -ti  --add-host mysql.default.svc:{} -v {}:{} -v {}:{} {}:{} --test"
GET_LICENSE_QRCODE_IMG = """docker images|grep feature|grep license|awk '{print $3}'"""
LICENSE_QRCODE_CMD = "docker run -u root  --rm --add-host mysql.default.svc:{} --rm -v {}:{} -v {}:{} {} --gen -o {}"
GET_NACOS_VERSION_CMD = "docker images --format='{{.Repository}} {{.Tag}}'|grep nacos|awk -F ' ' '{print $2}'|head -n 1"
