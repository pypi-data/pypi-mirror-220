# Nornir helper functions
from netbox_network_importer.helper import remove_key_from_results
from netbox_network_importer.outputers.output import html_output, json_output
from netbox_network_importer.processors.save_netbox_results import SaveNetboxResults
from nornir_rich.progress_bar import RichProgressBar
from nornir_rich.functions import print_result
from nornir_utils.plugins.functions import print_title
# Nornir tasks
from netbox_network_importer.tasks.connection_test import connection_test
from netbox_network_importer.tasks.synchronizer import synchronize_interfaces, synchronize_interfaces_lags, synchronize_interfaces_ips, synchronize_interfaces_vlans, synchronize_serials
# Connections
from netbox_network_importer.connections.Nornir import Nornir
from netbox_network_importer.connections.PyAts import PyAtsNetbox
from netbox_network_importer.connections.Netbox import Netbox
# System
import os
import click
# logging
from netbox_network_importer.config import setup_logger
from loguru import logger
import logging as old_logging
old_logging.getLogger('urllib3.connectionpool').setLevel(old_logging.INFO)
old_logging.getLogger('pyats').setLevel(old_logging.ERROR)
old_logging.getLogger('git').setLevel(old_logging.INFO)
old_logging.getLogger('genie').setLevel(old_logging.INFO)
old_logging.getLogger('nornir.core').setLevel(old_logging.WARN)
old_logging.getLogger('genie.utils.summary').setLevel(old_logging.ERROR)
old_logging.getLogger('genie.ops.base.maker').setLevel(old_logging.WARNING)
old_logging.getLogger('blib2to3.pgen2.driver').setLevel(old_logging.ERROR)
old_logging.getLogger('paramiko.transport').setLevel(old_logging.CRITICAL)
old_logging.getLogger('netmiko').setLevel(old_logging.CRITICAL)
old_logging.getLogger('napalm').setLevel(old_logging.CRITICAL)
old_logging.getLogger('pyats.contrib.creators.netbox').setLevel(
    old_logging.CRITICAL)



@click.group()
@click.option('--configs', '-c', type=click.Path(), multiple=False, help="path to folder with configurations")
def cli(configs):
    # set custom configs folder path
    if configs:
        os.environ["CONFIG_FOLDER_PATH"] = os.path.abspath(configs)


@cli.command()
@click.option('--device', '-d',  type=str, multiple=False, required=True, help="Run on specificied device")
@click.option('--command', '-c',  type=str, multiple=False, required=True, help="Run command e.g. show version")
def pyats(device, command):
    """
    Connect to device using pyats and pynetbox and print parsed command
    """

    pyats = PyAtsNetbox()
    nb = Netbox.connect()

    nb_dev = nb.dcim.devices.get(name=device)
    hostname = nb_dev.name

    dev = pyats.connect_device(hostname)

    from pprint import pprint
    pprint(dev.parse(command))


@cli.command()
@click.option('--devices', '-d',  type=str, multiple=True, help="Run on specificied devices")
@click.option('--platforms', '-p',  type=str, multiple=True, help="Run on specificied platforms")
@click.option('--no-progress-bar', is_flag=True)
@logger.catch
# CLI callable command
def synchronize(devices, platforms, no_progress_bar):
    """Run set of Nornir task to update data in Netbox from network devices

    Args:
        devices (str): device name filter, can be used multiple times
        platforms (str): platform name filter, can be used multiple times
        no_progress_bar (bool): use to hide progress bar
    Returns:
        dict: Dictionary of hosts, it's actions and results
    """

    result_data = run_synchronizer(devices, platforms, no_progress_bar)
    return result_data


def run_synchronizer(devices, platforms, no_progress_bar=True):
    """Run set of Nornir task to update data in Netbox from network devices

    Args:
        devices (str): device name filter, can be used multiple times
        platforms (str): platform name filter, can be used multiple times
        no_progress_bar (bool): use to hide progress bar
    Returns:
        dict: Dictionary of hosts, it's actions and results
    """
    # Init logging
    if not no_progress_bar:
        setup_logger(file=True, stderr=False)
    else:
        setup_logger()

    # store netbox process results into a dict
    save_netbox_results_data = {}

    # init devices (nornir) with Netbox
    # filter out devices without IP or Platform

    nr = Nornir.init_nornir_w_netbox(
        filter_parameters={"name": devices, "platform": platforms, 'has_primary_ip': True, 'platform_id__n': "null", "status": "active"})

    # init device connector with pyAts via Netbox
    # filter out devices without IP or Platform
    nb_pyats_devices = PyAtsNetbox(
        url_filter="platform_id__n=null&has_primary_ip=True")

    print_result_keys = ["name", "result", "diff", "exception"]

    # Connection Test - Skip failed hosts from this action
    print_title("Connection Test")
    nr = nr.with_processors(get_processors(
        save_netbox_results_data, no_progress_bar))
    connection_tests = nr.run(task=connection_test, pyats=nb_pyats_devices)
    print_result(connection_tests, vars=print_result_keys, expand=True)

    skipped_hosts = []
    if connection_tests.failed_hosts:
        # Skip failed hosts in other processing
        for host, result in connection_tests.failed_hosts.items():
            skipped_hosts.append(host)
            # remove host from other processing
            nr.inventory.hosts.pop(host)
        print_title(f"SKIPPING HOSTS: {skipped_hosts}")

    # Create/Update Netbox Interaces
    save_netbox_results_data = run_task(task_method=synchronize_serials,
                                        skipped_hosts=skipped_hosts,
                                        result_dict_data=save_netbox_results_data,
                                        no_progress_bar=no_progress_bar,
                                        print_result_keys=print_result_keys,
                                        nornir=nr,
                                        pyats=nb_pyats_devices)

    # Create/Update Netbox Interaces
    save_netbox_results_data = run_task(task_method=synchronize_interfaces,
                                        skipped_hosts=skipped_hosts,
                                        result_dict_data=save_netbox_results_data,
                                        no_progress_bar=no_progress_bar,
                                        print_result_keys=print_result_keys,
                                        nornir=nr,
                                        pyats=nb_pyats_devices)

    # CRUD Netbox LAGs
    save_netbox_results_data = run_task(task_method=synchronize_interfaces_lags,
                                        skipped_hosts=skipped_hosts,
                                        result_dict_data=save_netbox_results_data,
                                        no_progress_bar=no_progress_bar,
                                        print_result_keys=print_result_keys,
                                        nornir=nr,
                                        pyats=nb_pyats_devices)

    # CRUD netbox IPs on interfaces
    save_netbox_results_data = run_task(task_method=synchronize_interfaces_ips,
                                        skipped_hosts=skipped_hosts,
                                        result_dict_data=save_netbox_results_data,
                                        no_progress_bar=no_progress_bar,
                                        print_result_keys=print_result_keys,
                                        nornir=nr,
                                        pyats=nb_pyats_devices)

    # Create VLANs
    save_netbox_results_data = run_task(task_method=synchronize_interfaces_vlans,
                                        skipped_hosts=skipped_hosts,
                                        result_dict_data=save_netbox_results_data,
                                        no_progress_bar=no_progress_bar,
                                        print_result_keys=print_result_keys,
                                        nornir=nr,
                                        pyats=nb_pyats_devices)

    netbox_result_data_without_not_changed = remove_key_from_results(
        save_netbox_results_data, "NOT_CHANGED")
    json_output(save_netbox_results_data)
    html_output(netbox_result_data_without_not_changed)

    return save_netbox_results_data


def get_processors(netbox_result_data: dict, no_progress_bar=False):
    """Returns list of processors
    Created because of reseting RichProgressBar - if it's
    not reset, then it will print bad data

    Args:
        no_progress_bar (bool, optional): Wheter to use use RichProgressBar or not. Defaults to False.
        netbox_result_data (dict, optional): Dict, which will be filled with data.

    Returns:
        _type_: list of processors
    """
    processors = [SaveNetboxResults(netbox_result_data)]
    if not no_progress_bar:
        processors.append(RichProgressBar())
    return processors


def post_process_skipped_hosts(complete_task, skipped_hosts, data) -> dict:
    for skipped_host in skipped_hosts:
        data[skipped_host][complete_task.name] = {"skipped": True}
    return data


def run_task(task_method, skipped_hosts, result_dict_data, no_progress_bar, print_result_keys, nornir, pyats):
    # Create/Update Netbox Interaces
    print_title(f"Running {task_method.__name__} - skipping {skipped_hosts}")
    # always call with_processors - otherwise progress bar gets crazy
    nr = nornir.with_processors(get_processors(
        result_dict_data, no_progress_bar))

    nr_run_result = nr.run(task=task_method, on_failed=True, pyats=pyats)
    # add info to complete result, that task was skipped
    result_dict_data = post_process_skipped_hosts(complete_task=nr_run_result,
                                                  skipped_hosts=skipped_hosts,
                                                  data=result_dict_data)
    print_result(nr_run_result, vars=print_result_keys, expand=True)

    return result_dict_data


if __name__ == "__main__":
    # Display CLI
    cli()

