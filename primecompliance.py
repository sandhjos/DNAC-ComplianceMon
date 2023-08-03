#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: primecompliance.py
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

import utils
import difflib
import re  # needed for regular expressions matching
import logging
import warnings


import json
import xml
import xml.dom.minidom
import lxml.etree as et
import xmltodict
import select
import socket  # needed for IPv4 validation
import ipaddress  # needed for IPv4 address validation

#     ----------------------------- DEFINITIONS -----------------------------
