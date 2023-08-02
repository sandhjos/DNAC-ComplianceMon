# DNA Center Compliance Monitor
Using Cisco DNA Center for Configuration Monitoring and Compliance and sending notifications as incidents to ServiceNow

This repo will use xml formatted compliance rules from Cisco DNA Center to how to detect and mitigate unauthorized, or non-compliant configuration changes and notify ServiceNow or via Email.

This repo is based on ConfigMon-DNAC by Gabi Z

## The Challenge: 
 - 70% of policy violations are due to user errors
 - Configuration drifting
 - non compliant code
 - compliancy audits

## The Goal: 
 - Detect and alert on all network configuration changes
 - Automate roll back of non-compliant changes
 - Approval process for all compliant configuration changes
 - Report on Non Complaint configurations

## The Solution:
 - Integration between Cisco DNA Center, ServiceNow, IOS XE Programmability, and Webex Teams
 - The application may run on demand, scheduled or continuously

## Workflow:
 - Collect network devices running configurations using the Cisco DNA Center Command Runner APIs
 - Create a local folder with all the running configurations
 - If the device is new, add the configuration to the local folder
 - If device is known, check for configuration changes
 - If a change occurred, identify who made the change, the device name, physical location and device health
 - Record changes by creating a ServiceNow incident
 - Identify what changed and the relevant section of the configuration
 - Inspect against provided compliance policies:
   - no logging configuration changes, 
   - no access control lists configuration,
   - prevent IPv4 duplicate addresses
   - check for non compliant configurations using xml audits from Prime
 - Rollback configuration if compliance violations, test if successful or not, update the ServiceNow incident
 - If no compliance violations ask for approval from change control manager and update ServiceNow incident
 - Act upon the answer in ServiceNow - approved/denied or timeout by saving the new configuration or rollback the configuration
 - Update the ServiceNow incident with the approval process
 - The “configuration save to file”, “save to startup configuration”, and “configuration rollback” tasks are completed using NETCONF and RESTCONF
 - Notify IT organizations of new, updated and closed ServiceNow incidents using the ServiceNow to Webex Teams integration

## The Results: 
 - Non compliant configuration changes are mitigated in minutes
 - Troubleshooting assistance by providing a real time view of all device configuration changes

## Roadmap:
 - Build a web based dashboard
 - Create additional compliance checks
 - Create northbound APIs to provide additional services like - device configuration file retrieval, configurations search, archiving, reporting
 
## Setup and Configuration
 - The requirements.txt file include all the Python libraries needed for this application
 - This application requires:
   - Cisco DNA Center
   - IOS XE devices configured for NETCONF and RESTCONF
   - Cisco Webex Teams account
   - ServiceNow developer account
 - The config.py is the only file needed to be customized to match your environment
 