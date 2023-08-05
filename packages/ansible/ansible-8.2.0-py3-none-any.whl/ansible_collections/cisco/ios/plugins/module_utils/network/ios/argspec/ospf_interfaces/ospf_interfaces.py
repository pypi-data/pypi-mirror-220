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
The arg spec for the ios_ospf_interfaces module
"""


class Ospf_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_ospf_interfaces module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "address_family": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "afi": {
                            "type": "str",
                            "choices": ["ipv4", "ipv6"],
                            "required": True,
                        },
                        "process": {
                            "type": "dict",
                            "options": {
                                "id": {"type": "int"},
                                "area_id": {"type": "str"},
                                "secondaries": {"type": "bool"},
                                "instance_id": {"type": "int"},
                            },
                        },
                        "adjacency": {"type": "bool"},
                        "authentication": {
                            "type": "dict",
                            "options": {
                                "key_chain": {"type": "str", "no_log": True},
                                "message_digest": {"type": "bool"},
                                "null": {"type": "bool"},
                            },
                        },
                        "bfd": {"type": "bool"},
                        "cost": {
                            "type": "dict",
                            "options": {
                                "interface_cost": {"type": "int"},
                                "dynamic_cost": {
                                    "type": "dict",
                                    "options": {
                                        "default": {"type": "int"},
                                        "hysteresis": {
                                            "type": "dict",
                                            "options": {
                                                "percent": {"type": "int"},
                                                "threshold": {"type": "int"},
                                            },
                                        },
                                        "weight": {
                                            "type": "dict",
                                            "options": {
                                                "l2_factor": {"type": "int"},
                                                "latency": {"type": "int"},
                                                "oc": {"type": "bool"},
                                                "resources": {"type": "int"},
                                                "throughput": {"type": "int"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "database_filter": {"type": "bool"},
                        "dead_interval": {
                            "type": "dict",
                            "options": {
                                "time": {"type": "int"},
                                "minimal": {"type": "int"},
                            },
                        },
                        "demand_circuit": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "ignore": {"type": "bool"},
                                "disable": {"type": "bool"},
                            },
                        },
                        "flood_reduction": {"type": "bool"},
                        "hello_interval": {"type": "int"},
                        "lls": {"type": "bool"},
                        "manet": {
                            "type": "dict",
                            "options": {
                                "cost": {
                                    "type": "dict",
                                    "options": {
                                        "percent": {"type": "int"},
                                        "threshold": {"type": "int"},
                                    },
                                },
                                "link_metrics": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "cost_threshold": {"type": "int"},
                                    },
                                },
                            },
                        },
                        "mtu_ignore": {"type": "bool"},
                        "multi_area": {
                            "type": "dict",
                            "options": {
                                "id": {"type": "int"},
                                "cost": {"type": "int"},
                            },
                        },
                        "neighbor": {
                            "type": "dict",
                            "options": {
                                "address": {"type": "str"},
                                "cost": {"type": "int"},
                                "database_filter": {"type": "bool"},
                                "poll_interval": {"type": "int"},
                                "priority": {"type": "int"},
                            },
                        },
                        "network": {
                            "type": "dict",
                            "options": {
                                "broadcast": {"type": "bool"},
                                "manet": {"type": "bool"},
                                "non_broadcast": {"type": "bool"},
                                "point_to_multipoint": {"type": "bool"},
                                "point_to_point": {"type": "bool"},
                            },
                        },
                        "prefix_suppression": {"type": "bool"},
                        "priority": {"type": "int"},
                        "resync_timeout": {"type": "int"},
                        "retransmit_interval": {"type": "int"},
                        "shutdown": {"type": "bool"},
                        "transmit_delay": {"type": "int"},
                        "ttl_security": {
                            "type": "dict",
                            "options": {
                                "set": {"type": "bool"},
                                "hops": {"type": "int"},
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
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
