#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ec2_tag
version_added: 1.0.0
short_description: Create and remove tags on ec2 resources
description:
    - Creates, modifies and removes tags for any EC2 resource.
    - Resources are referenced by their resource id (for example, an instance being i-XXXXXXX, a VPC being vpc-XXXXXXX).
    - This module is designed to be used with complex args (tags), see the examples.
options:
  resource:
    description:
      - The EC2 resource id.
    required: true
    type: str
  state:
    description:
      - Whether the tags should be present or absent on the resource.
      - The use of I(state=list) to interrogate the tags of an instance was
        deprecated in release 1.0.0 and is no longer available in release 4.0.0.
        The 'list' functionality has been moved to a dedicated module
        M(amazon.aws.ec2_tag_info).
    default: present
    choices: ['present', 'absent']
    type: str
  tags:
    description:
      - A dictionary of tags to add or remove from the resource.
      - If the value provided for a key is not set and I(state=absent), the tag will be removed regardless of its current value.
    type: dict
    required: true
  purge_tags:
    description:
      - Whether unspecified tags should be removed from the resource.
      - Note that when combined with I(state=absent), specified tags with non-matching values are not purged.
    type: bool
    default: false

author:
  - Lester Wade (@lwade)
  - Paul Arthur (@flowerysong)
extends_documentation_fragment:
  - amazon.aws.common.modules
  - amazon.aws.region.modules
  - amazon.aws.boto3
"""

EXAMPLES = r"""
- name: Ensure tags are present on a resource
  amazon.aws.ec2_tag:
    region: eu-west-1
    resource: vol-XXXXXX
    state: present
    tags:
      Name: ubervol
      env: prod

- name: Ensure all volumes are tagged
  amazon.aws.ec2_tag:
    region:  eu-west-1
    resource: '{{ item.id }}'
    state: present
    tags:
      Name: dbserver
      Env: production
  loop: '{{ ec2_vol.volumes }}'

- name: Remove the Env tag
  amazon.aws.ec2_tag:
    region: eu-west-1
    resource: i-xxxxxxxxxxxxxxxxx
    tags:
      Env:
    state: absent

- name: Remove the Env tag if it's currently 'development'
  amazon.aws.ec2_tag:
    region: eu-west-1
    resource: i-xxxxxxxxxxxxxxxxx
    tags:
      Env: development
    state: absent

- name: Remove all tags except for Name from an instance
  amazon.aws.ec2_tag:
    region: eu-west-1
    resource: i-xxxxxxxxxxxxxxxxx
    tags:
        Name: ''
    state: absent
    purge_tags: true
"""

RETURN = r"""
tags:
  description: A dict containing the tags on the resource
  returned: always
  type: dict
added_tags:
  description: A dict of tags that were added to the resource
  returned: If tags were added
  type: dict
removed_tags:
  description: A dict of tags that were removed from the resource
  returned: If tags were removed
  type: dict
"""

from ansible_collections.amazon.aws.plugins.module_utils.modules import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.tagging import compare_aws_tags
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import describe_ec2_tags
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import ensure_ec2_tags
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import remove_ec2_tags


def main():
    argument_spec = dict(
        resource=dict(required=True),
        tags=dict(type="dict", required=True),
        purge_tags=dict(type="bool", default=False),
        state=dict(default="present", choices=["present", "absent"]),
    )
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)

    resource = module.params["resource"]
    tags = module.params["tags"]
    state = module.params["state"]
    purge_tags = module.params["purge_tags"]

    result = {"changed": False}

    ec2 = module.client("ec2")

    current_tags = describe_ec2_tags(ec2, module, resource)

    if state == "absent":
        removed_tags = {}
        for key in tags:
            if key in current_tags and (tags[key] is None or current_tags[key] == tags[key]):
                result["changed"] = True
                removed_tags[key] = current_tags[key]
        result["removed_tags"] = removed_tags
        remove_ec2_tags(ec2, module, resource, removed_tags.keys())

    if state == "present":
        tags_to_set, tags_to_unset = compare_aws_tags(current_tags, tags, purge_tags)
        if tags_to_unset:
            result["removed_tags"] = {}
            for key in tags_to_unset:
                result["removed_tags"][key] = current_tags[key]
        result["added_tags"] = tags_to_set
        result["changed"] = ensure_ec2_tags(ec2, module, resource, tags=tags, purge_tags=purge_tags)

    result["tags"] = describe_ec2_tags(ec2, module, resource)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
