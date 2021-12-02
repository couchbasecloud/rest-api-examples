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


def main(cmd_line_args):
    cappella_api = CapellaAPI()

    if cmd_line_args.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    # Delete the cluster and indicate that this cluster
    # will run in the customers own cloud by calling with False
    capella_api_response = cappella_api.delete_cluster(False, cmd_line_args.clusterID)

    # Check response code , 201 is success
    if capella_api_response.status_code == 202:
        print("Deleting cluster ")
        print("Check status here: " + cappella_api.API_BASE_URL +
              capella_api_response.headers['Location'] + '/status')
    else:
        print("Failed to delete cluster ")
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Deletes a cluster running in your cloud from Couchbase Capella')
    my_parser.ExampleCmdline = """-cid 1478c0f4-07b2-4818-a5e8-d15703ef79b0 """

    # Add the arguments
    my_parser.add_argument('-cid', '--clusterID',
                           dest="clusterID",
                           metavar="",
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='The ID of the cluster')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
