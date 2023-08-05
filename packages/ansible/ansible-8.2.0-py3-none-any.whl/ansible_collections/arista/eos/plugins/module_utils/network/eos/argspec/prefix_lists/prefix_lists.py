# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# cli_rm_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################

"""
The arg spec for the eos_prefix_lists module
"""


class Prefix_listsArgs(object):  # pylint: disable=R0903
    """The arg spec for the eos_prefix_lists module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "afi": {
                    "type": "str",
                    "required": True,
                    "choices": ["ipv4", "ipv6"],
                },
                "prefix_lists": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str", "required": True},
                        "entries": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "action": {
                                    "type": "str",
                                    "choices": ["deny", "permit"],
                                },
                                "address": {"type": "str"},
                                "match": {
                                    "type": "dict",
                                    "options": {
                                        "operator": {
                                            "type": "str",
                                            "choices": ["eq", "le", "ge"],
                                        },
                                        "masklen": {"type": "int"},
                                    },
                                },
                                "sequence": {"type": "int"},
                                "resequence": {
                                    "type": "dict",
                                    "options": {
                                        "default": {"type": "bool"},
                                        "start_seq": {"type": "int"},
                                        "step": {"type": "int"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": [
                "deleted",
                "merged",
                "overridden",
                "replaced",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
