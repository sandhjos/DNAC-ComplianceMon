data = {0: {'Scope': 'ALL_CONFIG', 'Operator': 'CONTAINS', 'Value': 'logging origin-id hostname', 'Message': 'MISSING logging origin-id hostname'}, 1: {'Scope': 'ALL_CONFIG', 'Operator': 'CONTAINS', 'Value': 'aaa authentication login default', 'Message': 'MISSING aaa authentication login default'}, 2: [{'Scope': 'SUBMODE_CONFIG', 'Operator': 'MATCHES_EXPRESSION', 'Value': 'interface (.*)Ethernet(.*)', 'Message': 'none'}, {'Scope': 'PREVIOUS_SUBMODE_CONFIG', 'Operator': 'MATCHES_EXPRESSION', 'Value': '(no ip address|switchport|shutdown)', 'Message': 'none'}, {'Scope': 'PREVIOUS_SUBMODE_CONFIG', 'Operator': 'MATCHES_EXPRESSION', 'Value': 'ip address .*', 'Message': 'none'}, {'Scope': 'PREVIOUS_SUBMODE_CONFIG', 'Operator': 'DOES_NOT_MATCH', 'Value': 'ip address (10|127|167\\.24\\.4[0-7]\\.*|172\\.(?:1[6-9]|2[0-9]|3[01])|192\\.168\\..* 255.255..*)', 'Message': 'none'}, {'Scope': 'PREVIOUS_SUBMODE_CONFIG', 'Operator': 'DOES_NOT_MATCH', 'Value': 'encapsulation dot1Q', 'Message': 'none'}, {'Scope': 'PREVIOUS_SUBMODE_CONFIG', 'Operator': 'MATCHES_EXPRESSION', 'Value': 'ip access-group (INTERNET-INBOUND|USAAVPN) in', 'Message': 'MISSING ip access-group INTERNET-INBOUND on <1.1> <1.2>'}]}

scopes = []

for key in data:
    if isinstance(data[key], dict):
        scopes.append(data[key]['Scope'])
    elif isinstance(data[key], list):
        for sub_dict in data[key]:
            scopes.append(sub_dict['Scope'])

print(scopes)

import re

my_string = "The quick brown fox jumps over the lazy dog."
my_regex = r"cat"

if not re.search(my_regex, my_string):
    print(f"The regex {my_regex} is not in the string.")
else:
    print(f"The regex {my_regex} is in the string.")



my_string = "The quick brown fox jumps over the lazy dog."
my_regex_str = "fox"

my_regex = re.compile(my_regex_str)

if not my_regex.search(my_string):
    print(f"The regex {my_regex_str} is not in the string.")
else:
    print(f"The regex {my_regex_str} is in the string.")

import re

my_string = "The quick brown fox jumps over the lazy dog."
my_regex_str = "^*The.*dog\.$"

if my_regex_str.startswith("*"):
    my_regex_str = "." + my_regex_str[1:]
if my_regex_str.startswith("^*"):
    my_regex_str = "^." + my_regex_str[2:]
if my_regex_str.startswith("^"):
    my_regex_str = "\\" + my_regex_str

if my_regex_str.endswith("$"):
    my_regex_str = my_regex_str[:-1] + "\\$"

my_regex = re.compile(my_regex_str)
if my_regex.search(my_string):
    print(f"The regex {my_regex_str} is in the string.")
else:
    print(f"The regex {my_regex_str} is not in the string.")

import re

# Read in the configuration file
with open("config.txt", "r") as f:
    config_data = f.read()

# Define the regular expression patterns for each criterion
interface_pattern = r"interface (.*)Ethernet(.*)"
no_ip_address_pattern = r"no ip address"
switchport_pattern = r"switchport"
shutdown_pattern = r"shutdown"
ip_address_pattern = r"ip address .*"
private_ip_pattern = r"ip address (10|127|167\.24\.4[0-7]\.*|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168\..* 255.255..*)"
dot1q_pattern = r"encapsulation dot1Q"
access_group_pattern = r"ip access-group (INTERNET-INBOUND|USAAVPN) in"

# Loop through each criterion and search for matches in the configuration data
for criterion in data:
    scope = criterion["Scope"]
    operator = criterion["Operator"]
    value = criterion["Value"]
    message = criterion["Message"]
    
    if scope == "SUBMODE_CONFIG":
        pattern = value
    elif scope == "PREVIOUS_SUBMODE_CONFIG":
        pattern = "(?s)(?<=^interface.*\n)(" + value + ")"
    else:
        continue
    
    regex = re.compile(pattern)
    matches = regex.findall(config_data)
    
    if operator == "MATCHES_EXPRESSION":
        if matches:
            print(f"{message}: {matches}")
        else:
            print(f"{message}: No matches found.")
    elif operator == "DOES_NOT_MATCH":
        if not matches:
            print(f"{message}: No matches found.")
        else:
            print(f"{message}: Matches found.")

