# -*- coding: utf-8 -*-
# Generic/Built-in
import sys
import inspect

# Other Libs


# Owned


__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.1'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'


# Extends exception handling so we can
# customise the messaging

class CbcAPIError(Exception):
    #Base class for our custom exceptions
    #Stops the traceback information being shown
    def __init__(self, msg):
        try:
            ln = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            ln = inspect.currentframe().f_back.f_lineno
        self.args = "{0.__name__} : {1}".format(type(self), msg),
        sys.exit(self)


class MissingAccessKeyError(CbcAPIError):
    # Raised when there is a problem with the environmental variable that defines the access key for the Public API
    pass


class MissingSecretKeyError(CbcAPIError):
    # Raised when there is a problem with the environmental variable that defines the secret key for the Public API
    pass


class MissingBaseURLError(CbcAPIError):
    #Raised when there is a problem with the environmental variable that defines the URL for the Public API
    pass


class AllowlistRuleError(CbcAPIError):
    #Allow list is wrong
    pass


class UserBucketAccessListError(CbcAPIError):
    #Raised when invalid list of buckets & access is given for a cluster user
    pass


class InvalidUuidError(CbcAPIError):
    #Raised when an invalid uuid is given
    pass

class GenericHTTPError(CbcAPIError):
    # Raised for generic http errors resulting
    # from calling the API
    pass
