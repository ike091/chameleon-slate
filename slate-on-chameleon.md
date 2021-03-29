# Creating a SLATE Cluster on Chameleon


**Chameleon:**

* Obtain Chameleon credentials
* Join a project
* Create a reservation for one instance and one floating public IP
* Launch one CentOS 7 instance, with a floating public IP mapped to the instance's private interface

* Set up Ansible playbook according to instructions here: [SLATE Cluster Creation with Kubespray and Ansible](https://slateci.io/docs/cluster/automated/introduction.html). 
* 

* Run playbook: `ansible-playbook -i inventory/<CLUSTER_NAME>/hosts.yaml --become --become-user=root -u <SSH_USER> cluster.yml`

```bash
ansible-playbook -i /path/to/kubespray/inventory/<CLUSTER_NAME>/hosts.yaml -u <SSH_USER> --become --become-user=root \
 -e 'slate_cli_token=<SLATE_CLI_TOKEN>' \
 -e 'slate_cli_endpoint=https://api.slateci.io:443' \
 -e 'cluster_access_ip=<EXTERNAL_NAT_IP>:6443' \
 -e 'slate_enable_ingress=false' \
 site.yml
```
