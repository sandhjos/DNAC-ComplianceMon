####################################################################################
# project: DNAC-ComplianceMon
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
####################################################################################

# This file contains the:
# DNAC username and password, server info and file locations

# Update this section with the DNA Center server info and user information
DNAC_URL = 'https://10.10.0.20'
DNAC_USER = 'admin'
DNAC_PASS = 'Cisco12345'

# File location to be used for configurations
CONFIG_PATH = f"."
CONFIG_STORE = f"DNAC-CompMon-Data"