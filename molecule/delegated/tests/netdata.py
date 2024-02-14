from .util.util import get_ansible, get_variable, get_from_url

testinfra_runner, testinfra_hosts = get_ansible()


def test_netdata_installation(host):
    package = host.package(get_variable(host, "netdata_package_name"))
    assert package.is_installed


def test_repository_configuration(host):
    if get_variable(host, "netdata_configure_repository"):
        repo = get_variable(host, "netdata_debian_repository")
        key_file = host.file("/etc/apt/trusted.gpg.d/netdata.asc")
        key_content = get_from_url(get_variable(host, "netdata_debian_repository_key"))
        assert key_file.exists
        assert key_file.content_string == key_content
        assert host.run(f"apt-cache policy | grep {repo.split(' ')[1]}").rc == 0


def test_configuration_files(host):
    configuration_files = get_variable(host, "netdata_configuration_files")
    for file in configuration_files:
        config_file = host.file(f"/etc/netdata/{file}")
        assert config_file.exists
        assert config_file.user == "root"
        assert config_file.group == "root"
        assert config_file.mode == 0o644
        assert (
            "# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN"
            in config_file.content_string
        )

    cloud_conf = host.file("/var/lib/netdata/cloud.d/cloud.conf")
    assert cloud_conf.exists
    assert cloud_conf.user == "netdata"
    assert cloud_conf.group == "netdata"
    assert cloud_conf.mode == 0o644
    assert "[global]" in cloud_conf.content_string


def test_directories_and_files(host):
    cloud_dir = host.file("/var/lib/netdata/cloud.d")
    opt_out_file = host.file("/etc/netdata/.opt-out-from-anonymous-statistics")

    assert cloud_dir.exists
    assert cloud_dir.is_directory
    assert cloud_dir.user == "netdata"
    assert cloud_dir.group == "netdata"
    assert cloud_dir.mode == 0o775

    assert not opt_out_file.exists or (
        opt_out_file.user == "root" and opt_out_file.group == "root"
    )


def test_netdata_user_group(host):
    netdata_user = host.user("netdata")
    assert "docker" in netdata_user.groups


def test_netdata_service_running(host):
    service = host.service(get_variable(host, "netdata_service_name"))
    assert service.is_running
    assert service.is_enabled


def test_host_specific_tasks(host):
    # testing server.yml task
    if host.file(get_variable(host, "netdata_host_type")) == "server":
        sysctl_file_path = "/etc/sysctl.d/50-netdata.conf"
        assert host.file(sysctl_file_path).exists

        expected_value = get_variable(host, "netdata_sys_vm_max_map_count")
        actual_value = host.sysctl("vm.max_map_count")
        assert actual_value == expected_value

    # testing client.yml task
    if host.file(get_variable(host, "netdata_host_type")) == "client":
        # no tasks in client.yml implemented yet
        assert True