# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# ansible.content_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the documentation in the module file and re-run
# ansible.content_builder commenting out
# the path to external 'docstring' in build.yaml.
#
##############################################

"""
The arg spec for the ios_service module
"""


class ServiceArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_service module"""

    argument_spec = {
        "config": {
            "options": {
                "call_home": {"type": "bool"},
                "compress_config": {"type": "bool"},
                "config": {"type": "bool"},
                "counters": {"type": "int", "default": 0},
                "dhcp": {"type": "bool", "default": True},
                "disable_ip_fast_frag": {"type": "bool"},
                "exec_callback": {"type": "bool"},
                "exec_wait": {"type": "bool"},
                "hide_telnet_addresses": {"type": "bool"},
                "internal": {"type": "bool"},
                "linenumber": {"type": "bool"},
                "log": {"type": "bool"},
                "log_hidden": {"type": "bool"},
                "nagle": {"type": "bool"},
                "old_slip_prompts": {"type": "bool"},
                "pad": {"type": "bool"},
                "pad_cmns": {"type": "bool"},
                "pad_from_xot": {"type": "bool"},
                "pad_to_xot": {"type": "bool"},
                "password_encryption": {"type": "bool"},
                "password_recovery": {"type": "bool", "default": True},
                "prompt": {"type": "bool", "default": True},
                "private_config_encryption": {"type": "bool"},
                "pt_vty_logging": {"type": "bool"},
                "scripting": {"type": "bool"},
                "sequence_numbers": {"type": "bool"},
                "slave_coredump": {"type": "bool"},
                "slave_log": {"type": "bool", "default": True},
                "tcp_keepalives_in": {"type": "bool"},
                "tcp_keepalives_out": {"type": "bool"},
                "tcp_small_servers": {
                    "options": {
                        "enable": {"type": "bool"},
                        "max_servers": {"type": "str"},
                    },
                    "type": "dict",
                },
                "telnet_zeroidle": {"type": "bool"},
                "timestamps": {
                    "elements": "dict",
                    "options": {
                        "msg": {"choices": ["debug", "log"], "type": "str"},
                        "enable": {"type": "bool"},
                        "timestamp": {
                            "choices": ["datetime", "uptime"],
                            "type": "str",
                        },
                        "datetime_options": {
                            "options": {
                                "localtime": {"type": "bool"},
                                "msec": {"type": "bool"},
                                "show_timezone": {"type": "bool"},
                                "year": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                    },
                    "type": "list",
                },
                "udp_small_servers": {
                    "options": {
                        "enable": {"type": "bool"},
                        "max_servers": {"type": "str"},
                    },
                    "type": "dict",
                },
                "unsupported_transceiver": {"type": "bool"},
            },
            "type": "dict",
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
