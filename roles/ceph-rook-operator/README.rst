Ansible role for installation and configuration of the ceph rook operator.


**Operator Variables**

.. zuul:rolevar:: operator_user
   :default: dragon

The user which will own the configuration directory and handles with Docker.

.. zuul:rolevar:: operator_group
   :default: operator_user

Group from the user which will own the configuration directory.

**Rook Variables**

.. zuul:rolevar:: container_registry_ceph_rook_operator
   :default: index.docker.io

Path to the registry that stores the container images for the rook operator.

.. zuul:rolevar:: ceph_rook_operator_image
   :default: {{ container_registry_ceph_rook_operator }}/rook/ceph

The container image to use.

.. zuul:rolevar:: ceph_rook_operator_image_tag
   :default: v1.13

Version from rook operator in form of a tag which should be used.

.. zuul:rolevar:: ceph_rook_operator_configuration_directory
   :default: /tmp/ceph_rook_operator/configuration

Work directory inside the osism-ansible container.
