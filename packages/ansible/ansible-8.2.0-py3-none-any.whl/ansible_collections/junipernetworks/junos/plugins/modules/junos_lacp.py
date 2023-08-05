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
The module file for junos_lacp
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: junos_lacp
short_description: Global Link Aggregation Control Protocol (LACP) Junos resource
  module
description: This module provides declarative management of global LACP on Juniper
  Junos network devices.
version_added: 1.0.0
author: Ganesh Nalawade (@ganeshrn)
options:
  config:
    description: A dictionary of LACP global options
    type: dict
    suboptions:
      system_priority:
        description:
        - LACP priority for the system.
        type: int
      link_protection:
        description:
        - Enable LACP link-protection for the system. If the value is set to C(non-revertive)
          it will not revert links when a better priority link comes up. By default
          the link will be reverted.
        type: str
        choices:
        - revertive
        - non-revertive
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the Junos device
      by executing the command B(show chassis aggregated-devices ethernet lacp).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result
    type: str
  state:
    description:
    - The state of the configuration after module completion
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
- Tested against vSRX JUNOS version 18.1R1.
- This module works with connection C(netconf). See L(the Junos OS Platform Options,../network/user_guide/platform_junos.html).
"""
EXAMPLES = """
# Using deleted

# Before state:
# -------------
# user@junos01# show chassis aggregated-devices ethernet lacp
# system-priority 63;
# link-protection {
#    non-revertive;
# }

- name: Delete global LACP attributes
  junipernetworks.junos.junos_lacp:
    state: deleted

# After state:
# ------------
# user@junos01# show chassis aggregated-devices ethernet lacp
#


# Using merged

# Before state:
# -------------
# user@junos01# show chassis aggregated-devices ethernet lacp
#

- name: Merge global LACP attributes
  junipernetworks.junos.junos_lacp:
    config:
      system_priority: 63
      link_protection: revertive
    state: merged

# After state:
# ------------
# user@junos01# show chassis aggregated-devices ethernet lacp
# system-priority 63;
# link-protection {
#    non-revertive;
# }


# Using replaced

# Before state:
# -------------
# user@junos01# show chassis aggregated-devices ethernet lacp
# system-priority 63;
# link-protection {
#    non-revertive;
# }

- name: Replace global LACP attributes
  junipernetworks.junos.junos_lacp:
    config:
      system_priority: 30
      link_protection: non-revertive
    state: replaced

# After state:
# ------------
# user@junos01# show chassis aggregated-devices ethernet lacp
# system-priority 30;
# link-protection;
#
# Using gathered
# Before state:
# ------------
#
# ansible@cm123456tr21# show chassis aggregated-devices ethernet lacp
# system-priority 63;
# link-protection;

- name: Gather junos lacp as in given arguments
  junipernetworks.junos.junos_lacp:
    state: gathered
# Task Output (redacted)
# -----------------------
#
# "gathered": {
#         "link_protection": "revertive",
#         "system_priority": 63
#     }
# After state:
# ------------
#
# ansible@cm123456tr21# show chassis aggregated-devices ethernet lacp
# system-priority 63;
# link-protection;
# Using rendered
- name: Render platform specific xml from task input using rendered state
  junipernetworks.junos.junos_lacp:
    config:
      system_priority: 63
      link_protection: revertive
    state: rendered
# Task Output (redacted)
# -----------------------
# "rendered": "<nc:chassis
#     xmlns:nc=\"urn:ietf:params:xml:ns:netconf:base:1.0\">
#     <nc:aggregated-devices>
#         <nc:ethernet>
#             <nc:lacp>
#                 <nc:system-priority>63</nc:system-priority>
#                 <nc:link-protection>
#                     <nc:non-revertive delete=\"delete\"/>
#                 </nc:link-protection>
#             </nc:lacp>
#         </nc:ethernet>
#     </nc:aggregated-devices>
# </nc:chassis>
#
# Using parsed
# parsed.cfg
# ------------
#
# <?xml version="1.0" encoding="UTF-8"?>
# <rpc-reply message-id="urn:uuid:0cadb4e8-5bba-47f4-986e-72906227007f">
#     <configuration changed-seconds="1590139550" changed-localtime="2020-05-22 09:25:50 UTC">
#     <chassis>
#         <aggregated-devices>
#             <ethernet>
#                 <lacp>
#                     <system-priority>63</system-priority>
#                     <link-protection>
#                     </link-protection>
#                 </lacp>
#             </ethernet>
#         </aggregated-devices>
#     </chassis>
#     </configuration>
# </rpc-reply>
# - name: Convert lacp config to argspec without connecting to the appliance
#   junipernetworks.junos.junos_lacp:
#     running_config: "{{ lookup('file', './parsed.cfg') }}"
#     state: parsed
# Task Output (redacted)
# -----------------------
# "parsed": {
#         "link_protection": "revertive",
#         "system_priority": 63
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
xml:
  description: The set of xml rpc payload pushed to the remote device.
  returned: always
  type: list
  sample: ['<nc:chassis
    xmlns:nc=\"urn:ietf:params:xml:ns:netconf:base:1.0\">
    <nc:aggregated-devices>
        <nc:ethernet>
            <nc:lacp>
                <nc:system-priority>63</nc:system-priority>
                <nc:link-protection>
                    <nc:non-revertive delete=\"delete\"/>
                </nc:link-protection>
            </nc:lacp>
        </nc:ethernet>
    </nc:aggregated-devices>
</nc:chassis>', 'xml 2', 'xml 3']
"""


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.argspec.lacp.lacp import (
    LacpArgs,
)
from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.config.lacp.lacp import (
    Lacp,
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
        argument_spec=LacpArgs.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    result = Lacp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
