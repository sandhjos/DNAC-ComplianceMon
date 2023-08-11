#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: showrunsection.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
####################################################################################

# This program is written to ingest all the XML files exported from Prime and build
# A dictionary of auditing rules to be used to check configurations

#     ------------------------------- IMPORTS -------------------------------

import re
import sys

#     ----------------------------- DEFINITIONS -----------------------------

# This function pulls relevant configuration sections
def show_run_section(lines, pattern):
    try:
        pattern = re.compile(pattern)
    except ValueError:
        print("Error: Search Parameter {} not found in configuration file".format(pattern))
        exit(1)
    # Find all the lines that match the pattern
    matching_lines = []
    found_section = False
    for line in lines:
        if re.search(pattern, line):
            found_section = True
            matching_lines.append(line)
        elif found_section and line.startswith(' '):
            matching_lines.append(line)
        elif found_section and line.startswith('!'):
            matching_lines.append(line)
            found_section = False
        else:
            found_section = False
    return matching_lines

#     ----------------------------- MAIN -----------------------------
# For testing purposes use the following but comment out and include the same 
# calls in the body of the main program

"""
# Open the Cisco configuration file
with open('./DNAC-CompMon-Data/CSW-9300-CORE.base2hq.com_run_config.txt', 'r') as config_file:

    # Read all the lines in the file
    lines = config_file.readlines()

    # Ask the user for the regular expression pattern to search for
    pattern = input('Enter the regular expression pattern to search for: ')
    matching_lines = []
    
    matching_lines = show_run_section(lines, pattern)

    # Print out each matching line
    for line in matching_lines:
        print(line.strip("\n"))
"""