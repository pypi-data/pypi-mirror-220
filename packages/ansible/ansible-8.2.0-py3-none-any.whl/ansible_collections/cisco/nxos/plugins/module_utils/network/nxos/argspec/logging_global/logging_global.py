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
The arg spec for the nxos_logging_global module
"""


class Logging_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_logging_global module"""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "dict",
            "options": {
                "console": {
                    "type": "dict",
                    "options": {
                        "state": {
                            "type": "str",
                            "choices": ["enabled", "disabled"],
                        },
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                    },
                },
                "event": {
                    "type": "dict",
                    "options": {
                        "link_status": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "default": {"type": "bool"},
                            },
                        },
                        "trunk_status": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "default": {"type": "bool"},
                            },
                        },
                    },
                },
                "history": {
                    "type": "dict",
                    "options": {
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                        "size": {"type": "int"},
                    },
                },
                "ip": {
                    "type": "dict",
                    "options": {
                        "access_list": {
                            "type": "dict",
                            "options": {
                                "cache": {
                                    "type": "dict",
                                    "options": {
                                        "entries": {"type": "int"},
                                        "interval": {"type": "int"},
                                        "threshold": {"type": "int"},
                                    },
                                },
                                "detailed": {"type": "bool"},
                                "include": {
                                    "type": "dict",
                                    "options": {"sgt": {"type": "bool"}},
                                },
                            },
                        },
                    },
                },
                "facilities": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "facility": {"type": "str"},
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                    },
                },
                "logfile": {
                    "type": "dict",
                    "options": {
                        "state": {
                            "type": "str",
                            "choices": ["enabled", "disabled"],
                        },
                        "name": {"type": "str"},
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                        "persistent_threshold": {"type": "int"},
                        "size": {"type": "int"},
                    },
                },
                "module": {
                    "type": "dict",
                    "options": {
                        "state": {
                            "type": "str",
                            "choices": ["enabled", "disabled"],
                        },
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                    },
                },
                "monitor": {
                    "type": "dict",
                    "options": {
                        "state": {
                            "type": "str",
                            "choices": ["enabled", "disabled"],
                        },
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                    },
                },
                "origin_id": {
                    "type": "dict",
                    "options": {
                        "hostname": {"type": "bool"},
                        "ip": {"type": "str"},
                        "string": {"type": "str"},
                    },
                },
                "rate_limit": {
                    "type": "str",
                    "choices": ["enabled", "disabled"],
                },
                "rfc_strict": {"type": "bool"},
                "hosts": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "host": {"type": "str"},
                        "severity": {
                            "type": "str",
                            "choices": [
                                "emergency",
                                "alert",
                                "critical",
                                "error",
                                "warning",
                                "notification",
                                "informational",
                                "debugging",
                            ],
                        },
                        "facility": {"type": "str"},
                        "port": {"type": "int"},
                        "secure": {
                            "type": "dict",
                            "options": {
                                "trustpoint": {
                                    "type": "dict",
                                    "options": {"client_identity": {"type": "str"}},
                                },
                            },
                        },
                        "use_vrf": {"type": "str"},
                    },
                },
                "source_interface": {"type": "str"},
                "timestamp": {
                    "type": "str",
                    "choices": ["microseconds", "milliseconds", "seconds"],
                },
            },
        },
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "parsed",
                "gathered",
                "rendered",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
