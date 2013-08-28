###  A logster parser file that can be used to count the number of different
###  messages in an Apache error_log
###
###  For example:
###  sudo ./logster --dry-run --output=ganglia ErrorLogLogster /var/log/httpd/error_log
###
###

import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class SpecjourLogster(LogsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        self.tests = []
        
        # Regular expression for matching lines we are interested in, and capturing
        # fields from the line
        self.reg = re.compile('.* (?P<computer_name>.*) specjour.log.*Finished (?P<test_path>[\./spec|features].*) in (?P<run_time>.*)s')


    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            # Apply regular expression to each line and extract interesting bits.
            regMatch = self.reg.match(line)

            if regMatch:
                linebits = regMatch.groupdict()
                test_path = linebits['test_path'].replace(".","").replace("/spec","spec").replace("/",".").replace(":",".")
                run_time = float(linebits['run_time'])
                graphite_path = "specjour." + linebits['computer_name'] + "." + test_path
                self.tests.append(MetricObject(graphite_path, run_time))

            else:
                raise LogsterParsingException, "regmatch failed to match"

        except Exception, e:
            raise LogsterParsingException, "regmatch or contents failed with %s" % e


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''

        # Return a list of metrics objects
        return self.tests
