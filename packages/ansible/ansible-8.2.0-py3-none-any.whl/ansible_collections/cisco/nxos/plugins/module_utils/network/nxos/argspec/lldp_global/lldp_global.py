#
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
The arg spec for the nxos_lldp_global module
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type


class Lldp_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_lldp_global module"""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "options": {
                "holdtime": {"type": "int"},
                "port_id": {"choices": [0, 1], "type": "int"},
                "reinit": {"type": "int"},
                "timer": {"type": "int"},
                "tlv_select": {
                    "options": {
                        "dcbxp": {"type": "bool"},
                        "management_address": {
                            "options": {
                                "v4": {"type": "bool"},
                                "v6": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "port": {
                            "options": {
                                "description": {"type": "bool"},
                                "vlan": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "power_management": {"type": "bool"},
                        "system": {
                            "options": {
                                "capabilities": {"type": "bool"},
                                "description": {"type": "bool"},
                                "name": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                    },
                    "type": "dict",
                },
            },
            "type": "dict",
        },
        "state": {
            "choices": [
                "merged",
                "replaced",
                "deleted",
                "gathered",
                "parsed",
                "rendered",
            ],
            "default": "merged",
            "type": "str",
        },
    }
