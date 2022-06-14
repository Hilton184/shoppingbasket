"""Module for the Promotion class - with functionality to store data about a promotion."""

from dataclasses import dataclass


@dataclass
class Promotion:
    """Blueprint for promotion object. Build in dataclass functionality handles initalisation.

    Args:
        id (int): The ID of the promotion.
        name (str): The name of the promotion.
        active (bool): Whether or not the promotion is active.
        qualifying_product_id (int): The product id of the product that must be purchased to qualify for the promotion.
        qualifying_product_quantity (int): The number of product with <qualifying_product_id> that must be purchased to qualify for the promotion.
        discounted_product_id (int): The product id of the product that is discounted by the promotion.
        percent_discount (int): The percentage discount to apply to the product with <qualifying_product_id>.
    """

    id: int
    name: str
    active: bool
    qualifying_product_id: int
    qualifying_product_quantity: int
    discounted_product_id: int
    percent_discount: int
