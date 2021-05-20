# -*- coding: utf-8 -*-

# Generic/Built-in
import json
import argparse

# Other Libs


# Owned
from cbcapi.cbc_api import cbc_api_get, cbc_api_post

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.1.2'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Sample'


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

    # This is the configuration of the cluster that will be created
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
        ]
    }

    # Call the API to create the cluster with our configuration
    create_cluster_response = cbc_api_post('/v2/clusters', cluster_configuration)

    # 202 is returned as the call is successful but the resource takes several
    # minutes to create
    if create_cluster_response['responseHTTPInfo']['httpStatus'] == 202:
        # This is the good path, the cluster is being created
        print(create_cluster_response['responseHTTPInfo']['httpMessage'])
    else:
        # Something went wrong.  Print out the messages
        print('Cluster creation failed')

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
    
