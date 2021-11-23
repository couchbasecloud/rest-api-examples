# -*- coding: utf-8 -*-

# Generic/Built-in
import json
import requests
import os
import logging
import pprint


# Other Libs


# Owned
from capellaAPI.CapellaAPIAuth import CapellaAPIAuth
from capellaAPI.CapellaExceptions import MissingBaseURLError, MissingAccessKeyError, MissingSecretKeyError

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
__version__ = '0.3.1'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'

# Handles talking to the endpoints over http 
# Returns the response
# Assumes that the caller deals with the response


class CapellaAPIRequests():

    def __init__(self):
        """ handles http requests - GET , PUT, POST, DELETE
        to the Couchbase Cloud APIs

        """
        # Read the values from the environmental variables

        if os.environ.get('api_base_url') is None:
            raise MissingBaseURLError('Environmental variable api_base_url has not been set')
        else:
            self.api_base_url = os.environ.get('api_base_url')


        self._log = logging.getLogger(__name__)

        # We will re-use the first session we setup to avoid
        # the overhead of creating new sessions for each request
        self.network_session = requests.Session()

    def set_logging_level(self, level):
        self._log.setLevel(level)



    # Methods
    def capella_api_get(self,api_endpoint):
        cbc_api_response = None

        self._log.info(api_endpoint)

        try:
            cbc_api_response = self.network_session.get(self.api_base_url + api_endpoint, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError as e:
            error = pprint.pformat(cbc_api_response.json())
            raise CbcAPIError(error)

        except MissingAccessKeyError:
            self._log.debug(f"Missing Access Key environment variable")
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            self._log.debug(f"Missing Access Key environment variable")
            print("Missing Access Key environment variable")

        return (cbc_api_response)




    def capella_api_post(self, api_endpoint, request_body):
        cbc_api_response = None

        self._log.info(api_endpoint)

        try:
            cbc_api_response = self.network_session.post(self.api_base_url + api_endpoint, json=request_body, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError as e:
            error = pprint.pformat(cbc_api_response.json())
            raise CbcAPIError(error)

        except MissingAccessKeyError:
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            print("Missing Access Key environment variable")

        return (cbc_api_response)


    def capella_api_put(self, api_endpoint, request_body):
        cbc_api_response = None

        self._log.info(api_endpoint)

        try:
            cbc_api_response = self.network_session.put(self.api_base_url + api_endpoint, json=request_body, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError as e:
            error = pprint.pformat(cbc_api_response.json())
            raise CbcAPIError(error)

        except MissingAccessKeyError:
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            print("Missing Access Key environment variable")

        return (cbc_api_response)


    def capella_api_del(self, api_endpoint, request_body = None ):
        cbc_api_response = None

        self._log.info(api_endpoint)

        try:
            if request_body is None:
                cbc_api_response = self.network_session.delete(self.api_base_url + api_endpoint, auth=CapellaAPIAuth())
            else:
                cbc_api_response = self.network_session.delete(self.api_base_url + api_endpoint, json=request_body, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError as e:
            error = pprint.pformat(cbc_api_response.json())
            raise CbcAPIError(error)

        except MissingAccessKeyError:
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            print("Missing Access Key environment variable")

        return (cbc_api_response)

def main():
    capella_request_test = CapellaAPIRequests()

    api_response = capella_request_test.capella_api_get('/v2/status')

    print(json.dumps(api_response.json(), indent=3))


if __name__ == '__main__':
        main()