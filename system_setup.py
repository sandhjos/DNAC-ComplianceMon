#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# author: kebaldwi@cisco.com
# module: system_setup.py
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
#            Bryn Pounds, PSA, WW Architectures, Cisco Systems
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
import zipfile
import pytz
from service_scheduler import *
from config import TIME_ZONE, CONFIG_PATH, COMPLIANCE_STORE

#     ----------------------------- DEFINITIONS -----------------------------

# This function sets the DNA Center connection details
def DNAC_setup(file_path):
    # Define the path to the Python file to update
    #test_file_path = "./file.py"

    # Loop until valid input is given or cancel is entered
    while True:
        dnac_ip = input("\n\nEnter the DNA Center IP address you wish to connect (or 'cancel' to exit): ")
        if dnac_ip.lower() == "cancel":
            break

        # Test for a valid IP address
        try:
            socket.inet_aton(dnac_ip)
        except socket.error:
            print("\nInvalid IP address. Please try again.")
            continue

        # Test the connection to the server with a ping
        ping_cmd = ["ping", "-c", "1", "-W", "1", dnac_ip]
        ping_result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ping_result.returncode != 0:
            print("\nServer is not reachable. Please try again.")
            continue

        # Do a DNS lookup for the FQDN of the server
        try:
            dnac_fqdn = socket.getfqdn(dnac_ip)
            dns_lookup = socket.gethostbyname(dnac_fqdn)
            if dns_lookup != dnac_ip:
                print("\nDNS lookup failed. Please try again.")
                continue
        except socket.error:
            print("DNS lookup failed. Please try again.")
            continue

        dnac_usr = input("Enter the username for DNA Center: ")
        dnac_pwd = input("Enter the password for DNA Center: ")

        #Try connecting to DNA Center
        try:
            DNAC_AUTH = HTTPBasicAuth(dnac_usr, dnac_pwd)
            DNAC_URL = "https://" + dnac_ip
            dnac_token = dnac_apis.test_dnac_jwt_token(DNAC_URL, DNAC_AUTH)
            print("\nDNA Center connection test passed.")
        except:
            print("\nCredentials failed. Please try again.")
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

def SMTP_setup(file_path):
    # Define the typical gmail server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Define the path to the Python file to update
    #test_file_path = "./file.py"

    # Loop until valid input is given or cancel is entered
    while True:
        # Ask for user input
        email_address = input("\n\nEnter your Gmail address (or 'cancel' to exit): ")
        if email_address.lower() == "cancel":
            break
        email_password = getpass.getpass("Enter your Gmail password: ")
        email_recipient = input("Enter the recipient email address: ")
        smtp_server = input("\nEnter the SMTP server address: ")
        smtp_port = input("Enter the SMTP port: ")
        
        # Test the connection to the SMTP server
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(email_address, email_password)
        except smtplib.SMTPAuthenticationError:
            print("\nAuthentication failed. Please try again.")
            continue
        except:
            print("\nConnection to SMTP server failed. Please try again.")
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
            print("\nFailed to send test email. Please try again.")
            continue
        
        # Print a success message and exit the loop
        print("\nTest email sent successfully!")

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
            elif "SMTP_FLAG =" in line:
                new_lines.append(f"SMTP_FLAG = True\n")
            else:
                new_lines.append(line)
        with open(file_path, "w") as f:
            f.writelines(new_lines)

        # Print a success message and exit the loop
        print("\nSMTP Server information updated successfully.")
        break
    return

# This function sets the DNA Center connection details
def TZONE_setup(file_path):
    # Define the path to the Python file to update
    #test_file_path = "./file.py"

    # Loop until valid input is given or cancel is entered
    while True:
        print("\n\nThe Time Zone is currently set for " + TIME_ZONE + ".\n\n")
        check = input("\nTo change the time zone enter [yes|y] (or 'cancel' to exit): ")
        if check.lower() == "cancel":
            break

        # Display a list of available countries
        print("\n\nAvailable countries:")
        country_codes = list(pytz.country_names.keys())
        max_len = max([len(pytz.country_names[cc]) for cc in country_codes])
        num_cols = 3
        rows = [country_codes[i:i+num_cols] for i in range(0, len(country_codes), num_cols)]
        for row in rows:
            cols = [f"{cc.ljust(2)} {pytz.country_names[cc].ljust(max_len)}" for cc in row]
            print("  ".join(cols))
        
        # Prompt the user to select a country
        country_code = input("\nEnter the 2-letter country code for your location: ")
        
        # Validate the country code entered by the user
        if country_code not in pytz.country_names:
            print("\nInvalid country code. Please try again.")
        else:
            # Display a list of available timezones for the selected country
            print(f"\n\nAvailable timezones for {pytz.country_names[country_code]}:")
            timezones = pytz.country_timezones.get(country_code)
            max_len = max([len(tz) for tz in timezones])
            num_cols = 3
            rows = [timezones[i:i+num_cols] for i in range(0, len(timezones), num_cols)]
            for i, row in enumerate(rows):
                cols = [f"{i*num_cols+j+1}. {tz.ljust(max_len)}" for j, tz in enumerate(row)]
                print("  ".join(cols))
            
            # Prompt the user to select a timezone by number
            timezone_num = input("\nEnter the number of your timezone: ")
            try:
                timezone_idx = int(timezone_num) - 1
                selected_timezone = timezones[timezone_idx]
                print("\nSelected timezone:", selected_timezone)
            except (ValueError, IndexError):
                print("\nInvalid timezone number. Please try again.")
            
            # If all tests pass, replace lines in the Python file
            with open(file_path, "r") as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                if "TIME_ZONE =" in line:
                    new_lines.append(f"TIME_ZONE = '{selected_timezone}'\n")
                else:
                    new_lines.append(line)
            with open(file_path, "w") as f:
                f.writelines(new_lines)

            # Print a success message and exit the loop
            print("\nTime Zone information updated successfully.")
            break

    return

def system_settings():
    # Define the path to the Python file to update
    file_path = "./config.py"

    # Loop until valid input is given or cancel is entered
    while True:
        # Ask for user input
        print("\n\nDNA Center Compliance Monitor Setup\n")
        print("1. DNA Center Connection Settings")
        print("2. SMTP Connection Settings")
        print("3. Time Zone Settings")
        print("4. Upload Prime Rules for IOS-XE")
        print("5. Schedule Settings")
        menu_input = input("\n\nEnter a number from above for setup (or 'cancel' to exit): ")

        if menu_input.lower() == "cancel":
            break

        # Test the connection to the SMTP server
        try:
            if int(menu_input) <= 5 and int(menu_input) >= 1:
                # If all the tests pass
                if int(menu_input) == 1:
                    DNAC_setup(file_path)
                elif int(menu_input) == 2:
                    SMTP_setup(file_path)
                elif int(menu_input) == 3:
                    TZONE_setup(file_path)
                elif int(menu_input) == 4:
                    PRIME_import(CONFIG_PATH, COMPLIANCE_STORE)
                elif int(menu_input) == 5:
                    menu_scheduler()
        except:
            print("\nValid selections only are 1 to 5. Please try again.")
            continue
    return

def PRIME_import(CONFIG_PATH, COMPLIANCE_STORE):
    
    # Loop until valid input is given or cancel is entered
    while True:
        file_path = input("\n\nEnter the file location to be uploaded (or 'cancel' to exit): ")

        if file_path.lower() == "cancel":
            break
        elif file_path.startswith('~'):
            file_path = os.path.expanduser(file_path)
        
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        Compliance_Files = os.path.join(CONFIG_PATH, COMPLIANCE_STORE)
        
        test_str = os.path.join(CONFIG_PATH, COMPLIANCE_STORE, file_name)

        if not os.path.exists(Compliance_Files):
            os.makedirs(Compliance_Files)
        
        if not os.path.exists(test_str):
            # Open the zip file and extract its contents to the destination folder
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(Compliance_Files)
        
            # Print a message to confirm that the extraction was successful
            print("\n\nThe zip file has been extracted to the destination folder.")
            break
        else:
            print("\n\nThe Compliance Audits have already been extracted to the destination folder.")
            break

#     ----------------------------- MAIN -----------------------------

# code below for development purposes and testing only

if __name__ == '__main__':
    system_settings()
