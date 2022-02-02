
import requests
from nornir_scrapli.tasks import netconf_edit_config, netconf_unlock, netconf_lock, netconf_discard, netconf_commit
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file

from datetime import datetime
import json



nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")


def load_vars(task):
    data = task.run(task=load_yaml, 
    file=f"./Nornir-Automation/host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    test_templates(task)


def test_templates(task):
    template = task.run(task=template_file, template="netospf.j2", 
    path="Nornir-Automation/templates")
    task.host["snmp_config"] = template.result
    rendered = task.host["snmp_config"]
    configuration = rendered.splitlines()
    task.run(task=netconf_edit_config, target="running", config=configuration)


results = nr.run(task=load_vars)
print_result(results)