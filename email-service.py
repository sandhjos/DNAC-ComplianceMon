#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: email_service.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
####################################################################################

# This section sends emails

#     ------------------------------- IMPORTS -------------------------------
import smtplib, ssl
from file import SMTP_SERVER, SMTP_PORT ,SMTP_EMAIL, SMTP_PASS, NOTIFICATION_EMAIL

subject = "DNA Center Compliance Report"
body = "This is the data from the report produced at TIME DATE."
message = f"Subject: {subject}\n\n{body}"
context = ssl.create_default_context()
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls(context=context)
    server.login(SMTP_EMAIL, SMTP_PASS)
    server.sendmail(SMTP_EMAIL, NOTIFICATION_EMAIL, message)
"""
msg = EmailMessage()
msg.set_content("Hello Underworld!")
msg['Subject'] = "Hello Underworld from Python Gmail!"
msg['From'] = sender_email
msg['To'] = receiver_email

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
"""