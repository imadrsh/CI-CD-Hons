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

# Select which features are to be pushed onto the devices
# Load the host_vars from the devices' respective files & temporarily save them under the "facts" key of each device
def load_vars(task):
    features_to_push = ["ntp","bgp"]
    host_data = task.run(task=load_yaml, 
    file=f"./Nornir-Automation/host_vars/{task.host}.yaml")
    task.host["facts"] = host_data.result
    for feature in features_to_push:
        configure_feature(task, feature)


# Build the configuration to be pushed from the Jinja2 templates & device's "facts"
def configure_feature(task, feature):
    feature_get_template = task.run(task=template_file,
            name=f"Building {feature} configuration",
            template=f"{feature}.j2",
            path="Nornir-Automation/templates")

    feature_template = feature_get_template.result


results = nr.run(task=load_vars)
print_result(results)