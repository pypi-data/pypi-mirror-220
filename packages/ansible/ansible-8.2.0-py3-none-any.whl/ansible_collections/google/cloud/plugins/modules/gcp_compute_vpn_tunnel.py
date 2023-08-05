#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    Type: MMv1     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_compute_vpn_tunnel
description:
- VPN tunnel resource.
short_description: Creates a GCP VpnTunnel
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
    type: str
  name:
    description:
    - Name of the resource. The name must be 1-63 characters long, and comply with
      RFC1035. Specifically, the name must be 1-63 characters long and match the regular
      expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must
      be a lowercase letter, and all following characters must be a dash, lowercase
      letter, or digit, except the last character, which cannot be a dash.
    required: true
    type: str
  description:
    description:
    - An optional description of this resource.
    required: false
    type: str
  target_vpn_gateway:
    description:
    - URL of the Target VPN gateway with which this VPN tunnel is associated.
    - 'This field represents a link to a TargetVpnGateway resource in GCP. It can
      be specified in two ways. First, you can place a dictionary with key ''selfLink''
      and value of your resource''s selfLink Alternatively, you can add `register:
      name-of-resource` to a gcp_compute_target_vpn_gateway task and then set this
      target_vpn_gateway field to "{{ name-of-resource }}"'
    required: false
    type: dict
  vpn_gateway:
    description:
    - URL of the VPN gateway with which this VPN tunnel is associated.
    - This must be used if a High Availability VPN gateway resource is created.
    - 'This field represents a link to a VpnGateway resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''selfLink'' and value
      of your resource''s selfLink Alternatively, you can add `register: name-of-resource`
      to a gcp_compute_vpn_gateway task and then set this vpn_gateway field to "{{
      name-of-resource }}"'
    required: false
    type: dict
  vpn_gateway_interface:
    description:
    - The interface ID of the VPN gateway with which this VPN tunnel is associated.
    required: false
    type: int
  peer_external_gateway:
    description:
    - URL of the peer side external VPN gateway to which this VPN tunnel is connected.
    - 'This field represents a link to a ExternalVpnGateway resource in GCP. It can
      be specified in two ways. First, you can place a dictionary with key ''selfLink''
      and value of your resource''s selfLink Alternatively, you can add `register:
      name-of-resource` to a gcp_compute_external_vpn_gateway task and then set this
      peer_external_gateway field to "{{ name-of-resource }}"'
    required: false
    type: dict
  peer_external_gateway_interface:
    description:
    - The interface ID of the external VPN gateway to which this VPN tunnel is connected.
    required: false
    type: int
  peer_gcp_gateway:
    description:
    - URL of the peer side HA GCP VPN gateway to which this VPN tunnel is connected.
    - If provided, the VPN tunnel will automatically use the same vpn_gateway_interface
      ID in the peer GCP VPN gateway.
    - 'This field represents a link to a VpnGateway resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''selfLink'' and value
      of your resource''s selfLink Alternatively, you can add `register: name-of-resource`
      to a gcp_compute_vpn_gateway task and then set this peer_gcp_gateway field to
      "{{ name-of-resource }}"'
    required: false
    type: dict
  router:
    description:
    - URL of router resource to be used for dynamic routing.
    - 'This field represents a link to a Router resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''selfLink'' and value
      of your resource''s selfLink Alternatively, you can add `register: name-of-resource`
      to a gcp_compute_router task and then set this router field to "{{ name-of-resource
      }}"'
    required: false
    type: dict
  peer_ip:
    description:
    - IP address of the peer VPN gateway. Only IPv4 is supported.
    required: false
    type: str
  shared_secret:
    description:
    - Shared secret used to set the secure session between the Cloud VPN gateway and
      the peer VPN gateway.
    required: true
    type: str
  ike_version:
    description:
    - IKE protocol version to use when establishing the VPN tunnel with peer VPN gateway.
    - Acceptable IKE versions are 1 or 2. Default version is 2.
    required: false
    default: '2'
    type: int
  local_traffic_selector:
    description:
    - Local traffic selector to use when establishing the VPN tunnel with peer VPN
      gateway. The value should be a CIDR formatted string, for example `192.168.0.0/16`.
      The ranges should be disjoint.
    - Only IPv4 is supported.
    elements: str
    required: false
    type: list
  remote_traffic_selector:
    description:
    - Remote traffic selector to use when establishing the VPN tunnel with peer VPN
      gateway. The value should be a CIDR formatted string, for example `192.168.0.0/16`.
      The ranges should be disjoint.
    - Only IPv4 is supported.
    elements: str
    required: false
    type: list
  region:
    description:
    - The region where the tunnel is located.
    required: true
    type: str
  project:
    description:
    - The Google Cloud Platform project to use.
    type: str
  auth_kind:
    description:
    - The type of credential used.
    type: str
    required: true
    choices:
    - application
    - machineaccount
    - serviceaccount
    - accesstoken
  service_account_contents:
    description:
    - The contents of a Service Account JSON file, either in a dictionary or as a
      JSON string that represents it.
    type: jsonarg
  service_account_file:
    description:
    - The path of a Service Account JSON file if serviceaccount is selected as type.
    type: path
  service_account_email:
    description:
    - An optional service account email address if machineaccount is selected and
      the user does not wish to use the default email.
    type: str
  access_token:
    description:
    - An OAuth2 access token if credential type is accesstoken.
    type: str
  scopes:
    description:
    - Array of scopes to be used
    type: list
    elements: str
  env_type:
    description:
    - Specifies which Ansible environment you're running this module within.
    - This should not be set unless you know what you're doing.
    - This only alters the User Agent string for any API requests.
    type: str
notes:
- 'API Reference: U(https://cloud.google.com/compute/docs/reference/rest/v1/vpnTunnels)'
- 'Cloud VPN Overview: U(https://cloud.google.com/vpn/docs/concepts/overview)'
- 'Networks and Tunnel Routing: U(https://cloud.google.com/vpn/docs/concepts/choosing-networks-routing)'
- for authentication, you can set service_account_file using the C(GCP_SERVICE_ACCOUNT_FILE)
  env variable.
- for authentication, you can set service_account_contents using the C(GCP_SERVICE_ACCOUNT_CONTENTS)
  env variable.
- For authentication, you can set service_account_email using the C(GCP_SERVICE_ACCOUNT_EMAIL)
  env variable.
- For authentication, you can set access_token using the C(GCP_ACCESS_TOKEN)
  env variable.
- For authentication, you can set auth_kind using the C(GCP_AUTH_KIND) env variable.
- For authentication, you can set scopes using the C(GCP_SCOPES) env variable.
- Environment variables values will only be used if the playbook values are not set.
- The I(service_account_email) and I(service_account_file) options are mutually exclusive.
'''

EXAMPLES = '''
- name: create a network
  google.cloud.gcp_compute_network:
    name: network-vpn-tunnel
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: network

- name: create a router
  google.cloud.gcp_compute_router:
    name: router-vpn-tunnel
    network: "{{ network }}"
    bgp:
      asn: 64514
      advertise_mode: CUSTOM
      advertised_groups:
      - ALL_SUBNETS
      advertised_ip_ranges:
      - range: 1.2.3.4
      - range: 6.7.0.0/16
    region: us-central1
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: router

- name: create a target vpn gateway
  google.cloud.gcp_compute_target_vpn_gateway:
    name: gateway-vpn-tunnel
    region: us-west1
    network: "{{ network }}"
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: gateway

- name: create a vpn tunnel
  google.cloud.gcp_compute_vpn_tunnel:
    name: test_object
    region: us-west1
    target_vpn_gateway: "{{ gateway }}"
    router: "{{ router }}"
    shared_secret: super secret
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
id:
  description:
  - The unique identifier for the resource. This identifier is defined by the server.
  returned: success
  type: str
creationTimestamp:
  description:
  - Creation timestamp in RFC3339 text format.
  returned: success
  type: str
name:
  description:
  - Name of the resource. The name must be 1-63 characters long, and comply with RFC1035.
    Specifically, the name must be 1-63 characters long and match the regular expression
    `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase
    letter, and all following characters must be a dash, lowercase letter, or digit,
    except the last character, which cannot be a dash.
  returned: success
  type: str
description:
  description:
  - An optional description of this resource.
  returned: success
  type: str
targetVpnGateway:
  description:
  - URL of the Target VPN gateway with which this VPN tunnel is associated.
  returned: success
  type: dict
vpnGateway:
  description:
  - URL of the VPN gateway with which this VPN tunnel is associated.
  - This must be used if a High Availability VPN gateway resource is created.
  returned: success
  type: dict
vpnGatewayInterface:
  description:
  - The interface ID of the VPN gateway with which this VPN tunnel is associated.
  returned: success
  type: int
peerExternalGateway:
  description:
  - URL of the peer side external VPN gateway to which this VPN tunnel is connected.
  returned: success
  type: dict
peerExternalGatewayInterface:
  description:
  - The interface ID of the external VPN gateway to which this VPN tunnel is connected.
  returned: success
  type: int
peerGcpGateway:
  description:
  - URL of the peer side HA GCP VPN gateway to which this VPN tunnel is connected.
  - If provided, the VPN tunnel will automatically use the same vpn_gateway_interface
    ID in the peer GCP VPN gateway.
  returned: success
  type: dict
router:
  description:
  - URL of router resource to be used for dynamic routing.
  returned: success
  type: dict
peerIp:
  description:
  - IP address of the peer VPN gateway. Only IPv4 is supported.
  returned: success
  type: str
sharedSecret:
  description:
  - Shared secret used to set the secure session between the Cloud VPN gateway and
    the peer VPN gateway.
  returned: success
  type: str
sharedSecretHash:
  description:
  - Hash of the shared secret.
  returned: success
  type: str
ikeVersion:
  description:
  - IKE protocol version to use when establishing the VPN tunnel with peer VPN gateway.
  - Acceptable IKE versions are 1 or 2. Default version is 2.
  returned: success
  type: int
localTrafficSelector:
  description:
  - Local traffic selector to use when establishing the VPN tunnel with peer VPN gateway.
    The value should be a CIDR formatted string, for example `192.168.0.0/16`. The
    ranges should be disjoint.
  - Only IPv4 is supported.
  returned: success
  type: list
remoteTrafficSelector:
  description:
  - Remote traffic selector to use when establishing the VPN tunnel with peer VPN
    gateway. The value should be a CIDR formatted string, for example `192.168.0.0/16`.
    The ranges should be disjoint.
  - Only IPv4 is supported.
  returned: success
  type: list
region:
  description:
  - The region where the tunnel is located.
  returned: success
  type: str
'''

################################################################################
# Imports
################################################################################

from ansible_collections.google.cloud.plugins.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, replace_resource_dict
import json
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(required=True, type='str'),
            description=dict(type='str'),
            target_vpn_gateway=dict(type='dict'),
            vpn_gateway=dict(type='dict'),
            vpn_gateway_interface=dict(type='int'),
            peer_external_gateway=dict(type='dict'),
            peer_external_gateway_interface=dict(type='int'),
            peer_gcp_gateway=dict(type='dict'),
            router=dict(type='dict'),
            peer_ip=dict(type='str'),
            shared_secret=dict(required=True, type='str', no_log=True),
            ike_version=dict(default=2, type='int'),
            local_traffic_selector=dict(type='list', elements='str'),
            remote_traffic_selector=dict(type='list', elements='str'),
            region=dict(required=True, type='str'),
        ),
        mutually_exclusive=[['peer_external_gateway', 'peer_gcp_gateway']],
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/compute']

    state = module.params['state']
    kind = 'compute#vpnTunnel'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), kind)
                fetch = fetch_resource(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link, kind):
    delete(module, self_link(module), kind)
    create(module, collection(module), kind)


def delete(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'kind': 'compute#vpnTunnel',
        u'name': module.params.get('name'),
        u'description': module.params.get('description'),
        u'targetVpnGateway': replace_resource_dict(module.params.get(u'target_vpn_gateway', {}), 'selfLink'),
        u'vpnGateway': replace_resource_dict(module.params.get(u'vpn_gateway', {}), 'selfLink'),
        u'vpnGatewayInterface': module.params.get('vpn_gateway_interface'),
        u'peerExternalGateway': replace_resource_dict(module.params.get(u'peer_external_gateway', {}), 'selfLink'),
        u'peerExternalGatewayInterface': module.params.get('peer_external_gateway_interface'),
        u'peerGcpGateway': replace_resource_dict(module.params.get(u'peer_gcp_gateway', {}), 'selfLink'),
        u'router': replace_resource_dict(module.params.get(u'router', {}), 'selfLink'),
        u'peerIp': module.params.get('peer_ip'),
        u'sharedSecret': module.params.get('shared_secret'),
        u'ikeVersion': module.params.get('ike_version'),
        u'localTrafficSelector': module.params.get('local_traffic_selector'),
        u'remoteTrafficSelector': module.params.get('remote_traffic_selector'),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind, allow_not_found=True):
    auth = GcpSession(module, 'compute')
    return return_if_object(module, auth.get(link), kind, allow_not_found)


def self_link(module):
    return "https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/vpnTunnels/{name}".format(**module.params)


def collection(module):
    return "https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/vpnTunnels".format(**module.params)


def return_if_object(module, response, kind, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError):
        module.fail_json(msg="Invalid JSON response with error: %s" % response.text)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)
    # shared_secret is returned with stars instead of the
    # actual secret
    keys_to_ignore = ("sharedSecret")

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in keys_to_ignore:
            continue
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in keys_to_ignore:
            continue
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'id': response.get(u'id'),
        u'creationTimestamp': response.get(u'creationTimestamp'),
        u'name': response.get(u'name'),
        u'description': module.params.get('description'),
        u'targetVpnGateway': replace_resource_dict(module.params.get(u'target_vpn_gateway', {}), 'selfLink'),
        u'vpnGateway': replace_resource_dict(module.params.get(u'vpn_gateway', {}), 'selfLink'),
        u'vpnGatewayInterface': module.params.get('vpn_gateway_interface'),
        u'peerExternalGateway': replace_resource_dict(module.params.get(u'peer_external_gateway', {}), 'selfLink'),
        u'peerExternalGatewayInterface': response.get(u'peerExternalGatewayInterface'),
        u'peerGcpGateway': response.get(u'peerGcpGateway'),
        u'router': replace_resource_dict(module.params.get(u'router', {}), 'selfLink'),
        u'peerIp': response.get(u'peerIp'),
        u'sharedSecret': response.get(u'sharedSecret'),
        u'sharedSecretHash': response.get(u'sharedSecretHash'),
        u'ikeVersion': response.get(u'ikeVersion'),
        u'localTrafficSelector': response.get(u'localTrafficSelector'),
        u'remoteTrafficSelector': response.get(u'remoteTrafficSelector'),
    }


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/operations/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response, 'compute#operation')
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['status'])
    wait_done = wait_for_completion(status, op_result, module)
    return fetch_resource(module, navigate_hash(wait_done, ['targetLink']), 'compute#vpnTunnel')


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while status != 'DONE':
        raise_if_errors(op_result, ['error', 'errors'], module)
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, 'compute#operation', False)
        status = navigate_hash(op_result, ['status'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


if __name__ == '__main__':
    main()
