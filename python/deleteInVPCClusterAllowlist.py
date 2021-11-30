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

    bucket_configuration = {
        "cidrBlock": cmd_line_args.cidrBlock
    }

    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.delete_cluster_allowlist(cmd_line_args.clusterID, bucket_configuration)

        # Did the delete work?
        if capella_api_response.status_code == 204:
            print("Deleting allowlist ")
        else:
            print("Failed to delete allowlist ")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()['message'])


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Deletes an allowlist from a cluster running in your cloud')
    my_parser.ExampleCmdline = "-cid d157a069-9451-4188-a4b1-8be2920db094 -cb 10.0.0.1"

    # Add the arguments

    my_parser.add_argument('-cid', '--clusterID',
                           dest="clusterID",
                           metavar="",
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='The ID of the cluster')

    my_parser.add_argument('-cb', '--cidrBlock',
                           dest="cidrBlock",
                           metavar="",
                           action='store',
                           required=True,
                           help='The cidr block of the allow list to delete')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
