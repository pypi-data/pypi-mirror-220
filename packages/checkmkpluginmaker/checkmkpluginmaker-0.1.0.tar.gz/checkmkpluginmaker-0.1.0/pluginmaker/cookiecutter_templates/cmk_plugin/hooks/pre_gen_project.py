import re
import sys


def check_agent_id():
    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
    agent_id = '{{ cookiecutter.agent_id }}'
    if not re.match(MODULE_REGEX, agent_id):
        msg = 'ERROR: agent_id get value "%s" is not a valid! Only allowed chars: a-z | A-Z | _' % agent_id
        return False, msg
    if not (8<= len(agent_id) <=30):
        msg = 'ERROR: agent_id get value "%s" is exceeded length! Only allowed 8-30 chars' % agent_id
        return False, msg
    return True, None

def check_project_slug():
    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
    project_slug = '{{ cookiecutter.project_slug }}'
    if not re.match(MODULE_REGEX, project_slug):
        msg = 'ERROR: project_slug get value "%s" is not a valid! Only allowed chars: a-z | A-Z | _' % project_slug
        return False, msg
    if not (8<= len(project_slug) <=30):
        msg = 'ERROR: project_slug get value "%s" is exceeded length! Only allowed 8-30 chars' % project_slug
        return False, msg
    return True, None


def run_the_checks():
    is_failed = False
    msg = '\n'
    for check in (
        check_agent_id,
        check_project_slug,
    ):
        is_passed, check_msg = check()
        if is_passed is False:
            msg = msg + '\n' + check_msg
            is_failed = True
        
    if is_failed:
        # exits with status 1 to indicate failure
        print(msg + '\n\n')
        sys.exit(1)

if __name__ == '__main__':
    run_the_checks()