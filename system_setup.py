#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# author: kebaldwi@cisco.com
# module: system_setup.py
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
####################################################################################

# This program is written to meet the requirements set out in the README.md
# This section sets up the various connection settings

#     ------------------------------- IMPORTS -------------------------------
import os
import sys
import os.path
import datetime
import time
import socket
import subprocess
from requests.auth import HTTPBasicAuth  # for Basic Auth
import dnac_apis
import smtplib
import ssl
import getpass

#     ----------------------------- DEFINITIONS -----------------------------

# This function sets the DNA Center connection details
def DNAC_setup():
    # Define the path to the Python file to update
    file_path = "./file.py"
    # Loop until valid input is given or cancel is entered
    while True:
        dnac_ip = input("Enter the IP address of the DNA Center you wish to connect (or 'cancel' to exit): ")
        if dnac_ip.lower() == "cancel":
            break
        dnac_usr = input("Enter the username for DNA Center: ")
        dnac_pwd = input("Enter the password for DNA Center: ")
        # Test for a valid IP address
        try:
            socket.inet_aton(dnac_ip)
        except socket.error:
            print("Invalid IP address. Please try again.")
            continue
        # Test the connection to the server with a ping
        ping_cmd = ["ping", "-c", "1", "-W", "1", dnac_ip]
        ping_result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ping_result.returncode != 0:
            print("Server is not reachable. Please try again.")
            continue
        # Do a DNS lookup for the FQDN of the server
        try:
            dnac_fqdn = socket.getfqdn(dnac_ip)
            dns_lookup = socket.gethostbyname(dnac_fqdn)
            if dns_lookup != dnac_ip:
                print("DNS lookup failed. Please try again.")
                continue
        except socket.error:
            print("DNS lookup failed. Please try again.")
            continue
        #Try connecting to DNA Center
        try:
            DNAC_AUTH = HTTPBasicAuth(dnac_usr, dnac_pwd)
            dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
            print("DNA Center connection test passed.")
        except:
            print("Credentials failed. Please try again.")
            continue
        # If all tests pass, replace lines in the Python file
        with open(file_path, "r") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if "DNAC_IP =" in line:
                new_lines.append(f"DNAC_IP = '{dnac_ip}'\n")
            elif "DNAC_USER =" in line:
                new_lines.append(f"DNAC_USER = '{dnac_usr}'\n")
            elif "DNAC_PASS =" in line:
                new_lines.append(f"DNAC_PASS = '{dnac_pwd}'\n")
            else:
                new_lines.append(line)
        with open(file_path, "w") as f:
            f.writelines(new_lines)
        # Print a success message and exit the loop
        print("Server information updated successfully.")
        break
    return

def SMTP_setup():
    # Define the typical gmail server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    # Define the path to the Python file to update
    file_path = "./file.py"
    # Loop until valid input is given or cancel is entered
    while True:
        # Ask for user input
        email_address = input("Enter your Gmail address (or 'cancel' to exit): ")
        if email_address.lower() == "cancel":
            break
        email_password = getpass.getpass("Enter your Gmail password: ")
        email_recipient = input("Enter the recipient email address: ")
        smtp_server = input("Enter the SMTP server address: ")
        smtp_port = input("Enter the SMTP port: ")
        
        # Test the connection to the SMTP server
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(email_address, email_password)
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Please try again.")
            continue
        except:
            print("Connection to SMTP server failed. Please try again.")
            continue
        
        # Send a test email
        try:
            subject = "Test email from DNAC-COMPLIANCEMON"
            body = "This is a test email sent from the DNAC Compliance APP."
            message = f"Subject: {subject}\n\n{body}"
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(email_address, email_password)
                server.sendmail(email_address, email_recipient, message)
        except:
            print("Failed to send test email. Please try again.")
            continue
        
        # Print a success message and exit the loop
        print("Test email sent successfully!")

        # If all tests pass, replace lines in the Python file
        with open(file_path, "r") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if "SMTP_SERVER =" in line:
                new_lines.append(f"SMTP_SERVER = '{smtp_server}'\n")
            elif "SMTP_PORT =" in line:
                new_lines.append(f"SMTP_PORT = '{smtp_port}'\n")
            elif "SMTP_EMAIL =" in line:
                new_lines.append(f"SMTP_EMAIL = '{email_address}'\n")
            elif "SMTP_PASS =" in line:
                new_lines.append(f"SMTP_PASS = '{email_password}'\n")
            elif "NOTIFICATION_EMAIL =" in line:
                new_lines.append(f"NOTIFICATION_EMAIL = '{email_recipient}'\n")
            else:
                new_lines.append(line)
        with open(file_path, "w") as f:
            f.writelines(new_lines)
        # Print a success message and exit the loop
        print("Server information updated successfully.")
        break
    return

#DNAC_setup()
SMTP_setup()