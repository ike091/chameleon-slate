import chi
from chi import lease
from chi import network

chi.use_site("CHI@TACC")
chi.set("project_name", "YOUR_PROJECT_NAME")
chi.set("image", "CC-CentOS8")


res = []
lease.add_node_reservation(res, node_type="compute_cascadelake_r", count=1)
lease.add_fip_reservation(res, count=2)
lease.add_network_reservation(res, network_name="chi-in-a-box-net")
start_date, end_date = lease.lease_duration(days=7)

l = lease.create_lease("chi-in-a-box-dev", res, start_date=start_date, end_date=end_date)
l = lease.wait_for_active(l["id"])


# Create the node network port. This will be used to host
# the CHI-in-a-Box API endpoints, amongst other things.
# This is a bit complicated because we need to assign two
# IP addresses to the instance on one interface.
try:
    port = network.get_port("chi-in-a-box-pubport")
except:
    network_id = network.get_network_id("sharednet1")
    subnet_id = network.get_subnet_id("sharednet1-subnet")
    port = chi.neutron().create_port(body={
        "port": {
            "name": "chi-in-a-box-pubport",
            "network_id": network_id,
            "fixed_ips": [{"subnet_id": subnet_id}, {"subnet_id": subnet_id}, {"subnet_id": subnet_id}]
        }
    })["port"]
finally:
    port_id = port["id"]


reserved_fips = lease.get_reserved_floating_ips(l["id"])

# Node will boot and acquire DHCP using last fixed_address in port.
# Bind a Floating IP to that--this is our management public connection IP.
network.bind_floating_ip(reserved_fips[0], port_id=port_id, fixed_ip_address=port["fixed_ips"][2]["ip_address"])

# Also bind a Floating IP to the public "VIP" for CHI-in-a-Box
network.bind_floating_ip(reserved_fips[1], port_id=port_id, fixed_ip_address=port["fixed_ips"][0]["ip_address"])

