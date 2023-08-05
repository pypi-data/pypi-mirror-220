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
The arg spec for the eos_snmp_server module
"""


class Snmp_serverArgs(object):  # pylint: disable=R0903
    """The arg spec for the eos_snmp_server module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "chassis_id": {"type": "str"},
                "communities": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str"},
                        "acl_v4": {"type": "str"},
                        "acl_v6": {"type": "str"},
                        "ro": {"type": "bool"},
                        "rw": {"type": "bool"},
                        "view": {"type": "str"},
                    },
                },
                "contact": {"type": "str"},
                "traps": {
                    "type": "dict",
                    "options": {
                        "bgp": {
                            "type": "dict",
                            "options": {
                                "arista_backward_transition": {"type": "bool"},
                                "arista_established": {"type": "bool"},
                                "backward_transition": {"type": "bool"},
                                "established": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "bridge": {
                            "type": "dict",
                            "options": {
                                "arista_mac_age": {"type": "bool"},
                                "arista_mac_learn": {"type": "bool"},
                                "arista_mac_move": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "capacity": {
                            "type": "dict",
                            "options": {
                                "arista_hardware_utilization_alert": {
                                    "type": "bool",
                                },
                                "enabled": {"type": "bool"},
                            },
                        },
                        "entity": {
                            "type": "dict",
                            "options": {
                                "arista_ent_sensor_alarm": {"type": "bool"},
                                "ent_config_change": {"type": "bool"},
                                "ent_state_oper": {"type": "bool"},
                                "ent_state_oper_disabled": {"type": "bool"},
                                "ent_state_oper_enabled": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "external_alarm": {
                            "type": "dict",
                            "options": {
                                "arista_external_alarm_asserted_notif": {
                                    "type": "bool",
                                },
                                "arista_external_alarm_deasserted_notif": {
                                    "type": "bool",
                                },
                                "enabled": {"type": "bool"},
                            },
                        },
                        "isis": {
                            "type": "dict",
                            "options": {
                                "adjacency_change": {"type": "bool"},
                                "area_mismatch": {"type": "bool"},
                                "attempt_to_exceed_max_sequence": {
                                    "type": "bool",
                                },
                                "authentication_type_failure": {
                                    "type": "bool",
                                },
                                "database_overload": {"type": "bool"},
                                "own_lsp_purge": {"type": "bool"},
                                "rejected_adjacency": {"type": "bool"},
                                "sequence_number_skip": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "lldp": {
                            "type": "dict",
                            "options": {
                                "rem_tables_change": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "mpls_ldp": {
                            "type": "dict",
                            "options": {
                                "mpls_ldp_session_down": {"type": "bool"},
                                "mpls_ldp_session_up": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "msdp": {
                            "type": "dict",
                            "options": {
                                "backward_transition": {"type": "bool"},
                                "established": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "ospf": {
                            "type": "dict",
                            "options": {
                                "if_config_error": {"type": "bool"},
                                "if_auth_failure": {"type": "bool"},
                                "if_state_change": {"type": "bool"},
                                "nbr_state_change": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "ospfv3": {
                            "type": "dict",
                            "options": {
                                "if_config_error": {"type": "bool"},
                                "if_rx_bad_packet": {"type": "bool"},
                                "if_state_change": {"type": "bool"},
                                "nbr_state_change": {"type": "bool"},
                                "nbr_restart_helper_status_change": {
                                    "type": "bool",
                                },
                                "nssa_translator_status_change": {
                                    "type": "bool",
                                },
                                "restart_status_change": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "pim": {
                            "type": "dict",
                            "options": {
                                "neighbor_loss": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "snmp": {
                            "type": "dict",
                            "options": {
                                "authentication": {"type": "bool"},
                                "link_down": {"type": "bool"},
                                "link_up": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "snmpConfigManEvent": {
                            "type": "dict",
                            "options": {
                                "arista_config_man_event": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "switchover": {
                            "type": "dict",
                            "options": {
                                "arista_redundancy_switch_over_notif": {
                                    "type": "bool",
                                },
                                "enabled": {"type": "bool"},
                            },
                        },
                        "test": {
                            "type": "dict",
                            "options": {
                                "arista_test_notification": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                        "vrrp": {
                            "type": "dict",
                            "options": {
                                "trap_new_master": {"type": "bool"},
                                "enabled": {"type": "bool"},
                            },
                        },
                    },
                },
                "engineid": {
                    "type": "dict",
                    "options": {
                        "local": {"type": "str"},
                        "remote": {
                            "type": "dict",
                            "options": {
                                "host": {"type": "str"},
                                "udp_port": {"type": "int"},
                                "id": {"type": "str"},
                            },
                        },
                    },
                },
                "extension": {
                    "type": "dict",
                    "options": {
                        "root_oid": {"type": "str"},
                        "script_location": {"type": "str"},
                        "oneshot": {"type": "bool"},
                    },
                },
                "groups": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "group": {"type": "str"},
                        "version": {
                            "type": "str",
                            "choices": ["v1", "v3", "v2c"],
                        },
                        "auth_privacy": {
                            "type": "str",
                            "choices": ["auth", "noauth", "priv"],
                        },
                        "context": {"type": "str"},
                        "notify": {"type": "str"},
                        "read": {"type": "str"},
                        "write": {"type": "str"},
                    },
                },
                "hosts": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "host": {"type": "str"},
                        "user": {"type": "str"},
                        "udp_port": {"type": "int"},
                        "informs": {"type": "bool"},
                        "traps": {"type": "bool"},
                        "version": {
                            "type": "str",
                            "choices": [
                                "1",
                                "2c",
                                "3 auth",
                                "3 noauth",
                                "3 priv",
                            ],
                        },
                        "vrf": {"type": "str"},
                    },
                },
                "acls": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "afi": {"type": "str", "choices": ["ipv4", "ipv6"]},
                        "acl": {"type": "str"},
                        "vrf": {"type": "str"},
                    },
                },
                "local_interface": {"type": "str"},
                "location": {"type": "str"},
                "notification": {"type": "int"},
                "objects": {
                    "type": "dict",
                    "options": {
                        "mac_address_tables": {"type": "bool"},
                        "route_tables": {"type": "bool"},
                    },
                },
                "qos": {"type": "int"},
                "qosmib": {"type": "int"},
                "transmit": {"type": "int"},
                "transport": {"type": "str"},
                "users": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "user": {"type": "str"},
                        "group": {"type": "str"},
                        "remote": {"type": "str"},
                        "udp_port": {"type": "int"},
                        "version": {
                            "type": "str",
                            "choices": ["v1", "v2c", "v3"],
                        },
                        "auth": {
                            "type": "dict",
                            "options": {
                                "algorithm": {"type": "str"},
                                "auth_passphrase": {
                                    "type": "str",
                                    "no_log": True,
                                },
                                "encryption": {"type": "str"},
                                "priv_passphrase": {
                                    "type": "str",
                                    "no_log": True,
                                },
                            },
                        },
                        "localized": {
                            "type": "dict",
                            "options": {
                                "engineid": {"type": "str"},
                                "algorithm": {"type": "str"},
                                "auth_passphrase": {
                                    "type": "str",
                                    "no_log": True,
                                },
                                "encryption": {"type": "str"},
                                "priv_passphrase": {
                                    "type": "str",
                                    "no_log": True,
                                },
                            },
                        },
                    },
                },
                "views": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "view": {"type": "str"},
                        "mib": {"type": "str"},
                        "action": {
                            "type": "str",
                            "choices": ["excluded", "included"],
                        },
                    },
                },
                "vrfs": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "vrf": {"type": "str"},
                        "local_interface": {"type": "str"},
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
