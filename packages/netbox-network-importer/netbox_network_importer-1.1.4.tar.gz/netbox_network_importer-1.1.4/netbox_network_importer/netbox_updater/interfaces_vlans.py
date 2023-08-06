from netbox_network_importer.connections.Netbox import Netbox
from netbox_network_importer.helper import get_diff
from netbox_network_importer.results.results import NetboxResult, Status, Action


def process_interfaces_vlans(host, parsed_data) -> list([NetboxResult]):
    RESULTS = []  # list of NetboxResult

    # Init connection to Netbox via PyNetbox
    netbox = Netbox.connect()

    # find the device instance in netbox
    netbox_device = netbox.dcim.devices.get(host.data['id'])

    # INIT Dictionary of stored vlans in NETBOX
    # if configured vlan is found, it will be removed from dict
    # vlans left in dictionary will be removed at the end
    netbox_interfaces_with_vlan = get_interfaces_with_vlan(
        netbox_conn=netbox, device_id=netbox_device.id)

    vlans_interfaces = parsed_data['vlans_interfaces']
    vlans_trunks = parsed_data['vlans_trunks']
    vlans = parsed_data['vlans']

    for interface_name, ifc_vlan_data in vlans_interfaces.items():
        netbox_ifc = netbox.dcim.interfaces.get(
            device_id=netbox_device.id, name__ie=interface_name)

        # skip if interface is not found in netbox
        if not netbox_ifc:
            RESULTS.append(
                NetboxResult(
                    result=f"Interface {interface_name} NOT FOUND in Netbox - check interface configuration on device",
                    status=Status.CHECK_MANUALLY,
                    action=Action.LOOKUP,
                    diff=ifc_vlan_data,
                )
            )
            continue

        # Skip IGNORED interfaces
        if netbox_ifc.custom_fields.get("ignore_importer", False) == True:
            RESULTS.append(NetboxResult(
                result=f"{netbox_ifc.name} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.LOOKUP, diff=""))
            continue

        # Assign multiple tagged vlan to interface
        if ifc_vlan_data['vlan'] == 'trunk':
            netbox_vlans = []

            # if interface is not found in configured TRUNKS
            if not vlans_trunks.get(interface_name):
                if netbox_ifc.lag != None:
                    NetboxResult(
                        result=f"Device: {host.name} Interface: {interface_name} mode: trunk. Part of port channel",
                        status=Status.NOT_CHANGED,
                        action=Action.LOOKUP,
                        diff=None
                    )
                    continue
                elif ifc_vlan_data.get("status", None) == 'disabled' or ifc_vlan_data.get("status", None) == 'notconnect':
                    continue
                else:
                    #RESULTS.append(
                    #    NetboxResult(
                    #        result=f"Device: {host.name} Interface: {interface_name} mode: trunk. Unable to parse trunks from device",
                    #        status=Status.CHECK_MANUALLY,
                    #        action=Action.LOOKUP,
                    #        diff={"vlan_data": ifc_vlan_data,
                    #              "trunks": vlans_trunks}
                    #    )
                    #)
                    continue

            vlans_vids_allowed_on_trunk = vlans_trunks[interface_name]['vlan_list']

            # Go through each vlan vid in trunk mode and assing it
            for vid_integer in vlans_vids_allowed_on_trunk:
                # convert vlan_vid int to string
                vid = str(vid_integer)

                # TODO: what if name does not exists
                vname = vlans.get(vid, {}).get('name')
                if not vname:
                    # TODO: Ignore vid;s which does not have crated VLANs
                    #RESULTS.append(
                    #    NetboxResult(
                    #        result=f"Device: {host.name} Interface: {interface_name} has configured VLAN ID: {vid}. But VLAN does not exists on Device.",
                    #        status=Status.CHECK_MANUALLY,
                    #        action=Action.LOOKUP,
                    #        diff={"host": host.name, "ifc": interface_name,
                    #              "vid": vid, "vlan_vid_data": vlans.get(vid, None)}
                    #    )
                    #)
                    continue

                # Skip VID == 1, skip 999?
                if vid == '1':
                    continue

                try:
                    RESULTS.append(create_vlan(
                        vname=vname, vid=vid, netbox_conn=netbox))
                    netbox_vlan = netbox.ipam.vlans.get(
                        vid=vid, name=vname, site_id='null')

                    netbox_vlans.append(netbox_vlan)
                except Exception as e:
                    RESULTS.append(
                        NetboxResult(
                            result=f"Unable to get/create vlan {vname} {vid} - Processing VLANs is aborted",
                            status=Status.EXCEPTION,
                            action=Action.LOOKUP,
                            exception=e,
                            diff={}
                        )
                    )
                    # end processing
                    return RESULTS

                # remove vlan from already configured vlans on interface (if exists)
                # vlans left in alredy configured vlans will be removed
                netbox_interfaces_with_vlan = remove_configured_vlan(
                    configured_vlan=netbox_interfaces_with_vlan,
                    ifc_name=netbox_ifc.name,
                    vid=netbox_vlan.vid,
                    vname=vname,
                    vlan_type='tagged_vlans')

            # assign VLAN to interface
            RESULTS.append(add_tagged_vlans_to_interface(
                netbox_ifc=netbox_ifc, netbox_vlans=netbox_vlans))

        elif ifc_vlan_data['vlan'] == 'routed':
            if ifc_vlan_data.get("status", None) == 'disabled' or ifc_vlan_data.get("status", None) == 'notconnect':
                continue
            else:
                RESULTS.append(
                    NetboxResult(
                        result=f"IFC: {netbox_ifc.name}, type {ifc_vlan_data['vlan']} - SKIPPING",
                        status=Status.NOT_CHANGED,
                        action=Action.LOOKUP,
                        diff={}
                    )
                )
                continue

        elif ifc_vlan_data['vlan'] in ['unassigned', 'unassigne']:
            continue

        # Assign untagged vlan to interface
        else:
            vid = str(ifc_vlan_data['vlan'])
            vname = vlans.get(vid, {}).get('name')
            if not vname:
                RESULTS.append(
                    NetboxResult(
                        result=f"Device: {host.name} Interface: {interface_name} has configured VLAN ID: {vid}. But VLAN does not exists on Device.",
                        status=Status.CHECK_MANUALLY,
                        action=Action.LOOKUP,
                        diff={"host": host.name, "ifc": interface_name,
                              "vid": vid, "vlan_vid_data": vlans.get(vid, None)}
                    )
                )
                continue

            if vid == '1':
                continue

            try:
                RESULTS.append(create_vlan(
                    vname=vname, vid=vid, netbox_conn=netbox))
                netbox_vlan = netbox.ipam.vlans.get(
                    vid=vid, name=vname, site_id='null')
            except Exception as e:
                RESULTS.append(
                    NetboxResult(
                        result=f"Unable to get/create vlan {vname} {vid} - Processing VLANs is aborted",
                        status=Status.EXCEPTION,
                        action=Action.LOOKUP,
                        exception=e,
                        diff={}
                    )
                )
                # end processing
                return RESULTS

            # add vlan to interface
            RESULTS.append(add_untagged_vlan_to_interface(
                netbox_ifc=netbox_ifc, netbox_vlan=netbox_vlan))

            # remove vlan from dictionary of already exisitng vlans in netbox (if exists)
            netbox_interfaces_with_vlan = remove_configured_vlan(configured_vlan=netbox_interfaces_with_vlan,
                                                                 ifc_name=netbox_ifc.name,
                                                                 vid=netbox_vlan.vid,
                                                                 vname=vname,
                                                                 vlan_type='untagged_vlan')

    # REMOVE vlan from interfaces which are not configured anymore
    # all vlans left in netbox_interfaces_with_vlan
    RESULTS.extend(delete_netbox_obsolete_vlans(
        vlans_to_remove=netbox_interfaces_with_vlan, netbox_device=netbox_device, netbox=netbox))
    return RESULTS


def add_tagged_vlans_to_interface(netbox_ifc, netbox_vlans):
    before = get_changes_tagged_vlans(netbox_ifc)

    for netbox_vlan in netbox_vlans:
        if not netbox_vlan in netbox_ifc.tagged_vlans:
            netbox_ifc.mode = 'tagged'
            netbox_ifc.tagged_vlans.append(netbox_vlan)

    after = get_changes_tagged_vlans(netbox_ifc)
    if netbox_ifc.save():
        return NetboxResult(status=Status.CHANGED,
                            diff=get_diff(before, after),
                            action=Action.CREATE,
                            result=f"{netbox_ifc.name} mode {netbox_ifc.mode} and VLANs ({netbox_vlans}) saved")
    else:
        return NetboxResult(status=Status.NOT_CHANGED,
                            diff=get_diff(before, after),
                            action=Action.CREATE,
                            result=f"{netbox_ifc.name} mode {netbox_ifc.mode}. VLANs already exists ({netbox_ifc.tagged_vlans})")


def remove_tagged_vlans_from_interface(netbox_vlans, netbox_ifc):
    before = get_changes_tagged_vlans(netbox_ifc)

    for identifier, nb_vlan in netbox_vlans.items():
        if nb_vlan in netbox_ifc.tagged_vlans:
            netbox_ifc.tagged_vlans.remove(nb_vlan)

    if not netbox_ifc.untagged_vlan and not netbox_ifc.tagged_vlans:
        netbox_ifc.mode = ""

    if netbox_ifc.save():
        netbox_ifc = netbox_ifc.api.dcim.interfaces.get(netbox_ifc.id)
        return NetboxResult(
            action=Action.DELETE,
            status=Status.CHANGED,
            result=f"Netbox tagged vlans {list(netbox_vlans.keys())} were removed from interface {netbox_ifc.name}",
            diff={"remove": [{"vid": vlan[0], "name": vlan[1]}
                             for vlan in netbox_vlans]}
        )
    else:
        return NetboxResult(
            action=Action.DELETE,
            status=Status.CHECK_MANUALLY,
            result=f"Unable to remove tagged vlans {netbox_vlans.keys()} from interface {netbox_ifc.name}",
            diff={}
        )


def add_untagged_vlan_to_interface(netbox_ifc, netbox_vlan):
    if netbox_vlan:
        before = get_changes_untagged_vlan(netbox_ifc)
        netbox_ifc.mode = 'access'
        netbox_ifc.untagged_vlan = netbox_vlan
    else:
        return NetboxResult(
            status=Status.FAILED,
            action=Action.LOOKUP,
            diff={},
            result=f"Vlan not found in netbox {netbox_ifc}, {netbox_vlan}")

    after = get_changes_untagged_vlan(netbox_ifc)
    if netbox_ifc.save():
        return NetboxResult(status=Status.CHANGED,
                            diff=get_diff(before, after),
                            action=Action.CREATE,
                            result=f"{netbox_ifc.name} mode {netbox_ifc.mode} and VLAN ({netbox_vlan.display}) saved")
    else:
        return NetboxResult(status=Status.NOT_CHANGED,
                            diff=get_diff(before, after),
                            action=Action.CREATE,
                            result=f"{netbox_ifc.name} mode {netbox_ifc.mode} and VLAN ({netbox_vlan.display}) already exists")


def remove_untagged_vlan_from_interface(netbox_vlan, netbox_ifc):
    before = get_changes_untagged_vlan(netbox_ifc)

    if netbox_ifc.untagged_vlan == netbox_vlan:
        netbox_ifc.untagged_vlan = None
        if not netbox_ifc.untagged_vlan and not netbox_ifc.tagged_vlans:
            netbox_ifc.mode = None

        if netbox_ifc.save():
            reload_ifc = netbox_ifc.api.dcim.interfaces.get(netbox_ifc.id)
            after = get_changes_untagged_vlan(reload_ifc)

            return NetboxResult(
                result=f"Untagged vlan: {netbox_vlan.display} removed from {netbox_ifc.name} - {netbox_ifc.device.name}",
                status=Status.CHANGED,
                action=Action.DELETE,
                exception=None,
                diff=get_diff(before, after)
            )
        else:
            return NetboxResult(
                result=f"Untagged vlan: {netbox_vlan.display} could not be removed from {netbox_ifc.name} - {netbox_ifc.device.name}",
                status=Status.ANOMALLY,
                action=Action.DELETE,
                exception=None,
                diff={}
            )
    else:
        return NetboxResult(
            result=f"Untagged vlan: {netbox_vlan.display} was already changed to {netbox_ifc.untagged_vlan.display} on {netbox_ifc.name} - {netbox_ifc.device.name}",
            status=Status.NOT_CHANGED,
            action=Action.UPDATE,
            exception=None,
            diff={}
        )


def create_vlan(vname, vid, netbox_conn):
    try:
        # lookup for vlan in netbox,
        # could raises error when multiple vlans are returned
        nb_vlan = netbox_conn.ipam.vlans.get(
            vid=vid, name=vname, site_id='null')
    except Exception as e:
        raise e

    if not nb_vlan:
        try:
            if netbox_conn.ipam.vlans.create({'vid': vid, 'name': vname}):
                return NetboxResult(status=Status.CHANGED,
                                    diff={'vid': vid, 'name': vname},
                                    action=Action.CREATE,
                                    result=f"Creating vlan ID: {vid} Name: {vname}")
            else:
                return NetboxResult(status=Status.ANOMALLY,
                                    diff={},
                                    action=Action.CREATE,
                                    result=f"Unable to create - Vlan ID: {vid} Name: {vname}")
        except Exception as e:
            # if request error on create, try to find again !!!
            # WORKAROUND: sometimes other thread creates a vlan in netbox before this action
            nb_vlan = netbox_conn.ipam.vlans.get(
                vid=vid, name=vname, site_id='null')
            if nb_vlan:
                return NetboxResult(status=Status.NOT_CHANGED,
                                    diff={},
                                    action=Action.CREATE,
                                    result=f"Vlan ID: {vid} Name: {vname} already exists")
            else:
                # TODO:
                raise e
    else:
        return NetboxResult(status=Status.NOT_CHANGED,
                            diff={},
                            action=Action.CREATE,
                            result=f"Vlan ID: {vid} Name: {vname} already exists")


def delete_netbox_obsolete_vlans(vlans_to_remove, netbox_device, netbox):
    RESULTS = []
    for ifc, type_vlans in vlans_to_remove.items():
        nb_ifc = netbox.dcim.interfaces.get(
            device_id=netbox_device.id, name=ifc)

        # Skip IGNORED interfaces
        if nb_ifc.custom_fields.get("ignore_importer", False) == True:
            RESULTS.append(NetboxResult(
                result=f"{nb_ifc.name} - Ignored by Importer - Skipping", status=Status.SKIPPED, action=Action.DELETE, diff=""))
            continue

        if type_vlans.get('untagged_vlan'):
            nb_vlan = type_vlans.get('untagged_vlan')
            RESULTS.append(
                remove_untagged_vlan_from_interface(nb_vlan, nb_ifc))

        if type_vlans.get('tagged_vlans'):
            tagged_vlans = type_vlans.get('tagged_vlans')
            # Remove all tagged_vlans at once
            RESULTS.append(remove_tagged_vlans_from_interface(
                tagged_vlans, nb_ifc))

    return RESULTS


def remove_configured_vlan(configured_vlan, ifc_name, vid, vname, vlan_type):
    if vlan_type == 'untagged_vlan':
        if configured_vlan.get(ifc_name):
            if configured_vlan[ifc_name].get(vlan_type):
                if configured_vlan[ifc_name][vlan_type].vid == vid:
                    configured_vlan[ifc_name].pop(vlan_type)

    if vlan_type == 'tagged_vlans':
        if configured_vlan.get(ifc_name):
            if configured_vlan[ifc_name].get(vlan_type):
                configured_vlan[ifc_name][vlan_type].pop((vid, vname), None)

    return configured_vlan


def get_interfaces_with_vlan(netbox_conn, device_id):
    tagged = get_tagged_vlans_interfaces(netbox_conn, device_id)
    untagged = get_untagged_vlan_interfaces(netbox_conn, device_id)

    merged_dict = {}

    for ifc, vlans in tagged.items():
        if merged_dict.get(ifc, None):
            merged_dict[ifc].update(vlans)
        else:
            merged_dict[ifc] = vlans

    for ifc, vlan in untagged.items():
        if merged_dict.get(ifc, None):
            merged_dict[ifc].update(vlan)
        else:
            merged_dict[ifc] = vlan

    return merged_dict


def get_tagged_vlans_interfaces(netbox_conn, device_id):
    """ return FORMAT
        {'GigabitEthernet0/2/16': {'tagged_vlans': {(1, 'default'): PYNETBOX_OBJECT,
                                            (12, 'dwdm-T6'): PYNETBOX_OBJECT}}
    """
    res = {
        ifc.name: {"tagged_vlans": {(vlan.vid, vlan.name): vlan for vlan in [
            vlan for vlan in ifc.tagged_vlans]}}
        for ifc in netbox_conn.dcim.interfaces.filter(device_id=device_id) if ifc.tagged_vlans
    }

    return res


def get_untagged_vlan_interfaces(netbox_conn, device_id):
    res = {
        ifc.name: {"untagged_vlan": ifc.untagged_vlan}
        for ifc in netbox_conn.dcim.interfaces.filter(device_id=device_id) if ifc.untagged_vlan
    }

    return res


def get_changes_tagged_vlans(netbox_ifc):
    # return {vlan.vid: vlan.name for vlan in netbox_ifc.tagged_vlans}
    return [{"name": vlan.name, "vid": vlan.vid} for vlan in netbox_ifc.tagged_vlans]


def get_changes_untagged_vlan(netbox_ifc):
    if netbox_ifc.untagged_vlan:
        return {"vid": netbox_ifc.untagged_vlan.vid, "name": netbox_ifc.untagged_vlan.name}
    else:
        return {}
