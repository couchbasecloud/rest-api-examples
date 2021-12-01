# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import re

# Owned
from capellaAPI.CapellaAPI import CapellaAPI
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
from capellaAPI.CapellaAPICommon import check_bucket_and_scope_type
from capellaAPI.CapellaExceptions import UserBucketAccessListError

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
        capella_logging('INFO')

    cluster_user_struct = {
        "password": cmd_line_args.password,
        "username": cmd_line_args.user_name,
        "buckets": []
    }

    # Go through each entry
    for bucket_and_scope_entry in cmd_line_args.buckets_and_scope.split(','):

        cluster_user_bucket_and_scope_access = {"name": "", "scope": "", "access": ""}

        # Split up into the individual bits we need
        bucket_and_scope_entry = bucket_and_scope_entry.strip()
        bucket_access = bucket_and_scope_entry.split(':')[2]
        bucket_scope = bucket_and_scope_entry.split(':')[1]
        bucket_name = bucket_and_scope_entry.split(':')[0]


        # Set the name of the bucket we're going to grant access to
        cluster_user_bucket_and_scope_access['name'] = bucket_name

        # Set the scope
        cluster_user_bucket_and_scope_access['scope'] = bucket_scope


        # Look at the access requested and then map to what the endpoint expects
        if bucket_access == 'r':
            cluster_user_bucket_and_scope_access["access"] = "data_reader"
        elif bucket_access == 'w':
            cluster_user_bucket_and_scope_access["access"] = "data_writer"
        elif bucket_access == 'rw':
            cluster_user_bucket_and_scope_access["access"] = "data_writer"
        elif bucket_access == 'wr':
            cluster_user_bucket_and_scope_access["access"] = "data_writer"
        else:
            # This should never have passed the regex test done in check_bucket_and_scope_type
            # but just in case....
            print('access not found for ' + bucket_and_scope_entry)
            raise UserBucketAccessListError('access not found for ' + bucket_and_scope_entry)

        cluster_user_struct["buckets"].append(cluster_user_bucket_and_scope_access)

    # Check Capella API status
    if capella_api.api_status().status_code == 200:
        capella_api_response = capella_api.create_cluster_user(True, cmd_line_args.cluster_id, cluster_user_struct)

        if capella_api_response.status_code == 201:
            print("Cluster user is being created")
        else:
            print("Failed to create user")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates a user for a cluster and grants them access to one or more buckets')
    my_parser.ExampleCmdline = """-cid d157a069-9451-4188-a4b1-8be2920db094 -un myuser -pwd Password123! -b 
    "bucket1:*:rw,bucket2:MyScope:rw" """

    # Add the arguments
    my_parser.add_argument("-cid", "--ClusterID",
                           dest="cluster_id",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster ")

    my_parser.add_argument('-un', '--UserName',
                           dest="user_name",
                           action='store',
                           required=True,
                           metavar="",
                           type=str,
                           help='Username to create')

    my_parser.add_argument('-pwd', '--Password',
                           dest="password",
                           action='store',
                           metavar="",
                           type=str,
                           required=True,
                           help='Password for the user')

    my_parser.add_argument('-b', '--Buckets',
                           dest="buckets_and_scope",
                           action='store',
                           metavar="",
                           type=check_bucket_and_scope_type,
                           required=True,
                           help='Bucket with scope and bucket access.\n  '
                                'Format: <bucket name>:<scope>:<bucket access> \n '
                                'Scope can be * for all scopes or the scope name \n '
                                'Bucket access can be r,w or rw. \n '
                                '* is not permitted for a bucket name')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
