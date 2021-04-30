# -*- coding: utf-8 -*-

# Generic/Built-in
import json
import argparse

# Other Libs
import texttable as tt

# Owned
from cbcapi.cbc_api import cbc_api_get, cbc_api_post

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.1.1'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Sample'


def _pretty_table(table_heading, table_rows):
    # This creates a formatted table using texttable

    pretty_table = ''

    tab_tt = tt.Texttable(900)

    # Characters used for horizontal & vertical lines
    # You can have different horizontal line for the header if wanted

    tab_tt.set_chars(['-', '|', '-', '-'])

    tab_tt.add_rows([table_heading] + table_rows)

    pretty_table = tab_tt.draw()

    return pretty_table


def get_api_status():
    returned_api_status = None

    status_api_response = cbc_api_get('/v2/status')

    if status_api_response is not None:
        # API got called , check if we got something back
        if status_api_response['responseStatus'] is not None:
            returned_api_status = status_api_response['responseHTTPInfo']['httpMessage']

    return returned_api_status


def post_projects_from_api(project_configuration):
    project_api_response = cbc_api_post('/v2/projects', project_configuration)

    return (project_api_response)


def create_project(project_name):
    project_configuration = { "name": project_name }

    create_project_response = post_projects_from_api(project_configuration)

    print(create_project_response['responseHTTPInfo']['httpMessage'])
    print(create_project_response['responseHTTPInfo']['httpStatus'])

    return


def main(cmdline_args):
    if get_api_status() == 'Success':
        create_project(cmdline_args.projectName)
    else:
        print('Whoops something has gone wrong')


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = argparse.ArgumentParser(description='create a cluster in Couchbase Cloud')

    # Add the arguments
    my_parser.add_argument('-pn', '--projectName',
                           action='store',
                           required=True,
                           help='Name for the project')
    args = my_parser.parse_args()

    main(args)
