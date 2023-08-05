#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ec2_vpc_net_info
version_added: 1.0.0
short_description: Gather information about ec2 VPCs in AWS
description:
    - Gather information about ec2 VPCs in AWS
author: "Rob White (@wimnat)"
options:
  vpc_ids:
    description:
      - A list of VPC IDs that exist in your account.
    type: list
    elements: str
    default: []
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value.
        See U(https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html) for possible filters.
    type: dict
    default: {}
extends_documentation_fragment:
  - amazon.aws.common.modules
  - amazon.aws.region.modules
  - amazon.aws.boto3
"""

EXAMPLES = r"""
# Note: These examples do not set authentication details, see the AWS Guide for details.

# Gather information about all VPCs
- amazon.aws.ec2_vpc_net_info:

# Gather information about a particular VPC using VPC ID
- amazon.aws.ec2_vpc_net_info:
    vpc_ids: vpc-00112233

# Gather information about any VPC with a tag key Name and value Example
- amazon.aws.ec2_vpc_net_info:
    filters:
      "tag:Name": Example
"""

RETURN = r"""
vpcs:
    description: Returns an array of complex objects as described below.
    returned: success
    type: complex
    contains:
        id:
            description: The ID of the VPC (for backwards compatibility).
            returned: always
            type: str
        vpc_id:
            description: The ID of the VPC.
            returned: always
            type: str
        state:
            description: The state of the VPC.
            returned: always
            type: str
        tags:
            description: A dict of tags associated with the VPC.
            returned: always
            type: dict
        instance_tenancy:
            description: The instance tenancy setting for the VPC.
            returned: always
            type: str
        is_default:
            description: True if this is the default VPC for account.
            returned: always
            type: bool
        cidr_block:
            description: The IPv4 CIDR block assigned to the VPC.
            returned: always
            type: str
        enable_dns_hostnames:
            description: True/False depending on attribute setting for DNS hostnames support.
            returned: always
            type: bool
        enable_dns_support:
            description: True/False depending on attribute setting for DNS support.
            returned: always
            type: bool
        cidr_block_association_set:
            description: An array of IPv4 cidr block association set information.
            returned: always
            type: complex
            contains:
                association_id:
                    description: The association ID.
                    returned: always
                    type: str
                cidr_block:
                    description: The IPv4 CIDR block that is associated with the VPC.
                    returned: always
                    type: str
                cidr_block_state:
                    description: A hash/dict that contains a single item. The state of the cidr block association.
                    returned: always
                    type: dict
                    contains:
                        state:
                            description: The CIDR block association state.
                            returned: always
                            type: str
        ipv6_cidr_block_association_set:
            description: An array of IPv6 cidr block association set information.
            returned: always
            type: complex
            contains:
                association_id:
                    description: The association ID.
                    returned: always
                    type: str
                ipv6_cidr_block:
                    description: The IPv6 CIDR block that is associated with the VPC.
                    returned: always
                    type: str
                ipv6_cidr_block_state:
                    description: A hash/dict that contains a single item. The state of the cidr block association.
                    returned: always
                    type: dict
                    contains:
                        state:
                            description: The CIDR block association state.
                            returned: always
                            type: str
        owner_id:
            description: The AWS account which owns the VPC.
            returned: always
            type: str
            sample: 123456789012
        dhcp_options_id:
            description: The ID of the DHCP options associated with this VPC.
            returned: always
            type: str
            sample: dopt-12345678
"""

try:
    import botocore
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict

from ansible_collections.amazon.aws.plugins.module_utils.modules import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.botocore import is_boto3_error_code
from ansible_collections.amazon.aws.plugins.module_utils.retries import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.transformation import ansible_dict_to_boto3_filter_list
from ansible_collections.amazon.aws.plugins.module_utils.tagging import boto3_tag_list_to_ansible_dict


def describe_vpcs(connection, module):
    """
    Describe VPCs.

    connection  : boto3 client connection object
    module  : AnsibleAWSModule object
    """
    # collect parameters
    filters = ansible_dict_to_boto3_filter_list(module.params.get("filters"))
    vpc_ids = module.params.get("vpc_ids")

    # init empty list for return vars
    vpc_info = list()

    # Get the basic VPC info
    try:
        response = connection.describe_vpcs(VpcIds=vpc_ids, Filters=filters, aws_retry=True)
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg=f"Unable to describe VPCs {vpc_ids}")

    # We can get these results in bulk but still needs two separate calls to the API
    dns_support = {}
    dns_hostnames = {}
    # Loop through the results and add the other VPC attributes we gathered
    for vpc in response["Vpcs"]:
        error_message = "Unable to describe VPC attribute {0} on VPC {1}"
        dns_support = describe_vpc_attribute(module, connection, vpc["VpcId"], "enableDnsSupport", error_message)
        dns_hostnames = describe_vpc_attribute(module, connection, vpc["VpcId"], "enableDnsHostnames", error_message)

        # add the two DNS attributes
        if dns_support:
            vpc["EnableDnsSupport"] = dns_support["EnableDnsSupport"].get("Value")
        if dns_hostnames:
            vpc["EnableDnsHostnames"] = dns_hostnames["EnableDnsHostnames"].get("Value")
        # for backwards compatibility
        vpc["id"] = vpc["VpcId"]
        vpc_info.append(camel_dict_to_snake_dict(vpc))
        # convert tag list to ansible dict
        vpc_info[-1]["tags"] = boto3_tag_list_to_ansible_dict(vpc.get("Tags", []))

    module.exit_json(vpcs=vpc_info)


def describe_vpc_attribute(module, connection, vpc, attribute, error_message):
    result = None
    try:
        return connection.describe_vpc_attribute(VpcId=vpc, Attribute=attribute, aws_retry=True)
    except is_boto3_error_code("InvalidVpcID.NotFound"):
        module.warn(error_message.format(attribute, vpc))
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg=error_message.format(attribute, vpc))
    return result


def main():
    argument_spec = dict(
        vpc_ids=dict(type="list", elements="str", default=[]),
        filters=dict(type="dict", default={}),
    )

    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)

    connection = module.client("ec2", retry_decorator=AWSRetry.jittered_backoff(retries=10))

    describe_vpcs(connection, module)


if __name__ == "__main__":
    main()
