#!/usr/bin/python
from __future__ import absolute_import, division, print_function

# Copyright: (c) 2022 Fortinet
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

__metaclass__ = type

ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "metadata_version": "1.1",
}

DOCUMENTATION = """
---
module: fortios_switch_controller_qos_ip_dscp_map
short_description: Configure FortiSwitch QoS IP precedence/DSCP in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS (FOS) device by allowing the
      user to set and modify switch_controller_qos feature and ip_dscp_map category.
      Examples include all parameters and values need to be adjusted to datasources before usage.
      Tested with FOS v6.0.0
version_added: "2.0.0"
author:
    - Link Zheng (@chillancezen)
    - Jie Xue (@JieX19)
    - Hongbin Lu (@fgtdev-hblu)
    - Frank Shen (@frankshen01)
    - Miguel Angel Munoz (@mamunozgonzalez)
    - Nicolas Thomas (@thomnico)
notes:
    - Legacy fortiosapi has been deprecated, httpapi is the preferred way to run playbooks

requirements:
    - ansible>=2.9
options:
    access_token:
        description:
            - Token-based authentication.
              Generated from GUI of Fortigate.
        type: str
        required: false
    enable_log:
        description:
            - Enable/Disable logging for task.
        type: bool
        required: false
        default: false
    vdom:
        description:
            - Virtual domain, among those defined previously. A vdom is a
              virtual instance of the FortiGate that can be configured and
              used as a different unit.
        type: str
        default: root
    member_path:
        type: str
        description:
            - Member attribute path to operate on.
            - Delimited by a slash character if there are more than one attribute.
            - Parameter marked with member_path is legitimate for doing member operation.
    member_state:
        type: str
        description:
            - Add or delete a member under specified attribute path.
            - When member_state is specified, the state option is ignored.
        choices:
            - 'present'
            - 'absent'

    state:
        description:
            - Indicates whether to create or remove the object.
        type: str
        required: true
        choices:
            - 'present'
            - 'absent'
    switch_controller_qos_ip_dscp_map:
        description:
            - Configure FortiSwitch QoS IP precedence/DSCP.
        default: null
        type: dict
        suboptions:
            description:
                description:
                    - Description of the ip-dscp map name.
                type: str
            map:
                description:
                    - Maps between IP-DSCP value to COS queue.
                type: list
                elements: dict
                suboptions:
                    cos_queue:
                        description:
                            - COS queue number.
                        type: int
                    diffserv:
                        description:
                            - Differentiated service.
                        type: list
                        elements: str
                        choices:
                            - 'CS0'
                            - 'CS1'
                            - 'AF11'
                            - 'AF12'
                            - 'AF13'
                            - 'CS2'
                            - 'AF21'
                            - 'AF22'
                            - 'AF23'
                            - 'CS3'
                            - 'AF31'
                            - 'AF32'
                            - 'AF33'
                            - 'CS4'
                            - 'AF41'
                            - 'AF42'
                            - 'AF43'
                            - 'CS5'
                            - 'EF'
                            - 'CS6'
                            - 'CS7'
                    ip_precedence:
                        description:
                            - IP Precedence.
                        type: list
                        elements: str
                        choices:
                            - 'network-control'
                            - 'internetwork-control'
                            - 'critic-ecp'
                            - 'flashoverride'
                            - 'flash'
                            - 'immediate'
                            - 'priority'
                            - 'routine'
                    name:
                        description:
                            - Dscp mapping entry name.
                        required: true
                        type: str
                    value:
                        description:
                            - Raw values of DSCP (0 - 63).
                        type: str
            name:
                description:
                    - Dscp map name.
                required: true
                type: str
"""

EXAMPLES = """
- hosts: fortigates
  collections:
    - fortinet.fortios
  connection: httpapi
  vars:
   vdom: "root"
   ansible_httpapi_use_ssl: yes
   ansible_httpapi_validate_certs: no
   ansible_httpapi_port: 443
  tasks:
  - name: Configure FortiSwitch QoS IP precedence/DSCP.
    fortios_switch_controller_qos_ip_dscp_map:
      vdom:  "{{ vdom }}"
      state: "present"
      access_token: "<your_own_value>"
      switch_controller_qos_ip_dscp_map:
        description: "<your_own_value>"
        map:
         -
            cos_queue: "0"
            diffserv: "CS0"
            ip_precedence: "network-control"
            name: "default_name_8"
            value: "<your_own_value>"
        name: "default_name_10"

"""

RETURN = """
build:
  description: Build number of the fortigate image
  returned: always
  type: str
  sample: '1547'
http_method:
  description: Last method used to provision the content into FortiGate
  returned: always
  type: str
  sample: 'PUT'
http_status:
  description: Last result given by FortiGate on last operation applied
  returned: always
  type: str
  sample: "200"
mkey:
  description: Master key (id) used in the last call to FortiGate
  returned: success
  type: str
  sample: "id"
name:
  description: Name of the table used to fulfill the request
  returned: always
  type: str
  sample: "urlfilter"
path:
  description: Path of the table used to fulfill the request
  returned: always
  type: str
  sample: "webfilter"
revision:
  description: Internal revision number
  returned: always
  type: str
  sample: "17.0.2.10658"
serial:
  description: Serial number of the unit
  returned: always
  type: str
  sample: "FGVMEVYYQT3AB5352"
status:
  description: Indication of the operation's result
  returned: always
  type: str
  sample: "success"
vdom:
  description: Virtual domain used
  returned: always
  type: str
  sample: "root"
version:
  description: Version of the FortiGate
  returned: always
  type: str
  sample: "v5.6.3"

"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import (
    FortiOSHandler,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import (
    check_legacy_fortiosapi,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import (
    schema_to_module_spec,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.fortios import (
    check_schema_versioning,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortimanager.common import (
    FAIL_SOCKET_MSG,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.data_post_processor import (
    remove_invalid_fields,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.comparison import (
    is_same_comparison,
)
from ansible_collections.fortinet.fortios.plugins.module_utils.fortios.comparison import (
    serialize,
)


def filter_switch_controller_qos_ip_dscp_map_data(json):
    option_list = ["description", "map", "name"]

    json = remove_invalid_fields(json)
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def flatten_single_path(data, path, index):
    if (
        not data
        or index == len(path)
        or path[index] not in data
        or not data[path[index]]
    ):
        return

    if index == len(path) - 1:
        data[path[index]] = " ".join(str(elem) for elem in data[path[index]])
    elif isinstance(data[path[index]], list):
        for value in data[path[index]]:
            flatten_single_path(value, path, index + 1)
    else:
        flatten_single_path(data[path[index]], path, index + 1)


def flatten_multilists_attributes(data):
    multilist_attrs = [
        ["map", "diffserv"],
        ["map", "ip_precedence"],
    ]

    for attr in multilist_attrs:
        flatten_single_path(data, attr, 0)

    return data


def underscore_to_hyphen(data):
    if isinstance(data, list):
        for i, elem in enumerate(data):
            data[i] = underscore_to_hyphen(elem)
    elif isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            new_data[k.replace("_", "-")] = underscore_to_hyphen(v)
        data = new_data

    return data


def switch_controller_qos_ip_dscp_map(data, fos, check_mode=False):

    vdom = data["vdom"]

    state = data["state"]

    switch_controller_qos_ip_dscp_map_data = data["switch_controller_qos_ip_dscp_map"]
    switch_controller_qos_ip_dscp_map_data = flatten_multilists_attributes(
        switch_controller_qos_ip_dscp_map_data
    )
    filtered_data = underscore_to_hyphen(
        filter_switch_controller_qos_ip_dscp_map_data(
            switch_controller_qos_ip_dscp_map_data
        )
    )

    # check_mode starts from here
    if check_mode:
        diff = {
            "before": "",
            "after": filtered_data,
        }
        mkey = fos.get_mkey(
            "switch-controller.qos", "ip-dscp-map", filtered_data, vdom=vdom
        )
        current_data = fos.get(
            "switch-controller.qos", "ip-dscp-map", vdom=vdom, mkey=mkey
        )
        is_existed = (
            current_data
            and current_data.get("http_status") == 200
            and isinstance(current_data.get("results"), list)
            and len(current_data["results"]) > 0
        )

        # 2. if it exists and the state is 'present' then compare current settings with desired
        if state == "present" or state is True:
            if mkey is None:
                return False, True, filtered_data, diff

            # if mkey exists then compare each other
            # record exits and they're matched or not
            if is_existed:
                is_same = is_same_comparison(
                    serialize(current_data["results"][0]), serialize(filtered_data)
                )
                return (
                    False,
                    not is_same,
                    filtered_data,
                    {"before": current_data["results"][0], "after": filtered_data},
                )

            # record does not exist
            return False, True, filtered_data, diff

        if state == "absent":
            if mkey is None:
                return (
                    False,
                    False,
                    filtered_data,
                    {"before": current_data["results"][0], "after": ""},
                )

            if is_existed:
                return (
                    False,
                    True,
                    filtered_data,
                    {"before": current_data["results"][0], "after": ""},
                )
            return False, False, filtered_data, {}

        return True, False, {"reason: ": "Must provide state parameter"}, {}

    if state == "present" or state is True:
        return fos.set(
            "switch-controller.qos", "ip-dscp-map", data=filtered_data, vdom=vdom
        )

    elif state == "absent":
        return fos.delete(
            "switch-controller.qos",
            "ip-dscp-map",
            mkey=filtered_data["name"],
            vdom=vdom,
        )
    else:
        fos._module.fail_json(msg="state must be present or absent!")


def is_successful_status(resp):
    return (
        "status" in resp
        and resp["status"] == "success"
        or "http_status" in resp
        and resp["http_status"] == 200
        or "http_method" in resp
        and resp["http_method"] == "DELETE"
        and resp["http_status"] == 404
    )


def fortios_switch_controller_qos(data, fos, check_mode):

    fos.do_member_operation("switch-controller.qos", "ip-dscp-map")
    if data["switch_controller_qos_ip_dscp_map"]:
        resp = switch_controller_qos_ip_dscp_map(data, fos, check_mode)
    else:
        fos._module.fail_json(
            msg="missing task body: %s" % ("switch_controller_qos_ip_dscp_map")
        )
    if check_mode:
        return resp
    return (
        not is_successful_status(resp),
        is_successful_status(resp)
        and (resp["revision_changed"] if "revision_changed" in resp else True),
        resp,
        {},
    )


versioned_schema = {
    "type": "list",
    "elements": "dict",
    "children": {
        "name": {
            "revisions": {
                "v7.4.0": True,
                "v7.2.4": True,
                "v7.2.2": True,
                "v7.2.1": True,
                "v7.2.0": True,
                "v7.0.8": True,
                "v7.0.7": True,
                "v7.0.6": True,
                "v7.0.5": True,
                "v7.0.4": True,
                "v7.0.3": True,
                "v7.0.2": True,
                "v7.0.1": True,
                "v7.0.0": True,
                "v6.4.4": True,
                "v6.4.1": True,
                "v6.4.0": True,
                "v6.2.7": True,
                "v6.2.5": True,
                "v6.2.3": True,
                "v6.2.0": True,
                "v6.0.5": True,
                "v6.0.11": True,
                "v6.0.0": True,
            },
            "type": "string",
            "required": True,
        },
        "description": {
            "revisions": {
                "v7.4.0": True,
                "v7.2.4": True,
                "v7.2.2": True,
                "v7.2.1": True,
                "v7.2.0": True,
                "v7.0.8": True,
                "v7.0.7": True,
                "v7.0.6": True,
                "v7.0.5": True,
                "v7.0.4": True,
                "v7.0.3": True,
                "v7.0.2": True,
                "v7.0.1": True,
                "v7.0.0": True,
                "v6.4.4": True,
                "v6.4.1": True,
                "v6.4.0": True,
                "v6.2.7": True,
                "v6.2.5": True,
                "v6.2.3": True,
                "v6.2.0": True,
                "v6.0.5": True,
                "v6.0.11": True,
                "v6.0.0": True,
            },
            "type": "string",
        },
        "map": {
            "type": "list",
            "elements": "dict",
            "children": {
                "name": {
                    "revisions": {
                        "v7.4.0": True,
                        "v7.2.4": True,
                        "v7.2.2": True,
                        "v7.2.1": True,
                        "v7.2.0": True,
                        "v7.0.8": True,
                        "v7.0.7": True,
                        "v7.0.6": True,
                        "v7.0.5": True,
                        "v7.0.4": True,
                        "v7.0.3": True,
                        "v7.0.2": True,
                        "v7.0.1": True,
                        "v7.0.0": True,
                        "v6.4.4": True,
                        "v6.4.1": True,
                        "v6.4.0": True,
                        "v6.2.7": True,
                        "v6.2.5": True,
                        "v6.2.3": True,
                        "v6.2.0": True,
                        "v6.0.5": True,
                        "v6.0.11": True,
                        "v6.0.0": True,
                    },
                    "type": "string",
                    "required": True,
                },
                "cos_queue": {
                    "revisions": {
                        "v7.4.0": True,
                        "v7.2.4": True,
                        "v7.2.2": True,
                        "v7.2.1": True,
                        "v7.2.0": True,
                        "v7.0.8": True,
                        "v7.0.7": True,
                        "v7.0.6": True,
                        "v7.0.5": True,
                        "v7.0.4": True,
                        "v7.0.3": True,
                        "v7.0.2": True,
                        "v7.0.1": True,
                        "v7.0.0": True,
                        "v6.4.4": True,
                        "v6.4.1": True,
                        "v6.4.0": True,
                        "v6.2.7": True,
                        "v6.2.5": True,
                        "v6.2.3": True,
                        "v6.2.0": True,
                        "v6.0.5": True,
                        "v6.0.11": True,
                        "v6.0.0": True,
                    },
                    "type": "integer",
                },
                "diffserv": {
                    "revisions": {
                        "v7.4.0": True,
                        "v7.2.4": True,
                        "v7.2.2": True,
                        "v7.2.1": True,
                        "v7.2.0": True,
                        "v7.0.8": True,
                        "v7.0.7": True,
                        "v7.0.6": True,
                        "v7.0.5": True,
                        "v7.0.4": True,
                        "v7.0.3": True,
                        "v7.0.2": True,
                        "v7.0.1": True,
                        "v7.0.0": True,
                        "v6.4.4": True,
                        "v6.4.1": True,
                        "v6.4.0": True,
                        "v6.2.7": True,
                        "v6.2.5": True,
                        "v6.2.3": True,
                        "v6.2.0": True,
                        "v6.0.5": True,
                        "v6.0.11": True,
                        "v6.0.0": True,
                    },
                    "type": "list",
                    "options": [
                        {
                            "value": "CS0",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS1",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF11",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF12",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF13",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS2",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF21",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF22",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF23",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS3",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF31",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF32",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF33",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS4",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF41",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF42",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "AF43",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS5",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "EF",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS6",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "CS7",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                    ],
                    "multiple_values": True,
                    "elements": "str",
                },
                "ip_precedence": {
                    "revisions": {
                        "v7.4.0": True,
                        "v7.2.4": True,
                        "v7.2.2": True,
                        "v7.2.1": True,
                        "v7.2.0": True,
                        "v7.0.8": True,
                        "v7.0.7": True,
                        "v7.0.6": True,
                        "v7.0.5": True,
                        "v7.0.4": True,
                        "v7.0.3": True,
                        "v7.0.2": True,
                        "v7.0.1": True,
                        "v7.0.0": True,
                        "v6.4.4": True,
                        "v6.4.1": True,
                        "v6.4.0": True,
                        "v6.2.7": True,
                        "v6.2.5": True,
                        "v6.2.3": True,
                        "v6.2.0": True,
                        "v6.0.5": True,
                        "v6.0.11": True,
                        "v6.0.0": True,
                    },
                    "type": "list",
                    "options": [
                        {
                            "value": "network-control",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "internetwork-control",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "critic-ecp",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "flashoverride",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "flash",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "immediate",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "priority",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                        {
                            "value": "routine",
                            "revisions": {
                                "v7.4.0": True,
                                "v7.2.4": True,
                                "v7.2.2": True,
                                "v7.2.1": True,
                                "v7.2.0": True,
                                "v7.0.8": True,
                                "v7.0.7": True,
                                "v7.0.6": True,
                                "v7.0.5": True,
                                "v7.0.4": True,
                                "v7.0.3": True,
                                "v7.0.2": True,
                                "v7.0.1": True,
                                "v7.0.0": True,
                                "v6.4.4": True,
                                "v6.4.1": True,
                                "v6.4.0": True,
                                "v6.2.7": True,
                                "v6.2.5": True,
                                "v6.2.3": True,
                                "v6.2.0": True,
                                "v6.0.5": True,
                                "v6.0.11": True,
                                "v6.0.0": True,
                            },
                        },
                    ],
                    "multiple_values": True,
                    "elements": "str",
                },
                "value": {
                    "revisions": {
                        "v7.4.0": True,
                        "v7.2.4": True,
                        "v7.2.2": True,
                        "v7.2.1": True,
                        "v7.2.0": True,
                        "v7.0.8": True,
                        "v7.0.7": True,
                        "v7.0.6": True,
                        "v7.0.5": True,
                        "v7.0.4": True,
                        "v7.0.3": True,
                        "v7.0.2": True,
                        "v7.0.1": True,
                        "v7.0.0": True,
                        "v6.4.4": True,
                        "v6.4.1": True,
                        "v6.4.0": True,
                        "v6.2.7": True,
                        "v6.2.5": True,
                        "v6.2.3": True,
                        "v6.2.0": True,
                        "v6.0.5": True,
                        "v6.0.11": True,
                        "v6.0.0": True,
                    },
                    "type": "string",
                },
            },
            "revisions": {
                "v7.4.0": True,
                "v7.2.4": True,
                "v7.2.2": True,
                "v7.2.1": True,
                "v7.2.0": True,
                "v7.0.8": True,
                "v7.0.7": True,
                "v7.0.6": True,
                "v7.0.5": True,
                "v7.0.4": True,
                "v7.0.3": True,
                "v7.0.2": True,
                "v7.0.1": True,
                "v7.0.0": True,
                "v6.4.4": True,
                "v6.4.1": True,
                "v6.4.0": True,
                "v6.2.7": True,
                "v6.2.5": True,
                "v6.2.3": True,
                "v6.2.0": True,
                "v6.0.5": True,
                "v6.0.11": True,
                "v6.0.0": True,
            },
        },
    },
    "revisions": {
        "v7.4.0": True,
        "v7.2.4": True,
        "v7.2.2": True,
        "v7.2.1": True,
        "v7.2.0": True,
        "v7.0.8": True,
        "v7.0.7": True,
        "v7.0.6": True,
        "v7.0.5": True,
        "v7.0.4": True,
        "v7.0.3": True,
        "v7.0.2": True,
        "v7.0.1": True,
        "v7.0.0": True,
        "v6.4.4": True,
        "v6.4.1": True,
        "v6.4.0": True,
        "v6.2.7": True,
        "v6.2.5": True,
        "v6.2.3": True,
        "v6.2.0": True,
        "v6.0.5": True,
        "v6.0.11": True,
        "v6.0.0": True,
    },
}


def main():
    module_spec = schema_to_module_spec(versioned_schema)
    mkeyname = "name"
    fields = {
        "access_token": {"required": False, "type": "str", "no_log": True},
        "enable_log": {"required": False, "type": "bool", "default": False},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "member_path": {"required": False, "type": "str"},
        "member_state": {
            "type": "str",
            "required": False,
            "choices": ["present", "absent"],
        },
        "state": {"required": True, "type": "str", "choices": ["present", "absent"]},
        "switch_controller_qos_ip_dscp_map": {
            "required": False,
            "type": "dict",
            "default": None,
            "options": {},
        },
    }
    for attribute_name in module_spec["options"]:
        fields["switch_controller_qos_ip_dscp_map"]["options"][
            attribute_name
        ] = module_spec["options"][attribute_name]
        if mkeyname and mkeyname == attribute_name:
            fields["switch_controller_qos_ip_dscp_map"]["options"][attribute_name][
                "required"
            ] = True

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    check_legacy_fortiosapi(module)

    versions_check_result = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        if "access_token" in module.params:
            connection.set_option("access_token", module.params["access_token"])

        if "enable_log" in module.params:
            connection.set_option("enable_log", module.params["enable_log"])
        else:
            connection.set_option("enable_log", False)
        fos = FortiOSHandler(connection, module, mkeyname)
        versions_check_result = check_schema_versioning(
            fos, versioned_schema, "switch_controller_qos_ip_dscp_map"
        )

        is_error, has_changed, result, diff = fortios_switch_controller_qos(
            module.params, fos, module.check_mode
        )

    else:
        module.fail_json(**FAIL_SOCKET_MSG)

    if versions_check_result and versions_check_result["matched"] is False:
        module.warn(
            "Ansible has detected version mismatch between FortOS system and your playbook, see more details by specifying option -vvv"
        )

    if not is_error:
        if versions_check_result and versions_check_result["matched"] is False:
            module.exit_json(
                changed=has_changed,
                version_check_warning=versions_check_result,
                meta=result,
                diff=diff,
            )
        else:
            module.exit_json(changed=has_changed, meta=result, diff=diff)
    else:
        if versions_check_result and versions_check_result["matched"] is False:
            module.fail_json(
                msg="Error in repo",
                version_check_warning=versions_check_result,
                meta=result,
            )
        else:
            module.fail_json(msg="Error in repo", meta=result)


if __name__ == "__main__":
    main()
