# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import re

import fe

# Owned
from capellaAPI.CapellaAPI import CapellaAPI
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid


__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def main(cmd_line_args):
    capella_api = CapellaAPI()

    if cmd_line_args.debug:
        capella_logging('debug')
        capella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')


    # Check Capella API status
    if capella_api.api_status().status_code == 200:
        capella_api_response = capella_api.delete_cluster_user(False, cmd_line_args.clusterID, cmd_line_args.UserName)

        if capella_api_response.status_code == 204:
            print("Cluster user is deleted")
        else:
            print("Failed to delete user")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Deletes a user from a cluster')
    my_parser.ExampleCmdline = " -cid d157a069-9451-4188-a4b1-8be2920db094 -un myuser "

    # Add the arguments

    my_parser.add_argument('-cid', '--clusterID',
                           dest="clusterID",
                           metavar="",
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='The ID of the cluster')

    my_parser.add_argument('-un', '--UserName',
                           dest="UserName",
                           metavar="",
                           action='store',
                           required=True,
                           type=str,
                           help='Username to delete')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
