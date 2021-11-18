# -*- coding: utf-8 -*-

# Generic/Built-in

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
    """Base class for other exceptions"""
    def __init__(self):
        super().__init__()

    pass


class MissingAccessKeyError(CbcAPIError):
    def __init__(self, message_to_display):
        print(message_to_display)

        super(MissingAccessKeyError, self).__init__(message_to_display)

    pass


class MissingSecretKeyError(CbcAPIError):
    def __init__(self, message_to_display):
        print(message_to_display)

        super(MissingSecretKeyError, self).__init__(message_to_display)

    pass


class MissingBaseURLError(CbcAPIError):
    def __init__(self, message_to_display):
        print(message_to_display)

        super(MissingBaseURLError, self).__init__(message_to_display)

    pass


class AllowlistRuleError(CbcAPIError):
    def __init__(self, message_to_display):
        print(message_to_display)

        super(AllowlistRuleError, self).__init__(message_to_display)

    pass


class UserBucketAccessListError(CbcAPIError):
    """Raised when invalid list of buckets & access is given for a cluster user"""
    def __init__(self, message_to_display):
        print(message_to_display)

        super(UserBucketAccessListError, self).__init__(message_to_display)

    pass

class InvalidUuidError(CbcAPIError):
    """Raised when an invalid uuid is given"""
    def __init__(self, message_to_display):
        print(message_to_display)

        super(InvalidUuidError, self).__init__(message_to_display)

    pass
