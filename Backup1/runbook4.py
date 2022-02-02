from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="/home/imad/Nornir-Automation/config.yaml")


def test_templates(task):
    template = task.run(
        task=template_file, template="k2.j2", path="/home/imad/Nornir-Automation"
    )
    task.host["_config"] = template.result
    rendered = task.host["_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)


results = nr.run(task=test_templates)
print_result(results)