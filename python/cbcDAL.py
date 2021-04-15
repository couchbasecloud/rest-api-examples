# -*- coding: utf-8 -*-

# Generic/Built-in


from requests.auth import AuthBase

# Other Libs
import maya



# Owned
from cbcAPI import cbc_api_get, cbc_api_put, cbc_api_del


__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


def list_clouds():

    clouds_api_response = cbc_api_get('/v2/clouds')

    cloud_list = []

    if clouds_api_response['responseStatus'] is not None:
        list_of_clouds = clouds_api_response['responseContent']

        # Did we get a list?
        if list_of_clouds is not None:
            for cloud in list_of_clouds['data']:
                # Builds up a row to display in a table
                # Table is generated by _pretty_table
                # by whomever called this function
                cloud_list.append([cloud['name'],cloud['provider'] , cloud['region'], cloud['id']])

    return(cloud_list)


def get_api_status():

    returned_api_status = None

    status_api_response = cbc_api_get('/v2/status')

    if status_api_response['responseStatus'] is not None:
        returned_api_status = status_api_response['responseHTTPInfo']['httpMessage']

    return returned_api_status





