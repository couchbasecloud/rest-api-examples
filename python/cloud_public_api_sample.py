
# -*- coding: utf-8 -*-

# Generic/Built-in

# Other Libs
from cbcDAL import list_clouds, get_api_status

import texttable as tt

# Owned
from cbcDAL import list_clouds

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


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


def ListClouds():
    # Lists all clouds showing the name, provider, creation date and ID

    # Get a list of clouds
    # which will be used as rows in the output table

    cloud_table_rows = list_clouds()
    if len(cloud_table_rows) > 0:
        # We got data back
        # Table heading / rows for the output
        cloud_table_headings = ['Name','Provider','Region', 'ID']

        print('Cloud')
        print( _pretty_table(cloud_table_headings,cloud_table_rows))
    else:
        # We didn't get anything back
        print('Whoops something has gone wrong')
        print('Check environmental variables')


    return


def main():
    if get_api_status() == 'Success':
        ListClouds()
    else:
        print('Whoops something has gone wrong')

if __name__ == '__main__':
        main()


