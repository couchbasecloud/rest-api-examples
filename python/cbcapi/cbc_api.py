# -*- coding: utf-8 -*-

# Generic/Built-in
import requests
import json
import os
from requests.structures import CaseInsensitiveDict


# Other Libs



# Owned
from .cbc_api_auth import CbcAPIAuth

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'GPL 3.0'
__version__ = '0.2.1'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'

# Handles talking to the endpoints
# Returns a dictionary with the response and some metadata
# api_response = { responseContent : ' response ' ,
# responseHTTPInfo : { httpStatus : 'http response', httpMessage : 'http message' },
# responseStatus : '' }
#
# responseHTTPInfo allows the caller to take action on the http Status e.g 401 and the http
# message e.g Authentication failed if it wishes to
# responseStatus is set to None if something went wrong and Success if everything is ok



def _cbc_api_get_environ():
    # Get the environmental variables that hold
    # the values we will need
    # Return value, set to None

    api_access_info = None

    api_access_info_values = None


    # Read the values from the environmental variables
    api_access_info_values = {'access_key': os.environ.get('cbc_access_key'),
                       'secret_key': os.environ.get('cbc_secret_key'),
                       'api_base_url': os.environ.get('cbc_base_url')
                       }

    # Check we got all of the values
    # It's a None if the environment variable was not set
    if api_access_info_values['access_key'] is not None:
        if api_access_info_values['secret_key'] is not None:
            if api_access_info_values['api_base_url'] is not None:
                api_access_info = api_access_info_values
            else:
                api_access_info = None
                print('Environmental variable api_base_url is missing or empty')
        else:
            print('Environmental variable secret_key is missing or empty')
    else:
        print('Environmental variable access_key is missing or empty')

    return api_access_info


def cbc_api_get(api_endpoint):
    api_access_values = None

    api_access_values = _cbc_api_get_environ()

    cbc_api_checked_response = None

    if api_access_values is not None:
        cbc_api_get_response = requests.get(api_access_values['api_base_url'] + api_endpoint, auth=CbcAPIAuth(api_access_values['access_key'], api_access_values['secret_key']))

        cbc_api_checked_response = _check_response(cbc_api_get_response)

    return cbc_api_checked_response


def cbc_api_post(api_endpoint, request_body):

    cbc_api_checked_response = None

    api_access_values = _cbc_api_get_environ()

    if api_access_values is not None:
        cbc_api_post_response = requests.post(api_access_values['api_base_url'] + api_endpoint, json=request_body, auth=CbcAPIAuth(api_access_values['access_key'], api_access_values['secret_key']))

        cbc_api_checked_response = _check_response(cbc_api_post_response)

    return cbc_api_checked_response


def cbc_api_del(api_endpoint):

    cbc_api_checked_response = None

    api_access_values = _cbc_api_get_environ()

    if api_access_values is not None:
        cbc_api_del_response = requests.delete(api_access_values['api_base_url'] + api_endpoint, auth=CbcAPIAuth(api_access_values['access_key'], api_access_values['secret_key']))

        cbc_api_checked_response = _check_response(cbc_api_del_response)


    return cbc_api_checked_response


def _check_response(response):
    # responseHTTPInfo allows the caller to take action on the http 
    api_response = {'responseContent': {},
                    'responseHTTPInfo': {
                        'httpStatus': '',
                        'httpMessage': ''
                    },
                    'responseStatus' : ''
                    }

    http_message = ''

    api_response['responseHTTPInfo']['httpStatus'] = response.status_code

    api_response['responseContent'] = None

    # Do we have JSON response ?
    if response.headers['content-type'] == 'application/json':
        # Is there anything in it?
        # We use response.text as this is a string
        # response.content is in bytes which we use for json.loads
        if len(response.text) > 0 :
            api_response['responseContent'] = json.loads(response.content)

    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        http_message = 'Server Error '  + str(response.status_code)
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code))
        http_message = 'URL not found: ' + str(response.status_code)
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        http_message = 'Authentication Failed ' + str(response.status_code)
    elif response.status_code >= 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        http_message = 'Bad Request ' + str(response.status_code)
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected redirect.'.format(response.status_code))
        http_message = 'Unexpected redirect ' + str(response.status_code)
    elif response.status_code == 200:
        http_message = 'Success'
    elif response.status_code == 201:
        # We may have a Location field that indicates where to check
        # the status of the resource
        if response.headers.get('location') is not None:
            http_message = 'Success. Resource status can be checked here:- ' + response.headers.get('location')
        else:
            http_message = 'Success'
    elif response.status_code == 202:
        # We may have a Location field that indicates where to check
        # the status of the resource
        if response.headers.get('location') is not None:
            http_message = 'Success. Resource status can be checked here:- ' + response.headers.get('location')
        else:
            http_message = 'Success'
    elif response.status_code == 204:
        http_message = 'Success'
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        http_message = 'Unexpected Error: ' + str(response.status_code)

    api_response['responseHTTPInfo']['httpMessage'] = http_message

    return api_response

