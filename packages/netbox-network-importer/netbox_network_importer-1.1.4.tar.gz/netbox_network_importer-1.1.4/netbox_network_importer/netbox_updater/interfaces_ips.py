from netbox_network_importer.results.results import NetboxResult, Status, Action
from netbox_network_importer.helper import canonical_interface_name_edited, get_diff
from netbox_network_importer.connections.Netbox import Netbox


def process_interfaces_ips(host, parsed_interfaces) -> list:
    """CRUD on netbox interfaces IPs
    - Delete IPs, that exists in netbox but are not passed from device
    - Update IPs, which already exists in netbox
    - Create IPs, which does not exists in netbox

    :param parsed_interfaces: parsed interfaces for netbox operations
    """

    # Init connection to Netbox via PyNetbox
    nb = Netbox.connect()

    RESULTS = []

    # find the device instance in netbox
    dev = nb.dcim.devices.get(host.data['id'])

    # find interfaces linked to the device
    all_device_ifcs_recordset = nb.dcim.interfaces.filter(device_id=dev.id)

    # convert filtered interfaces into dictionary of pynetbox interface instances
    nb_interfaces_dict = {canonical_interface_name_edited(
        nb_ifc.name): nb_ifc for nb_ifc in all_device_ifcs_recordset}

    # Create DICT of ALL
    #    = parsed interfaces from genie (that with IP address assigned)
    #    = all interfaces stored in netbox (if not parsed with genie, empty dict of ip addresses passed)
    ALL_INTERFACES = {}
    ALL_INTERFACES.update({k: {} for k in nb_interfaces_dict})
    ALL_INTERFACES.update(parsed_interfaces)

    # Loop over all interfaces and process their IP addreses (CRUD)
    for ifc, parsed_ips in ALL_INTERFACES.items():
        # get NB interface instance
        nb_ifc = nb_interfaces_dict.get(ifc, None)
        # get NB interface ip addresses and convert to dictionary
        if nb_ifc == None:
            RESULTS.append(
                NetboxResult(
                    result=f"Interface {ifc} NOT FOUND!, Configured IPS: {parsed_ips} - Check manually",
                    status=Status.ANOMALLY,
                    action=Action.LOOKUP,
                    diff={}
                )
            )
            continue

        # Skip IGNORED interfaces
        if nb_ifc.custom_fields.get("ignore_importer", False) == True:
            RESULTS.append(NetboxResult(
                result=f"{nb_ifc.name} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.LOOKUP, diff=""))
            continue

        nb_interface_ips_recordset = nb.ipam.ip_addresses.filter(
            interface_id=nb_ifc.id)

        # key = ip address without mask
        nb_interface_ips_dict = {
            ip.address.split('/')[0]: ip for ip in nb_interface_ips_recordset}

        # Go through different family addresses
        for address_family in parsed_ips:
            if address_family == 'ipv4':
                family = {"value": 4, "label": "IPv4"}
            elif address_family == 'ipv6':
                family = {"value": 6, "label": "IPv6"}

            for ip in parsed_ips[address_family]:
                # TODO:
                if ip == '0.0.0.0':
                    continue

                # Pop device from dictionary - if none, create it
                if not nb_interface_ips_dict.pop(ip, None):
                    ip_params = {
                        'assigned_object_type':  "dcim.interface",
                        'assigned_object_id': nb_ifc.id,
                        'family': family,
                        'address': ip
                    }
                    RESULTS.append(ip_create(ip_params=ip_params,
                                   nb=nb, ifc_name=nb_ifc.name))

        # TODO: DELETE!!
        # If any interface is left in `nb_interfaces_dict`, then it should be removed from netbox
        #   - Interface exists in netbox, but the interface was not passed from network
        for _k, nb_ip_address in nb_interface_ips_dict.items():
            # Skip IGNORED interfaces
            if nb_ifc.custom_fields.get("ignore_importer", False) == True:
                RESULTS.append(NetboxResult(
                    result=f"{ifc.name} - {nb_ip_address.address} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.DELETE, diff=""))
                continue
            RESULTS.append(ip_delete(ip=nb_ip_address, ifc_name=nb_ifc.name))

    return RESULTS


def ip_delete(ip, ifc_name):
    if ip.delete():
        return NetboxResult(
            result=f"{ifc_name} - {ip.address} - deleted successfully",
            status=Status.CHANGED,
            action=Action.DELETE,
            diff={}
        )
    else:
        return NetboxResult(result=f"{ifc_name} - {ip.address} - could not be deleted",
                            status=Status.FAILED,
                            action=Action.DELETE,
                            diff={}
                            )


def ip_create(ip_params, nb, ifc_name):
    netbox_ip = nb.ipam.ip_addresses.create(ip_params)

    if netbox_ip:
        return NetboxResult(
            result=f"{ifc_name} - {netbox_ip.address} - created successfully",
            status=Status.CHANGED,
            action=Action.CREATE,
            diff=ip_params
        )
    else:
        return NetboxResult(
            result=f"{ifc_name} - {ip_params['address']} - Unable to create",
            status=Status.FAILED,
            action=Action.CREATE,
            diff={}
        )
