#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: network_device_linecard_details_info
short_description: Information module for Network Device Linecard Details
description:
- Get all Network Device Linecard Details.
- Get line card detail for a given deviceuuid. Response will contain serial no, part no, switch no and slot no.
version_added: '3.1.0'
extends_documentation_fragment:
  - cisco.dnac.module_info
author: Rafael Campos (@racampos)
options:
  headers:
    description: Additional headers.
    type: dict
  deviceUuid:
    description:
    - DeviceUuid path parameter. Instanceuuid of device.
    type: str
requirements:
- dnacentersdk >= 2.5.5
- python >= 3.5
seealso:
- name: Cisco DNA Center documentation for Devices GetLinecardDetails
  description: Complete reference of the GetLinecardDetails API.
  link: https://developer.cisco.com/docs/dna-center/#!get-linecard-details
notes:
  - SDK Method used are
    devices.Devices.get_linecard_details,

  - Paths used are
    get /dna/intent/api/v1/network-device/{deviceUuid}/line-card,

"""

EXAMPLES = r"""
- name: Get all Network Device Linecard Details
  cisco.dnac.network_device_linecard_details_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers: "{{my_headers | from_json}}"
    deviceUuid: string
  register: result

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "response": [
        {
          "serialno": "string",
          "partno": "string",
          "switchno": "string",
          "slotno": "string"
        }
      ],
      "version": "string"
    }
"""
