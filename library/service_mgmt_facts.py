#!/usr/bin/env python

import docker

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


def get_docker_containers(module, container_list):
    if len(container_list) == 0:
        pass
    client = docker.from_env()
    try:
        containers = client.containers.list()
        docker_list = [{'container_image': i.attrs['Config']['Image'],
                        'container_name': i.attrs['Name'].strip('/')} for i
                       in containers if i.attrs['Name'].strip('/') in
                       container_list]

        return docker_list
    except docker.errors.APIError as e:
        module.fail_json(
            msg='Error listing containers: {}'.format(to_native(e)))
    # TODO: handle permission errors from client


def get_systemd_services(module, service_unit_list):
    if len(service_unit_list) == 0:
        pass
    systemctl_path = \
        module.get_bin_path("systemctl",
                            opt_dirs=["/usr/bin", "/usr/local/bin"])
    if systemctl_path is None:
        return None
    systemd_list = []
    for i in service_unit_list:
        rc, stdout, stderr = \
            module.run_command("{} is-enabled {}".format(systemctl_path, i),
                               use_unsafe_shell=True)
        if stdout == "enabled\n":
            state_val = "enabled"
        else:
            state_val = "disabled"
        systemd_list.append({"name": i,  "state": state_val})
    return systemd_list


def run_module():

    module_args = dict(service_name=dict(type=dict, required=False))
    # ok so that's a dict that looks like
    # cinder['service'] == ['openstack-cinder-api', 'openstack-cinder-volume']
    # cinder['container_list'] == ['cinder_api', 'cinder_api_cron']

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    service_unit_list = module.params.get('service_name')['systemd_unit']
    container_list = module.params.get('service_name')['container_name']

    result = dict(
        ansible_facts=dict(
            docker_containers=get_docker_containers(module, container_list),
            systemd_services=get_systemd_services(module, service_unit_list),
        )
    )

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

