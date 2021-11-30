# -*- coding: utf-8 -*-
# Generic/Built-in

# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
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

def show_cluster_server_configuration(configuration_to_show):
    cluster_server_table_rows = []

    if configuration_to_show is not None:
        # Check that is not blank and there are entries
        if len(configuration_to_show) > 0:
            table_Heading = ['Services', 'Nodes', 'Compute', 'Storage size', 'Storage IOPs','Storage type']
            for cluster_server_entry in configuration_to_show:
                server_Services = cluster_server_entry['services']
                server_Nodes = cluster_server_entry['size']
                server_Compute = cluster_server_entry['compute']
                server_Storage_Size = cluster_server_entry['storage']['size']
                server_Storage_IOPs = cluster_server_entry['storage']['IOPS']
                server_Storage_Type = cluster_server_entry['storage']['type']


                # Put the completed row in the table
                cluster_server_table_rows.append([server_Services, server_Nodes, server_Compute, server_Storage_Size, server_Storage_IOPs, server_Storage_Type ])

            # Display the table, which uses pretty table to make things easier
            print(pretty_table(table_Heading, cluster_server_table_rows))


def main(CmdLineArgs):

    # This represents the new server service configuration
    new_server_service_configuration = {
        "servers": [
            {
                "compute": "m5.xlarge",
                "size": 3,
                "services": ["data"],
                "storage": {
                    "size": 300,
                    "IOPS": 3000,
                    "type": "GP3"
                }
            }
        ]
    }

    cappella_api = CapellaAPI()

    if CmdLineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    # Check API is up
    if cappella_api.api_status().status_code == 200:

        # Show the current cluster configuration
        # first we'll need to get the configuration
        capella_api_response = cappella_api.get_cluster_info(True, CmdLineArgs.ClusterID)

        #Then pass the bit we're interested in to the function that will display it
        if capella_api_response.status_code == 200:
            print('Current cluster configuration')
            show_cluster_server_configuration(capella_api_response.json()['servers'])

            # Now we will tell the API to change the configuration
            capella_api_response = cappella_api.update_cluster_servers(CmdLineArgs.ClusterID, new_server_service_configuration)

            # Check response code , 201 is success
            if capella_api_response.status_code == 202:
                # Got a response back
                print("Changing cluster to ")
                show_cluster_server_configuration(new_server_service_configuration['servers'])


            else:
                print("Failed to change the cluster configuration " )
                print("Capella API returned " + str(capella_api_response.status_code))
                print("Full error message")
                print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description="Scales the cluster to run each service on it's own set of 3 nodes with 300Gb storage on each ")
    my_parser.ExampleCmdline = """-cid "1478c0f4-07b2-4818-a5e8-d15703ef79b0" """

    # Add the arguments

    my_parser.add_argument('-cid', '--ClusterID',
                           action='store',
                           required=True,
                           type=str,
                           help='ID of the cluster')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)


