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