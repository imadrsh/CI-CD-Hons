
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")

def configure_stuff(task):
    template_to_load = task.run (task=template_file, template="netospf.j2" , path="/home/imad/Nornir-Automation/templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="running", config=configuration)

results = nr.run(task=configure_stuff)
print_result(results)