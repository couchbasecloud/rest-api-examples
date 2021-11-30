# -*- coding: utf-8 -*-
# Generic/Built-in
import base64

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


def main(CmdLineArgs):
    cappella_api = CapellaAPI()

    if CmdLineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    # Check the status of the API, response code = 200 is success
    if cappella_api.api_status().status_code == 200:
        # Work out the bucket ID
        # which is the base64 value of the bucket name
        bucketName_bytes = CmdLineArgs.bucketName.encode('ascii')
        base64_bytes = base64.b64encode(bucketName_bytes)
        bucketName_base64  = base64_bytes.decode('ascii')

        # Get the current cluster buckets
        capella_api_response = cappella_api.get_cluster_buckets(CmdLineArgs.ClusterID)

        # We got the buckets, now check that we have the one we want to update
        if capella_api_response.status_code == 200:
            cluster_buckets = capella_api_response.json()
            found_bucket = False
            for cluster_bucket in cluster_buckets:
                if cluster_bucket['name'] == CmdLineArgs.bucketName:
                    cluster_bucket['memoryQuota'] = CmdLineArgs.MemoryQuota
                    found_bucket = True
                    # Now update the bucket
                    capella_api_response = cappella_api.update_cluster_bucket(CmdLineArgs.ClusterID, bucketName_base64, cluster_bucket)

                    # Did the update work?
                    if capella_api_response.status_code == 202:
                        print("Bucket memory quota is being updated ")
                    else:
                        print("Failed to update bucket ")
                        print("Capella API returned " + str(capella_api_response.status_code))
                        print("Full error message")
                        print(capella_api_response.json()["message"])
            if not found_bucket:
                # We didn't find the bucket to update
                print("Unable to find " + CmdLineArgs.bucketName + " to update on this cluster")

        else:
            print("This cluster cannot be found")
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")

if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Updates the memory quota bucket for a cluster running in your cloud')
    my_parser.ExampleCmdline = """-cid "d157a069-9451-4188-a4b1-8be2920db094" -m 250 -n "my-new-bucket" """

    # Add the arguments

    my_parser.add_argument('-cid', '--ClusterID',
                           dest="ClusterID",
                           metavar="",
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='The ID of the cluster')

    my_parser.add_argument('-n', '--bucketName',
                           dest="bucketName",
                           metavar="",
                           action='store',
                           required=True,
                           type=str,
                           help='The name of the bucket')

    my_parser.add_argument('-m', '--MemoryQuota',
                           dest="MemoryQuota",
                           metavar="",
                           action='store',
                           type=int,
                           required=False,
                           help='Memory to assign for this bucket')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)


