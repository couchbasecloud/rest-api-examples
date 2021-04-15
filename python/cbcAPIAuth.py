# -*- coding: utf-8 -*-

# Generic/Built-in
import base64
import hmac
import hashlib
import datetime

from requests.auth import AuthBase

# Other Libs



# Owned


__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


class CbcAPIAuth(AuthBase):
    """
    Couchbase Cloud API Authentication Handler for Requests.

    """

    def __init__(self, access_key, secret_key ):
        """ Create an authentication handler for Couchbase Cloud APIs
        :param str access_key: access key for Couchbase Cloud
        :param str secret_key: secret key for Couchbase Cloud

        """

        self.access_key = access_key
        self.secret_key = secret_key

    def __call__(self, r):
        # r = request itself


        # Epoch time in milliseconds
        cbc_api_now = str(int(datetime.datetime.now().timestamp() * 1000))

        # This is the endpoint being called
        # Split out from the entire URL
        cbc_api_endpoint = r.url.split(".com",1)[-1]

        # The method being used
        cbc_api_method = r.method

        # You have to use a newline character between each of these , because we copied an AWS example....
        cbc_api_message = cbc_api_method + '\n' + cbc_api_endpoint + '\n' + cbc_api_now

        # This is part of the bearer token used for auth with the API.
        cbc_api_signature = base64.b64encode(hmac.new(bytes(self.secret_key, 'utf-8'), bytes(cbc_api_message, 'utf-8'),
                                                      digestmod=hashlib.sha256).digest())

        # In the header we need to have Authorization and Couchbase-Timestamp.
        # Authorization will use a Bearer token which is the access key with the signature calculated above
        # seperated by a :
        # Couchbase-Timestamp is the epoch time that we used when calculating the signature
        cbc_api_request_headers = {
            'Authorization': 'Bearer ' + self.access_key + ':' + cbc_api_signature.decode(),
            'Couchbase-Timestamp': str(cbc_api_now)
        }

        # Add our key:values to the request header
        r.headers.update( cbc_api_request_headers )



        # Return the request back
        return r
