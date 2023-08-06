import sys
import traceback
import pytest
from rich.console import Console
from audiodotturn.errors import AudiodotturnError

console = Console()

def test_error_handling_option_error():
    """Test the AudiodotturnError class when passed the 'error' option."""
    with pytest.raises(SystemExit):
        try:
            1/0
        except ZeroDivisionError as error:
            AudiodotturnError(error, ("error",), console, if_exit=True)

def test_error_handling_option_warning():
    """Test the AudiodotturnError class when passed the 'warning' option."""
    with pytest.raises(SystemExit):
        try:
            x = "hello"
            y = x + 1
        except TypeError as error:
            AudiodotturnError(error, ("warning",), console, if_exit=True)

def test_error_handling_option_info():
    """Test the AudiodotturnError class when passed the 'info' option."""
    with pytest.raises(SystemExit):
        try:
            raise NotImplementedError("This is an informational message.")
        except NotImplementedError as error:
            AudiodotturnError(error, ("info",), console, if_exit=True)
