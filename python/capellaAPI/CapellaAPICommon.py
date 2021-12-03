# -*- coding: utf-8 -*-
# Generic/Built-in
import logging
import argparse
import sys

# Other
import texttable as tt
import re


# Owned
from .CapellaExceptions import *

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.0'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'

# Several class / functions that are used in a number of places


class MyParser(argparse.ArgumentParser):
    def __init__(self, description):
        super().__init__()
        self._log = logging.getLogger(__name__)
        self.description = description
        self.example_cmdline = ""

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        print("Example usage")
        print(self.ExampleCmdline)
        sys.exit(2)


def capella_logging(CappellaLogLevel):

    if CappellaLogLevel == "debug":
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.debug("logging is on at DEBUG level")
    else:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.debug("logging is on at INFO level")

    # Stop noisy urllib3 info logs
    logging.getLogger("requests").setLevel(logging.WARNING)


def pretty_table(table_heading, table_rows):
    # This creates a formatted table using texttable

    pretty_table = ''

    tab_tt = tt.Texttable(900)

    # Characters used for horizontal & vertical lines
    # You can have different horizontal line for the header if wanted

    tab_tt.set_chars(['-', '|', '-', '-'])

    tab_tt.add_rows([table_heading] + table_rows)

    pretty_table = tab_tt.draw()

    return pretty_table


def check_if_valid_uuid(uuid):
    # Need to check if a valid uuid is given

    regex_for_uuid = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'

    # compile the regex
    compiled_regex = re.compile(regex_for_uuid)

    # Throw an exception if any entry doesn't meet the regex
    result = compiled_regex.findall(uuid.strip())

    # if result = false, then it didn't meet the requirement
    # throw our custom exception

    if not result:
        raise InvalidUuidError(uuid + " does not match the format for an unique identifier.")
    else:
        return (uuid)

# Need to check bucket and scopes are valid
def check_bucket_and_scope_type(bucket_and_scope_access_list):
    # We should have a string like this <bucket name>:<bucket access rw, r or w>
    # our regex to check that we've got the right format
    # hate these btw
    # CB Server 7x supports more characters for bucket names compared to CB 6x
    regex_for_bucket_and_scope_access = r'(^[a-zA-Z0-9-._%]+[:]+[a-zA-Z0-9_* ]+[:]+[rw])'

    # compile the regex as will we could use it several times
    # and it's quicker in those cases to do this.

    compiled_regex = re.compile(regex_for_bucket_and_scope_access)

    # Throw an exception if any entry doesn't meet the regex
    for entry in bucket_and_scope_access_list.split(','):
        result = compiled_regex.findall(entry.strip())
        if not result:
            raise UserBucketAccessListError(entry + " is not valid.  "
                                                    "must be <bucket name>:<scope>:<access> where access is r,w or rw.  "
                                                    "* is not permitted for bucket name.  ")

    return (bucket_and_scope_access_list)


