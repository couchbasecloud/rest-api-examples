# -*- coding: utf-8 -*-
# Generic/Built-in

# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
from capellaAPI.CapellaAPICommon import pretty_table
from capellaAPI.CapellaAPI import CapellaAPI

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def main(cmd_line_args):
    cappella_api = CapellaAPI()

    if cmd_line_args.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.get_cluster_health(cmd_line_args.ClusterID)

        print("Cluster status: " + capella_api_response.json()["status"] + "\n")
        if capella_api_response.status_code == 200:
            # Show a table with the node information
            table_rows = []
            table_header = ["Node name", "Services", "Status"]

            if "nodeStats" in capella_api_response.json():
                table_entries = capella_api_response.json()["nodeStats"]
            else:
                table_entries = None
                print("Node information not available\n")

            # We should have a list of nodes, but just in case, check
            # Then we will build the table
            if table_entries is not None:
                # Make sure the list is not empty
                if len(table_entries) > 0:
                    cluster_node_count = str(table_entries["totalCount"])
                    for entry in table_entries["serviceStats"]:
                        service_list_as_str = ' '.join(entry["services"])
                        table_rows.append([entry["nodeName"], service_list_as_str, entry["status"]])

                    print('Cluster nodes: ' + cluster_node_count)
                    print(pretty_table(table_header, table_rows))

            # Reset everything, we're going to do another table with the bucket information
            table_rows = []
            table_header = ["Bucket name", "Status"]

            if "bucketStats" in capella_api_response.json():
                table_entries = capella_api_response.json()["bucketStats"]
            else:
                table_entries = None
                print("Bucket information not available\n")

            if table_entries is not None:
                # Make sure the list is not empty
                if len(table_entries) > 0:
                    cluster_bucket_count = str(table_entries["totalCount"])
                    for entry_key in table_entries["healthStats"].keys():
                        table_rows.append([entry_key, table_entries["healthStats"][entry_key]])

                    print('Cluster buckets: ' + cluster_bucket_count)
                    print(pretty_table(table_header, table_rows))

        else:
            print("Failed to get health for cluster ID " + cmd_line_args.ClusterID)
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Get the health of a cluster running in your cloud')
    my_parser.ExampleCmdline = "-cid 1478c0f4-07b2-4818-a5e8-d15703ef79b0"

    # Add the arguments
    my_parser.add_argument("-cid", "--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster ")

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
