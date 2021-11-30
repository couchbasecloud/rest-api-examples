# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import re

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
        capella_logging('INFO')

    cluster_user_struct = {
        "password": cmd_line_args.Password,
        "username": cmd_line_args.UserName,
        "buckets": []
    }

    # Go through each entry
    for bucket_and_access_entry in cmd_line_args.Buckets.split(','):

        cluster_user_bucket_access_struct = {"bucketName": "", "bucketAccess": []}

        # Split up into the individual bits we need
        bucket_and_access_entry = bucket_and_access_entry.strip()
        bucket_access_requested = bucket_and_access_entry.split(':')[1]
        bucket_access_name = bucket_and_access_entry.split(':')[0]

        # Set the name of the bucket we're going to grant access to
        cluster_user_bucket_access_struct['bucketName'] = bucket_access_name

        # Look at the access requested and then map to what the endpoint expects
        if bucket_access_requested == 'r':
            cluster_user_bucket_access_struct["bucketAccess"].append("data_reader")
        elif bucket_access_requested == 'w':
            cluster_user_bucket_access_struct["bucketAccess"].append("data_writer")
        elif bucket_access_requested == 'rw':
            cluster_user_bucket_access_struct["bucketAccess"].append("data_writer")
            cluster_user_bucket_access_struct["bucketAccess"].append("data_reader")
        elif bucket_access_requested == 'wr':
            cluster_user_bucket_access_struct["bucketAccess"].append("data_writer")
            cluster_user_bucket_access_struct["bucketAccess"].append("data_reader")
        else:
            print('access not found for ' + bucket_and_access_entry)
            raise UserBucketAccessListError('access not found for ' + bucket_and_access_entry)

        cluster_user_struct["buckets"].append(cluster_user_bucket_access_struct)

    # Check Capella API status
    if capella_api.api_status().status_code == 200:
        capella_api_response = capella_api.create_cluster_user(cmd_line_args.ClusterID, cluster_user_struct)

        if capella_api_response.status_code == 201:
            print("Cluster user is being created")
        else:
            print("Failed to create user")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")


# Need to check that list of buckets
def bucket_access_type(bucket_access_list):
    # We should have a string like this <bucket name>:<bucket access rw, r or w>
    # our regex to check that we've got the right format
    # hate these btw
    regex_for_bucket_and_access = r'(?:^[a-zA-Z0-9.-]+[:]+[rw])'

    # compile the regex as will we could use it several times
    # and it's quicker in those cases to do this.

    compiled_regex = re.compile(regex_for_bucket_and_access)

    # Throw an exception if any entry doesn't meet the regex
    for entry in bucket_access_list.split(','):
        result = compiled_regex.findall(entry.strip())
        if not result:
            raise UserBucketAccessListError(entry + " is not valid.  "
                                                    "must be <bucket name>:<access> where access is r,w or rw.  "
                                                    "* is not permitted for bucket name.  ")

    return (bucket_access_list)


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates a user for a cluster and grants them access to one or more buckets')
    my_parser.ExampleCmdline = """-cid d157a069-9451-4188-a4b1-8be2920db094 -un myuser -pwd Password123! -b 
    "bucket1:rw,bucket2:rw" """

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

    my_parser.add_argument('-b', '--Buckets',
                           dest="Buckets",
                           action='store',
                           metavar="",
                           type=bucket_access_type,
                           required=True,
                           help='List of buckets and access for each.\n  '
                                'Format: <bucket name>:<bucket access>  Bucket access can be r,w or rw. \n'
                                '* is not permitted for a bucket name')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
