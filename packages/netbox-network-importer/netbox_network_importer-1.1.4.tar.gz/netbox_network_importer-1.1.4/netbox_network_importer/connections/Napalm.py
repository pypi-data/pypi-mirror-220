import napalm
from netbox_network_importer.config import get_config
from napalm.pyIOSXR.exceptions import XMLCLIError

import logging
logger = logging.getLogger(__name__)

driver_iosxr = napalm.get_network_driver('iosxr')
driver_ios = napalm.get_network_driver('ios')
driver_iosxr_netconf = napalm.get_network_driver('iosxr_netconf')
driver_nxos = napalm.get_network_driver('nxos_ssh')
driver_junos = napalm.get_network_driver('junos')


class Napalm:
    def __init__(self, address, driver):
        self.address = address
        self.driver = driver

        # connection to napalm device
        # supports https://napalm.readthedocs.io/en/latest/base.html commands
        self.connection = None

    # set napalm_driver
    def __set_napalm_driver(self, hostname, driver, port=22):
        conn_param = {
            "hostname": hostname,
            "username": get_config()['tacacs']['TACACS_USERNAME'],
            "password": get_config()['tacacs']['TACACS_PASSWORD'],
            "timeout": 60,
            "optional_args": {
                "fast_cli": False,
                "allow_agent": False,
                "look_for_keys": False,
                "conn_timeout": 30,
                "secret": get_config()['tacacs']['TACACS_PASSWORD']
            }
        }

        if driver == "ios" or driver == "iosxe":
            return driver_ios(**conn_param)
        elif driver == "iosxr":
            return driver_iosxr(**conn_param)
        elif driver == "iosxr_netconf":
            conn_param['optional_args'] = {}
            conn_param['optional_args']['port'] = port
            return driver_iosxr_netconf(**conn_param)
        elif driver == 'nxos' or driver == 'nxos_ssh':
            conn_param['optional_args'] = {'read_timeout_override': 300}
            return driver_nxos(**conn_param)
        elif driver == 'junos':
            return driver_junos(**conn_param)
        else:
            logger.critical(
                "Cannot connect do this type of device: %s", driver)
            return False

    def open(self):
        try:
            self.connection = self.__set_napalm_driver(
                self.address, self.driver)
            self.connection.open()

        except Exception as e:
            #logger.critical("Unable to Connect, Global exception")
            raise e

    def close(self):
        self.connection.close()
        self.connection = None

    def get_interfaces_ip(self):
        try:
            self.open()
            res = self.connection.get_interfaces_ip()
            self.close()
            return res
        except XMLCLIError as e:
            if self.driver == 'iosxr':
                self.driver = 'iosxr_netconf'
                return self.get_interfaces_ip()
        except Exception as e:
            raise e

    def get_interfaces(self):
        try:
            self.open()
            res = self.connection.get_interfaces()
            self.close()
            return res
        except XMLCLIError as e:
            if self.driver == 'iosxr':
                self.driver = 'iosxr_netconf'
                return self.get_interfaces()
        except Exception as e:
            raise e

    def get_facts(self):
        try:
            self.open()
            res = self.connection.get_facts()
            self.close()
            return res
        except XMLCLIError as e:
            if self.driver == 'iosxr':
                self.driver = 'iosxr_netconf'
                return self.get_facts()
        except Exception as e:
            raise e

    def connection_test(self):
        try:
            self.open()
            # self.connection.get_facts() # Throws error for some IOSXR devices, Opened issue on Napalm
            self.connection.get_interfaces()
            self.close()
            return (True, f"{self.address} connected successfuly")
        except XMLCLIError as e:
            if self.driver == 'iosxr':
                self.driver = 'iosxr_netconf'
                return self.connection_test()
            else:
                return (False, e)
        except Exception as e:
            return (False, e)
