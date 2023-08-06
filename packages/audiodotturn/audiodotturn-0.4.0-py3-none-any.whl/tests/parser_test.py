import pytest
from audiodotturn.config import Config
from audiodotturn.parser import Parser


# A fixture to initialize the parser with default settings
@pytest.fixture
def parser_defaults():
    config = Config('/home/turn/Documents/mytools/audiodotturn/adt/audiodotturn/config/config.json')
    defaults = config.defaults.program
    parser = Parser(defaults)
    return parser


# Test the "set" subcommand of the parser
def test_set_subcommand(parser_defaults):
    args = parser_defaults.parse_args(["set", "--artist", "John"])
    assert args.command == "set"
    assert args.artist == "John"


# Test the "create" subcommand of the parser
def test_create_subcommand(parser_defaults):
    args = parser_defaults.parse_args(["create", "-f", "file.mp3"])
    assert args.command == "create"
    assert args.formatfile == "file.mp3"


# Test the "view" subcommand of the parser
def test_view_subcommand(parser_defaults):
    args = parser_defaults.parse_args(["view", "artists", "-t"])
    assert args.command == "view"
    assert args.view_command == "artists"
    assert args.tracks is True

# Test to make sure the "defaults" argument is handled correctly
def test_defaults_arg(parser_defaults):
    args = parser_defaults.parse_args(["--defaults", "all"])
    assert args.defaults == "all"

# Test to make sure the "version" argument is handled correctly
def test_version_arg(parser_defaults):
    args = parser_defaults.parse_args(["-v"])
    assert args.version is True

# Test to make sure the "create" subcommand with the "--formatdir" argument is handled correctly
def test_create_subcommand_with_formatdir(parser_defaults):
    args = parser_defaults.parse_args(["create", "-F"])
    assert args.command == "create"
    assert args.formatdir is True

# Test to make sure the "create" subcommand with the "--dump" argument is handled correctly
def test_create_subcommand_with_dump(parser_defaults):
    args = parser_defaults.parse_args(["create", "-D"])
    assert args.command == "create"
    assert args.dump is True

# Test to make sure the "create" subcommand with the "--dry" argument is handled correctly
def test_create_subcommand_with_dry(parser_defaults):
    args = parser_defaults.parse_args(["create", "--dry"])
    assert args.command == "create"
    assert args.dry is True

# Test to make sure the "create" subcommand with the "--directory" argument is handled correctly
def test_create_subcommand_with_directory(parser_defaults):
    args = parser_defaults.parse_args(["create", "--directory", "/path/to/directory"])
    assert args.command == "create"
    assert args.directory == "/path/to/directory"

# Test to make sure the "artists" subcommand of the "view" command with the "--names" argument is handled correctly
def test_view_artists_with_names(parser_defaults):
    args = parser_defaults.parse_args(["view", "artists", "--names"])
    assert args.command == "view"
    assert args.view_command == "artists"
    assert args.names is True

# Test to make sure the "songs" subcommand of the "view" command with the "--artist" argument is handled correctly
def test_view_songs_with_artist(parser_defaults):
    args = parser_defaults.parse_args(["view", "songs", "--artist", "Eminem"])
    assert args.command == "view"
    assert args.view_command == "songs"
    assert args.artist == "Eminem"
