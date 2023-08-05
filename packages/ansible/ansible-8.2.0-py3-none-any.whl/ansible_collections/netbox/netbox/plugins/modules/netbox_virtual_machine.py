#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Gaelle Mangin (@gmangin)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_virtual_machine
short_description: Create, update or delete virtual_machines within NetBox
description:
  - Creates, updates or removes virtual_machines from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Gaelle MANGIN (@gmangin)
requirements:
  - pynetbox
version_added: '0.1.0'
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    type: dict
    description:
      - Defines the virtual machine configuration
    suboptions:
      name:
        description:
          - The name of the virtual machine
        required: true
        type: str
      site:
        description:
          - The name of the site attach to the virtual machine
        required: false
        type: raw
      cluster:
        description:
          - The name of the cluster attach to the virtual machine
        required: false
        type: raw
      virtual_machine_role:
        description:
          - The role of the virtual machine
        required: false
        type: raw
      vcpus:
        description:
          - Number of vcpus of the virtual machine
        required: false
        type: float
      tenant:
        description:
          - The tenant that the virtual machine will be assigned to
        required: false
        type: raw
      platform:
        description:
          - The platform of the virtual machine
        required: false
        type: raw
      primary_ip4:
        description:
          - Primary IPv4 address assigned to the virtual machine
        required: false
        type: raw
      primary_ip6:
        description:
          - Primary IPv6 address assigned to the virtual machine
        required: false
        type: raw
      memory:
        description:
          - Memory of the virtual machine (MB)
        required: false
        type: int
      disk:
        description:
          - Disk of the virtual machine (GB)
        required: false
        type: int
      device:
        description:
          - The device the virtual machine is pinned to in the cluster
        required: false
        type: raw
        version_added: "3.9.0"
      status:
        description:
          - The status of the virtual machine
        required: false
        type: raw
      tags:
        description:
          - Any tags that the virtual machine may need to be associated with
        required: false
        type: list
        elements: raw
      custom_fields:
        description:
          - Must exist in NetBox
        required: false
        type: dict
      local_context_data:
        description:
          - configuration context of the virtual machine
        required: false
        type: dict
      description:
        description:
          - The description of the virtual machine
        required: false
        type: str
        version_added: "3.10.0"
      comments:
        description:
          - Comments of the virtual machine
        required: false
        type: str
    required: true
"""

EXAMPLES = r"""
- name: "Test NetBox modules"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create virtual machine within NetBox with only required information
      netbox_virtual_machine:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Virtual Machine
          cluster: test cluster
        state: present

    - name: Delete virtual machine within netbox
      netbox_virtual_machine:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Virtual Machine
        state: absent

    - name: Create virtual machine with tags
      netbox_virtual_machine:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Another Test Virtual Machine
          cluster: test cluster
          site: Test Site
          tags:
            - Schnozzberry
        state: present

    - name: Update vcpus, memory and disk of an existing virtual machine
      netbox_virtual_machine:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Virtual Machine
          cluster: test cluster
          vcpus: 8
          memory: 8
          disk: 8
        state: present
"""

RETURN = r"""
virtual machine:
  description: Serialized object as created or already existent within NetBox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_virtualization import (
    NetboxVirtualizationModule,
    NB_VIRTUAL_MACHINES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    site=dict(required=False, type="raw"),
                    cluster=dict(required=False, type="raw"),
                    virtual_machine_role=dict(required=False, type="raw"),
                    vcpus=dict(required=False, type="float"),
                    tenant=dict(required=False, type="raw"),
                    platform=dict(required=False, type="raw"),
                    primary_ip4=dict(required=False, type="raw"),
                    primary_ip6=dict(required=False, type="raw"),
                    memory=dict(required=False, type="int"),
                    disk=dict(required=False, type="int"),
                    device=dict(required=False, type="raw"),
                    status=dict(required=False, type="raw"),
                    tags=dict(required=False, type="list", elements="raw"),
                    custom_fields=dict(required=False, type="dict"),
                    local_context_data=dict(required=False, type="dict"),
                    description=dict(required=False, type="str"),
                    comments=dict(required=False, type="str"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_virtual_machine = NetboxVirtualizationModule(module, NB_VIRTUAL_MACHINES)
    netbox_virtual_machine.run()


if __name__ == "__main__":  # pragma: no cover
    main()
