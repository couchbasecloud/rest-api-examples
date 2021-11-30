# -*- coding: utf-8 -*-
# Generic/Built-in


# Other Libs
import maya

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

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.get_projects()

        # Check response code , 200 is success
        if capella_api_response.status_code == 200:
            project_table_rows = []
            list_of_projects = capella_api_response.json()

            for project in list_of_projects['data']:
                project_table_rows.append([project['name'], maya.parse(project['createdAt']),
                                           project['id']])

            # Table heading / rows for the output
            project_table_headings = ['Name', 'Created at', 'ID']

            print('Projects')
            print(pretty_table(project_table_headings, project_table_rows))

        else:
            print("Failed to get projects ")
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser

    my_parser = MyParser(description='List projects defined in Couchbase Capella')
    my_parser.ExampleCmdline = "With debug on -d \nWith debug off "

    # Add the arguments
    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
