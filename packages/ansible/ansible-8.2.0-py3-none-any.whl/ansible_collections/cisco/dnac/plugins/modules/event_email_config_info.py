#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: event_email_config_info
short_description: Information module for Event Email Config
description:
- Get all Event Email Config.
- Get Email Destination.
version_added: '6.7.0'
extends_documentation_fragment:
  - cisco.dnac.module_info
author: Rafael Campos (@racampos)
options:
  headers:
    description: Additional headers.
    type: dict
requirements:
- dnacentersdk >= 2.5.5
- python >= 3.5
seealso:
- name: Cisco DNA Center documentation for Event Management GetEmailDestination
  description: Complete reference of the GetEmailDestination API.
  link: https://developer.cisco.com/docs/dna-center/#!get-email-destination
notes:
  - SDK Method used are
    event_management.EventManagement.get_email_destination,

  - Paths used are
    get /dna/intent/api/v1/event/email-config,

"""

EXAMPLES = r"""
- name: Get all Event Email Config
  cisco.dnac.event_email_config_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers: "{{my_headers | from_json}}"
  register: result

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: list
  elements: dict
  sample: >
    [
      {
        "emailConfigId": "string",
        "primarySMTPConfig": {
          "hostName": "string",
          "port": "string",
          "userName": "string",
          "password": "string",
          "security": "string"
        },
        "secondarySMTPConfig": {
          "hostName": "string",
          "port": "string",
          "userName": "string",
          "password": "string",
          "security": "string"
        },
        "fromEmail": "string",
        "toEmail": "string",
        "subject": "string",
        "version": "string",
        "tenantId": "string"
      }
    ]
"""
