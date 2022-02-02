from distutils.command.config import config
import requests
from nornir_scrapli.tasks import netconf_edit_config, netconf_unlock, netconf_lock, netconf_discard, netconf_commit
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.filter import F
from datetime import datetime
import json

nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")


def load_vars(task):

    host_data = task.run(task=load_yaml, file= f"Nornir-Automation/host_vars/{task.host}.yaml")
    task.host["facts"] = host_data.result


def configure_k2(task):
    template_to_load = task.run(task=template_file, template="k2.j2",path="/home/imad/Nornir-Automation")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)


    var = nr.run(task=load_vars)
    print_result(var)

    config = nr.run(task=configure_k2)
    print_result(config)