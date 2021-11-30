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

    # Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.delete_project(cmd_line_args.projectID)
        if capella_api_response.status_code == 204:
            # Our project was created
            print("Deleted project with ID " + cmd_line_args.projectID)
        else:
            print("Failed to delete project with ID " + cmd_line_args.projectID)
            print("Capella API returned " + str(capella_api_response.status_code))
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='Deletes a project from Couchbase Capella')
    my_parser.ExampleCmdline = '-pid e50323f2-2c1c-4506-8234-504d5332f400 \n ' \
                               'With debug  -pid e50323f2-2c1c-4506-8234-504d5332f400 -d'

    # Add the arguments

    my_parser.add_argument('-pid', '--projectID',
                           dest="projectID",
                           metavar="",
                           action='store',
                           required=True,
                           type=check_if_valid_uuid,
                           help='ID of the project to delete.  Must be a valid unique identifier.')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)
