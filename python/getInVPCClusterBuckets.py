# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import maya

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

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.get_cluster_buckets(cmd_line_args.ClusterID)

        # Check response code , 200 is success
        if capella_api_response.status_code == 200:
            bucket_table_rows = []
            list_of_buckets = capella_api_response.json()

            # We should have a list of buckets, but just in case, check
            # Then we will build rows to show in a table
            if list_of_buckets is not None:
                # Check to see if we got any buckets back
                if len(list_of_buckets) > 0:
                    for bucket in list_of_buckets:
                        bucket_table_rows.append(bucket.values())

                    print('Buckets')
                    print(pretty_table(list_of_buckets[0].keys(), bucket_table_rows))
                else:
                    print("No buckets found")
            else:
                print("No buckets found")

        else:
            print("Failed to get buckets ")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Get buckets for a cluster running in your cloud')
    my_parser.ExampleCmdline = """-cid "1478c0f4-07b2-4818-a5e8-d15703ef79b0" """

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
