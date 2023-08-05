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
The module file for eos_l3_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: eos_l3_interfaces
short_description: L3 interfaces resource module
description: This module provides declarative management of Layer 3 interfaces on
  Arista EOS devices.
version_added: 1.0.0
author: Nathaniel Case (@qalthos)
notes:
- Tested against Arista EOS 4.24.6F
- This module works with connection C(network_cli). See the L(EOS Platform Options,../network/user_guide/platform_eos.html).
  'eos_l2_interfaces/eos_interfaces' should be used for preparing the interfaces , before applying L3 configurations using
  this module (eos_l3_interfaces).
options:
  config:
    description: A dictionary of Layer 3 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of the interface, i.e. Ethernet1.
        type: str
        required: true
      ipv4:
        description:
        - List of IPv4 addresses to be set for the Layer 3 interface mentioned in
          I(name) option.
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - IPv4 address to be set in the format <ipv4 address>/<mask> eg. 192.0.2.1/24,
              or C(dhcp) to query DHCP for an IP address.
            type: str
          secondary:
            description:
            - Whether or not this address is a secondary address.
            type: bool
          virtual:
            description:
            - Whether or not this address is a virtual address.
            type: bool
      ipv6:
        description:
        - List of IPv6 addresses to be set for the Layer 3 interface mentioned in
          I(name) option.
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - IPv6 address to be set in the address format is <ipv6 address>/<mask>
              eg. 2001:db8:2201:1::1/64 or C(auto-config) to use SLAAC to chose an
              address.
            type: str
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the EOS device by
      executing the command B(show running-config | section ^interface).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
    - The state of the configuration after module completion
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - parsed
    - gathered
    - rendered
    default: merged

"""

EXAMPLES = """

# Using deleted

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 192.0.2.12/24
# !
# interface Ethernet2
#    ipv6 address 2001:db8::1/64
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config

- name: Delete L3 attributes of given interfaces.
  arista.eos.eos_l3_interfaces:
    config:
    - name: Ethernet1
    - name: Ethernet2
    state: deleted

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
# !
# interface Ethernet2
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config


# Using merged

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 192.0.2.12/24
# !
# interface Ethernet2
#    ipv6 address 2001:db8::1/64
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config

- name: Merge provided configuration with device configuration.
  arista.eos.eos_l3_interfaces:
    config:
    - name: Ethernet1
      ipv4:
      - address: 198.51.100.14/24
    - name: Ethernet2
      ipv4:
      - address: 203.0.113.27/24
    state: merged

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 198.51.100.14/24
# !
# interface Ethernet2
#    ip address 203.0.113.27/24
#    ipv6 address 2001:db8::1/64
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config


# Using overridden

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 192.0.2.12/24
# !
# interface Ethernet2
#    ipv6 address 2001:db8::1/64
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config

- name: Override device configuration of all L2 interfaces on device with provided
    configuration.
  arista.eos.eos_l3_interfaces:
    config:
    - name: Ethernet1
      ipv6:
      - address: 2001:db8:feed::1/96
    - name: Management1
      ipv4:
      - address: dhcp
    ipv6: auto-config
    state: overridden

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ipv6 address 2001:db8:feed::1/96
# !
# interface Ethernet2
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config


# Using replaced

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 192.0.2.12/24
# !
# interface Ethernet2
#    ipv6 address 2001:db8::1/64
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config

- name: Replace device configuration of specified L2 interfaces with provided configuration.
  arista.eos.eos_l3_interfaces:
    config:
    - name: Ethernet2
      ipv4:
      - address: 203.0.113.27/24
    state: replaced

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 192.0.2.12/24
# !
# interface Ethernet2
#    ip address 203.0.113.27/24
# !
# interface Management1
#    ip address dhcp
#    ipv6 address auto-config

# Using parsed:

# parsed.cfg
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 198.51.100.14/24
# !
# interface Ethernet2
#    ip address 203.0.113.27/24
# !

- name: Use parsed to convert native configs to structured data
  arista.eos.interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Output:

# parsed:
#    - name: Ethernet1
#      ipv4:
#        - address: 198.51.100.14/24
#    - name: Ethernet2
#      ipv4:
#        - address: 203.0.113.27/24

# Using rendered:

- name: Use Rendered to convert the structured data to native config
  arista.eos.eos_l3_interfaces:
    config:
    - name: Ethernet1
      ipv4:
      - address: 198.51.100.14/24
    - name: Ethernet2
      ipv4:
      - address: 203.0.113.27/24
    state: rendered

# Output
# ------------
#rendered:
#   - "interface Ethernet1"
#   - "ip address 198.51.100.14/24"
#   - "interface Ethernet2"
#   - "ip address 203.0.113.27/24"

# using gathered:

# Native COnfig:
# veos#show running-config | section interface
# interface Ethernet1
#    ip address 198.51.100.14/24
# !
# interface Ethernet2
#    ip address 203.0.113.27/24
# !

- name: Gather l3 interfaces facts from the device
  arista.eos.l3_interfaces:
    state: gathered

#    gathered:
#      - name: Ethernet1
#        ipv4:
#          - address: 198.51.100.14/24
#      - name: Ethernet2
#        ipv4:
#          - address: 203.0.113.27/24


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
  sample: ['interface Ethernet2', 'ip address 192.0.2.12/24']
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.arista.eos.plugins.module_utils.network.eos.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.config.l3_interfaces.l3_interfaces import (
    L3_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """

    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]
    module = AnsibleModule(
        argument_spec=L3_interfacesArgs.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive,
    )

    result = L3_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
