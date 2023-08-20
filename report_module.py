#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: report_builder.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
#            Bryn Pounds, PSA, WW Architectures, Cisco Systems
####################################################################################

# This program is written to ingest all the XML files exported from Prime and build
# a report from the audit of configuration files.

#     ------------------------------- IMPORTS -------------------------------

import os
import sys
import os.path
import datetime
import time
import pytz
from fpdf import FPDF

#     ----------------------------- DEFINITIONS -----------------------------

# Convert a text string to a pdf report and return the pdf
def pdf_converter():
    return