#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright(C) 2020 Inspur Inc. All Rights Reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
---
module: edit_fru
version_added: "1.0.0"
author:
    - WangBaoshan (@ispim)
short_description: Set fru settings
description:
   - Set fru settings on Inspur server.
notes:
   - Does not support C(check_mode).
options:
    attribute:
        description:
            - Attribute,CP is Chassis Part Number,CS is Chassis Serial,PM is Product Manufacturer,
            - PPN is Product Part Number,PS is Product Serial,PN is Product Name,PV is Product Version,
            - PAT is Product Asset Tag,BM is Board Mfg,BPN is Board Product Name,BS is Board Serial,
            - BP is Board Part Number.
        choices: ['CP', 'CS', 'PM', 'PPN', 'PS', 'PN', 'PV','PAT', 'BM', 'BPN', 'BS', 'BP']
        required: true
        type: str
    value:
        description:
            - Set the value of attribute.
        required: true
        type: str
extends_documentation_fragment:
    - inspur.ispim.ism
'''

EXAMPLES = '''
- name: Fru test
  hosts: ism
  connection: local
  gather_facts: no
  vars:
    ism:
      host: "{{ ansible_ssh_host }}"
      username: "{{ username }}"
      password: "{{ password }}"

  tasks:

  - name: "Set Fru"
    inspur.ispim.edit_fru:
      attribute: "CP"
      value: "Inspur"
      provider: "{{ ism }}"

'''

RETURN = '''
message:
    description: Messages returned after module execution.
    returned: always
    type: str
state:
    description: Status after module execution.
    returned: always
    type: str
changed:
    description: Check to see if a change was made on the device.
    returned: always
    type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.inspur.ispim.plugins.module_utils.ism import (ism_argument_spec, get_connection)


class UID(object):
    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()
        self.results = dict()

    def init_module(self):
        """Init module object"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=False)

    def run_command(self):
        self.module.params['subcommand'] = 'setfru'
        self.results = get_connection(self.module)
        if self.results['State'] == 'Success':
            self.results['changed'] = True

    def show_result(self):
        """Show result"""
        self.module.exit_json(**self.results)

    def work(self):
        """Worker"""
        self.run_command()
        self.show_result()


def main():
    argument_spec = dict(
        attribute=dict(type='str', required=True, choices=['CP', 'CS', 'PM', 'PPN', 'PS', 'PN', 'PV', 'PAT', 'BM', 'BPN', 'BS', 'BP']),
        value=dict(type='str', required=True),
    )
    argument_spec.update(ism_argument_spec)
    uid_obj = UID(argument_spec)
    uid_obj.work()


if __name__ == '__main__':
    main()
