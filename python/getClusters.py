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



def main(CmdlineArgs):
    cappella_api = CapellaAPI()

    if CmdlineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    capella_api_response = cappella_api.get_clusters_v3()

    # Check response code , 200 is success
    if capella_api_response.status_code == 200:
        clusters_table_rows = []
        cluster_entries = capella_api_response.json()['data']['items']

        # We should have a list of clusters, but just in case, check
        # Then we will build rows to show in a table
        if cluster_entries is not None:
            # Check to see if we got any users back
            if len(cluster_entries) > 0:
                ClusterTableHeading = ['Environment', 'Name', 'Cluster ID', 'Cloud ID', 'Project ID']
                for cluster_entry in cluster_entries:
                    clusterEnvironment = cluster_entry['environment']
                    clusterID = cluster_entry['id']
                    clusterName = cluster_entry['name']
                    projectID = cluster_entry['projectId']
                    # if the cluster is inVPC, then we will have a cloud ID
                    if clusterEnvironment == 'inVpc':
                        clusterCloudID = cluster_entry['cloudId']
                    else:
                        clusterCloudID = 'N/A'

                    # Put the completed row in the table
                    clusters_table_rows.append([clusterEnvironment, clusterName, clusterID, clusterCloudID, projectID])

                # Display the table, which uses pretty table to make things easier
                print('Capella Clusters ')
                print(pretty_table(ClusterTableHeading, clusters_table_rows))

            else:
                print("No users found for this cluster")
        else:
            print("No users found for this cluster")
    else:
        print("Failed to get list of users for this cluster ")
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser

    my_parser = MyParser(description='List clusters managed by Couchbase Capella')
    my_parser.ExampleCmdline = """With debug on -d \nWith debug off """

    # Add the arguments
    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)