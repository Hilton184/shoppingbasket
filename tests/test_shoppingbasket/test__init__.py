"""Test suite for the __init__ file."""

from shoppingbasket import __version__


def test_version():
    """Ensure the package version is correct."""
    assert __version__ == "0.1.0"
