import pytest
from audiodotturn.config import Config


def test_config():
    '''
    Test that config creates datasets
    '''
    test = Config('/home/turn/Documents/mytools/audiodotturn/adt/audiodotturn/config/config.json')
    assert isinstance(test.defaults, object)
    assert isinstance(test.format_defaults, dict)
    assert isinstance(test.program_defaults, dict)
    assert isinstance(test.options, object)
    assert isinstance(test.format_options, dict)
    assert isinstance(test.program_options, dict)


def test_config_path():
    '''
    Test that config path sets correctly
    '''
    test = Config('/home/turn/Documents/mytools/audiodotturn/adt/audiodotturn/config/config.json')
    assert test.config_path == '/home/turn/Documents/mytools/audiodotturn/adt/audiodotturn/config/config.json'


# def test_config_missing_key():
#     console = Console()
#     with pytest.raises(AudiodotturnError):
#         test = Config('/path/to/config_missing_key.json')


def test_config_bad_path():
    '''
    Path doesnt contain config
    '''
    with pytest.raises(BaseException):
        Config('/path/to/missing_config.json')
        