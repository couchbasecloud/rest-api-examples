# -*- coding: utf-8 -*-
# Generic/Built-in

# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import pretty_table
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

    capella_api_response = cappella_api.get_cluster_users(False, cmd_line_args.ClusterID)

    # Check response code , 200 is success
    if capella_api_response.status_code == 200:
        cluster_user_table_rows = []
        cluster_users = capella_api_response.json()

        # We should have a list of users, but just in case, check
        # Then we will build rows to show in a table
        if cluster_users is not None:
            # Check to see if we got any users back
            if len(cluster_users) > 0:
                ClusterUserTableHeading = ['Name', 'Bucket', 'Access']
                for cluster_user in cluster_users:
                    user_name = cluster_user['username']
                    # We use this to determine if the user has access to more than one bucket
                    # to help with formatting the table
                    first_entry = True
                    for cluster_user_access in cluster_user['access']:
                        bucket_name = cluster_user_access['bucketName']
                        if bucket_name == '*':
                            bucket_name = 'All'
                        # Do they have read & write ?
                        if (len(cluster_user_access['bucketAccess'])) == 2:
                            bucket_access = cluster_user_access['bucketAccess'][0] + ' ' + \
                                            cluster_user_access['bucketAccess'][1]
                        else:
                            bucket_access = cluster_user_access['bucketAccess'][0]
                        # If it's the first entry, then we include the user name
                        # Otherwise we leave that out so the table looks ok
                        if first_entry:
                            cluster_user_table_rows.append([user_name, bucket_name, bucket_access])
                            first_entry = False
                        else:
                            cluster_user_table_rows.append(['', bucket_name, bucket_access])

                # Display the table, which uses pretty table to make things easier
                print('Cluster users')
                print(pretty_table(ClusterUserTableHeading, cluster_user_table_rows))

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
    my_parser = MyParser(description='Get list of users for a cluster running in your cloud')
    my_parser.ExampleCmdline = "-cid 1478c0f4-07b2-4818-a5e8-d15703ef79b0"

    # Add the arguments
    my_parser.add_argument("-cid", "--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster ")

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
