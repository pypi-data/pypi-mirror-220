#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: user_info
short_description: Information module for User
description:
- Get all User.
- Get all users for the Cisco DNA Center system.
version_added: '6.7.0'
extends_documentation_fragment:
  - cisco.dnac.module_info
author: Rafael Campos (@racampos)
options:
  headers:
    description: Additional headers.
    type: dict
  invokeSource:
    description:
    - InvokeSource query parameter. The source that invokes this API.
    type: str
requirements:
- dnacentersdk >= 2.5.5
- python >= 3.5
seealso:
- name: Cisco DNA Center documentation for User and Roles GetUsersAPI
  description: Complete reference of the GetUsersAPI API.
  link: https://developer.cisco.com/docs/dna-center/#!get-users-api
notes:
  - SDK Method used are
    userand_roles.UserandRoles.get_users_ap_i,

  - Paths used are
    get /dna/system/api/v1/user,

"""

EXAMPLES = r"""
- name: Get all User
  cisco.dnac.user_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers: "{{my_headers | from_json}}"
    invokeSource: string
  register: result

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "users": [
        {
          "firstName": "string",
          "lastName": "string",
          "authSource": "string",
          "passphraseUpdateTime": "string",
          "roleList": [
            "string"
          ],
          "userId": "string",
          "email": "string",
          "username": "string"
        }
      ]
    }
"""
