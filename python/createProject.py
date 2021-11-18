# -*- coding: utf-8 -*-

# Generic/Built-in
import argparse


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
    cappella_api = CapellaAPI()

    if CmdLineArgs.debug:
        capella_logging('debug')
        cappella_api.set_logging_level('DEBUG')
    else:
        capella_logging('info')

    #Check Capella API status
    if cappella_api.api_status().status_code == 200:
        capella_api_response = cappella_api.create_project(dict(name=CmdLineArgs.projectName))
        if capella_api_response.status_code == 201:
            #Our project was created
            print("Created project " + CmdLineArgs.projectName + " with ID of " + capella_api_response.json()['id'])
        else:
            print("Failed to create project " + CmdLineArgs.project)
            print("Capella API returned " + str(capella_api_response.status_code) )
            print("Full error message")
            print(capella_api_response.json()["message"])

    else:
        print("Check Capella API is up.")



if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = MyParser(description='create a project in Couchbase Capella')
    my_parser.ExampleCmdline = """Create new project:  -n "My new project"\nWith debug on -p "My new project" -d """

    # Add the arguments

    my_parser.add_argument('-n', '--projectName',
                           action='store',
                           required=True,
                           type=str,
                           help='Name of the project to create')

    my_parser.add_argument("-d", "--debug",
                           default=False,
                           action="store_true",
                           help="Turn on logging at debug level")

    args = my_parser.parse_args()

    main(args)

