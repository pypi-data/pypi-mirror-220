#!/usr/bin/env python3
from .agent_based_api.v1 import *


def discover_handler(section):
    yield Service()


def check_handler(section):
    # modify if you need
    for line in section:
        if 'OK' in line:
            # line look like ['OK', '-', 'Some', 'message', 'go', 'here']
            yield Result(state=State.OK, summary=f"{' '.join(line[2:])}")
            return

    yield Result(state=State.CRIT, summary=f"section {section}")
    

def agent_section_parser(string_table):
    # modify if you need
    return string_table


register.check_plugin(
    name = "{{cookiecutter.agent_id}}",
    service_name = "{{cookiecutter.service_name}}",
    discovery_function = discover_handler,
    check_function = check_handler,
)


register.agent_section(
    name="{{cookiecutter.agent_id}}",
    parse_function=agent_section_parser,
)
