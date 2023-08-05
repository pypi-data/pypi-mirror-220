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
The arg spec for the iosxr_acl_interfaces module
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class Acl_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the iosxr_acl_interfaces module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "elements": "dict",
            "options": {
                "access_groups": {
                    "elements": "dict",
                    "options": {
                        "acls": {
                            "elements": "dict",
                            "options": {
                                "direction": {
                                    "choices": ["in", "out"],
                                    "type": "str",
                                    "required": True,
                                },
                                "name": {"type": "str", "required": True},
                            },
                            "type": "list",
                        },
                        "afi": {
                            "choices": ["ipv4", "ipv6"],
                            "type": "str",
                            "required": True,
                        },
                    },
                    "type": "list",
                },
                "name": {"type": "str", "required": True},
            },
            "type": "list",
        },
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "parsed",
                "rendered",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
