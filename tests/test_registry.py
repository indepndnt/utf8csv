import pytest
from utf8csv import registry


def test_options_key():
    # Antecedent: running on a Windows platform
    # Behavior: request the registry key for Excel options
    key = registry.excel_options_key()
    # Consequence: receive a key path string (empty if not found, or the path found)
    assert isinstance(key, str)


def test_open_assoc_ok():
    # Antecedent: running on a Windows platform
    # Behavior: request the open command for a .bat file from the registry
    cmd = registry.get_open_association(".bat")
    # Consequence: receive a command string
    assert isinstance(cmd, str)


def test_open_assoc_bad():
    # Antecedent: running on a Windows platform with no .xyzpleasedontexist file association
    # Behavior: request the open command for a .xyzpleasedontexist file from the registry
    with pytest.raises(OSError) as exit_obj:
        cmd = registry.get_open_association(".xyzpleasedontexist")
    # Consequence: an OSError is raised
    assert exit_obj.type == OSError
