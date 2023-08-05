#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: sg_acl_bulk_request
short_description: Resource module for SGACL Bulk Request
description:
- Manage operation update of the resource SGACL Bulk Request.
- This API allows the client to submit the bulk request.
version_added: '1.0.0'
extends_documentation_fragment:
  - cisco.ise.module
author: Rafael Campos (@racampos)
options:
  operationType:
    description: SGACL Bulk Request's operationType.
    type: str
  resourceMediaType:
    description: SGACL Bulk Request's resourceMediaType.
    type: str
requirements:
- ciscoisesdk >= 2.0.8
- python >= 3.5
seealso:
- name: Cisco ISE documentation for SecurityGroupsACLs
  description: Complete reference of the SecurityGroupsACLs API.
  link: https://developer.cisco.com/docs/identity-services-engine/v1/#!sgacl
notes:
  - SDK Method used are
    security_groups_acls.SecurityGroupsAcls.bulk_request_for_security_groups_acl,

  - Paths used are
    put /ers/config/sgacl/bulk/submit,

"""

EXAMPLES = r"""
- name: Update all
  cisco.ise.sg_acl_bulk_request:
    ise_hostname: "{{ise_hostname}}"
    ise_username: "{{ise_username}}"
    ise_password: "{{ise_password}}"
    ise_verify: "{{ise_verify}}"
    operationType: string
    resourceMediaType: string

"""

RETURN = r"""
ise_response:
  description: A dictionary or list with the response returned by the Cisco ISE Python SDK
  returned: always
  type: dict
  sample: >
    {}
"""
