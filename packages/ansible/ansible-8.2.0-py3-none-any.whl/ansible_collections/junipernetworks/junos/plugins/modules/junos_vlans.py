#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for junos_vlans
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: junos_vlans
short_description: VLANs resource module
description:
- This module creates and manages VLAN configurations on Junos OS.
version_added: 1.0.0
author: Daniel Mellado (@dmellado)
requirements:
- ncclient (>=v0.6.4)
notes:
- This module requires the netconf system service be enabled on the remote device
  being managed
- Tested against Junos OS 18.4R1
- This module works with connection C(netconf).
- See L(the Junos OS Platform Options,https://docs.ansible.com/ansible/latest/network/user_guide/platform_junos.html).
options:
  config:
    description: A dictionary of Vlan options
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
        - IEEE 802.1q VLAN identifier for VLAN (1..4094).
        type: int
      name:
        description:
        - Name of VLAN.
        type: str
        required: true
      description:
        description:
        - Text description of VLANs
        type: str
      l3_interface:
        description:
        - Name of logical layer 3 interface.
        type: str
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the Junos device
      by executing the command B(show vlans).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result
    type: str
  state:
    description:
    - The state of the configuration after module completion.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - parsed
    - rendered
    default: merged
"""

EXAMPLES = """
# Using merged
#
# Before state
# ------------
#
# vagrant@vsrx# show vlans
#
# [edit]

- name: Merge provided Junos vlans config with running-config
  junipernetworks.junos.junos_vlans:
    config:
    - name: vlan1
      vlan_id: 1
    - name: vlan2
      vlan_id: 2
      l3_interface: irb.12
    state: merged
#
# -------------------------
# Module Execution Result
# -------------------------
#     "after": [
#         {
#             "name": "vlan1",
#             "vlan_id": 1
#         },
#         {
#             "l3_interface": "irb.12",
#             "name": "vlan2",
#             "vlan_id": 2
#         }
#     ],
#     "before": [],
#     "changed": true,
#     "commands": [
#         "<nc:vlans xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">"
#         "<nc:vlan><nc:name>vlan1</nc:name><nc:vlan-id>1</nc:vlan-id></nc:vlan>"
#         "<nc:vlan><nc:name>vlan2</nc:name><nc:vlan-id>2</nc:vlan-id><nc:l3-interface>irb.12</nc:l3-interface>"
#         "</nc:vlan></nc:vlans>"
#     ]
# After state
# -----------
#
# vagrant@vsrx# show vlans
# vlan1 {
#     vlan-id 1;
# }
# vlan2 {
#     vlan-id 2;
#     l3-interface irb.12;
# }

# Using replaced
#
# Before state
# ------------
#
# vagrant@vsrx# show vlans
# vlan1 {
#     vlan-id 1;
# }
# vlan2 {
#     vlan-id 2;
#     l3-interface irb.12;
# }

- name: Replace Junos vlans running-config with the provided config
  junipernetworks.junos.junos_vlans:
    config:
    - name: vlan1
      vlan_id: 11
      l3_interface: irb.10

    - name: vlan2
      vlan_id: 2
    state: replaced
# -------------------------
# Module Execution Result
# -------------------------
#     "after": [
#         {
#             "l3_interface": "irb.10",
#             "name": "vlan1",
#             "vlan_id": 11
#         },
#         {
#             "name": "vlan2",
#             "vlan_id": 2
#         }
#     ],
#     "before": [
#         {
#             "name": "vlan1",
#             "vlan_id": 1
#         },
#         {
#             "l3_interface": "irb.12",
#             "name": "vlan2",
#             "vlan_id": 2
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "<nc:vlans xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">"
#         "<nc:vlan delete="delete"><nc:name>vlan1</nc:name></nc:vlan>"
#         "<nc:vlan delete="delete"><nc:name>vlan2</nc:name></nc:vlan>"
#         "<nc:vlan><nc:name>vlan1</nc:name><nc:vlan-id>11</nc:vlan-id>"
#         "<nc:l3-interface>irb.10</nc:l3-interface></nc:vlan><nc:vlan>"
#         "<nc:name>vlan2</nc:name><nc:vlan-id>2</nc:vlan-id></nc:vlan></nc:vlans>"
#     ]
# After state
# -----------
#
# vagrant@vsrx# show vlans
# vlan1 {
#     vlan-id 11;
#     l3-interface irb.10;
# }
# vlan2 {
#     vlan-id 2;
# }
#
# Using overridden
#
# Before state
# ------------
#
# vagrant@vsrx# show vlans
# vlan1 {
#     vlan-id 11;
#     l3-interface irb.10;
# }
# vlan2 {
#     vlan-id 2;
# }
- name: Override Junos running-config with provided config
  junipernetworks.junos.junos_vlans:
    config:
    - name: vlan3
      vlan_id: 3
      l3_interface: irb.13
    state: overridden
# -------------------------
# Module Execution Result
# -------------------------
#     "after": [
#         {
#             "l3_interface": "irb.13",
#             "name": "vlan3",
#             "vlan_id": 3
#         }
#     ],
#     "before": [
#         {
#             "l3_interface": "irb.10",
#             "name": "vlan1",
#             "vlan_id": 11
#         },
#         {
#             "name": "vlan2",
#             "vlan_id": 2
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "<nc:vlans xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">"
#         "<nc:vlan delete="delete"><nc:name>vlan1</nc:name></nc:vlan><nc:vlan delete="delete">"
#         "<nc:name>vlan2</nc:name></nc:vlan><nc:vlan><nc:name>vlan3</nc:name><nc:vlan-id>3</nc:vlan-id>"
#         "<nc:l3-interface>irb.13</nc:l3-interface></nc:vlan></nc:vlans>"
#     ]
# After state
# -----------
#
# vagrant@vsrx# show vlans
# vlan3 {
#     vlan-id 3;
#     l3-interface irb.13;
# }
#
# Using deleted
#
# Before state
# ------------
#
# vagrant@vsrx# show vlans
# vlan3 {
#     vlan-id 3;
#     l3-interface irb.13;
# }
- name: Delete specific vlan
  junipernetworks.junos.junos_vlans:
    config:
    - name: vlan3
    state: deleted
# -------------------------
# Module Execution Result
# -------------------------
#     "after": [],
#     "changed": true,
#     "commands": [
#         "<nc:vlans xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
#         "<nc:vlan delete="delete"><nc:name>vlan3</nc:name></nc:vlan></nc:vlans>"
#     ]
# After state
# -----------
#
# vagrant@vsrx# show vlans
# vlan1 {
#     vlan-id 11;
#     l3-interface irb.10;
# }
# vlan2 {
#     vlan-id 2;
# }


- name: Gather running vlans configuration
  junipernetworks.junos.junos_vlans:
    state: gathered
#
# -------------------------
# Module Execution Result
# -------------------------
#     "gathered": [
#         {
#             "l3_interface": "irb.10",
#             "name": "vlan1",
#             "vlan_id": 11
#         },
#         {
#             "name": "vlan2",
#             "vlan_id": 2
#         }
#     ],
#     "changed": false,
#
# Using rendered
#
# Before state
# ------------
#
- name: Render xml for provided facts.
  junipernetworks.junos.junos_vlans:
    config:
    - name: vlan1
      vlan_id: 1

    - name: vlan2
      vlan_id: 2
      l3_interface: irb.12
    state: rendered
#
# -------------------------
# Module Execution Result
# -------------------------
#     "rendered": [
#         "<nc:vlans xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">"
#         "<nc:vlan><nc:name>vlan1</nc:name><nc:vlan-id>1</nc:vlan-id></nc:vlan>"
#         "<nc:vlan><nc:name>vlan2</nc:name><nc:vlan-id>2</nc:vlan-id><nc:l3-interface>irb.12</nc:l3-interface>"
#         "</nc:vlan></nc:vlans>"
#     ]
# Using parsed
# parsed.cfg
# ------------
# <?xml version="1.0" encoding="UTF-8"?>
# <rpc-reply message-id="urn:uuid:0cadb4e8-5bba-47f4-986e-72906227007f">
#     <configuration changed-seconds="1590139550" changed-localtime="2020-05-22 09:25:50 UTC">
#         <version>18.4R1-S2.4</version>
#         <vlans>
#           <vlan>
#             <name>vlan1</name>
#             <vlan-id>1</vlan-id>
#           </vlan>
#           <vlan>
#             <name>vlan2</name>
#             <vlan-id>2</vlan-id>
#             <l3-interface>irb.12</l3-interface>
#           </vlan>
#        </vlans>
#     </configuration>
# </rpc-reply>

- name: Parse routing instance running config
  junipernetworks.junos.junos_vlans:
    running_config: "{{ lookup('file', './parsed.cfg') }}"
    state: parsed
#
#
# -------------------------
# Module Execution Result
# -------------------------
#
#
# "parsed":  [
#         {
#             "name": "vlan1",
#             "vlan_id": 1
#         },
#         {
#             "l3_interface": "irb.12",
#             "name": "vlan2",
#             "vlan_id": 2
#         }
#     ]
#
"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['<nc:vlans xmlns:nc=\"urn:ietf:params:xml:ns:netconf:base:1.0\">
            <nc:vlan><nc:name>vlan1</nc:name><nc:vlan-id>1</nc:vlan-id>
            </nc:vlan><nc:vlan><nc:name>vlan2</nc:name><nc:vlan-id>2</nc:vlan-id>
            <nc:l3-interface>irb.12</nc:l3-interface></nc:vlan></nc:vlans>', 'xml 2', 'xml 3']
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.argspec.vlans.vlans import (
    VlansArgs,
)
from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.config.vlans.vlans import (
    Vlans,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]

    module = AnsibleModule(
        argument_spec=VlansArgs.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    result = Vlans(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
