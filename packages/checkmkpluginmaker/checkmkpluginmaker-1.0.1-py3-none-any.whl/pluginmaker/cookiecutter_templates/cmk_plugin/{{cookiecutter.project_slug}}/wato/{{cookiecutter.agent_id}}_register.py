#!/usr/bin/env python3
# to local/share/check_mk/web/plugins/wato

#import required to register agent
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextInput,
    TextAscii
)
from cmk.gui.plugins.wato import (
    IndividualOrStoredPassword,
    RulespecGroup,
    monitoring_macro_help,
    rulespec_group_registry,
    rulespec_registry,
    HostRulespec,
)
#import structure where special agent will be registered
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourcePrograms

#Some WATO form definition, to ask user for port number
def _valuespec_special_agent_myspecial():
    return Dictionary(
        title=_("{{cookiecutter.wato_title}}"),
        help=_("{{cookiecutter.wato_description}}"),
        optional_keys=[],
        elements=[
            ("name", TextAscii(title=_("Name displayed on Service check"), default_value="Default")),
            ("warning", Integer(title=_("Warning threshold"), default_value=-100)),
            ("critical", Integer(title=_("Critical threshold"), default_value=-150)),
            (
                "oid", 
                TextAscii(
                    title=_("oid value"), 
                    default_value='1.3.6.1.4.1.3607.2.30.1.1.1.3.16395.2.10'  # default value, you could change   
                )
            ),
        ],
        # Add or remove elements on your need
    )

# -------------------------------------
# All set, DO NOT MODIFY
# In that piece of code we registering Special Agent
#
rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourcePrograms,
        #IMPORTANT, name must follow special_agents:<name>, 
        #where filename of our special agent located in path local/share/check_mk/agents/special/ is  agent_<name>
        name="special_agents:{{cookiecutter.agent_id}}",
        valuespec=_valuespec_special_agent_myspecial,
    ))
