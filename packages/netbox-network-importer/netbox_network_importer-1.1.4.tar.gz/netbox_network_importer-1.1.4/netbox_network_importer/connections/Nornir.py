import logging
from netbox_network_importer.config import get_config
from nornir import InitNornir

logger = logging.getLogger("base." + __name__)


class Nornir:
    def init_nornir_w_netbox(filter_parameters={}):
        """Init nornir with Netbox.

        :param filter_parameters: params to filter certain devices
        """

        nr = InitNornir(
            logging={"enabled": False, "level": "DEBUG"},
            inventory={
                "plugin": "NetBoxInventory2",
                "options": {
                    "nb_url": get_config()['netbox']["NETBOX_INSTANCE_URL"],
                    "nb_token": get_config()['netbox']["NETBOX_API_TOKEN"],
                    "flatten_custom_fields": False,
                    "filter_parameters": filter_parameters,
                    "use_platform_slug": False,
                    "use_platform_napalm_driver": False,
                    # group_file,
                    # defaults_file - could be used for username and password for devices - connection options
                }
            },
            runner={
                'plugin': 'threaded',
                'options': {
                    'num_workers': 20  # default
                }
            }
        )

        return nr
