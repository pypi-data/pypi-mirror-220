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
The module file for junos_lldp_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: junos_lldp_global
short_description: LLDP resource module
description:
- This module manages link layer discovery protocol (LLDP) attributes on Juniper JUNOS
  devices.
version_added: 1.0.0
author: Ganesh Nalawade (@ganeshrn)
options:
  config:
    description: The list of link layer discovery protocol attribute configurations
    type: dict
    suboptions:
      enabled:
        description:
        - This argument is a boolean value to enabled or disable LLDP.
        type: bool
      interval:
        description:
        - Frequency at which LLDP advertisements are sent (in seconds).
        type: int
      address:
        description:
        - This argument sets the management address from LLDP.
        type: str
      transmit_delay:
        description:
        - Specify the number of seconds the device waits before sending advertisements
          to neighbors after a change is made in local system.
        type: int
      hold_multiplier:
        description:
        - Specify the number of seconds that LLDP information is held before it is
          discarded. The multiplier value is used in combination with the C(interval)
          value.
        type: int
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the Junos device
      by executing the command B(show protocols lldp).
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
    - deleted
    - gathered
    - rendered
    - parsed
    default: merged
requirements:
- ncclient (>=v0.6.4)
notes:
- This module requires the netconf system service be enabled on the remote device
  being managed.
- Tested against vSRX JUNOS version 18.4R1.
- This module works with connection C(netconf). See L(the Junos OS Platform Options,../network/user_guide/platform_junos.html).
"""
EXAMPLES = """
# Using merged
# Before state:
# -------------
# user@junos01# # show protocols lldp
#
- name: Merge provided configuration with device configuration
  junipernetworks.junos.junos_lldp_global:
    config:
      interval: 10000
      address: 10.1.1.1
      transmit_delay: 400
      hold_multiplier: 10
    state: merged

# After state:
# -------------
# user@junos01# show protocols lldp
# management-address 10.1.1.1;
# advertisement-interval 10000;
# transmit-delay 400;
# hold-multiplier 10;

# Using replaced
# Before state:
# -------------
# user@junos01# show protocols lldp
# management-address 10.1.1.1;
# advertisement-interval 10000;
# transmit-delay 400;
# hold-multiplier 10;

- name: Replace provided configuration with device configuration
  junipernetworks.junos.junos_lldp_global:
    config:
      address: 20.2.2.2
      hold_multiplier: 30
      enabled: false
    state: replaced

# After state:
# -------------
# user@junos01# show protocols lldp
# disable;
# management-address 20.2.2.2;
# hold-multiplier 30;

# Using deleted
# Before state:
# -------------
# user@junos01# show protocols lldp
# management-address 20.2.2.2;
# hold-multiplier 30;

- name: Delete lldp configuration (this will by default remove all lldp configuration)
  junipernetworks.junos.junos_lldp_global:
    state: deleted

# After state:
# -------------
# user@junos01# # show protocols lldp
#
#
# Using gathered
# Before state:
# ------------
#
# ansible@cm123456tr21# show protocols lldp
# management-address 10.1.1.1;
# advertisement-interval 10000;
# transmit-delay 400;
# hold-multiplier 10;
# interface ge-0/0/1;
# interface ge-0/0/2 {
#     disable;
# }
- name: Gather junos lldp_global as in given arguments
  junipernetworks.junos.junos_lldp_global:
    state: gathered
# Task Output (redacted)
# -----------------------
#
# "gathered": {
#         "address": "10.1.1.1",
#         "hold_multiplier": 10,
#         "interval": 10000,
#         "transmit_delay": 400
#     }
# After state:
# ------------
#
# ansible@cm123456tr21# show protocols lldp
# management-address 10.1.1.1;
# advertisement-interval 10000;
# transmit-delay 400;
# hold-multiplier 10;
# interface ge-0/0/1;
# interface ge-0/0/2 {
#     disable;
# }
# Using rendered
- name: Render platform specific xml from task input using rendered state
  junipernetworks.junos.junos_lldp_global:
    config:
      interval: 10000
      address: 10.1.1.1
      transmit_delay: 400
      hold_multiplier: 10
    state: rendered
# Task Output (redacted)
# -----------------------
# "rendered": "<nc:protocols
#     xmlns:nc=\"urn:ietf:params:xml:ns:netconf:base:1.0\">
#     <nc:lldp>
#         <nc:management-address>10.1.1.1</nc:management-address>
#         <nc:advertisement-interval>10000</nc:advertisement-interval>
#         <nc:transmit-delay>400</nc:transmit-delay>
#         <nc:hold-multiplier>10</nc:hold-multiplier>
#         <nc:disable delete=\"delete\"/>
#     </nc:lldp>
# </nc:protocols>"
#
# parsed.cfg
# ------------
#
# <?xml version="1.0" encoding="UTF-8"?>
# <rpc-reply message-id="urn:uuid:0cadb4e8-5bba-47f4-986e-72906227007f">
#     <configuration changed-seconds="1590139550" changed-localtime="2020-05-22 09:25:50 UTC">
#         <protocols>
#             <ospf>
#                 <area>
#                     <name>0.0.0.0</name>
#                     <interface>
#                         <name>ge-0/0/0.0</name>
#                     </interface>
#                 </area>
#             </ospf>
#             <lldp>
#                 <management-address>10.1.1.1</management-address>
#                 <advertisement-interval>10000</advertisement-interval>
#                 <transmit-delay>400</transmit-delay>
#                 <hold-multiplier>10</hold-multiplier>
#                 <interface>
#                     <name>ge-0/0/1</name>
#                 </interface>
#                 <interface>
#                     <name>ge-0/0/2</name>
#                     <disable/>
#                 </interface>
#             </lldp>
#         </protocols>
#     </configuration>
# </rpc-reply>
# - name: Convert lldp global config to argspec without connecting to the appliance
#   junipernetworks.junos.junos_lldp_global:
#     running_config: "{{ lookup('file', './parsed.cfg') }}"
#     state: parsed
# Task Output (redacted)
# -----------------------
# "parsed": {
#         "address": "10.1.1.1",
#         "hold_multiplier": 10,
#         "interval": 10000,
#         "transmit_delay": 400
#     }
"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: dict
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: dict
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['<nc:protocols
    xmlns:nc=\"urn:ietf:params:xml:ns:netconf:base:1.0\">
    <nc:lldp>
        <nc:management-address>10.1.1.1</nc:management-address>
        <nc:advertisement-interval>10000</nc:advertisement-interval>
        <nc:transmit-delay>400</nc:transmit-delay>
        <nc:hold-multiplier>10</nc:hold-multiplier>
        <nc:disable delete=\"delete\"/>
    </nc:lldp>
</nc:protocols>', 'xml 2', 'xml 3']
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.argspec.lldp_global.lldp_global import (
    Lldp_globalArgs,
)
from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.config.lldp_global.lldp_global import (
    Lldp_global,
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
        ("state", "parsed", ("running_config",)),
    ]

    module = AnsibleModule(
        argument_spec=Lldp_globalArgs.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    result = Lldp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
