import sys

import pytest

sys.path.insert(0, './')

from src.Kathara.parser.netkit.OptionParser import OptionParser


def test_one_option():
    parsed_options = OptionParser.parse(["mem='64m'"])
    assert parsed_options['mem'] == '64m'


def test_two_option():
    parsed_options = OptionParser.parse(["mem=64m", "image=kathara/netkit_base"])
    assert parsed_options['mem'] == '64m'
    assert parsed_options['image'] == 'kathara/netkit_base'


def test_option_error():
    with pytest.raises(ValueError):
        OptionParser.parse(["option:syntax_error"])


def test_option_error2():
    with pytest.raises(ValueError):
        OptionParser.parse(["option=syntax_error=2"])
