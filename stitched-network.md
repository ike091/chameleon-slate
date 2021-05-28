
To create a lease, use the lease-create command. The following arguments are required:

    --reservation with the `resource_type` and `network_name` attributes
    --start-date in "YYYY-MM-DD HH:MM" format
    --end-date in "YYYY-MM-DD HH:MM" format
    A lease name


Command:
`blazar lease-create --reservation resource_type=network,network_name=slate-network,resource_properties='["==","$physical_network","exogeni"]' --start-date "2021-05-10 8:00" --end-date "2021-05-13 19:00" vlan-lease-1`

`blazar lease-create --reservation resource_type=network,network_name=slate-network,resource_properties='["==","$physical_network","exogeni"]' --start-date "2021-05-10 8:00" --end-date "2021-05-13 19:00" vlan-lease-2`



"After having stitchable isolated networks on UC and TACC sites, a request should be sent to the Help Desk for creation of AL2S circuits. In the request, following information should be specified: - Information for the network at UC (Project ID, name of the network, ID of the network) - Information for the network at TACC (Project ID, name of the network, ID of the network) - Duration of the circuit in active state"


Matches: ('min=1,max=1', 'resource_properties', '["=", "$node_type", "compute_haswell"]')
Matches: ('min=1', 'max', '1')
Matches: (None, 'min', '1')
ERROR: Internal Server Error


`blazar lease-create --physical-reservation min=1,max=1,resource_properties='["=", "$node_type","compute_haswell"]' --start-date "2021-05-10 06:00" --end-date "2021-05-13 19:00" slate_reservation`

