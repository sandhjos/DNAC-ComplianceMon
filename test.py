import json
from prettytable import PrettyTable

with open('./DNAC-CompMon-Data/JSONdata/DCR-ASW-C9300-48-DEMO.base2hq.com-08_21_2023.json') as f:
    data = json.load(f)

# Print timestamp
print(f"Timestamp: {data['timestamp']}")

# Print device name
print(f"Device Name: {data['device']['name']}")

# Create table
table = PrettyTable()
table.field_names = ["Test ID", "Result", "Message"]

# Add rows to table
for test in data['tests']:
    table.add_row([test['id'], test['result'], test['message']])

# Print table
print(table)
