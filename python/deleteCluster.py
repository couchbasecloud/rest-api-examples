
# -*- coding: utf-8 -*-

# Generic/Built-in
import json
import argparse

# Other Libs
import texttable as tt

# Owned
from cbcapi.cbc_api import cbc_api_del, cbc_api_get

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.1.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def get_api_status():

    returned_api_status = None

    status_api_response = cbc_api_get('/v2/status')

    if status_api_response is not None:
        # API got called , check if we got something back
        if status_api_response['responseStatus'] is not None:
            returned_api_status = status_api_response['responseHTTPInfo']['httpMessage']

    return returned_api_status


def delete_cluster_from_api(cluster_id):

    cluster_api_response = cbc_api_del('/v2/clusters/' + cluster_id )

    return (cluster_api_response)


def delete_cluster(id):
    # Deletes the cluster identified by id

    delete_cluster_response = delete_cluster_from_api(id)


    if delete_cluster_response['responseHTTPInfo']['httpStatus'] == 202:
        # This is the good path, the cluster has been deleted
        print('Cluster is being deleted')
        print(delete_cluster_response['responseHTTPInfo']['httpMessage'])
    elif delete_cluster_response['responseHTTPInfo']['httpStatus'] == 404:
        # Something went wrong.  Print out the messages
        print('Could not locate the cluster')
        print('Check the Cluster ID')
    else:
        # An error occurred
        print('Whoops something has gone wrong')
        print(delete_cluster_response['responseContent']['message'])

    return


def main(cmdline_args):
    if get_api_status() == 'Success':
        delete_cluster(cmdline_args.clusterID)
    else:
        print('Whoops something has gone wrong')


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = argparse.ArgumentParser(description='delete a cluster in Couchbase Cloud')

    # Add the arguments

    my_parser.add_argument('-cid', '--clusterID',
                           action='store',
                           required=True,
                           help='ID of the cluster to delete')

    args = my_parser.parse_args()

    main(args)
