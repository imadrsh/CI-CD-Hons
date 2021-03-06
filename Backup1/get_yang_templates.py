from warnings import filters
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result


nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")

def get_yang(task):
    task.run(task=netconf_get_config, 
    source="running", filter_type="xpath", filters="/native/router")


results = nr.run(task=get_yang)
print_result(results)