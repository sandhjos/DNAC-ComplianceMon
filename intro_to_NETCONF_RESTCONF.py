

# developed by Gabi Zapodeanu, TME, Enterprise Networks, Cisco


import requests
import ncclient
import xml
import xml.dom.minidom
import json
import lxml.etree as et
import xmltodict
import netconf_restconf

from ncclient import manager

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth
from config import IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS, IOS_XE_PORT

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

ROUTER_AUTH = HTTPBasicAuth(IOS_XE_USER, IOS_XE_PASS)


def main():
    """
    This sample script will show how to work with the device configurations using NETCONF and RESTCONF
    """

    # retrieve the device capabilities using RESTCONF
    print('Device Capabilities via RESTCONF: ')
    capabilities = netconf_restconf.restconf_get_capabilities(IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS)
    print(json.dumps(capabilities, indent=4, separators=(' , ', ' : ')))

    # retrieve the device hostname using RESTCONF
    device_hostname = netconf_restconf.restconf_get_hostname(IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS)
    print(str('\nDevice Hostname via RESTCONF: \n' + device_hostname))

    # retrieve interface operationla state using NETCONF
    interface_state = netconf_restconf.netconf_get_int_oper_status('GigabitEthernet1', IOS_XE_HOST, IOS_XE_PORT, IOS_XE_USER, IOS_XE_PASS)
    print(str('\nInterface Operational Status via NETCONF: \n' + interface_state))

    # retrieve the interface statistics using RESTCONF
    interface_statistics = netconf_restconf.restconf_get_int_oper_data('GigabitEthernet1', IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS)
    print('\nGigabitEthernet1 Interface Statistics via RESTCONF: \n')
    print(json.dumps(interface_statistics, indent=4, separators=(' , ', ' : ')))

    # save running configuration to startup configuration using RESTCONF
    save_result = netconf_restconf.restconf_save_running_config(IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS)
    print('\nRunning Config saved to device using RESTCONF: ', save_result)

    # save running configuration to file using NETCONF
    save_file = 'flash:/CONFIG_FILES/base_config'
    save_file_result = netconf_restconf.netconf_save_running_config_to_file(save_file, IOS_XE_HOST, IOS_XE_PORT, IOS_XE_USER, IOS_XE_PASS)
    print('\nRunning Config saved to file using NETCONF: ', save_file_result[1])

    # rollback configuration to saved file using RESTCONF
    rollback_file = 'flash:/CONFIG_FILES/base_config'
    rollback_result = netconf_restconf.restconf_rollback_to_saved_config(rollback_file, IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS)
    print('\nRollback of Config from saved file using RESTCONF: ', rollback_result)

if __name__ == '__main__':
    main()


