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


def main(cmd_line_args):
    cappella_api = CapellaAPI()

    if cmd_line_args.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    cluster_allowlist_configuration = {
        "cidrBlock": cmd_line_args.CidrBlock,
        "ruleType": cmd_line_args.RuleType.lower(),

    }

    if cmd_line_args.RuleType.lower() == 'temporary':
        cluster_allowlist_configuration["duration"] = str(cmd_line_args.Duration) + "h0m0s"

    if cmd_line_args.RuleType.lower() == 'permanent':
        # If rule is permanent , Duration should not be given
        # Will look into seeing if arg parser can deal with this
        # For now, the check is here
        if cmd_line_args.Duration is not None:
            raise AllowlistRuleError("Duration is not a permitted option for allow list when type is permanent")


    if cmd_line_args.Comment is not None:
        cluster_allowlist_configuration["comment"] = cmd_line_args.Comment

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.create_cluster_allowlist(cmd_line_args.ClusterID,
                                                                     cluster_allowlist_configuration)

        if capella_api_response.status_code == 202:
            print("Allow list is being created")
        else:
            print("Failed to create allowlist ")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])
    else:
        print("Check Capella API is up.")


def allow_list_rule_type(rule_type):
    if rule_type.lower() == 'temporary':
        return (rule_type.lower())
    elif rule_type.lower() == 'permanent':
        return (rule_type.lower())
    else:
        raise AllowlistRuleError(rule_type + " is not a permitted option for allow list rule type")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Creates an allow list entry for a cluster running in your cloud')
    my_parser.ExampleCmdline = "-cid 1478c0f4-07b2-4818-a5e8-d15703ef79b0 -cb 10.0.0.1 " \
                               "-rt \"temporary\" -dt 1 -ct \"1 hour access\"  "

    # Add the arguments
    my_parser.add_argument("-cid", "--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster ")

    my_parser.add_argument('-cb ', '--CidrBlock',
                           dest="CidrBlock",
                           metavar="",
                           action='store',
                           required=True,
                           type=str,
                           help='Allow list cidr block e.g 10.0.0.1 or IP address e.g 192.168.2.14')

    my_parser.add_argument('-rt', '--RuleType',
                           dest="RuleType",
                           metavar="",
                           action='store',
                           type=allow_list_rule_type,
                           required=True,
                           help='temporary or permanent')

    my_parser.add_argument('-dt', '--Duration',
                           dest="Duration",
                           metavar="",
                           action='store',
                           type=int,
                           required=False,
                           help='if temporary, how long in hours.')

    my_parser.add_argument('-ct', '--Comment',
                           dest="Comment",
                           metavar="",
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
