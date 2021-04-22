# -*- coding: utf-8 -*-

# Generic/Built-in
import json
import argparse

# Other Libs

# Owned
from cbcapi.cbc_api import cbc_api_get

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'GPL 2.0'
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


def get_cluster_from_api(cluster_id):
    cluster_api_response = cbc_api_get('/v2/clusters/' + cluster_id )

    return (cluster_api_response)


def check_cluster( cluster_id):

    check_cluster_response = get_cluster_from_api(cluster_id)

    if check_cluster_response['responseHTTPInfo']['httpStatus'] == 200:
        # This is the good path, the cluster has been found
        print('Cluster information found')
        print(json.dumps(check_cluster_response['responseContent'], indent=2))
    else:
        # Something went wrong.  Print out the messages
        print('Could not get the Cluster information')
        print('Check the Cluster ID')
        print(check_cluster_response['responseContent']['message'])

    return


def main(cmdline_args):
    if get_api_status() == 'Success':
        check_cluster(cmdline_args.clusterID )
    else:
        print('Whoops something has gone wrong')


if __name__ == '__main__':
    # Process command line args
    # Create the parser
    my_parser = argparse.ArgumentParser(description='create a cluster in Couchbase Cloud')

    # Add the arguments

    my_parser.add_argument('-cid', '--clusterID',
                           action='store',
                           required=True,
                           help='ID of the cluster to check')

    args = my_parser.parse_args()

    main(args)
