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


def post_clusters_from_api(cluster_configuration):
    cluster_api_response = cbc_api_post('/v2/clusters', cluster_configuration)

    return (cluster_api_response)


def create_cluster(cloud_id, project_id, cluster_name):
    cluster_configuration = {
        "cloudId": cloud_id,
        "name": cluster_name,
        "projectId": project_id,
        "servers": [
            {
                "services": [
                    "data"
                ],
                "size": 3,
                "aws": {
                    "ebsSizeGib": 128,
                    "instanceSize": "m5.xlarge"
                }
            }
        ],
        "version": ""
    }

    create_cluster_response = cbc_api_post('/v2/clusters', cluster_configuration)

    if create_cluster_response['responseHTTPInfo']['httpStatus'] == 201:
        # This is the good path, the cluster is being created
        print(create_cluster_response['responseHTTPInfo']['httpMessage'])
    else:
        # Something went wrong.  Print out the messages
        print('Cluster creation failed')
        print(create_cluster_response['responseContent']['message'])

    return


def main(cmdline_args):
    if get_api_status() == 'Success':
        create_cluster(cmdline_args.cloudID,cmdline_args.projectID,cmdline_args.clusterName)
    else:
        print('Whoops something has gone wrong')


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = argparse.ArgumentParser(description='create a cluster in Couchbase Cloud')

    # Add the arguments

    my_parser.add_argument('-cid', '--cloudID',
                           action='store',
                           required=True,
                           help='ID of the Cloud connection to use with the cluster')

    my_parser.add_argument('-pid', '--projectID',
                           action='store',
                           required=True,
                           help='ID of the Project to use with the cluster')

    my_parser.add_argument('-cn', '--clusterName',
                           action='store',
                           required=True,
                           help='Name for the cluster')
    args = my_parser.parse_args()

    main(args)
