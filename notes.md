# Chameleon Notes


## MetalLB Notes

`openstack port set <port-id> --allowed-address ip-address=<additional-ip-address>`
*Note that this command is not allowed on the main "shared-net".*

`openstack port set <port-id> --disable-port-security`
results in the following error: "ConflictException: 409: Client Error for url: https://chi.uc.chameleoncloud.org:9696/v2.0/ports/183c2e42-8d82-4263-9236-8b9a2cbcf376, Port Security must be enabled in order to have allowed address pairs on a port."

Was able to get everything up and running, can use additional internal IP
Not sure if allowing additional addresses per port was necessary - verify this
Verify that I can reach the ingress controller from another machine on subnet


## Random

Compute haswell nodes seem to have multiple interfaces? - verify in docs

To set up a Chameleon instance without shared-net1: bring up another subnet, with a router connected to the "global" network


## Kubespray Cluster behind NAT

* In `hosts.yaml`, set `access_ip` to the internal IP - `ansible_host` will be set to the external IP, and `ip` will be set to the internal IP

* Add this variable in `group_vars/k8s-cluster/k8s-cluster.yml`: 
`supplementary_addresses_in_ssl_keys: ['<EXTERNAL_NAT_IP>']`

* Disable firewall: `sudo ufw disable`


## SLATE Registration

**Manual Registration:**

* Make a copy of `/etc/kubernetes/admin.conf` and change the `server:` field to the public IP of cluster (port 6443)
* Modify `KUBECONFIG` environment variable: `export KUBECONFIG=/path/to/copied/admin.conf`
* On the SLATE CLI, use the `--kubeconfig` flag to point to the updated `admin.conf`



**SLATE-Ansible Registration:**

* Add `-e slate_enable_ingress=false`

* Add `-e 'cluster_access_ip=<PUBLIC_NAT_IP:6443>'`

`ansible-playbook -i ../kubespray/inventory/chameleon/hosts.yaml -u cc --become --become-user=root -e 'slate_cli_token=cr3UI1NG1bQYh3o_htdR0k' -e 'slate_cli_endpoint=https://api-dev.slateci.io:18080' -e 'slate_enable_ingress=false' -e 'cluster_access_ip=<PUBLIC_NAT_IP>:6443' site.yml`


## Ingress controller notes:

To enable an ingress controller using the node's public IP, run the following command: `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/baremetal/deploy.yaml`

Note that anything accessed through this ingress controller operates through NodePort, and that any resources accessed through this must have the `ingress-nginx` port appended.

To find this port, run `kubectl get services -A`.

Regular bare-metal ingress controller results in a 404 not-found error

SLATE ingress controller failed deployment works - never assigns public IP


## Things to Learn

Ingress controllers vs. load balancers
Layer 7 networking
Complete SLATE networking model
Understanding how exactly MetalLB "assigns" floating IPs
Need a better understanding of ARP



** Errors: **

slate: Exception: Unable to list deployments in the kube-system namespace; this command needs to be run with kubernetes administrator privileges in order to create the correct environment (with limited privileges) for SLATE to use.
Kubernetes error: Unable to connect to the server: dial tcp 192.5.87.86:6443: i/o timeout


The entered/detected Kubernetes API server address,
"https://10.140.81.219:6443"
has a possible problem:
Host address appears to be in the 10.0.0.0/8 private CIDR block
Public cluster URL or continue with existing? [https://10.140.81.219:6443]:

TASK [kubernetes-apps/ingress_controller/cert_manager : Cert Manager | Apply ClusterIssuer manifest] *******************
fatal: [node1]: FAILED! => {"changed": false, "msg": "error running kubectl (/usr/local/bin/kubectl apply --force --filename=/etc/kubernetes/addons/cert_manager/clusterissuer-cert-manager.yml) command (rc=1), out='', err='Error from server: error when retrieving current configuration of:\nResource: \"cert-manager.io/v1alpha2, Resource=clusterissuers\", GroupVersionKind: \"cert-manager.io/v1alpha2, Kind=ClusterIssuer\"\nName: \"ca-issuer\", Namespace: \"\"\nfrom server for: \"/etc/kubernetes/addons/cert_manager/clusterissuer-cert-manager.yml\": conversion webhook for cert-manager.io/v1, Kind=ClusterIssuer failed: Post \"https://cert-manager-webhook.cert-manager.svc:443/convert?timeout=30s\": x509: certificate signed by unknown authority (possibly because of \"x509: ECDSA verification failure\" while trying to verify candidate authority certificate \"cert-manager-webhook-ca\")\n'"}


