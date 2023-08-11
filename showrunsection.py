import re
import sys

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

# Open the Cisco configuration file
with open('./DNAC-CompMon-Data/CSW-9300-CORE.base2hq.com_run_config.txt', 'r') as config_file:

    # Read all the lines in the file
    lines = config_file.readlines()

    # Ask the user for the regular expression pattern to search for
    pattern = input('Enter the regular expression pattern to search for: ')
    matching_lines = []
    """
    try:
        pattern = re.compile(pattern)
    except ValueError:
        print("Error: Interface {} not found in configuration file".format(interface_name))
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
    """
    matching_lines = show_run_section(lines, pattern)

    # Print out each matching line
    for line in matching_lines:
        print(line.strip())
    

