####################################################################################
# project: DNAC-ComplianceMon
# module: config.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
#            Bryn Pounds, PSA, WW Architectures, Cisco Systems
####################################################################################

import socket

# This file contains the:
# DNAC username and password, server info and file locations

# Update this section with the DNA Center server info and user information
DNAC_IP = '10.10.0.20'
DNAC_USER = 'demouser'
DNAC_PASS = 'C1sco12345'
DNAC_URL = 'https://' + DNAC_IP
DNAC_FQDN = socket.getfqdn(DNAC_IP)

# Update this section for Email Notification 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# Enter your address
SMTP_EMAIL = "sender@gmail.com"
SMTP_PASS = "16-digit-app-password"
# Enter receiver address
NOTIFICATION_EMAIL = "receiver@gmail.com"
# SMTP unset FLAG
SMTP_FLAG = False

# Update this section for the Time Zone
TIME_ZONE = 'America/Indiana/Indianapolis'

# File location to be used for configurations
CONFIG_PATH = f"./"
CONFIG_STORE = f"DNAC-CompMon-Data/Configs/"
JSON_STORE = f"DNAC-CompMon-Data/JSONdata/"
REPORT_STORE = f"DNAC-CompMon-Data/Reports/"
COMPLIANCE_STORE = f"PrimeComplianceChecks/"