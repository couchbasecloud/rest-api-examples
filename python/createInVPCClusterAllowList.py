# -*- coding: utf-8 -*-

# Generic/Built-in

# Other Libs

# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaExceptions import AllowlistRuleError
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



def main(CmdlineArgs):
    cappella_api = CapellaAPI()

    if CmdlineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    cluster_allowlist_configuration ={
        "cidrBlock": CmdlineArgs.CidrBlock,
        "ruleType": CmdlineArgs.RuleType,

    }

    if CmdlineArgs.RuleType == 'temporary':
        cluster_allowlist_configuration["duration"] = str(CmdlineArgs.Duration) + "h0m0s"

    if CmdlineArgs.Comment is not None:
        cluster_allowlist_configuration["comment"] = CmdlineArgs.Comment

    #Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.create_cluster_allowlist(CmdlineArgs.ClusterID, cluster_allowlist_configuration)

        if capella_api_response.status_code == 202:
            print("Allow list is being created")
        else:
            print("Failed to create allowlist " )
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")


def allow_list_rule_type(rule_type):

    #new_allow_list_rule_error = AllowlistRuleError()

    if rule_type == 'temporary':
        return(rule_type)
    elif rule_type == 'permanent':
        return (rule_type)
    else:
        raise AllowlistRuleError(rule_type +  " is not a permitted option for allow list rule type")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates an allow list entry for a cluster running in your cloud')
    my_parser.ExampleCmdline = """-cid 1478c0f4-07b2-4818-a5e8-d15703ef79b0 -cb 10.0.0.1 -rt "temporary" -dt 1 -ct "1 hour access"  """

    # Add the arguments
    my_parser.add_argument("-cid", "--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster ")

    my_parser.add_argument('-cb ', '--CidrBlock',
                           action='store',
                           required=True,
                           type=str,
                           help='Allowlist cidr block e.g 10.0.0.1 or IP address e.g 192.168.2.14')

    my_parser.add_argument('-rt', '--RuleType',
                           action='store',
                           type=allow_list_rule_type,
                           required=True,
                           help='temporary or permanent')

    my_parser.add_argument('-dt', '--Duration',
                           action='store',
                           type=int,
                           default=1,
                           required=False,
                           help='if temporary, how long in hours. Default = 1')

    my_parser.add_argument('-ct', '--Comment',
                           action='store',
                           required=False,
                           type=str,
                           help='Any description for this entry')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")


    args = my_parser.parse_args()

    main(args)