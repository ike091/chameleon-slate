import chi
from chi.lease import create_lease
import argparse

# Install python module with:
# pip install python-chi


SLATE_PROJECT_NAME = 'SLATE'
SLATE_PROJECT_ID = 'CHI-210813'
DEFAULT_SITE = 'CHI@UC'
DEFAULT_NODE_TYPE = 'compute_skylake'
DEFAULT_LEASE_LENGTH = 1


def main():

    parser = argparse.ArgumentParser(description='Parse command line options.')

    # Set up various command line arguments
    parser.add_argument('-s', '--site', help='The site to spin up cluster at.', choices=['CHI@UC', 'CHI@TACC'], default=DEFAULT_SITE)
    parser.add_argument('-p', '--project', help='The name of your Chameleon project.', default=SLATE_PROJECT_NAME)
    parser.add_argument('-c', '--code', help='Chameleon project code.', default=SLATE_PROJECT_ID)
    parser.add_argument('-n', '--nodetype', help='The type of node to request.', default=DEFAULT_NODE_TYPE)
    parser.add_argument('-d', '--duration', type=int, help='The length of lease to request.', default=DEFAULT_LEASE_LENGTH)

    args = parser.parse_args()


    # Select appropriate site, project name, and project charge code
    #  chi.set(args.project, args.code)
    chi.use_site(args.site)
    session = chi.session()


    reservations = []
    # Make a reservation for one node of type "compute_skylake"
    chi.lease.add_node_reservation(reservations, node_type=args.nodetype, count=1)
    # Add a floating IP to reservation
    chi.lease.add_fip_reservation(reservations, count=1)

    # Set reservation start and end dates
    start_date, end_date = chi.lease.lease_duration(days=args.duration)

    lease_name = "slate-lease"

    # Create lease
    chi.lease.create_lease(lease_name, reservations, start_date=start_date, end_date=end_date)

    reservation_id = get_node_reservation(lease_name)

    server_name = "slate-cluster"
    server = create_server(server_name, reservation_id=reservation_id)

    server_id = server.get_server_id()

    ip = associate_floating_ip(server_id)


    # We assume a lease has already been created, for example with
    # chi.lease.create_lease

    print("Waiting for network connectivity...")
    wait_for_tcp(ip, port=22)
    print("Network connectivity established.")
    print("Node created successfully.")



if __name__ == "__main__":

    main()





