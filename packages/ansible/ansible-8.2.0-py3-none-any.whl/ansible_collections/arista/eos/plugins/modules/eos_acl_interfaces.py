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
The module file for eos_acl_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: eos_acl_interfaces
short_description: ACL interfaces resource module
description:
- This module manages adding and removing Access Control Lists (ACLs) from interfaces
  on devices running EOS software.
version_added: 1.0.0
author: GomathiSelvi S (@GomathiselviS)
options:
  config:
    description: A dictionary of ACL options for interfaces.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name/Identifier for the interface.
        type: str
        required: true
      access_groups:
        type: list
        elements: dict
        description:
        - Specifies ACLs attached to the interfaces.
        suboptions:
          afi:
            description:
            - Specifies the AFI for the ACL(s) to be configured on this interface.
            type: str
            choices:
            - ipv4
            - ipv6
            required: true
          acls:
            type: list
            description:
            - Specifies the ACLs for the provided AFI.
            elements: dict
            suboptions:
              name:
                description:
                - Specifies the name of the IPv4/IPv4 ACL for the interface.
                type: str
                required: true
              direction:
                description:
                - Specifies the direction of packets that the ACL will be applied
                  on.
                type: str
                choices:
                - in
                - out
                required: true
  running_config:
    description:
    - The module, by default, will connect to the remote device and retrieve the current
      running-config to use as a base for comparing against the contents of source.
      There are times when it is not desirable to have the task get the current running-config
      for every task in a playbook.  The I(running_config) argument allows the implementer
      to pass in the configuration to use as the base config for comparison. This
      value of this option should be the output received from device by executing
      command
    type: str
  state:
    description:
    - The state the configuration should be left in.
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
# Using Merged

# Before state:
# -------------
#
# eos#sh running-config | include interface|access-group
# interface Ethernet1
# interface Ethernet2
# interface Ethernet3

- name: Merge module attributes of given access-groups
  arista.eos.eos_acl_interfaces:
    config:
    - name: Ethernet2
      access_groups:
      - afi: ipv4
        acls:
          name: acl01
          direction: in
      - afi: ipv6
        acls:
          name: acl03
          direction: out
    state: merged

# Commands Fired:
# ---------------
#
# interface Ethernet2
# ip access-group acl01 in
# ipv6 access-group acl03 out

# After state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Loopback888
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 in
#  ipv6 access-group acl03 out
# interface Ethernet3


# Using Replaced

# Before state:
# -------------
#
# eos#sh running-config | include interface|access-group
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 in
#  ipv6 access-group acl03 out
# interface Ethernet3
#  ip access-group acl01 in

- name: Replace module attributes of given access-groups
  arista.eos.eos_acl_interfaces:
    config:
    - name: Ethernet2
      access_groups:
      - afi: ipv4
        acls:
          name: acl01
          direction: out
    state: replaced

# Commands Fired:
# ---------------
#
# interface Ethernet2
# no ip access-group acl01 in
# no ipv6 access-group acl03 out
# ip access-group acl01 out

# After state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Loopback888
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 out
# interface Ethernet3
#  ip access-group acl01 in


# Using Overridden

# Before state:
# -------------
#
# eos#sh running-config | include interface|access-group
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 in
#  ipv6 access-group acl03 out
# interface Ethernet3
#  ip access-group acl01 in

- name: Override module attributes of given access-groups
  arista.eos.eos_acl_interfaces:
    config:
    - name: Ethernet2
      access_groups:
      - afi: ipv4
        acls:
          name: acl01
          direction: out
    state: overridden

# Commands Fired:
# ---------------
#
# interface Ethernet2
# no ip access-group acl01 in
# no ipv6 access-group acl03 out
# ip access-group acl01 out
# interface Ethernet3
# no ip access-group acl01 in

# After state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Loopback888
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 out
# interface Ethernet3


# Using Deleted

# Before state:
# -------------
#
# eos#sh running-config | include interface|access-group
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 in
#  ipv6 access-group acl03 out
# interface Ethernet3
#  ip access-group acl01 out

- name: Delete module attributes of given access-groups
  arista.eos.eos_acl_interfaces:
    config:
    - name: Ethernet2
      access_groups:
      - afi: ipv4
        acls:
          name: acl01
          direction: in
      - afi: ipv6
        acls:
          name: acl03
          direction: out
    state: deleted

# Commands Fired:
# ---------------
#
# interface Ethernet2
# no ip access-group acl01 in
# no ipv6 access-group acl03 out

# After state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Loopback888
# interface Ethernet1
# interface Ethernet2
# interface Ethernet3
#  ip access-group acl01 out


# Before state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 in
#  ipv6 access-group acl03 out
# interface Ethernet3
#  ip access-group acl01 out

- name: Delete module attributes of given access-groups from ALL Interfaces
  arista.eos.eos_acl_interfaces:
    config:
    state: deleted

# Commands Fired:
# ---------------
#
# interface Ethernet2
# no ip access-group acl01 in
# no ipv6 access-group acl03 out
# interface Ethernet3
# no ip access-group acl01 out

# After state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Loopback888
# interface Ethernet1
# interface Ethernet2
# interface Ethernet3

# Before state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Ethernet1
# interface Ethernet2
#  ip access-group acl01 in
#  ipv6 access-group acl03 out
# interface Ethernet3
#  ip access-group acl01 out

- name: Delete acls under afi
  arista.eos.eos_acl_interfaces:
    config:
    - name: Ethernet3
      access_groups:
      - afi: ipv4
    - name: Ethernet2
      access_groups:
      - afi: ipv6
    state: deleted

# Commands Fired:
# ---------------
#
# interface Ethernet2
# no ipv6 access-group acl03 out
# interface Ethernet3
# no ip access-group acl01 out

# After state:
# -------------
#
# eos#sh running-config | include interface| access-group
# interface Loopback888
# interface Ethernet1
# interface Ethernet2
#   ip access-group acl01 in
# interface Ethernet3


"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample:
    - interface Ethernet2
    - ip access-group acl01 in
    - ipv6 access-group acl03 out
    - interface Ethernet3
    - ip access-group acl01 out
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.arista.eos.plugins.module_utils.network.eos.argspec.acl_interfaces.acl_interfaces import (
    Acl_interfacesArgs,
)
from ansible_collections.arista.eos.plugins.module_utils.network.eos.config.acl_interfaces.acl_interfaces import (
    Acl_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Acl_interfacesArgs.argument_spec,
        supports_check_mode=True,
    )

    result = Acl_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
