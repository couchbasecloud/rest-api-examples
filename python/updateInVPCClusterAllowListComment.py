# -*- coding: utf-8 -*-
# Generic/Built-in

# Other Libs


# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import check_if_valid_uuid
from capellaAPI.CapellaAPI import CapellaAPI
from capellaAPI.CapellaExceptions import AllowlistRuleError

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'



def main(CmdLineArgs):
    cappella_api = CapellaAPI()

    if CmdLineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    # Caution :  The endpoint treats the allow list as a single resource
    #            This means the new, updated, configuration will replace what is already there
    #            We will get the current allow list, alter the allow list entry that we're changing
    #            and then send everything back.  The change just being the comment key : value
    #            If we didn't do this, we'd end up with a cluster with just the allow list entry we're updating...

    # Step 1 - get the allow list with all of its entries
    if cappella_api.api_status().status_code == 200:
        cluster_allowlist_from_API = cappella_api.get_cluster_allowlist(CmdLineArgs.ClusterID)

        # Check response code , 200 is success
        if cluster_allowlist_from_API.status_code == 200:

            # Did we actually get any entries in the allow list?
            if cluster_allowlist_from_API.json() is not None:
                # Yep, we did.
                # Step 2 - Find the allow list entry that we want to update. cidr is unique, so we can search on that
                allow_list_entry_found = False
                allow_list_entries = cluster_allowlist_from_API.json()
                for allow_list in allow_list_entries:
                    # The allow list cidr has /xx and we only need the first bit
                    # so we split it apart on the / and use the first entry in the resulting list
                    # which has an index of zero
                    if allow_list['cidrBlock'].split('/')[0] == CmdLineArgs.cidrBlock:
                        allow_list_entry_found = True

                        # There should always be a value for comment, but just in case
                        if CmdLineArgs.Comment is not None:
                            allow_list["Comment"] = CmdLineArgs.Comment

                        # We can now update the allow list entry
                        capella_api_response = cappella_api.update_cluster_allowlist(CmdLineArgs.ClusterID, allow_list_entries)

                        # Did the update work?
                        if capella_api_response.status_code == 202:
                            print("Updating allow list ")
                        else:
                            print("Failed to update allow list ")
                            print("Capella API returned " + str(capella_api_response.status_code))
                            print("Full error message")
                            print(capella_api_response.json()["message"])

                if not allow_list_entry_found:
                    print("Unable to find " + CmdLineArgs.Name + " for this cluster")
        else:
            print("Failed to find cluster for the allow list ")
            print("Capella API returned " + str(cluster_allowlist_from_API.status_code))
            print("Full error message")
            print(cluster_allowlist_from_API.json()["message"])


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Updates the comment for an allow list entry')
    my_parser.ExampleCmdline = """Change comment of an allow list entry with a cidr of 10.2.1.0\n-cid d157a069-9451-4188-a4b1-8be2920db094 -cidr 10.2.1.0 -ct "New comment" """

    # Add the arguments

    my_parser.add_argument("-cid","--ClusterID",
                           dest="ClusterID",
                           action='store',
                           required=True,
                           metavar="",
                           type=check_if_valid_uuid,
                           help="The ID of the cluster " )

    my_parser.add_argument('-cb', '--cidrBlock',
                           dest="cidrBlock",
                           metavar="",
                           action='store',
                           type=str,
                           required=True,
                           help='The cidrBlock of the allow list entry to update')

    my_parser.add_argument('-ct', '--Comment',
                           dest="Comment",
                           metavar="",
                           action='store',
                           type=str,
                           required=True,
                           help='Comment for the allow list entry')


    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)


