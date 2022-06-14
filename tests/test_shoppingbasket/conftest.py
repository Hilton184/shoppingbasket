"""Configuration file and fixtures for shoppingbasket package tests."""

import json
import pathlib

import pytest
from shoppingbasket.promotion import Promotion


@pytest.fixture
def product_string_json_data() -> str:
    """Product JSON data to use for tests in the form of a string.

    Returns:
        str: A string representation of the product JSON data to use for tests.
    """
    data = """{
            "products": [
                {
                    "id": 1,
                    "name": "SOUP",
                    "unit_price": 65,
                    "available": true
                },
                {
                    "id": 2,
                    "name": "BREAD",
                    "unit_price": 80,
                    "available": true
                },
                {
                    "id": 3,
                    "name": "MILK",
                    "unit_price": 130,
                    "available": true
                },
                {
                    "id": 4,
                    "name": "APPLES",
                    "unit_price": 100,
                    "available": true
                },
                {
                    "id": 5,
                    "name": "TOMATOES",
                    "unit_price": 50,
                    "available": false
                },
                {
                    "id": 6,
                    "name": "CUCUMBER",
                    "unit_price": 90,
                    "available": false
                },
                {
                    "id": 7,
                    "name": "PEANUTS",
                    "unit_price": 210,
                    "available": false
                },
                {
                    "id": 8,
                    "name": "LAMB STEAK",
                    "unit_price": 450,
                    "available": false
                }
            ]
        }
        """

    return data


@pytest.fixture
def promotion_string_json_data() -> str:
    """Promotion JSON data to use for tests in the form of a string.

    Returns:
        str: A string representation of the promotion JSON data to use for tests.
    """
    data = """{
            "promotions": [
                {
                    "id": 1,
                    "name": "Apples 10% off",
                    "active": true,
                    "qualifying_product_id": 4,
                    "qualifying_product_quantity": 1,
                    "discounted_product_id": 4,
                    "percent_discount": 10
                },
                {
                    "id": 2,
                    "name": "Purchase 2 tins of soup and get half price off bread",
                    "active": true,
                    "qualifying_product_id": 1,
                    "qualifying_product_quantity": 2,
                    "discounted_product_id": 2,
                    "percent_discount": 50
                },
                {
                    "id": 3,
                    "name": "Buy 1 get 1 free on milk",
                    "active": false,
                    "qualifying_product_id": 3,
                    "qualifying_product_quantity": 2,
                    "discounted_product_id": 3,
                    "percent_discount": 100
                }
            ]
        }
        """

    return data


@pytest.fixture
def product_json_data_filepath(
    tmp_path: pathlib.Path, product_string_json_data: str
) -> str:
    """Return the filepath to the JSON file storing the product JSON data, making use of pytest tmp_path fixure to provide a temporary directory unique to the test invocation.

    Returns:
        str: A string representation of the path to the product JSON data to use for tests.
    """
    directory = tmp_path / "data"
    directory.mkdir(exist_ok=True)
    file_path = directory / "products.json"

    json_data = json.loads(product_string_json_data)

    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file)

    return str(file_path)


@pytest.fixture
def promotion_json_data_filepath(
    tmp_path: pathlib.Path, promotion_string_json_data: str
) -> str:
    """Return the filepath to the JSON file storing the promotions JSON data, making use of pytest tmp_path fixure to provide a temporary directory unique to the test invocation.

    Returns:
        str: A string representation of the path to the promotions JSON data to use for tests.
    """
    directory = tmp_path / "data"
    directory.mkdir(exist_ok=True)
    file_path = directory / "promotions.json"

    json_data = json.loads(promotion_string_json_data)

    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file)

    return str(file_path)


@pytest.fixture
def apples_promotion():
    """Return a promotion object for the test apples promotion."""
    return Promotion(1, "Apples 10% off", True, 4, 1, 4, 10)


@pytest.fixture
def soup_bread_promotion():
    """Return a promotion object for the test soup and bread promotion."""
    return Promotion(
        2, "Purchase 2 tins of soup and get half price off bread", True, 1, 2, 2, 50
    )
