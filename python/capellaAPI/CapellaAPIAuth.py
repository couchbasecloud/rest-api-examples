# -*- coding: utf-8 -*-
# Generic/Built-in
import base64
import hmac
import hashlib
import datetime
import os
from requests.auth import AuthBase

# Other Libs

# Owned
from .CapellaExceptions import *

# EnvVars.py sets the environmental variables used here
# If EnvVars.py does not exist, then we'll try the OS environment variables instead
try:
    import capellaAPI.EnvVars
except ImportError:
    pass

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.1.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


class CapellaAPIAuth(AuthBase):
    # Extends requests AuthBase for
    # Couchbase Cloud API Authentication Handler.

    def __init__(self):
        # Create an authentication handler for Couchbase Cloud APIs
        # :param str access_key: access key for Couchbase Cloud
        # :param str secret_key: secret key for Couchbase Cloud

        # Read the values from the environmental variables
        if os.environ.get('CBC_ACCESS_KEY') is None:
            raise MissingAccessKeyError
        else:
            self.ACCESS_KEY = os.environ.get('CBC_ACCESS_KEY')

        if os.environ.get('CBC_SECRET_KEY') is None:
            raise MissingSecretKeyError
        else:
            self.SECRET_KEY = os.environ.get('CBC_SECRET_KEY')

    def __call__(self, r):
        # r = request itself

        # Epoch time in milliseconds
        cbc_api_now = str(int(datetime.datetime.now().timestamp() * 1000))

        # This is the endpoint being called
        # Split out from the entire URL
        cbc_api_endpoint = r.url.split(".com", 1)[-1]

        # The method being used
        cbc_api_method = r.method

        # You have to use a newline character between each of these , because we copied an AWS example....
        cbc_api_message = cbc_api_method + '\n' + cbc_api_endpoint + '\n' + cbc_api_now

        # This is part of the bearer token used for auth with the API.
        cbc_api_signature = base64.b64encode(hmac.new(bytes(self.SECRET_KEY, 'utf-8'), bytes(cbc_api_message, 'utf-8'),
                                                      digestmod=hashlib.sha256).digest())

        # In the header we need to have Authorization and Couchbase-Timestamp.
        # Authorization will use a Bearer token which is the access key with the signature calculated above
        # seperated by a :
        # Couchbase-Timestamp is the epoch time that we used when calculating the signature
        cbc_api_request_headers = {
            'Authorization': 'Bearer ' + self.ACCESS_KEY + ':' + cbc_api_signature.decode(),
            'Couchbase-Timestamp': str(cbc_api_now)
        }

        # Add our key:values to the request header
        r.headers.update(cbc_api_request_headers)

        # Return the request back
        return r
