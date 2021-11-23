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


def main(CmdLineArgs):
    cappella_api = CapellaAPI()

    if CmdLineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    # Caution :  The endpoint treats the clusters buckets as a single resource
    #            This means the new, updated, configuration will replace what is already there
    #            We will get the current buckets, alter the bucket that we're changing
    #            and then send everything back.
    #            If we didn't do this, we'd end up with a cluster with just the bucket we're updating...

    # Step 1 - get the clusters current buckets
    if cappella_api.api_status().status_code == 200:
        cluster_buckets_from_API = cappella_api.get_cluster_buckets(CmdLineArgs.ClusterID)

        # Check response code , 200 is success
        if cluster_buckets_from_API.status_code == 200:
            # Did we actually get any buckets?
            if cluster_buckets_from_API.json() is not None:
                # Yep, we did.
                # Step 2 - Find the bucket that we want to update. Buckets have unique names, so we can search on that
                bucket_found = False
                cluster_buckets = cluster_buckets_from_API.json()
                for cluster_bucket in cluster_buckets:
                    if cluster_bucket['name'] == CmdLineArgs.Name:
                        bucket_found = True
                        # Check which bucket configuration parameters are present
                        # If they are not present, then we leave the current value in place
                        if CmdLineArgs.MemoryQuota is not None:
                            cluster_bucket["memoryQuota"] = CmdLineArgs.MemoryQuota

                        # We can now update the clusters buckets
                        capella_api_response = cappella_api.update_cluster_bucket(CmdLineArgs.ClusterID, cluster_buckets)

                        # Did the update work?
                        if capella_api_response.status_code == 201:
                            print("Updating bucket ")
                        else:
                            print("Failed to update bucket ")
                            print("Capella API returned " + str(capella_api_response.status_code))
                            print("Full error message")
                            print(capella_api_response.json()["message"])

                if not bucket_found:
                    print("Unable to find " + CmdLineArgs.Name + " for this cluster")


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

    my_parser.add_argument('-n', '--Name',
                           dest="Name",
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


