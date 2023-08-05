#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {"metadata_version": "1.1", "status": ["preview"], "supported_by": "community"}

DOCUMENTATION = r"""
---
module: mso_role
short_description: Manage roles
description:
- Manage roles on Cisco ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
options:
  role:
    description:
    - The name of the role.
    type: str
    aliases: [ name ]
  display_name:
    description:
    - The name of the role to be displayed in the web UI.
    type: str
  description:
    description:
    - The description of the role.
    type: str
  read_permissions:
    description:
    - A list of read permissions tied to this role.
    type: list
    elements: str
    choices:
    - backup-db
    - manage-audit-records
    - manage-labels
    - manage-roles
    - manage-schemas
    - manage-sites
    - manage-tenants
    - manage-tenant-schemas
    - manage-users
    - platform-logs
    - view-all-audit-records
    - view-labels
    - view-roles
    - view-schemas
    - view-sites
    - view-tenants
    - view-tenant-schemas
    - view-users
  write_permissions:
    description:
    - A list of write permissions tied to this role.
    type: list
    elements: str
    aliases: [ permissions ]
    choices:
    - backup-db
    - manage-audit-records
    - manage-labels
    - manage-roles
    - manage-schemas
    - manage-sites
    - manage-tenants
    - manage-tenant-schemas
    - manage-users
    - platform-logs
    - view-all-audit-records
    - view-labels
    - view-roles
    - view-schemas
    - view-sites
    - view-tenants
    - view-tenant-schemas
    - view-users
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: cisco.mso.modules
"""

EXAMPLES = r"""
- name: Add a new role
  cisco.mso.mso_role:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    role: readOnly
    display_name: Read Only
    description: Read-only access for troubleshooting
    read_permissions:
    - view-roles
    - view-schemas
    - view-sites
    - view-tenants
    - view-tenant-schemas
    - view-users
    write_permissions:
    - manage-roles
    - manage-schemas
    - manage-sites
    - manage-tenants
    - manage-tenant-schemas
    - manage-users
    state: present
  delegate_to: localhost

- name: Remove a role
  cisco.mso.mso_role:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    role: readOnly
    state: absent
  delegate_to: localhost

- name: Query a role
  cisco.mso.mso_role:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    role: readOnly
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all roles
  cisco.mso.mso_role:
    host: mso_host
    username: admin
    password: SomeSecretPassword
    state: query
  delegate_to: localhost
  register: query_result
"""

RETURN = r"""
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.mso.plugins.module_utils.mso import MSOModule, mso_argument_spec


def main():
    argument_spec = mso_argument_spec()
    argument_spec.update(
        role=dict(type="str", aliases=["name"]),
        display_name=dict(type="str"),
        description=dict(type="str"),
        read_permissions=dict(
            type="list",
            elements="str",
            choices=[
                "backup-db",
                "manage-audit-records",
                "manage-labels",
                "manage-roles",
                "manage-schemas",
                "manage-sites",
                "manage-tenants",
                "manage-tenant-schemas",
                "manage-users",
                "platform-logs",
                "view-all-audit-records",
                "view-labels",
                "view-roles",
                "view-schemas",
                "view-sites",
                "view-tenants",
                "view-tenant-schemas",
                "view-users",
            ],
        ),
        write_permissions=dict(
            type="list",
            elements="str",
            aliases=["permissions"],
            choices=[
                "backup-db",
                "manage-audit-records",
                "manage-labels",
                "manage-roles",
                "manage-schemas",
                "manage-sites",
                "manage-tenants",
                "manage-tenant-schemas",
                "manage-users",
                "platform-logs",
                "view-all-audit-records",
                "view-labels",
                "view-roles",
                "view-schemas",
                "view-sites",
                "view-tenants",
                "view-tenant-schemas",
                "view-users",
            ],
        ),
        state=dict(type="str", default="present", choices=["absent", "present", "query"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ["state", "absent", ["role"]],
            ["state", "present", ["role"]],
        ],
    )

    role = module.params.get("role")
    description = module.params.get("description")
    read_permissions = module.params.get("read_permissions")
    write_permissions = module.params.get("write_permissions")
    state = module.params.get("state")

    mso = MSOModule(module)

    role_id = None
    path = "roles"

    # Query for existing object(s)
    if role:
        mso.existing = mso.get_obj(path, name=role)
        if mso.existing:
            role_id = mso.existing.get("id")
            # If we found an existing object, continue with it
            path = "roles/{id}".format(id=role_id)
    else:
        mso.existing = mso.query_objs(path)

    if state == "query":
        pass

    elif state == "absent":
        mso.previous = mso.existing
        if mso.existing:
            if module.check_mode:
                mso.existing = {}
            else:
                mso.existing = mso.request(path, method="DELETE")

    elif state == "present":
        mso.previous = mso.existing

        payload = dict(
            id=role_id,
            name=role,
            displayName=role,
            description=description,
            readPermissions=read_permissions,
            writePermissions=write_permissions,
        )

        mso.sanitize(payload, collate=True)

        if mso.existing:
            if mso.check_changed():
                if module.check_mode:
                    mso.existing = mso.proposed
                else:
                    mso.existing = mso.request(path, method="PUT", data=mso.sent)
        else:
            if module.check_mode:
                mso.existing = mso.proposed
            else:
                mso.existing = mso.request(path, method="POST", data=mso.sent)

    mso.exit_json()


if __name__ == "__main__":
    main()
