"""Data store for products and promotions.

PRODUCTS should be a dictionary, with keys the product names and values the unit price of the product in pence.

PROMOTIONS should be a dictionary, with keys the promotion names and values a dictionary of promotion details. The dictionary of promotion details should include:

- qualifying_product: The name of the product that must be purchased to qualify for the promotion.
- qualifying_product_quantity: The number of the qualifying product that must be purchased to qualify for the promotion.
- discounted_product: the name of the product to be discounted.
- percent_discount: The percentage to discount the discounted product.
"""

from typing import Dict, Union

PRODUCTS: Dict[str, int] = {"SOUP": 65, "BREAD": 80, "MILK": 130, "APPLES": 100}

PROMOTIONS: Dict[str, Dict[str, Union[str, int]]] = {
    "Apples 10% off": {
        "qualifying_product": "APPLES",
        "qualifying_product_quantity": 1,
        "discounted_product": "APPLES",
        "percent_discount": 10,
    },
    "Purchase 2 tins of soup and get half price off bread": {
        "qualifying_product": "SOUP",
        "qualifying_product_quantity": 2,
        "discounted_product": "BREAD",
        "percent_discount": 50,
    },
}
