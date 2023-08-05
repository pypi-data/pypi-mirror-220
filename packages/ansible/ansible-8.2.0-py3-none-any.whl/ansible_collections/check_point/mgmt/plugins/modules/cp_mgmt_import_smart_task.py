#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage CheckPoint Firewall (c) 2019
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: cp_mgmt_import_smart_task
short_description: Import SmartTask from a file.
description:
  - Import SmartTask from a file. <br>This command is available only in a Security Management environment or in Multi-Domain environment when logged into
    local domain.
  - All operations are performed over Web Services API.
version_added: "5.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  file_path:
    description:
      - Path to the SmartTask file to be imported. <br>Should be the full file path (example, "/home/admin/exported-smart-task.txt").
    type: str
    required: True
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: import-smart-task
  cp_mgmt_import_smart_task:
    file_path: /home/admin/smart-task.txt
"""

RETURN = """
cp_mgmt_import_smart_task:
  description: The checkpoint import-smart-task output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        file_path=dict(type='str', required=True)
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "import-smart-task"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
