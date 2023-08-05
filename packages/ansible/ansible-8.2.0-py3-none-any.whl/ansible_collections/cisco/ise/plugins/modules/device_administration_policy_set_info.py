#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: device_administration_policy_set_info
short_description: Information module for Device Administration Policy Set
description:
- Get all Device Administration Policy Set.
- Get Device Administration Policy Set by id.
- Device Admin - Get policy set attributes.
- Device Admin - List of policy sets.
version_added: '1.0.0'
extends_documentation_fragment:
  - cisco.ise.module_info
author: Rafael Campos (@racampos)
options:
  id:
    description:
    - Id path parameter. Policy id.
    type: str
requirements:
- ciscoisesdk >= 2.0.8
- python >= 3.5
seealso:
- name: Cisco ISE documentation for Device Administration - Policy Set
  description: Complete reference of the Device Administration - Policy Set API.
  link: https://developer.cisco.com/docs/identity-services-engine/v1/#!policy-openapi
notes:
  - SDK Method used are
    device_administration_policy_set.DeviceAdministrationPolicySet.get_device_admin_policy_set_by_id,
    device_administration_policy_set.DeviceAdministrationPolicySet.get_device_admin_policy_sets,

  - Paths used are
    get /device-admin/policy-set,
    get /device-admin/policy-set/{id},

"""

EXAMPLES = r"""
- name: Get all Device Administration Policy Set
  cisco.ise.device_administration_policy_set_info:
    ise_hostname: "{{ise_hostname}}"
    ise_username: "{{ise_username}}"
    ise_password: "{{ise_password}}"
    ise_verify: "{{ise_verify}}"
  register: result

- name: Get Device Administration Policy Set by id
  cisco.ise.device_administration_policy_set_info:
    ise_hostname: "{{ise_hostname}}"
    ise_username: "{{ise_username}}"
    ise_password: "{{ise_password}}"
    ise_verify: "{{ise_verify}}"
    id: string
  register: result

"""

RETURN = r"""
ise_response:
  description: A dictionary or list with the response returned by the Cisco ISE Python SDK
  returned: always
  type: dict
  sample: >
    {
      "condition": {
        "conditionType": "string",
        "isNegate": true,
        "link": {
          "href": "string",
          "rel": "string",
          "type": "string"
        },
        "description": "string",
        "id": "string",
        "name": "string",
        "attributeName": "string",
        "attributeValue": "string",
        "dictionaryName": "string",
        "dictionaryValue": "string",
        "operator": "string",
        "children": [
          {
            "conditionType": "string",
            "isNegate": true,
            "link": {
              "href": "string",
              "rel": "string",
              "type": "string"
            }
          }
        ],
        "datesRange": {
          "endDate": "string",
          "startDate": "string"
        },
        "datesRangeException": {
          "endDate": "string",
          "startDate": "string"
        },
        "hoursRange": {
          "endTime": "string",
          "startTime": "string"
        },
        "hoursRangeException": {
          "endTime": "string",
          "startTime": "string"
        },
        "weekDays": [
          "string"
        ],
        "weekDaysException": [
          "string"
        ]
      },
      "default": true,
      "description": "string",
      "hitCounts": 0,
      "id": "string",
      "isProxy": true,
      "link": {
        "href": "string",
        "rel": "string",
        "type": "string"
      },
      "name": "string",
      "rank": 0,
      "serviceName": "string",
      "state": "string"
    }
"""
