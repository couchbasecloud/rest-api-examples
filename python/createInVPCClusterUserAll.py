# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs

# Owned
from capellaAPI.CapellaAPI import CapellaAPI
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
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
        capella_logging('info')

    cluster_user_struct = {
        "password": cmd_line_args.Password,
        "username": cmd_line_args.UserName,
    }

    # Split up into the individual bits we need
    all_bucket_access = cmd_line_args.Access.strip()

    # Look at the access requested and then map to what the endpoint expects
    if all_bucket_access == 'r':
        cluster_user_struct['allBucketsAccess']="data_reader"
    elif all_bucket_access == 'w':
        cluster_user_struct['allBucketsAccess']="data_writer"
    else:
        raise UserBucketAccessListError('access not found')

    # Check Capella API status
    if capella_api.api_status().status_code == 200:
        capella_api_response = capella_api.create_cluster_user(False, cmd_line_args.ClusterID, cluster_user_struct)

        if capella_api_response.status_code == 201:
            print("Cluster user is being created")
        else:
            print("Failed to create user")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")


def bucket_access_type(bucket_access_list):
    # We should have a string like this r or w
    # nothing else is allowed

    if bucket_access_list == 'r':
        return (bucket_access_list)
    elif bucket_access_list == 'w':
        return (bucket_access_list)
    else:
        raise UserBucketAccessListError(bucket_access_list + " is not valid access permission.  must be r or w.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates a user for a cluster and grants them access to all buckets')
    my_parser.ExampleCmdline = "-cid d157a069-9451-4188-a4b1-8be2920db094 -un myuser -pwd Password123! -a w"

    # Add the arguments

    my_parser.add_argument("-cid", "--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster ")

    my_parser.add_argument('-un', '--UserName',
                           dest="UserName",
                           action='store',
                           required=True,
                           metavar="",
                           type=str,
                           help='Username to create')

    my_parser.add_argument('-pwd', '--Password',
                           dest="Password",
                           action='store',
                           metavar="",
                           type=str,
                           required=True,
                           help='Password for the user')

    my_parser.add_argument('-a', '--Access',
                           action='store',
                           type=bucket_access_type,
                           required=True,
                           help='Access for all buckets in the cluster.\n  Bucket access can be r or w')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
