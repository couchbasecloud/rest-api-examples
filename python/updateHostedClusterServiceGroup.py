# -*- coding: utf-8 -*-

# Generic/Built-in

# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPI import CapellaAPI

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def main(CmdLineArgs):

    new_cluster_configuration = {
        "servers": [
            {
                "compute": "m5.xlarge",
                "size": 3,
                "services": ["data", "index"],
                "storage": {
                    "size": 300,
                    "IOPS": 3000,
                    "type": "IO2"
                },
            }
        ]
    }

    if CmdLineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    cappella_api = CapellaAPI()

    # Create the cluster, pass the configuration
    # and indicate that this cluster will run in the customers own cloud by calling with True
    capella_api_response = cappella_api.create_cluster(True,cluster_configuration)
    capella_api_response = cappella_api.modify_cluster_servers(True, new_cluster_configuration)

    # Check response code , 201 is success
    if capella_api_response.status_code == 202:
        print("Creating cluster ")
        print("Check deployment status here: " + cappella_api.api_base_url + capella_api_response.headers['Location'] + '/status')
    else:
        print("Failed to create cluster " )
        print("Capella API returned " + str(capella_api_response.status_code))
        print("Full error message")
        print(capella_api_response.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Updates the service group for a cluster in Couchbases managed cloud in Couchbase Capella')
    my_parser.ExampleCmdline = """-cn "ANewCluster" -pid "1478c0f4-07b2-4818-a5e8-d15703ef79b0" """

    # Add the arguments

    my_parser.add_argument('-cid', '--ClusterID',
                           action='store',
                           required=True,
                           type=str,
                           help='ID of the cluster to modify service group')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)


