#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
####################################################################################

# This program is written to meet the requirements set out in the README.md

#     ------------------------------- IMPORTS -------------------------------

import os
import sys
import os.path
import datetime
import time

import requests
import difflib
import urllib3
import logging
import json
import warnings

import utils
import dnac_apis

from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

from config import DNAC_URL, DNAC_PASS, DNAC_USER, CONFIG_PATH, CONFIG_STORE

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

#     ----------------------------- DEFINITIONS -----------------------------

def os_setup():
    """Define OS settings for display"""
    if (os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

def pause():
    """Define pause for keystroke to continue"""
    input("\nPress Enter to continue...\n") 
    if (os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')

def config_library(CONFIG_PATH, CONFIG_STORE):
    Config_Files = os.path.join(CONFIG_PATH, CONFIG_STORE)
    if not os.path.exists(Config_Files):
        os.makedirs(Config_Files)
    os.chdir(Config_Files)

def main():
    os_setup()
    config_library(CONFIG_PATH,CONFIG_STORE)

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='application_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    print("DNA Center Compliance Monitor:\n")
    print("We are going to collect all configurations for routers and switches your DNA Center\n")
    print("\n\nThis is the Token we will use for Authentication:")
    dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
    print('\nDNA Center AUTH Token: \n', dnac_token, '\n')
    pause()   

    temp_run_config = 'temp_run_config.txt'
    
    # get the DNA C managed devices list (excluded wireless, for one location)
    all_devices_info = dnac_apis.get_all_device_info(dnac_token)
    all_devices_hostnames = []
    for device in all_devices_info:
        if device['family'] == 'Switches and Hubs' or device['family'] == 'Routers':
            all_devices_hostnames.append(device['hostname'])
    print(all_devices_hostnames)
    # get the config files, compare with existing (if one existing). Save new config if file not existing.
    for device in all_devices_hostnames:
        device_run_config = dnac_apis.get_device_config(device, dnac_token)
        filename = str(device) + '_run_config.txt'
        # save the running config to a temp file
        f_temp = open(filename, 'w')
        f_temp.write(device_run_config)
        f_temp.seek(0)  # reset the file pointer to 0
        f_temp.close()

if __name__ == '__main__':
    main()
