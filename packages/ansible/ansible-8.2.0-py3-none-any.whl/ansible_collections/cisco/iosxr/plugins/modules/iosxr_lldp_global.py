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
The module file for iosxr_lldp_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: iosxr_lldp_global
short_description: Resource module to configure LLDP.
description:
- This module manages Global Link Layer Discovery Protocol (LLDP) settings on IOS-XR
  devices.
version_added: 1.0.0
notes:
- This module works with connection C(network_cli). See L(the IOS-XR Platform Options,../network/user_guide/platform_iosxr.html).
author: Nilashish Chakraborty (@NilashishC)
options:
  config:
    description: The provided global LLDP configuration.
    type: dict
    suboptions:
      holdtime:
        description:
        - Specifies the holdtime (in sec) to be sent in packets.
        type: int
      reinit:
        description:
        - Specifies the delay (in sec) for LLDP initialization on any interface.
        type: int
      subinterfaces:
        description:
        - Enable or disable LLDP over sub-interfaces.
        type: bool
      timer:
        description:
        - Specifies the rate at which LLDP packets are sent (in sec).
        type: int
      tlv_select:
        description:
        - Specifies the LLDP TLVs to enable or disable.
        type: dict
        suboptions:
          management_address:
            description:
            - Enable or disable management address TLV.
            type: bool
          port_description:
            description:
            - Enable or disable port description TLV.
            type: bool
          system_capabilities:
            description:
            - Enable or disable system capabilities TLV.
            type: bool
          system_description:
            description:
            - Enable or disable system description TLV.
            type: bool
          system_name:
            description:
            - Enable or disable system name TLV.
            type: bool
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the IOS-XR device
      by executing the command B(show running-config lldp).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
    - The state of the configuration after module completion.
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - parsed
    - gathered
    - rendered
    default: merged

"""
EXAMPLES = """
# Using merged
#
#
# -------------
# Before State
# -------------
#
#
# RP/0/0/CPU0:an-iosxr#sh run lldp
# Tue Aug  6 19:27:54.933 UTC
# % No such configuration item(s)
#
#

- name: Merge provided LLDP configuration with the existing configuration
  cisco.iosxr.iosxr_lldp_global:
    config:
      holdtime: 100
      reinit: 2
      timer: 3000
      subinterfaces: true
      tlv_select:
        management_address: false
        system_description: false
    state: merged

#
#
# ------------------------
# Module Execution Result
# ------------------------
#
#  "before": {}
#
#  "commands": [
#        "lldp subinterfaces enable",
#        "lldp holdtime 100",
#        "lldp reinit 2",
#        "lldp tlv-select system-description disable",
#        "lldp tlv-select management-address disable",
#        "lldp timer 3000"
#  ]
#
#  "after": {
#        "holdtime": 100,
#        "reinit": 2,
#        "subinterfaces": true,
#        "timer": 3000,
#        "tlv_select": {
#            "management_address": false,
#            "system_description": false
#        }
#  }
#
#
# ------------
# After state
# ------------
#
#
# RP/0/0/CPU0:an-iosxr#sh run lldp
# Tue Aug  6 21:31:10.587 UTC
# lldp
#  timer 3000
#  reinit 2
#  subinterfaces enable
#  holdtime 100
#  tlv-select
#   management-address disable
#   system-description disable
#  !
# !
#
#


# Using replaced
#
#
# -------------
# Before State
# -------------
#
# RP/0/0/CPU0:an-iosxr#sh run lldp
# Tue Aug  6 21:31:10.587 UTC
# lldp
#  timer 3000
#  reinit 2
#  subinterfaces enable
#  holdtime 100
#  tlv-select
#   management-address disable
#   system-description disable
#  !
# !
#
#

- name: Replace existing LLDP device configuration with provided configuration
  cisco.iosxr.iosxr_lldp_global:
    config:
      holdtime: 100
      tlv_select:
        port_description: false
        system_description: true
        management_description: true
    state: replaced

#
#
# ------------------------
# Module Execution Result
# ------------------------
#
#  "before": {
#        "holdtime": 100,
#        "reinit": 2,
#        "subinterfaces": true,
#        "timer": 3000,
#        "tlv_select": {
#            "management_address": false,
#            "system_description": false
#        }
#  }
#
#  "commands": [
#        "no lldp reinit 2",
#        "no lldp subinterfaces enable",
#        "no lldp timer 3000",
#        "no lldp tlv-select management-address disable",
#        "no lldp tlv-select system-description disable",
#        "lldp tlv-select port-description disable"
#  ]
#
#  "after": {
#        "holdtime": 100,
#        "tlv_select": {
#            "port_description": false
#        }
#  }
#
#
# ------------
# After state
# ------------
#
# RP/0/0/CPU0:an-iosxr#sh run lldp
# Tue Aug  6 21:53:08.407 UTC
# lldp
#  holdtime 100
#  tlv-select
#   port-description disable
#  !
# !
#
#


# Using deleted
#
# ------------
# Before state
# ------------
#
#
# RP/0/0/CPU0:an-iosxr#sh run lldp
# Tue Aug  6 21:31:10.587 UTC
# lldp
#  timer 3000
#  reinit 2
#  subinterfaces enable
#  holdtime 100
#  tlv-select
#   management-address disable
#   system-description disable
#  !
# !
#
#

- name: Deleted existing LLDP configurations from the device
  cisco.iosxr.iosxr_lldp_global:
    state: deleted

#
#
# ------------------------
# Module Execution Result
# ------------------------
#
#  "before": {
#        "holdtime": 100,
#        "reinit": 2,
#        "subinterfaces": true,
#        "timer": 3000,
#        "tlv_select": {
#            "management_address": false,
#            "system_description": false
#        }
#  },
#
#  "commands": [
#        "no lldp holdtime 100",
#        "no lldp reinit 2",
#        "no lldp subinterfaces enable",
#        "no lldp timer 3000",
#        "no lldp tlv-select management-address disable",
#        "no lldp tlv-select system-description disable"
#  ]
#
#  "after": {}
#
#
# -----------
# After state
# -----------
#
# RP/0/0/CPU0:an-iosxr#sh run lldp
# Tue Aug  6 21:38:31.187 UTC
# lldp
# !
#
# Using parsed:

# parsed.cfg
# lldp
#  timer 3000
#  reinit 2
#  subinterfaces enable
#  holdtime 100
#  tlv-select
#   management-address disable
#   system-description disable
#  !
# !

- name: Convert lldp global config to argspec without connecting to the appliance
  cisco.iosxr.iosxr_lldp_global:
    running_config: "{{ lookup('file', './parsed.cfg') }}"
    state: parsed

# ------------------------
# Module Execution Result
# ------------------------
# parsed:
#     holdtime: 100
#     reinit: 2
#     timer: 3000
#     subinterfaces: True
#     tlv_select:
#       management_address: False
#       system_description: False

# using gathered:

# Device config:
# lldp
#  timer 3000
#  reinit 2
#  subinterfaces enable
#  holdtime 100
#  tlv-select
#   management-address disable
#   system-description disable
#  !
# !

- name: Gather IOSXR lldp global configuration
  cisco.iosxr.iosxr_lldp_global:
    config:
    state: gathered


# ------------------------
# Module Execution Result
# ------------------------
# gathered:
#     holdtime: 100
#     reinit: 2
#     timer: 3000
#     subinterfaces: True
#     tlv_select:
#       management_address: False
#       system_description: False

# using rendered:

- name: Render platform specific commands from task input using rendered state
  cisco.iosxr.iosxr_lldp_global:
    config:
      holdtime: 100
      reinit: 2
      timer: 3000
      subinterfaces: true
      tlv_select:
        management_address: false
        system_description: false
    state: rendered

#
#
# ------------------------
# Module Execution Result
# ------------------------
#
#  "rendered": [
#        "lldp subinterfaces enable",
#        "lldp holdtime 100",
#        "lldp reinit 2",
#        "lldp tlv-select system-description disable",
#        "lldp tlv-select management-address disable",
#        "lldp timer 3000"
#  ]



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
  sample: ['lldp subinterfaces enable', 'lldp holdtime 100', 'no lldp tlv-select management-address disable']
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.argspec.lldp_global.lldp_global import (
    Lldp_globalArgs,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.config.lldp_global.lldp_global import (
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
    mutually_exclusive = [("config", "running_config")]
    module = AnsibleModule(
        argument_spec=Lldp_globalArgs.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive,
    )

    result = Lldp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
