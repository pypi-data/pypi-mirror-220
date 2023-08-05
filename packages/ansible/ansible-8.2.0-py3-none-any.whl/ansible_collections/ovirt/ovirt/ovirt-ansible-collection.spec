%global namespace ovirt
%global collectionname ovirt
%global ansible_collections_dir ansible/collections/ansible_collections

Name:		ovirt-ansible-collection
Summary:	Ansible collection to manage all ovirt modules and inventory
Version:	3.1.2
Release:	1%{?release_suffix}%{?dist}
Source0:	http://resources.ovirt.org/pub/src/ovirt-ansible-collection/ovirt-ansible-collection-3.1.2.tar.gz
License:	ASL 2.0 and GPLv3+
BuildArch:	noarch
Url:		http://www.ovirt.org

BuildRequires:	ansible-core
BuildRequires:	ansible-test
%if 0%{?rhel} > 7 && 0%{?rhel} < 9
BuildRequires:	glibc-langpack-en
%endif

Requires:	ansible-core >= 2.13.0
Requires:	ansible-collection-ansible-netcommon
Requires:	ansible-collection-ansible-posix
Requires:	ansible-collection-ansible-utils
Requires:	qemu-img

%if 0%{?rhel} >= 9
Requires:	python3.11-ovirt-imageio-client
Requires:	python3.11-ovirt-engine-sdk4 >= 4.5.0
Requires:	python3.11-jmespath
Requires:	python3.11-passlib
%endif

%if 0%{?rhel} < 9
Requires:	python3.11-ovirt-imageio-client
Requires:	python3.11-ovirt-engine-sdk4 >= 4.5.0
Requires:	python3.11-jmespath
Requires:	python3.11-passlib
%endif

Obsoletes:	ansible < 2.10.0
Obsoletes:	ovirt-ansible-cluster-upgrade
Obsoletes:	ovirt-ansible-disaster-recovery
Obsoletes:	ovirt-ansible-engine-setup
Obsoletes:	ovirt-ansible-hosted-engine-setup
Obsoletes:	ovirt-ansible-image-template
Obsoletes:	ovirt-ansible-infra
Obsoletes:	ovirt-ansible-manageiq
Obsoletes:	ovirt-ansible-repositories
Obsoletes:	ovirt-ansible-roles
Obsoletes:	ovirt-ansible-shutdown-env
Obsoletes:	ovirt-ansible-vm-infra

Provides:	ovirt-ansible-cluster-upgrade
Provides:	ovirt-ansible-disaster-recovery
Provides:	ovirt-ansible-engine-setup
Provides:	ovirt-ansible-hosted-engine-setup
Provides:	ovirt-ansible-image-template
Provides:	ovirt-ansible-infra
Provides:	ovirt-ansible-manageiq
Provides:	ovirt-ansible-repositories
Provides:	ovirt-ansible-roles
Provides:	ovirt-ansible-shutdown-env
Provides:	ovirt-ansible-vm-infra

%description
This Ansible collection is to manage all ovirt modules and inventory

%prep
%setup -c -q

%build

%install
export PKG_DATA_DIR_ORIG=%{_datadir}/%{ansible_collections_dir}
export PKG_DATA_DIR=%{buildroot}$PKG_DATA_DIR_ORIG
export PKG_DOC_DIR=%{buildroot}%{_pkgdocdir}
sh build.sh install %{collectionname}

%files
%{_datadir}/%{ansible_collections_dir}/%{namespace}
%if "%{collectionname}" == "rhv"
%{_datadir}/%{ansible_collections_dir}/ovirt
%endif

%doc README.md
%doc examples/

%license licenses

%changelog
* Thu Mar 23 2023 Martin Necas <mnecas@redhat.com> - 3.1.2-1
- Add Python 3.11 subpackage to be usable in ansible-core 2.14 for el8

* Fri Mar 3 2023 Martin Necas <mnecas@redhat.com> - 3.1.1-1
- hosted_engine_setup - Vdsm now uses -n flag for all qemu-img convert calls.
- ovirt_cluster_info - Fix example patter.
- ovirt_host - Fix refreshed state action.
- Add Python 3.11 subpackage to be usable in ansible-core 2.14

* Tue Feb 14 2023 Martin Necas <mnecas@redhat.com> - 3.1.0-1
- ovirt_host - Add refreshed state.
- ovirt_host - Wait for host to be in result state during upgrade.
- ovirt_network - Add default_route usage to the ovirt_network module.
- engine_setup - Remove provision_docker from tests.
- he-setup - Log the output sent to the serial console of the HostedEngineLocal VM to a file on the host, to allow diagnosing failures in that stage.
- he-setup - Run virt-install with options more suitable for debugging.
- he-setup - recently `virsh net-destroy default` doesn't delete the `virbr0`, so we need to delete it expicitly.
- info modules - Use dynamic collection name instead of ovirt.ovirt for deprecation warning.
- module_utils - replace `getargspec` with `getfullargspec` to support newer python 3.y versions.

* Mon Nov 28 2022 Martin Perina <mperina@redhat.com> - 3.0.0-1
- filters: Fix ovirtvmipsv4 with attribute and network
- ovirt_host: Fix kernel_params elemets
- ovirtvmipsv4: Fix filter list
- cluster_upgrade: Add default random uuid to engine_correlation_id
- image_template: Add template_bios_type
- Support ansible 2.14
- ovirt_nic: Add network_filter_parameters
- Support ansible-core-2.13 on EL8
- Use Python 3.9 on CS8 and CS9 builds
- Improving "ovirt_disk" (mostly documentation)
- cluster_upgrade: Fix the engine_correlation_id location

* Thu Oct 13 2022 Martin Necas <mnecas@redhat.com> - 2.3.0-1
- ovirt_host - Honor activate and reboot_after_installation when they are set to false with reinstalled host state
- ovirt_disk - Add read_only param for disk attachments
- ovirt_disk - Fix disk attachment to VM
- filters - Add documentation to all filters
- filters- Fix ovirtvmipsv4 when using attribute
- he-setup - Fix static ipv6 ifcfg setup
- repositories - RHV 4.4 SP1 is supported only on RHEL 8.6 EUS

* Mon Aug 15 2022 Martin Necas <mnecas@redhat.com> - 2.2.3-1
- cluster_upgrade - Skip host upgrades without anything to update
- hosted_engine_setup - Fix ovirt-provider-ovn-driver broken link
- hosted_engine_setup - restore - Remove host also based on name
- repositories - Fix example variable names

* Tue Aug 9 2022 Martin Necas <mnecas@redhat.com> - 2.2.2-1
- hosted_engine_setup - Detect hosted-engine-ha version using /usr/libexec/platform-python
- hosted_engine_setup - update ansible version in README
- repositories - Add mod_auth_openidc:2.3 and nodejs:14 to dnf modules

* Wed Aug 3 2022 Martin Necas <mnecas@redhat.com> - 2.2.1-1
- hosted_engine_setup - Fix hosted-engine.conf permissions and ownership
- hosted_engine_setup - During he_setup, configure ovn with he_host_address

* Mon Jul 25 2022 Martin Necas <mnecas@redhat.com> - 2.2.0-1
- cluster_upgrade - Fix starting up pinned vms
- disaster_recovery - Fix ansible-lint version 6.0.0 violations
- fix ansible-lint for basic roles(infra, vm_infra, engine_setup, repositories, cluster_upgrade)
- gluster_heal_info - Replacing gluster module to CLI to support RHV automation hub
- image_template - Remove static no - unsupported in ansible 2.12
- hosted_engine - During he_setup, configure ovn with he_host_name for correct operation of ovn
- hosted_engine - Handle migration to hosts that use systemd-coredump
- hosted_engine - Specify fqcn for ovirt_system_option_info
- hosted_engine - Align role with ansible-lint-6.0
- hosted_engine - Fix cleanup on el9
- ovirt_disk - Add warning for disk attachments
- ovirt_disk - Fix disk attachment to VM
- ovirt_disk - Updating the documentation - vm_name/vm_id and/or disk id parameter(s) are required when extending disk with non-unique name
- ovirt_host - Fix host wait
- ovirt_host - Fix restarted wait condition
- ovirt_qos, ovirt_disk_profile, ovirt_disk - Add modules to allow for creation and updating of disk_profiles
- ovirt_snapshot - Add vm_id to select VM
- ovirt_storage_domain - Fix inaccessible exception
- ovirt_vm - Add reset of VM
- ovirt_vm - Add virtio_scsi_enabled and multi_queues_enabled
- ovirt_vm - Add volatile
- ovirt_vm - Check if user inputed graphical protocol
- remove_stale_lun - Fix ansible-lint version 6.0.0 violations
- repositories - Add ovirt_repositories_rhsm_environment and FIPS fix
- repositories - Replace redhat_subscription and rhsm_repository with command
- repositories - Move fips check to satellite CA install block
- shutdown_env - Align role with ansible-lint-6.0.0

* Thu Jun 9 2022 Martin Necas <mnecas@redhat.com> - 2.1.0-1
- Add convert_to_bytes filter
- automation - Use python38 on el8 with ansible-core 2.12 and python39 on el9 with ansible-core 2.13
- engine_setup - Allow to disable cert validation
- ovirt - Remove deprecated distutils
- ovirt_vm - add wait_after_lease
- ovirt_vm - Fix parsing None arguments
- ovirt_vm - check if the snapshot exists
- hosted_engine_setup - make vdsm config cleanup optional
- hosted_engine_setup - Fix "'ansible' ModuleNotFoundError" in Disaster Recovery scripts
- hosted_engine_setup - Use command instead of firewalld module

* Fri Jun 3 2022 Martin Necas <mnecas@redhat.com> - 2.0.4-1
- Fix the admin user name when using keycloak
- Use cryptography < 37.0.0, as 37.0.0 emits a warning that fails testing
- Use rstcheck < 3.5.0, as 3.5.0 emits a warning that fails testing
- cluster_upgrade - fix wait_condition
- hosted_engine_setup - Allocate 128MiB instead of 1GiB for he_metadata
- hosted_engine_setup - Collect logs also on failures in 03_hosted_engine_final_tasks.yml
- hosted_engine_setup - Fix keycloak activation/checking
- hosted_engine_setup - Require 'detail' to be 'Up'
- hosted_engine_setup - fix archive ownership
- infra - add warning for multiple storage connections

* Wed Apr 13 2022 Martin Necas <mnecas@redhat.com> - 2.0.3-1
- spec: Obsolete ansible < 2.10.0
- ovirt_vm - Fix creating a RAW VM from a COW template
- ovirt_affinity_group - Add affinity labels
- invenory - Fix url address

* Wed Apr 6 2022 Martin Necas <mnecas@redhat.com> - 2.0.2-1
- cluster_upgrade: fix upgrade progress log_progress task

* Tue Apr 5 2022 Martin Necas <mnecas@redhat.com> - 2.0.1-1
- ovirt_storage_domain: make storage_format optional

* Mon Apr 4 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-1
- ovirt_template: add boot_menu and bios_type
- roles: hosted_engine_setup - Add an option to set the storage format when createing a storage domain and use it
- spec: Add python38-ovirt-imageio-client requirement

* Fri Mar 25 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-0.9.BETA
- roles: hosted_engine_setup: Fix call to engine-psql for vds_spm_id

* Fri Mar 25 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-0.8.BETA
- roles: cluster_upgrade: Directly log progress to the cluster
- spec: Add collections requirements

* Thu Mar 24 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-0.7.BETA
- roles: hosted_engine_setup: Replace calls to psql as postgres with engine_psql.sh
- spec: Add python38 requirements

* Tue Mar 8 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-0.6.BETA
- roles: hosted_engine_setup: Make cloud-init removal airgapped compatible
- roles: hosted_engine_setup: Replace xml community module
- roles: hosted_engine_setup: Support disa stig profile
- roles: hosted_engine_setup: Use cat command instead of lookup
- roles: repositories: Add satellite support
- plugins: Remove unused imports
- ovirt_host: Add enroll_certificate

* Tue Feb 15 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-0.5.BETA
- spec: Remove ansible requirements
- roles: cluster_upgrade: Shutdown vms only on pinned to upgrade host
- roles: hosted_engine_setup: Fix default gateway variable name

* Tue Jan 25 2022 Martin Necas <mnecas@redhat.com> - 2.0.0-0.4.BETA
- roles: cluster_upgrade: Add progress tracking/reporting
- roles: hosted_engine_setup: Adjust files permissions
- roles: hosted_engine_setup: Add an option to define OpenSCAP security profile name
- roles: engine_setup: Prepare answer files and default values for 4.5 release
- info - Add follow link url to api model links_summary

* Thu Dec 16 2021 Martin Perina <mperina@redhat.com> - 2.0.0-0.3.BETA
- roles: hosted_engine_setup: Set ownership of copied engine logs
- roles: hosted_engine_setup: Remove SPICE from graphic protocols

* Wed Dec 8 2021 Martin Perina <mperina@redhat.com> - 2.0.0-0.2.BETA
- Fix ovirt_storage_domain entity
- roles: hosted_engine_setup: check if abrt config files exists on HE deploy
- manageiq: deprecate role
- Fix remove_stale_lun whitespace
- ovirt_remove_stale_lun: Use add_host instead of delegate_to
- manageiq: add deprecation info
- ovirt_remove_stale_lun: Retry "multipath -f" while removing the LUNs
- engine_setup: skip pkg install in offline mode
- add virtio_scsi_multi_queues parameter to ovirt_vm
- Fix offline deployment
- ovirt_host: fix failed_state_after_reinstall condition

* Fri Dec 3 2021 Martin Necas <mnecas@redhat.com> - 2.0.0-0.1.BETA
- ovirt_disk - Use imageio client

* Fri Nov 26 2021 Martin Necas <mnecas@redhat.com> - 1.6.6-1
- ovirt_remove_stale_lun - Allow user to remove multiple LUNs
- ovirt_remove_stale_lun - Retry "multipath -f" while removing the LUNs
- manageiq - Add deprecation info
- info - Enable follow parameter
- info - bump deprecate version for fetch_nested and nested_attributes
- info - Rename follows to follow parameter and add alias

* Tue Oct 19 2021 Martin Necas <mnecas@redhat.com> - 1.6.5-1
- repositories - Update host and engine repositories to 4.4.9

* Mon Sep 27 2021 Martin Necas <mnecas@redhat.com> - 1.6.4-1
- repositories - Add no_log to redhat_subscription

* Tue Sep 21 2021 Martin Necas <mnecas@redhat.com> - 1.6.3-1
- repositories - Replace redhat_subscription and rhsm_repository with command
- gluster_heal_info - Replacing gluster module to CLI to support RHV automation hub
- image_template - Remove static no - unsupported in ansible 2.12

* Thu Aug 26 2021 Martin Necas <mnecas@redhat.com> - 1.6.2-1
- remove_stale_lun - Fix example for `remote_stale_lun` role to be able to run it from engine

* Wed Aug 25 2021 Martin Necas <mnecas@redhat.com> - 1.6.1-1
- ovirt_auth - Fix no_log token issue
- hosted_engine_setup - Use default bridge for IPv6 advertisements

* Wed Aug 11 2021 Martin Necas <mnecas@redhat.com> - 1.6.0-1
- remove_stale_lun - Add role for removing stale LUN
- readme - Update Ansible requirement
- ovirt_disk - Fix update_check with no VM
- ovirt_auth - Fix password and username requirements
- engine_setup - Wait for webserver up after engine-config reboot
- hosted_engine_setup - Update Ansible requirements in README
- hosted_engine_setup - Pause deployment on failure of 'engine-backup --mode=restore'
- hosted_engine_setup - Text change - Consistently use 'bootstrap engine VM'
- hosted_engine_setup - Align with ansible-lint 5.0.0

* Thu Jul 22 2021 Martin Necas <mnecas@redhat.com> - 1.5.4-1
- hosted_engine_setup - Allow FIPS on HE VM
- hosted_engine_setup - remove duplicate tasks
- hosted_engine_setup - Use forward network during an IPv6 deployment
- ovirt_permission - fix group search that has space in it's name

* Fri Jun 25 2021 Martin Necas <mnecas@redhat.com> - 1.5.3-1
- disaster_recovery - Don't rely on safe_eval being able to do math/concat
- hosted_engine_setup - Minor doc update
- hosted_engine_setup - Fix engine vm add_host for the target machine

* Wed Jun 23 2021 Martin Necas <mnecas@redhat.com> - 1.5.2-1
- ovirt_vm - Add default return value to check_placement_policy.
- hosted_engine_setup - Do not try to sync at end of full_execution.

* Thu Jun 17 2021 Martin Necas <mnecas@redhat.com> - 1.5.1-1
- hosted_engine_setup - Filter VLAN devices with bad names
- ovirt_vm - Add placement_policy_hosts
- infra - Add external_provider parameter on networks role of infra role
- hosted_engine_setup - use-ansible-host
- hosted_engine_setup - Remove cloud-init configuration
- ovirt inventory plugin - allow several valid values for the `plugin` key

* Fri Jun 4 2021 Martin Necas <mnecas@redhat.com> - 1.5.0-1
- ovirt_host - Update iscsi target struct
- infra - Storage fix parameters typo
- disaster_recovery - Change conf paths to relative paths
- hosted_engine_setup - Add pause option before engine-setup
- hosted_engine_setup - Align with ansible-lint 5.0.0
- hosted_engine_setup - Remove leftover code and omit parameters
- hosted_engine_setup - Use ovirt_host module to discover iscsi

* Fri Apr 23 2021 Martin Necas <mnecas@redhat.com> - 1.4.2-1
- repositories - Add ppc host
- repositories - Remove ansible channels from RHV 4.4
- infra - Remove storage connection target usage
- hosted_engine_setup - Fix the appliance distribution
- hosted_engine_setup - Add an error message for FIPS on CentOS
- ovirt_vm - Allow cluster migration

* Mon Mar 22 2021 Martin Necas <mnecas@redhat.com> - 1.4.1-1
- hosted_engine_setup - Fix auth revoke

* Tue Mar 16 2021 Martin Necas <mnecas@redhat.com> - 1.4.0-1
- cluster_upgrade - Add correlation-id header
- engine_setup - Add skip renew pki confirm
- examples - Add recipe for removing DM device
- hosted_engine_setup - Filter devices with unsupported bond mode
- infra - Add reboot host parameters
- ovirt_disk - Add SATA support
- ovirt_user - Add ssh_public_key
- Set auth options into argument spec definition

* Wed Feb 10 2021 Martin Necas <mnecas@redhat.com> - 1.3.1-1
- ovirt_host - Add reboot_after_installation option
- hosted_engine_setup - Disable reboot_after_installation

* Thu Jan 28 2021 Martin Necas <mnecas@redhat.com> - 1.3.0-1
- ovirt_system_option_info - Add new module
- ansible-builder - Update bindep
- hosted_engine_setup - Collect all engine /var/log
- hosted_engine_setup - Use ovirt_system_option_info instead of REST API
- ovirt_disk - Add install warning
- ovirt_info - Fragment add auth suboptions to documentation

* Mon Dec 14 2020 Martin Necas <mnecas@redhat.com> - 1.2.4-1
- infra - Allow remove of user without password
- inventory plugin - Correct os_type name
- ovirt_disk - automatically detect virtual size of qcow image

* Mon Nov 30 2020 Martin Necas <mnecas@redhat.com> - 1.2.3-1
- Add hosted_engine_setup after_add_host hook
- Add engine_setup restore files

* Thu Nov 12 2020 Martin Perina <mperina@redhat.com> - 1.2.2-1
- inventory plugin - Fix Python 2 timestamp issue
- hosted_engine_setup - Clean VNC encryption config
- RPM packaging - Add Provides to previous oVirt Ansible roles RPMs to
  minimize upgrade issues

* Mon Nov 2 2020 Martin Necas <mnecas@redhat.com> - 1.2.1-1
- Split README for build and GitHub
- Add ovirt_repositories_disable_gpg_check to repositories

* Tue Oct 27 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-1
- Fix ovirt_disk ignore moving of hosted engine disks
- Obsolete old roles

* Mon Oct 12 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-0.2
- Add role disaster_recovery
- Fix engine_setup yum.conf
- Fix hosted_engine_setup - Allow uppercase characters in mac address

* Mon Oct 12 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-0.2
- Add ovirt_vm_info current_cd
- Add ovirt_nic_info template
- Add ovirt_nic template_version
- Fix ovirt_disk move
- Fix ovirt inventory connection close
- Fix ovirt_vm rename q35_sea to q35_sea_bios
- Fix ovirt_vm template search

* Wed Sep 16 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-0.1
- Add role cluster_upgrade
- Add role engine_setup
- Add role vm_infra
- Add role infra
- Add role manageiq
- Add role hosted_engine_setup
- Add role image_template
- Add role shutdown_env

* Mon Aug 17 2020 Martin Necas <mnecas@redhat.com> - 1.1.2-1
- Add ansible changelogs

* Wed Aug 12 2020 Martin Necas <mnecas@redhat.com> - 1.1.1-1
- Fix ovirt_permission FQCNs

* Wed Aug 12 2020 Martin Necas <mnecas@redhat.com> - 1.1.0-1
- Add ovirt_vm_os_info module
- Add ovirt_disk backup
- Add ovirt_disk autodetect size when uploading
- Add ovirt_host add ssh_port
- Add ovirt_network support of removing vlan_tag
- Fix ovirt_disk upload

* Thu Apr 9 2020 Martin Necas <mnecas@redhat.com> - 1.0.0-1
- Initial release
