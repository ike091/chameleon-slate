import chi
from chi import lease
from chi import network
from chi import server
from chi.ssh import Remote

PROJECT_NAME = 'SLATE'
PROJECT_ID = 'CHI-210813'
DEFAULT_SITE = 'CHI@TACC'

#  chi.use_site(DEFAULT_SITE)
#  chi.set("project_name", PROJECT_NAME)
chi.set("image", "CC-CentOS8")
chi.set("project_domain_id", "ba9774ff83e946689d066c501a2fd106")


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


reservation_id = lease.get_node_reservation(l["id"])
server.create_server(
    "chi-in-a-box-dev",
    reservation_id=reservation_id,
    nics=[{"port-id": port_id}],
    image_name=chi.get("image")
)

# Due to a quirk, the node initially only has the second public IP wired,
# so waiting for reserved_fips[0] will not work! We will fix this in the next step.
server.wait_for_tcp(reserved_fips[1], port=22)




public_mgmt_address = reserved_fips[0]
public_vip_address = reserved_fips[1]
public_vip_address_internal_pair = port['fixed_ips'][0]['ip_address']
private_vip_address = port['fixed_ips'][1]['ip_address']

# Verify we can connect via the public management address
hostname = Remote(ip=public_mgmt_address).run("hostname", hide=True).stdout
print(f"Hostname: {hostname.strip()} ({public_mgmt_address})")

print(f"""
Management address: {public_mgmt_address}
Public VIP: {public_vip_address}
Private VIP: {private_vip_address}
""")


