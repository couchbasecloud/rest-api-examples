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
            "replicas": cmd_line_args.replicas,
            "name": cmd_line_args.name,
            "memoryQuota": cmd_line_args.memory_quota
        }

    # Create the bucket
    capella_api_response = cappella_api.create_cluster_bucket(cmd_line_args.cluster_id, bucket_configuration)

    # Check response code , 201 is success
    if capella_api_response.status_code == 201:
        print("Creating bucket ")
    else:
        print("Failed to create bucket ")
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates a bucket for a cluster using '
                                     'Couchbases own cloud in Couchbase Capella')
    my_parser.ExampleCmdline = "-cid d157a069-9451-4188-a4b1-8be2920db094 -n mynewbucket -r 0 -m 250 "

    # Add the arguments

    my_parser.add_argument('-cid', '--clusterID',
                           dest="cluster_id",
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='The ID of the cluster')

    my_parser.add_argument('-n', '--Name',
                           dest="name",
                           action='store',
                           required=True,
                           type=str,
                           help='The name of the bucket')

    my_parser.add_argument('-r', '--Replicas',
                           dest="replicas",
                           action='store',
                           type=int,
                           required=True,
                           help='The number of replicas')

    my_parser.add_argument('-m', '--MemoryQuota',
                           dest="memory_quota",
                           action='store',
                           type=int,
                           required=True,
                           help='Memory to assign for this bucket')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
