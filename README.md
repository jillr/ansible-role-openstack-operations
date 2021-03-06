# OpenStack Operations #


Perform various common OpenStack operations by calling this role with an action and appropriate variables.

## [WIP] Restart Services ##

Restarting OpenStack service is complex. This role aims to intelligently evaluate the environment and determine how a service is running, what components constitute that service, and restart those components appropriately. This allows the operator to think in terms of the service that needs restarting rather than having to remember all the details required to restart that service.

## Fetch Logs ##

To fetch logs with this role, use the `fetch_logs.yml` tasks file. By default, every log file in `/var/log` matching the `*.log` pattern will be fetched from the remote and put into a folder adjacent to the playbook named for each host, preserving the directory structure as found on the remote host.

See `defaults/main.yml` for the dictionary of options to control logs that are fetched.

## Cleanup Docker ##

**WARNING:** This will delete images, containers, and volumes from the target system(s).

To perform the most common cleanup tasks -- delete dangling images and volumes and delete exited or dead containers -- use the `cleanup_docker.yml` tasks file. This role includes a `docker_facts` module for enumerating images, volumes, and containers. The filtered lists (one each for images, containers, and volumes) returned by this module is used to determine which items to remove. The module accepts a list of `k=v` filter arguments that will be passed to the `-f` option of Docker. Specifying multiple filters creates an `and` match, so all filters must match.

See Docker guides for [images](https://docs.docker.com/engine/reference/commandline/images/#filtering), [containers](https://docs.docker.com/engine/reference/commandline/ps/#filtering), and [volumes](https://docs.docker.com/engine/reference/commandline/volume_ls/#filtering) for filter options.


## Requirements ##

 - ansible >= 2.4
 - python >= 2.6
 - docker-py >= 1.7.0
 - Docker API >= 1.20

## Role Variables ##


**Variables used for cleaning up Docker**

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `operations_image_filters` | `['dangling=true']` | List of image filters. |
| `operations_volume_filters` | `['dangling=true']` | List of volume filters. |
| `operations_container_filters` | `['status=exited', 'status=dead']` | List of container filters. |

**Variables for fetching logs**

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `operations_log_destination` | `{{ playbook_dir }}` | Path where logs will be stored when fetched from remote systems. |


**Variables for restarting services**

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `operations_service_names` | `[]` | List of services to restart on target systems. |


## Dependencies ##

None

## Example Playbooks ##


### Restart Services ###

    - hosts: all
      tasks:
        - name: Restart a service
          import_role:
            name: openstack-operations
            tasks_from: restart_service.yml
          vars:
            operations_service_names:
              - docker
              - keystone
              - mariadb


### Cleanup Docker ###

    - name: Cleanup dangling and dead images, containers, and volumes
      hosts: all
      tasks:
        - name: Cleanup unused Docker images, containers, and volumes
          import_role:
            name: openstack-operations
            tasks_from: cleanup_docker.yml

    - name: Use custom filters for cleaning
      hosts: all
      tasks:
        - name: Cleanup unused Docker images, containers, and volumes
          import_role:
            name: openstack-operations
            tasks_from: cleanup_docker.yml
          vars:
            operations_image_filters:
              - before=image1
            operations_volume_filters:
              - label=my_volume
            operations_container_filters:
              - name=keystone



### Fetch Logs ###
    - hosts: all
      tasks:
        - name: Fetch logs
          import_role:
            name: openstack-operations
            tasks_from: fetch_logs.yml

License
-------

Apache 2.0
