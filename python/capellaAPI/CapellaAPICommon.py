# -*- coding: utf-8 -*-

# Generic/Built-in
import logging
import argparse
import sys

#Other
import texttable as tt
import re

#Owned
from capellaAPI.CapellaExceptions import InvalidUuidError


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

    if CappellaLogLevel == "debug" :
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
        logging.debug("logging is on at DEBUG level")
    else:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
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

    # compile the regex as will we could use it several times
    # and it's quicker in those cases to do this.

    compiled_regex = re.compile(regex_for_uuid)

    # Throw an exception if any entry doesn't meet the regex
    result = compiled_regex.findall(uuid.strip())

    # if result = false, then it didn't meet the requirement
    # throw our custom exception

    if not result:
        raise InvalidUuidError(uuid + " does not match the format for an unique identifier.  ")
    else:
        return (uuid)

def main():
    pass


if __name__ == '__main__':
        main()

