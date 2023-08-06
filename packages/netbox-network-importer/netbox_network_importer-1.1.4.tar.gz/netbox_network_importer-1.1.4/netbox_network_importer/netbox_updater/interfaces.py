from netbox_network_importer.helper import canonical_interface_name_edited, get_diff
from netbox_network_importer.connections.Netbox import Netbox
from netbox_network_importer.results.results import NetboxResult, Status, Action


def process_interfaces(host, parsed_interfaces) -> list:
    """CRUD on netbox interfaces
    - Delete interfaces, that exists in netbox but are not passed from device
    - Update interfaces, which already exists in netbox
    - Create interfaces, which does not exists in netbox

    :param parsed_interfaces: parsed interfaces for netbox operations
    :param host: host of the task (netbox device representation)

    :returns: list of NetboxResult
    """

    RESULTS = []  # list of NetboxResult

    # Init connection to Netbox via PyNetbox
    nb = Netbox.connect()

    # find the device instance in netbox
    dev = nb.dcim.devices.get(host.data['id'])

    # find interfaces linked to the device
    ifcs_filter = nb.dcim.interfaces.filter(device_id=dev.id)

    # convert filtered interfaces into dictionary of pynetbox interface instances
    nb_interfaces_dict = {canonical_interface_name_edited(ifc.name): ifc for ifc in [
        ifc for ifc in ifcs_filter]}

    # setup NB parameters
    for ifc, properties in parsed_interfaces.items():
        ifc_params = {
            'name': ifc,
            'enabled': properties['enabled'],
            'description': properties['description'].strip(),
            'type': properties['type'],
            'mtu': properties['mtu'],
            'mac_address': properties['mac_address']
        }

        # get NB interface instance
        nb_ifc = nb_interfaces_dict.get(ifc, None)

        if nb_ifc:
            # Skip IGNORED interfaces
            if nb_ifc.custom_fields.get("ignore_importer", False) == True:
                RESULTS.append(NetboxResult(
                    result=f"{nb_ifc.name} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.LOOKUP, diff=""))

                nb_interfaces_dict.pop(nb_ifc.name, None)
                continue
            else:
                # If interface already exists in netbox, update it
                RESULTS.append(interface_update(
                    nb_ifc=nb_ifc, params=ifc_params))
        else:
            # Otherwise, create it
            ifc_params['device'] = {'id': dev.id}
            RESULTS.append(interface_create(ifc_params=ifc_params, nb=nb))

        # Pop device from dictionary if it's updated / created
        nb_interfaces_dict.pop(ifc, None)

    # If any interface is left in `nb_interfaces_dict`, then it should be removed from netbox
    #   - Interface exists in netbox, but the interface was not passed from network
    for ifc_name, nb_ifc in nb_interfaces_dict.items():
        RESULTS.append(interface_delete(ifc=nb_ifc))

    return RESULTS


def interface_delete(ifc):
    try:
        if ifc.cable:
            return NetboxResult(
                result=f"{ifc.name} - CHECK MANUALLY - Cable exists",
                status=Status.CHECK_MANUALLY,
                action=Action.DELETE,
                diff={"name": ifc.name, "device_name": ifc.device.name,
                       "description": ifc.description, "cable_id": ifc.cable.id}
            )

        if ifc.custom_fields.get("ignore_importer", False) == True: 
            return NetboxResult(
                    result=f"{ifc.name} - CHECK MANUALLY - Inteface Ignored",
                    status=Status.CHECK_MANUALLY,
                    action=Action.DELETE,
                    diff={"name": ifc.name, "device_name": ifc.device.name,
                       "description": ifc.description, "ignore_importer": ifc.custom_fields.get("ignore_importer", False)}
                    )

        if ifc.delete():
            return NetboxResult(
                result=f"{ifc.name} - deleted successfully",
                status=Status.CHANGED,
                action=Action.DELETE,
                diff={"name": ifc.name, "device": ifc.device.name,
                       "description": ifc.description}
            )
        else:
            return NetboxResult(result=f"{ifc.name} - could not be deleted", status=Status.ANOMALLY, action=Action.DELETE, diff={})
    except Exception as e:
        return NetboxResult(result=f"{ifc.name} - Exception Occurs: {e}", status=Status.EXCEPTION, action=Action.DELETE, diff={}, exception=e)


def interface_update(nb_ifc, params):
    try:
        # Get data before changes
        before = get_changed_params(nb_ifc)

        # TODO: Don't change ifc type if Other -
        if params.get("type", None) == 'other':
            params.pop('type')

        if nb_ifc.update(params):
            # TODO: Reload ifc
            nb_ifc = nb_ifc.api.dcim.interfaces.get(nb_ifc.id)
            after = get_changed_params(nb_ifc)

            return NetboxResult(
                result=f"{nb_ifc.name} - saved successfully",
                status=Status.CHANGED,
                action=Action.UPDATE,
                diff=get_diff(before, after)
            )
        else:
            return NetboxResult(
                result=f"{nb_ifc.name} - nothing to do",
                action=Action.UPDATE,
                status=Status.NOT_CHANGED,
                diff={}
            )
    except Exception as e:
        return NetboxResult(result=f"{nb_ifc.name} - Exception Occurs: {e}", status=Status.EXCEPTION, action=Action.DELETE, diff={}, exception=e)


def interface_create(ifc_params, nb):
    try:
        netbox_interface = nb.dcim.interfaces.create(ifc_params)

        if netbox_interface:
            return NetboxResult(
                result=f"{netbox_interface.name} - created successfully",
                status=Status.CHANGED,
                action=Action.CREATE,
                diff=ifc_params
            )
        else:
            return NetboxResult(
                result=f"{ifc_params['name']} - ERROR!",
                status=Status.FAILED,
                action=Action.CREATE,
                diff={}
            )
    except Exception as e:
        return NetboxResult(result=f"{ifc_params['name']} - Exception Occurs: {e}", status=Status.EXCEPTION, action=Action.DELETE, diff={}, exception=e)


def get_changed_params(nb_interface):
    return {'name': nb_interface.name,
            'enabled': nb_interface.enabled,
            'description': nb_interface.description,
            'type': nb_interface.type,
            'mtu': nb_interface.mtu,
            'mac_address': nb_interface.mac_address}
