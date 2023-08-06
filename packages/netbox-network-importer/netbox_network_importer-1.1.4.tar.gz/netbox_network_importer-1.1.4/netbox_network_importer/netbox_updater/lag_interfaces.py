from netbox_network_importer.helper import canonical_interface_name_edited, get_diff, get_netbox_interface_type
from netbox_network_importer.connections.Netbox import Netbox
from netbox_network_importer.results.results import NetboxResult, Status, Action

import logging
logger = logging.getLogger(__name__)


def process_lag_interfaces(host, parsed_lag_interfaces) -> list:
    """Update netbox lag interfaces
    - Update lag interfaces, which already exists in netbox

    :param parsed_interfaces: parsed interfaces for netbox operations
    """

    RESULTS = []

    # Init connection to Netbox via PyNetbox
    nb = Netbox.connect()

    # find the device instance in netbox
    dev = nb.dcim.devices.get(host.data['id'])

    # NETBOX LAG INTERFACES
    NB_LAG_INTERFACES = nb.dcim.interfaces.filter(device_id=dev.id, type='lag')
    NB_LAG_INTERFACES_dict = {ifc.name: ifc for ifc in [
        ifc for ifc in NB_LAG_INTERFACES]}

    # NETBOX LAG CHILDREN
    NB_LAG_CHILDREN = nb.dcim.interfaces.filter(
        device_id=dev.id, lag_id__n='null')
    NB_LAG_CHILDREN_dict = {ifc.name: ifc for ifc in [
        ifc for ifc in NB_LAG_CHILDREN]}

    for parent_lag, children_of_lag in parsed_lag_interfaces.items():
        nb_parent_lag_ifc = nb.dcim.interfaces.get(
            device_id=dev.id, name__ie=canonical_interface_name_edited(parent_lag))

        # if parent not found in netbox, skip to next record
        if not nb_parent_lag_ifc:
            RESULTS.append(
                NetboxResult(result=f"Parent LAG interface: {parent_lag} - could not be found in netbox on device: {host.name}", diff={
                }, action=Action.LOOKUP, status=Status.ANOMALLY)
            )
            continue

        # Skip IGNORED interfaces
        if nb_parent_lag_ifc.custom_fields.get("ignore_importer", False) == True:
            RESULTS.append(NetboxResult(
                result=f"{nb_parent_lag_ifc.name} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.LOOKUP, diff=""))
            NB_LAG_INTERFACES_dict.pop(nb_parent_lag_ifc.name, None)

        else:
            # SET parent interface as lag
            RESULTS.append(interface_parent_update(
                nb_ifc=nb_parent_lag_ifc, params={'type': 'lag'}))

            # Pop processed parent of already existing lags
            NB_LAG_INTERFACES_dict.pop(nb_parent_lag_ifc.name, None)

        for lag_child in children_of_lag:
            nb_child_ifc = nb.dcim.interfaces.get(
                device_id=dev.id, name__ie=canonical_interface_name_edited(lag_child))

            # if child not found in netbox, skip to next record
            if not nb_child_ifc:
                RESULTS.append(
                    NetboxResult(result=f"Child interface {canonical_interface_name_edited(lag_child)} could not be found in netbox on device {host.name}",
                                 action=Action.LOOKUP, status=Status.ANOMALLY, diff={})

                )
                continue

            # Skip IGNORED interfaces
            if nb_child_ifc.custom_fields.get("ignore_importer", False) == True:
                RESULTS.append(NetboxResult(
                    result=f"{nb_child_ifc.name} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.LOOKUP, diff=""))
                NB_LAG_CHILDREN_dict.pop(nb_child_ifc.name, None)
                continue
            elif nb_parent_lag_ifc.custom_fields.get("ignore_importer", False) == True:
                RESULTS.append(NetboxResult(
                    result=f"{nb_child_ifc.name} - PARENT Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.LOOKUP, diff=""))
                NB_LAG_CHILDREN_dict.pop(nb_child_ifc.name, None)
                continue
            else:
                # set parent to a child interface
                RESULTS.append(interface_child_update(
                    nb_ifc=nb_child_ifc, params={'lag': nb_parent_lag_ifc}))

                # Pop processed child of alredy existing children
                NB_LAG_CHILDREN_dict.pop(nb_child_ifc.name, None)

    # TODO: Process (remove) lags which are not parsed
    # unset parent
    for ifc_name, nb_ifc in NB_LAG_CHILDREN_dict.items():
        RESULTS.append(interface_child_update(
            nb_ifc=nb_ifc, params={'lag': None}))

    # change type from lag to virtual
    # TODO: Lag without children can exists
    for ifc_name, nb_ifc in NB_LAG_INTERFACES_dict.items():
        RESULTS.append(interface_parent_update(
            nb_ifc=nb_ifc, params={'type': get_netbox_interface_type(ifc_name)}))

    return RESULTS


def interface_parent_update(nb_ifc, params):
    before = get_changes_parent_interface(nb_ifc)

    if nb_ifc.update(params):
        # TODO: Reload ifc
        nb_ifc = nb_ifc.api.dcim.interfaces.get(nb_ifc.id)
        after = get_changes_parent_interface(nb_ifc)

        return NetboxResult(
            result=f"{nb_ifc.name} - LAG updated successfully",
            status=Status.CHANGED,
            action=Action.UPDATE,
            diff=get_diff(before, after)
        )
    else:
        return NetboxResult(
            result=f"{nb_ifc.name} - LAG - nothing to update",
            status=Status.NOT_CHANGED,
            action=Action.UPDATE,
            diff={}
        )


def interface_child_update(nb_ifc, params):
    before = get_changes_child_interface(nb_ifc)

    if nb_ifc.update(params):
        # TODO: Reload ifc
        nb_ifc = nb_ifc.api.dcim.interfaces.get(nb_ifc.id)
        after = get_changes_child_interface(nb_ifc)

        return NetboxResult(
            result=f"{nb_ifc.name} - LAG - Parent set successfully",
            status=Status.CHANGED,
            action=Action.UPDATE,
            diff=get_diff(before, after)
        )
    else:
        return NetboxResult(
            result=f"{nb_ifc.name} - nothing to update",
            status=Status.NOT_CHANGED,
            action=Action.UPDATE,
            diff={}
        )


def get_changes_parent_interface(nb_ifc):
    return {'type': nb_ifc.type.label}


def get_changes_child_interface(nb_ifc):
    if nb_ifc.lag:
        return {'lag': nb_ifc.lag.name}
    else:
        return {'lag': None}
