import sys
from cli import CLI, print, exit, confirm, run, CLR
from config import Config
from functools import reduce
import kubernetes.client as k8s


### THe kubernetes namespace that objects of this target fall under.
### This allows staging and prod to work well in the same cluster.
# ~cfg~ gcp_gke_namespace ''

### A shorter name for marking auxillary services.  Can be the same as :ref:`config_gcp_project_name`.
# ~cfg~ gcp_nickname ''

### The Google Cloud project name.
# ~cfg~ gcp_project_name ''

### Google Kubernetes Engine cluster name
# ~cfg~ gcp_gke_cluster_name ''

### Image prefix for remote container storage for deployed docker image
# ~cfg~ gcp_gke_image_store ''


class K8MicroService():
    def __init__(self, image, port, replicas):
        self.image = image
        self.namespace, name = name.split('_',1)
        self.name, self.ver = name.rsplit('_',1)
        self.port = port
        self.replicas = replicas

    
    def deploy(self, api):
        svc = k8s.V1APIService(metadata = k8s.V1ObjectMeta(name=f"{self.name}-service", namespace=self.namespace),
            spec = k8s.V1ServiceSpec(type = 'NodePort',
                selector={'name':self.name, 'ver':self.ver})),
                #ports=[port=self.port, target_port=9000]))
                #internal_traffic_policy, session_affinity, 
        dpy = k8s.V1Deployment(metadata = k8s.V1ObjectMeta(name=f"{self.name}-deployment", namespace=self.namespace),
            spec = k8s.V1ServiceSpec(min_ready_seconds=1, replicas=self.replicas,
                strategy = k8s.V1DeploymentStrategy(type='Recreate' if self.replicas == 1 else 'RollingUpdate'),
                selector = k8s.V1LabelSelector(match_labels={'name':self.name, 'ver':self.ver}),
                template = k8s.V1PodTemplateSpec(metadata=k8s.V1ObjectMeta(labels={'name':self.name, 'ver':self.ver})),
                    spec = k8s.V1PodSpec(
                        containers = [k8s.V1Container(image="")]
                    )))
            




def lookup_my_ip():
    return run('dig +short myip.opendns.com @resolver1.opendns.com', msg='', read=True).strip()


def set_gke_cluster_config_credentials(cfg, region=None):
    verify_gcloud_project(cfg)
    region = region or run('gcloud config get-value compute/region', read=True, msg='').strip()
    run(f'gcloud container clusters get-credentials {cfg.gcp_gke_cluster_name} --region {region}', read=True, msg='')
    k8s.config.load_kube_config()



def verify_gcloud_project(cfg):
    if not cfg.gcp_project_name: exit(print.ERR, f"No `gcp_project_name` configured for target '{cfg.target}'~lang ja~'{cfg.target}'のtargetには`gcp_project_name`が設定されてない。")

    cur_project = run('gcloud config get-value project', read=True, msg='',
        err=Text(print.ERR, '''The `gcloud` command could not be found.  Install it and try again.
            ~lang ja~`gcloud`コマンドが見つかりませんでした。インストールして再試行してください。''')).strip()
    if cur_project != cfg.gcp_project_name: exit(print.ERR, f'''
        gcloud is currently configured for gcp project '{cur_project}'\n
        Use `gcloud init` or `gcloud config configurations activate` to change the project to '{cfg.gcp_project_name}'
        ~lang ja~
        gcloudは「{cur_project}」のプロジェクトで設定してある。\n
        `gcloud init`や`gcloud config configurations activate`を使って「{cfg.gcp_project_name}」のgcpプロジェクトを設定してください。
        ''')



@CLI()
def control_plane_auth(*, add__a=None, remove__r=None):
    ''' Add/remove/view the GKE control-plane authorized networks.~lang ja~GKEコントロールプレーンで承認されたネットワークを追加/削除/表示します。

    The GKE control plane only allows https connections from the authorized networks.
    ~lang ja~GKEコントロールプレーンは、承認されたネットワークからのhttps接続のみを許可します

    `<https://cloud.google.com/kubernetes-engine/docs/how-to/authorized-networks>`_

    Without parameters this just prints the current configuration.~lang ja~パラメータがない場合、これは現在の構成を出力するだけです。

    Parameters:
        --add <ip>, -a <ip>
            Add an IP network: e.g. ``192.168.1.0/24``.  You can also use ``me`` to add your ip address.
            ~lang ja~IPネットワークを追加します：例： ``192.168.1.0/24``。 `` me``を使用してIPアドレスを追加することもできます。
        --remove <ip>, -r <ip>
            Same as adding.~lang ja~ 同上

    Examples:
        $ ./cli.py -t prod gcp control-plane-auth -a me
    '''
    cfg = Config()

    verify_gcloud_project(cfg)
    region = run('gcloud config get-value compute/region', read=True, msg='').strip()
    cur = run(f'gcloud container clusters describe {cfg.gcp_gke_cluster_name} --region {region} --format flattened(masterAuthorizedNetworksConfig.cidrBlocks[])', read=True, msg='')
    networks = set(line.split(':')[1].strip() for line in cur.split('\n') if line.strip())
    networks.discard('None')
    print.ln('Current authorized addresses:~lang ja~現在の許可されているIPアドレス:')
    print.ln([f'   {x}' for x in networks])
    new_networks = set(networks)
    if add__a:
        if add__a == 'me': add__a = f'{lookup_my_ip()}/32'
        print.ln(f"Add Ip: {add__a}~lang ja~追加のIPアドレス: {add__a}")
        new_networks.add(add__a)
    if remove__r:
        if remove__r == 'me': remove__r = f'{lookup_my_ip()}/32'
        print.ln(f"Remove Ip: {add__a}~lang ja~削除のIPアドレス: {add__a}")
        new_networks.discard(remove__r)


    if new_networks == networks: return
    if not new_networks: exit("Can't remove all the networks~lang ja~すべてのネットワークを削除できません")
    run(['gcloud','container','clusters','update',cfg.gcp_gke_cluster_name, '--region', region, '--enable-master-authorized-networks','--master-authorized-networks', ','.join(new_networks)])




def _create_cluster(cfg, region):
    clusters = run('gcloud container clusters list', read=True, msg='').strip().splitlines()
    print.ln(clusters)
    exists = reduce(lambda a, l: a or l.split(' ')[0] == cfg.gcp_gke_cluster_name, clusters, False)
    print.ftr('Cluster~lang ja~クラスター', ['']*2, CLR.g if exists else CLR.lb, 'Exists~lang ja~既にある' if exists else 'Create~lang ja~作成する', CLR.x)
    if exists: return

    cmd = [
        'gcloud','container','clusters','create-auto',cfg.gcp_gke_cluster_name,
        '--create-subnetwork', f'name={cfg.gcp_nickname}-subnet',
        '--enable-master-authorized-networks', # specifies that access to the public endpoint is restricted to IP address ranges that you authorize.
        '--enable-private-nodes', # indicates that the cluster's nodes do not have external IP addresses.
        #'--enable-private-endpoint', # indicates that the cluster is managed using the private IP address of the control plane API endpoint.
        '--master-ipv4-cidr','172.16.0.16/28', # Default internal IP address range for the control plane
        '--region', region,
    ]

    confirm(f''' This will create a kubernetes cluster '{cfg.gcp_gke_cluster_name}' in GCP project '{cfg.gcp_project_name}'
        ~lang ja~これにより、GCPプロジェクト「{cfg.gcp_project_name}」にkubernetesクラスタ「{cfg.gcp_gke_cluster_name}」が作成されます。
        ''', ['']*3, ' '.join(cmd), ['']*3, 'Continue?~lang ja~継続する？', ' [y/N]')

    run(cmd, msg="Creating cluster...~lang ja~クラスターを作成する...",
        err=Text(print.ERR, '''Cluster creation failed. Ensure that you have enabled the Google Kubernetes Engine API.
            ~lang ja~クラスターの作成に失敗しました。Google Kubernetes EngineAPIが有効になっていることを確認してください。'''))

    

def _add_namespaces(cfg):
    api = k8s.client.CoreV1Api()
    names = [i.metadata.name for i in api.list_namespace(watch=False).items]
    print.ln([f'   {n}' for n in names])
    exists = cfg.gcp_gke_namespace in names
    print.ftr('Namespace~lang ja~名前空間', ['']*2, 'Exists~lang ja~既にある' if exists else 'Created~lang ja~作成した')
    if exists: return
    print.ln(f"Creating namespace '{cfg.gcp_gke_namespace}'~lang ja~「{cfg.gcp_gke_namespace}」の名前空間を作成する",'...')
    try: api.create_namespace(k8s.client.V1Namespace(metadata=k8s.client.V1ObjectMeta(name=cfg.gcp_gke_namespace)))
    except k8s.client.exceptions.ApiException as e:
        if e.status not in [409, 200]: raise e


def _cloud_nat(cfg, region):
    # Cloud NAT
    routers = run(f'gcloud compute routers list', read=True, msg='').splitlines()
    print.ln(routers)
    exists = reduce(lambda a,l: a or l.split(' ')[0] == f'{cfg.gcp_nickname}-router', routers, False)
    print.ftr('NAT Router for private cluster~lang ja~プライベートクラスター用のNATルーター', ['']*2, 'Exists~lang ja~既にある' if exists else 'Created~lang ja~作成した')
    if exists: return
    run(f'gcloud compute routers create {cfg.gcp_nickname}-router --region {region} --network default')
    run(f'gcloud beta compute routers nats create nat --router={cfg.gcp_nickname}-router --region {region} --auto-allocate-nat-external-ips --nat-all-subnet-ip-ranges')


def _ingress(cfg):
    'networking.k8s.io/v1'


@CLI()
def init():
    ''' Create a Google Kubernetes Engine (gke) cluster to host this project.

    This only needs to be called once.
    However, it will ask for confirmation before actaully creating anything so it is safe to call anytime.
    '''
    cfg = Config()
    verify_gcloud_project(cfg)
    region = run('gcloud config get-value compute/region', read=True, msg='').strip()
    _create_cluster(cfg, region)
    exists = control_plane_auth(add__a='me')
    print.ftr('Add me to GKE Control plane auth networks~lang ja~GKEコントロールプレーン認証ネットワークに追加する', ['']*2, 'Exists' if exists else 'Added')

    set_gke_cluster_config_credentials(cfg, region)
    k8s.config.load_kube_config()
    _add_namespaces(cfg)
    _cloud_nat(cfg, region)





@CLI()
def info(*, all__a=False):
    ''' Show information about gke objects~lang ja~gkeオブジェクトに関する情報を表示する

    Parameters:
        --all, -a
            Show information for all namespaces.  By default only show information for the current target's namespace.
            ~lang ja~ すべての名前空間の情報を表示します。 デフォルトでは、現在のターゲットの名前空間の情報のみが表示されます。
    '''
    cfg = Config()
    set_gke_cluster_config_credentials(cfg)

    v1 = k8s.client.CoreV1Api()
    if all__a:
        pods = v1.list_pod_for_all_namespaces().items
        services = v1.list_service_for_all_namespaces().items
    else:
        pods = v1.list_namespaced_pod(cfg.gcp_gke_namespace).items
        services = v1.list_namespaced_service(cfg.gcp_gke_namespace).items

    def _svc_fmt(i):
        ports = [f'{p.port}/{p.protocol}' for p in i.spec.ports]
        return f'{i.metadata.namespace:>20}  {i.metadata.name:<30} {i.spec.cluster_ip} {" ".join(ports)}'
    def _pod_fmt(i):
        return f'{i.metadata.namespace:>20}  {i.metadata.name:<30} {i.status.pod_ip}'
    
    print.ln([_pod_fmt(p) for p in pods])
    print.ftr("Pods")
    
    print.ln([_svc_fmt(s) for s in services])
    print.ftr("Services")
