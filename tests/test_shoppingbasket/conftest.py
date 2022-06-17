"""Configuration file and fixtures for shoppingbasket package tests."""


import pytest
from shoppingbasket.basket import Basket


@pytest.fixture
def basket():
    """Return an empty basket object."""
    return Basket()
