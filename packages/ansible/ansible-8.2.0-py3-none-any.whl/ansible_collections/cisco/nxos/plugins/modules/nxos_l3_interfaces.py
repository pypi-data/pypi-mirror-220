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
The module file for nxos_l3_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: nxos_l3_interfaces
short_description: L3 interfaces resource module
description: This module manages Layer-3 interfaces attributes of NX-OS Interfaces.
version_added: 1.0.0
author: Trishna Guha (@trishnaguha)
notes:
- Tested against NXOS 7.3.(0)D1(1) on VIRL
- Unsupported for Cisco MDS
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section '^interface').
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A dictionary of Layer-3 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of L3 interface, i.e. Ethernet1/1.
        type: str
        required: true
      dot1q:
        description:
        - Configures IEEE 802.1Q VLAN encapsulation on a subinterface.
        type: int
      ipv4:
        description:
        - IPv4 address and attributes of the L3 interface.
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - IPV4 address of the L3 interface.
            type: str
          tag:
            description:
            - URIB route tag value for local/direct routes.
            type: int
          secondary:
            description:
            - A boolean attribute to manage addition of secondary IP address.
            type: bool
      ipv6:
        description:
        - IPv6 address and attributes of the L3 interface.
        type: list
        elements: dict
        suboptions:
          address:
            description:
            - IPV6 address of the L3 interface.
            type: str
          tag:
            description:
            - URIB route tag value for local/direct routes.
            type: int
      redirects:
        description:
        - Enables/disables ipv4 redirects.
        type: bool
      ipv6_redirects:
        description:
        - Enables/disables ipv6 redirects.
        type: bool
      unreachables:
        description:
        - Enables/disables ip redirects.
        type: bool
      evpn_multisite_tracking:
        description:
        -  VxLAN evpn multisite Interface tracking. Supported only on selected model.
        type: str
        version_added: 1.1.0
        choices:
        - fabric-tracking
        - dci-tracking
  state:
    description:
    - The state of the configuration after module completion.
    - The state I(overridden) would override the IP address configuration
      of all interfaces on the device with the provided configuration in
      the task. Use caution with this state as you may loose access to the
      device.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - rendered
    - parsed
    default: merged

"""
EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Merge provided configuration with device configuration.
  cisco.nxos.nxos_l3_interfaces:
    config:
    - name: Ethernet1/6
      ipv4:
      - address: 192.168.1.1/24
        tag: 5
      - address: 10.1.1.1/24
        secondary: true
        tag: 10
      ipv6:
      - address: fd5d:12c9:2201:2::1/64
        tag: 6
    - name: Ethernet1/7.42
      redirects: false
      unreachables: false
    state: merged

# Task Output
# -----------
#
# before:
# - name: Ethernet1/6
# - name: Ethernet1/7
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - ip address 192.168.1.1/24 tag 5
# - ip address 10.1.1.1/24 secondary tag 10
# - ipv6 address fd5d:12c9:2201:2::1/64 tag 6
# - interface Ethernet1/7
# - no ip redirects
# after:
# - ipv4:
#   - address: 192.168.1.1/24
#     tag: 5
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   ipv6:
#   - address: fd5d:12c9:2201:2::1/64
#     tag: 6
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.1.1/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management


# Using replaced

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.1.1/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Replace device configuration of specified L3 interfaces with provided configuration.
  cisco.nxos.nxos_l3_interfaces:
    config:
    - name: Ethernet1/6
      ipv4:
        - address: 192.168.22.3/24
    state: replaced

# Task Output
# -----------
#
# before:
# - ipv4:
#   - address: 192.168.1.1/24
#     tag: 5
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   ipv6:
#   - address: fd5d:12c9:2201:2::1/64
#     tag: 6
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - ip address 192.168.22.3/24
# - no ipv6 address fd5d:12c9:2201:2::1/64
# - ip redirects
# after:
# - ipv4:
#   - address: 192.168.22.3/24
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.22.3/24
#   ip address 10.1.1.1/24 secondary tag 10
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

# Using overridden

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.1.1/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface Ethernet1/7.42
#   no ip redirects
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Override device configuration with provided configuration.
  cisco.nxos.nxos_l3_interfaces:
    config:
    - ipv4:
      - address: dhcp
      name: mgmt0
    - name: Ethernet1/6
      ipv4:
      - address: 192.168.22.3/24
    state: overridden

# Task Output
# -----------
#
# before:
# - ipv4:
#   - address: 192.168.1.1/24
#     tag: 5
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   ipv6:
#   - address: fd5d:12c9:2201:2::1/64
#     tag: 6
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - name: Ethernet1/7.42
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - no ipv6 address fd5d:12c9:2201:2::1/64
# - no ip address 10.1.1.1/24 secondary
# - ip address 192.168.22.3/24
# - ip redirects
# - interface Ethernet1/7
# - ip redirects
# - interface Ethernet1/7.42
# - ip redirects
# after:
# - ipv4:
#   - address: 192.168.22.3/24
#   name: Ethernet1/6
# - name: Ethernet1/7
# - name: Ethernet1/7.42
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   ip address 192.168.22.3/24
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface Ethernet1/7.42
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

# Using deleted

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   ip address 192.168.22.3/24
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface Ethernet1/7.42
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Delete L3 attributes of given interfaces (This won't delete the interface
    itself).
  cisco.nxos.nxos_l3_interfaces:
    config:
    - name: Ethernet1/6
    - name: Ethernet1/2
    state: deleted

# Task Output
# -----------
#
# before:
# - name: Ethernet1/2
# - ipv4:
#   - address: 192.168.22.3/24
#   name: Ethernet1/6
# - name: Ethernet1/7
# - name: Ethernet1/7.42
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - no ip address
# after:
# - name: Ethernet1/2
# - name: Ethernet1/7
# - name: Ethernet1/7.42
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface Ethernet1/7.42
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

# Using rendered

- name: Use rendered state to convert task input to device specific commands
  cisco.nxos.nxos_l3_interfaces:
    config:
    - name: Ethernet1/800
      ipv4:
      - address: 192.168.1.100/24
        tag: 5
      - address: 10.1.1.1/24
        secondary: true
        tag: 10
    - name: Ethernet1/800
      ipv6:
      - address: fd5d:12c9:2201:2::1/64
        tag: 6
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - interface Ethernet1/800
#   - ip address 192.168.1.100/24 tag 5
#   - ip address 10.1.1.1/24 secondary tag 10
#   - interface Ethernet1/800
#   - ipv6 address fd5d:12c9:2201:2::1/64 tag 6

# Using parsed

# parsed.cfg
# ----------
#
# interface Ethernet1/800
#   ip address 192.168.1.100/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   no ip redirects
# interface Ethernet1/801
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   ip unreachables
# interface mgmt0
#   ip address dhcp
#   vrf member management

- name: Use parsed state to convert externally supplied config to structured format
  cisco.nxos.nxos_l3_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output
# -----------
#
# parsed:
#   - name: Ethernet1/800
#     ipv4:
#       - address: 192.168.1.100/24
#         tag: 5
#       - address: 10.1.1.1/24
#         secondary: True
#         tag: 10
#     redirects: False
#   - name: Ethernet1/801
#     ipv6:
#      - address: fd5d:12c9:2201:2::1/64
#        tag: 6
#     unreachables: True

# Using gathered

# Before state:
# -------------
#
# interface Ethernet1/1
#   ip address 192.0.2.100/24
# interface Ethernet1/2
#   no ip redirects
#   ip address 203.0.113.10/24
#   ip unreachables
#   ipv6 address 2001:db8::1/32

- name: Gather l3_interfaces facts from the device using nxos_l3_interfaces
  cisco.nxos.nxos_l3_interfaces:
    state: gathered

# Task output
# -----------
#
# gathered:
#   - name: Ethernet1/1
#     ipv4:
#       - address: 192.0.2.100/24
#   - name: Ethernet1/2
#     ipv4:
#       - address: 203.0.113.10/24
#     ipv6:
#       - address: 2001:db8::1/32
#     redirects: False
#     unreachables: True
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
  sample: ['interface Ethernet1/2', 'ip address 192.168.0.1/2']
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.l3_interfaces.l3_interfaces import (
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
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    result = L3_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
