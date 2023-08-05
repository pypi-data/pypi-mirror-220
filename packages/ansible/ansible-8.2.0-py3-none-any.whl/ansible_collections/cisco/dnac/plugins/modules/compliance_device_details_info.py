#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: compliance_device_details_info
short_description: Information module for Compliance Device Details
description:
- Get all Compliance Device Details.
- Return Compliance Detail.
version_added: '3.1.0'
extends_documentation_fragment:
  - cisco.dnac.module_info
author: Rafael Campos (@racampos)
options:
  headers:
    description: Additional headers.
    type: dict
  complianceType:
    description:
    - >
      ComplianceType query parameter. ComplianceType can have any value among 'NETWORK_PROFILE', 'IMAGE',
      'APPLICATION_VISIBILITY', 'FABRIC', 'PSIRT', 'RUNNING_CONFIG', 'WORKFLOW'.
    type: str
  complianceStatus:
    description:
    - >
      ComplianceStatus query parameter. Compliance status can have value among 'COMPLIANT', 'NON_COMPLIANT',
      'IN_PROGRESS', 'NOT_AVAILABLE', 'NOT_APPLICABLE', 'ERROR'.
    type: str
  deviceUuid:
    description:
    - DeviceUuid query parameter. Comma separated deviceUuids.
    type: str
  offset:
    description:
    - Offset query parameter. Offset/starting row.
    type: int
  limit:
    description:
    - Limit query parameter. Number of records to be retrieved.
    type: int
requirements:
- dnacentersdk >= 2.5.5
- python >= 3.5
seealso:
- name: Cisco DNA Center documentation for Compliance GetComplianceDetail
  description: Complete reference of the GetComplianceDetail API.
  link: https://developer.cisco.com/docs/dna-center/#!get-compliance-detail
notes:
  - SDK Method used are
    compliance.Compliance.get_compliance_detail,

  - Paths used are
    get /dna/intent/api/v1/compliance/detail,

"""

EXAMPLES = r"""
- name: Get all Compliance Device Details
  cisco.dnac.compliance_device_details_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers: "{{my_headers | from_json}}"
    complianceType: string
    complianceStatus: string
    deviceUuid: string
    offset: 0
    limit: 0
  register: result

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "version": "string",
      "response": [
        {
          "complianceType": "string",
          "lastSyncTime": 0,
          "deviceUuid": "string",
          "displayName": "string",
          "status": "string",
          "category": "string",
          "lastUpdateTime": 0,
          "state": "string"
        }
      ]
    }
"""
