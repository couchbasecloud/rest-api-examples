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

    capella_api_response = cappella_api.get_clusters()

    # Check response code , 200 is success
    if capella_api_response.status_code == 200:
        cluster_table_rows = []
        list_of_clusters = capella_api_response.json()


        # We should have a list of clusters, but just in case, check
        # Then we will build rows to show in a table
        if list_of_clusters is not None:
            for Cluster in list_of_clusters['data']:
                cluster_table_rows.append([Cluster['name'], Cluster['id'], Cluster['nodes'], Cluster['services']])

        ClusterTableHeading = ['Name', 'ID', 'Nodes', 'Services']

        # Display the table, which uses pretty table to make things easier
        print('Clusters')
        print(pretty_table(ClusterTableHeading, cluster_table_rows))

    else:
        print("Failed to get list of InVPC clusters " )
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser

    my_parser = MyParser(description='Gets list of clusters running in your cloud account from Couchbase Capella')
    my_parser.ExampleCmdline = """With debug on  -d \nWith debug off  """

    # Add the arguments

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)

