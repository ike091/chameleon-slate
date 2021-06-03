# Chameleon Stitched Network Notes

## Commands:

### Network leases
```bash
blazar lease-create --reservation resource_type=network,network_name=slate-network-1,resource_properties='["==","$physical_network","exogeni"]' --start-date "2021-05-10 8:00" --end-date "2021-05-13 19:00" vlan-lease-1
```
```bash
`blazar lease-create --reservation resource_type=network,network_name=slate-network-2,resource_properties='["==","$physical_network","exogeni"]' --start-date "2021-05-10 8:00" --end-date "2021-05-13 19:00" vlan-lease-2`
```

### Leases in general
Use the lease-create command. The following arguments are required:
* `--reservation` with the `resource_type` and `network_name` attributes
* `--start-date` in "YYYY-MM-DD HH:MM" format
* `--end-date` in "YYYY-MM-DD HH:MM" format
* A lease name

Example:
```bash
blazar lease-create --physical-reservation min=1,max=1,resource_properties='["=", "$node_type","compute_haswell"]' --start-date "2021-05-10 06:00" --end-date "2021-05-13 19:00" slate_reservation
```

### Instructions

Once the stitched networks have been created, a subnet must be added to each network.
Additionally, a router must be attached to each network for external access.

"After having stitchable isolated networks on UC and TACC sites, a request should be sent to the Help Desk for creation of AL2S circuits. In the request, following information should be specified: - Information for the network at UC (Project ID, name of the network, ID of the network) - Information for the network at TACC (Project ID, name of the network, ID of the network) - Duration of the circuit in active state"


## Pitfalls
* Be aware of Blazar client versions. Seems to only work with 2.2.2, not 3.2.0.
* Both networks cannot be named the same, otherwise an error will result.


## Experiments

* Ran `iperf` between both nodes - very high speeds - 700 megabits or so - see screenshot
* Hosted an Nginx application (without ingress controller) on both nodes, and accessed from other node

### perfSONAR
* Ran the `perfsonar-testpoint` application (stable) on one cluster
* Then, ran the `perfsonar-checker` application (incubator) on the other cluster
* Used `/etc/hosts` files to give each cluster a DNS name

