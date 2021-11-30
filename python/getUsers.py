# -*- coding: utf-8 -*-
# Generic/Built-in

# Other Libs

# Owned
from capellaAPI.CapellaAPICommon import MyParser
from capellaAPI.CapellaAPICommon import capella_logging
from capellaAPI.CapellaAPICommon import pretty_table
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
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.get_users()

        # Check Capella API status
        if capella_api_response.status_code == 200:
            user_table_rows = []
            list_of_users = capella_api_response.json()['data']

            for user in list_of_users:
                user_table_rows.append([user['name'], user['email'], user['id']])

            # Table heading / rows for the output
            user_table_headings = ['Name', 'Email', 'ID']
            print('Users')
            print(pretty_table(user_table_headings, user_table_rows))
        else:
            print("Failed to get users ")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser

    my_parser = MyParser(description='List users defined in Couchbase Capella')
    my_parser.ExampleCmdline = """With debug on -d \nWith debug off """

    # Add the arguments
    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
