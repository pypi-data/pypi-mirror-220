import os
import sys
from pathlib import Path

import pytest
from fs.errors import CreateFailed

sys.path.insert(0, './')

from src.Kathara.model.Lab import Lab
from src.Kathara import utils
from tempfile import mkdtemp
from src.Kathara.exceptions import MachineOptionError, MachineAlreadyExistsError, MachineNotFoundError, \
    LinkAlreadyExistsError, LinkNotFoundError


@pytest.fixture()
def default_scenario():
    return Lab("default_scenario")


@pytest.fixture()
def temporary_path():
    return mkdtemp("kathara_test/")


@pytest.fixture()
def directory_scenario(temporary_path):
    Path(os.path.join(temporary_path, "shared.startup")).touch()
    Path(os.path.join(temporary_path, "shared.shutdown")).touch()
    return Lab("directory_scenario", path=temporary_path)


def test_default_scenario_creation(default_scenario: Lab):
    assert default_scenario.name == "default_scenario"
    assert default_scenario.description is None
    assert default_scenario.version is None
    assert default_scenario.author is None
    assert default_scenario.email is None
    assert default_scenario.web is None
    assert default_scenario.machines == {}
    assert default_scenario.links == {}
    assert default_scenario.general_options == {}
    assert not default_scenario.has_dependencies
    assert default_scenario.fs_type() == "memory"
    assert default_scenario.shared_path is None
    assert default_scenario.hash == utils.generate_urlsafe_hash(default_scenario.name)


def test_default_scenario_creation_with_non_existing_path():
    with pytest.raises(CreateFailed):
        Lab(None, path="/lab/path")


def test_directory_scenario_creation_with_shared_files(directory_scenario: Lab, temporary_path: str):
    assert directory_scenario.name == "directory_scenario"
    assert directory_scenario.description is None
    assert directory_scenario.version is None
    assert directory_scenario.author is None
    assert directory_scenario.email is None
    assert directory_scenario.web is None
    assert directory_scenario.machines == {}
    assert directory_scenario.links == {}
    assert directory_scenario.general_options == {}
    assert not directory_scenario.has_dependencies
    assert os.path.normpath(directory_scenario.fs_path()) == os.path.normpath(temporary_path)
    assert directory_scenario.shared_path is None
    assert directory_scenario.hash == utils.generate_urlsafe_hash(directory_scenario.name)


def test_new_machine(default_scenario: Lab):
    assert len(default_scenario.machines) == 0
    default_scenario.new_machine("pc1")
    assert len(default_scenario.machines) == 1
    assert "pc1" in default_scenario.machines


def test_new_machine_already_exists_error(default_scenario: Lab):
    default_scenario.new_machine("pc1")
    with pytest.raises(MachineAlreadyExistsError):
        default_scenario.new_machine("pc1")


def test_get_machine(default_scenario: Lab):
    default_scenario.new_machine("pc1")
    device = default_scenario.get_machine("pc1")
    assert device.name == "pc1"


def test_get_machine_not_found_error(default_scenario: Lab):
    with pytest.raises(MachineNotFoundError):
        default_scenario.get_machine("pc1")


def test_get_or_new_machine_not_exist(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']


def test_get_or_new_machine_exists(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    default_scenario.get_or_new_machine("pc1")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']


def test_get_or_new_machine_two_devices(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    default_scenario.get_or_new_machine("pc2")
    assert len(default_scenario.machines) == 2
    assert default_scenario.machines['pc1']
    assert default_scenario.machines['pc2']


def test_new_link(default_scenario: Lab):
    assert len(default_scenario.links) == 0
    link = default_scenario.new_link("A")
    assert len(default_scenario.links) == 1
    assert link.name in default_scenario.links


def test_new_link_already_exists_error(default_scenario: Lab):
    default_scenario.new_link("A")
    with pytest.raises(LinkAlreadyExistsError):
        default_scenario.new_link("A")


def test_get_link(default_scenario: Lab):
    created_link = default_scenario.new_link("A")
    link = default_scenario.get_link("A")
    assert link == created_link


def test_get_link_not_found_error(default_scenario: Lab):
    with pytest.raises(LinkNotFoundError):
        default_scenario.get_link("A")


def test_get_or_new_link_not_exists(default_scenario: Lab):
    default_scenario.get_or_new_link("A")
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']


def test_get_or_new_link_exists(default_scenario: Lab):
    default_scenario.get_or_new_link("A")
    default_scenario.get_or_new_link("A")
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']


def test_get_or_new_link_two_cd(default_scenario: Lab):
    default_scenario.get_or_new_link("A")
    default_scenario.get_or_new_link("B")
    assert len(default_scenario.links) == 2
    assert default_scenario.links['A']
    assert default_scenario.links['B']


def test_connect_one_machine_to_link(default_scenario: Lab):
    result_1 = default_scenario.connect_machine_to_link("pc1", "A")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    assert default_scenario.machines['pc1'].interfaces[0].name == 'A'
    assert result_1 == (default_scenario.machines['pc1'], default_scenario.links['A'])


def test_connect_two_machine_to_link(default_scenario: Lab):
    result_1 = default_scenario.connect_machine_to_link("pc1", "A")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    result_2 = default_scenario.connect_machine_to_link("pc2", "A")
    assert len(default_scenario.machines) == 2
    assert default_scenario.machines['pc2']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    assert default_scenario.machines['pc1'].interfaces[0].name == 'A'
    assert default_scenario.machines['pc2'].interfaces[0].name == 'A'
    assert result_1 == (default_scenario.machines['pc1'], default_scenario.links['A'])
    assert result_2 == (default_scenario.machines['pc2'], default_scenario.links['A'])


def test_connect_machine_to_two_links(default_scenario: Lab):
    result_1 = default_scenario.connect_machine_to_link("pc1", "A")
    result_2 = default_scenario.connect_machine_to_link("pc1", "B")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 2
    assert default_scenario.links['A']
    assert default_scenario.links['B']
    assert default_scenario.machines['pc1'].interfaces[0].name == 'A'
    assert default_scenario.machines['pc1'].interfaces[1].name == 'B'
    assert result_1 == (default_scenario.machines['pc1'], default_scenario.links['A'])
    assert result_2 == (default_scenario.machines['pc1'], default_scenario.links['B'])


def test_connect_machine_to_link_iface_numbers(default_scenario: Lab):
    result_1 = default_scenario.connect_machine_to_link("pc1", "A", machine_iface_number=2)
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    assert default_scenario.machines['pc1'].interfaces[2].name == 'A'
    assert result_1 == (default_scenario.machines['pc1'], default_scenario.links['A'])


def test_connect_one_machine_obj_to_link(default_scenario: Lab):
    pc1 = default_scenario.new_machine("pc1")
    result_1 = default_scenario.connect_machine_obj_to_link(pc1, "A")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    assert default_scenario.machines['pc1'].interfaces[0].name == 'A'
    assert result_1 == (default_scenario.links['A'], 0)


def test_connect_two_machine_obj_to_link(default_scenario: Lab):
    pc1 = default_scenario.new_machine("pc1")
    result_1 = default_scenario.connect_machine_obj_to_link(pc1, "A")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    pc2 = default_scenario.new_machine("pc2")
    result_2 = default_scenario.connect_machine_obj_to_link(pc2, "A")
    assert len(default_scenario.machines) == 2
    assert default_scenario.machines['pc2']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    assert default_scenario.machines['pc1'].interfaces[0].name == 'A'
    assert default_scenario.machines['pc2'].interfaces[0].name == 'A'
    assert result_1 == (default_scenario.links['A'], 0)
    assert result_2 == (default_scenario.links['A'], 0)


def test_connect_machine_obj_to_two_links(default_scenario: Lab):
    pc1 = default_scenario.new_machine("pc1")
    result_1 = default_scenario.connect_machine_obj_to_link(pc1, "A")
    result_2 = default_scenario.connect_machine_obj_to_link(pc1, "B")
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 2
    assert default_scenario.links['A']
    assert default_scenario.links['B']
    assert default_scenario.machines['pc1'].interfaces[0].name == 'A'
    assert default_scenario.machines['pc1'].interfaces[1].name == 'B'
    assert result_1 == (default_scenario.links['A'], 0)
    assert result_2 == (default_scenario.links['B'], 1)


def test_connect_machine_obj_to_link_iface_numbers(default_scenario: Lab):
    pc1 = default_scenario.new_machine("pc1")
    result_1 = default_scenario.connect_machine_obj_to_link(pc1, "A", machine_iface_number=2)
    assert len(default_scenario.machines) == 1
    assert default_scenario.machines['pc1']
    assert len(default_scenario.links) == 1
    assert default_scenario.links['A']
    assert default_scenario.machines['pc1'].interfaces[2].name == 'A'
    assert result_1 == (default_scenario.links['A'], None)


def test_assign_meta_to_machine(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    result = default_scenario.assign_meta_to_machine("pc1", "test_meta", "test_value")
    assert "test_meta" in default_scenario.machines['pc1'].meta
    assert default_scenario.machines['pc1'].meta["test_meta"] == "test_value"
    assert result is None


def test_assign_meta_to_machine_overwrite(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    result = default_scenario.assign_meta_to_machine("pc1", "test_meta", "test_value")
    assert "test_meta" in default_scenario.machines['pc1'].meta
    assert default_scenario.machines['pc1'].meta["test_meta"] == "test_value"
    assert result is None
    result = default_scenario.assign_meta_to_machine("pc1", "test_meta", "test_new_value")
    assert "test_meta" in default_scenario.machines['pc1'].meta
    assert default_scenario.machines['pc1'].meta["test_meta"] == "test_new_value"
    assert result == "test_value"


def test_assign_meta_to_machine_overwrite_sysctl(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    result = default_scenario.assign_meta_to_machine("pc1", "sysctl", "net.test.a=1")
    assert default_scenario.machines['pc1'].meta["sysctls"]["net.test.a"] == 1
    assert result is None
    result = default_scenario.assign_meta_to_machine("pc1", "sysctl", "net.test.a=2")
    assert default_scenario.machines['pc1'].meta["sysctls"]["net.test.a"] == 2
    assert result == 1


def test_assign_meta_to_machine_overwrite_env(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    result = default_scenario.assign_meta_to_machine("pc1", "env", "TEST_ENV=abc")
    assert default_scenario.machines['pc1'].meta["envs"]["TEST_ENV"] == "abc"
    assert result is None
    result = default_scenario.assign_meta_to_machine("pc1", "env", "TEST_ENV=def")
    assert default_scenario.machines['pc1'].meta["envs"]["TEST_ENV"] == "def"
    assert result == "abc"


def test_assign_meta_to_machine_overwrite_port(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    result = default_scenario.assign_meta_to_machine("pc1", "port", "3000:4000")
    assert default_scenario.machines['pc1'].meta["ports"][(3000, "tcp")] == 4000
    assert result is None
    result = default_scenario.assign_meta_to_machine("pc1", "port", "3000:5000")
    assert default_scenario.machines['pc1'].meta["ports"][(3000, "tcp")] == 5000
    assert result == 4000


def test_assign_meta_to_machine_exception(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    with pytest.raises(MachineOptionError):
        default_scenario.assign_meta_to_machine("pc1", "port", "value")


def test_intersect_machines(default_scenario: Lab):
    default_scenario.connect_machine_to_link("pc1", "A")
    default_scenario.connect_machine_to_link("pc2", "A")
    default_scenario.connect_machine_to_link("pc2", "B")
    assert len(default_scenario.machines) == 2
    links = default_scenario.get_links_from_machines(machines=["pc1"])
    assert len(default_scenario.machines) == 2
    assert 'pc1' in default_scenario.machines
    assert 'pc2' in default_scenario.machines
    assert 'A' in links
    assert 'B' not in links


def test_intersect_machines_objs(default_scenario: Lab):
    default_scenario.connect_machine_to_link("pc1", "A")
    default_scenario.connect_machine_to_link("pc2", "A")
    default_scenario.connect_machine_to_link("pc2", "B")
    assert len(default_scenario.machines) == 2
    links = default_scenario.get_links_from_machine_objs(machines=[default_scenario.get_machine("pc1")])
    assert len(default_scenario.machines) == 2
    assert 'pc1' in default_scenario.machines
    assert 'pc2' in default_scenario.machines
    assert 'A' in links
    assert 'B' not in links


def test_create_shared_folder(directory_scenario: Lab):
    directory_scenario.create_shared_folder()
    assert directory_scenario.fs.isdir('shared')


def test_create_shared_folder_no_path(default_scenario: Lab):
    assert default_scenario.create_shared_folder() is None


def test_apply_dependencies(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    default_scenario.get_or_new_machine("pc2")
    default_scenario.get_or_new_machine("pc3")

    default_scenario.apply_dependencies(["pc3", "pc1", "pc2"])

    assert default_scenario.machines.popitem()[0] == "pc2"
    assert default_scenario.machines.popitem()[0] == "pc1"
    assert default_scenario.machines.popitem()[0] == "pc3"


def test_find_machine_true(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")

    assert default_scenario.has_machine("pc1")


def test_find_machine_false(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")

    assert not default_scenario.has_machine("pc2")


def test_find_machines_true(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    default_scenario.get_or_new_machine("pc2")
    default_scenario.get_or_new_machine("pc3")

    assert default_scenario.has_machines({"pc1", "pc2", "pc3"})


def test_find_machines_false(default_scenario: Lab):
    default_scenario.get_or_new_machine("pc1")
    default_scenario.get_or_new_machine("pc2")

    assert not default_scenario.has_machines({"pc1", "pc2", "pc3"})
