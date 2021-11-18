# -*- coding: utf-8 -*-

# Generic/Built-in



# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
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

    #Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.get_cluster_status(False, CmdlineArgs.ClusterID)
        if capella_api_response.status_code == 200:
            #Cluster information was found
            print("Status for cluster with ID " + CmdlineArgs.ClusterID + " is " + capella_api_response.json()['status'])
        else:
            print("Failed to get status for cluster ID " + CmdlineArgs.ClusterID)
            print("Capella API returned " + str(capella_api_response.status_code) )
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")



if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Get the status of a cluster running in your cloud')
    my_parser.ExampleCmdline = """-cid "1478c0f4-07b2-4818-a5e8-d15703ef79b0" """

    # Add the arguments

    my_parser.add_argument("-cid","--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster " )

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
