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

# Defines our own class, based on argparse so we can define a custom help
# message with an example


def main(cmd_line_args):

    cappella_api = CapellaAPI()

    if cmd_line_args.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    cluster_configuration = {
        "cloudId": cmd_line_args.cloudID,
        "name": cmd_line_args.clusterName,
        "projectId": cmd_line_args.projectID,
        "servers": [
            {
                "services": [
                    "data", "index", "query", "search"
                ],
                "size": 3,
                "aws": {
                    "ebsSizeGib": 50,
                    "instanceSize": "m5.xlarge"
                }
            }
        ],
        "version": "latest"
    }

    # Create the cluster, pass the configuration
    # and indicate that this cluster will run in the customers own cloud by calling with False
    capella_api_response = cappella_api.create_cluster(False, cluster_configuration)

    # Check response code , 201 is success
    if capella_api_response.status_code == 202:
        print("Creating cluster ")
        print("Check deployment status here: " + cappella_api.API_BASE_URL +
              capella_api_response.headers['Location'] + '/status')
    else:
        print("Failed to create cluster ")
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates a cluster using customers own cloud in Couchbase Capella')
    my_parser.ExampleCmdline = """-cn "ANewCluster" -cid "070a3be4-5246-40e3-9b57-5a51a2663d20" -pid "1478c0f4-07b2-4818-a5e8-d15703ef79b0" """

    # Add the arguments
    my_parser.add_argument('-cn', '--clusterName',
                           action='store',
                           required=True,
                           type=str,
                           help='The name to use for the cluster')

    my_parser.add_argument('-cld', '--cloudID',
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help='ID of the cloud to use with the cluster')

    my_parser.add_argument('-pid', '--projectID',
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help='ID of the project to use with the cluster')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
