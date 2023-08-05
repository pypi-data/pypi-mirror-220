#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: associate_site_to_network_profile
short_description: Resource module for Associate Site To Network Profile
description:
- Manage operation create of the resource Associate Site To Network Profile.
- Associate Site to a Network Profile.
version_added: '4.0.0'
extends_documentation_fragment:
  - cisco.dnac.module
author: Rafael Campos (@racampos)
options:
  networkProfileId:
    description: NetworkProfileId path parameter. Network-Profile Id to be associated.
    type: str
  siteId:
    description: SiteId path parameter. Site Id to be associated.
    type: str
requirements:
- dnacentersdk >= 2.5.5
- python >= 3.5
seealso:
- name: Cisco DNA Center documentation for Site Design Associate
  description: Complete reference of the Associate API.
  link: https://developer.cisco.com/docs/dna-center/#!associate
notes:
  - SDK Method used are
    site_design.SiteDesign.associate,

  - Paths used are
    post /dna/intent/api/v1/networkprofile/{networkProfileId}/site/{siteId},

"""

EXAMPLES = r"""
- name: Create
  cisco.dnac.associate_site_to_network_profile:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    networkProfileId: string
    siteId: string

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "version": "string",
      "response": {
        "taskId": "string",
        "url": "string"
      }
    }
"""
