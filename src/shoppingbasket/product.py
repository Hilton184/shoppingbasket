"""Module for the Product class - with functionality to store data about a product and apply promotions to a product."""

from typing import Union

import shoppingbasket._utils
from shoppingbasket.promotion import Promotion


class Product:
    """Blueprint for product object."""

    def __init__(self, name: str, id: int, unit_price: int, available: bool) -> None:
        """Create a Product object without a promotion applied.

        Args:
            name (str): The name of the product.
            id (int): The ID of the product.
            unit_price (int): The unit price of the product.
            available (bool): Whether or not the product is available.
        """
        self.name = name.upper()
        self.id = id
        self.unit_price = unit_price
        self.available = available
        self.promotion = None

    def __eq__(self, other) -> bool:
        """Implement definition of one Product being equal to another Product."""
        if not isinstance(other, Product):
            return False

        return (
            self.name == other.name
            and self.id == other.id
            and self.unit_price == other.unit_price
            and self.available == other.available
            and self.promotion == other.promotion
        )

    def __repr__(self) -> str:
        """Developer friendly representation of object."""
        return f"Product(name='{self.name}', id={self.id}, unit_price={self.unit_price}, available={self.available}, promotion={self.promotion})"

    def apply_promotion(self, promotion: Promotion) -> bool:
        """Add a promotion to the product.

        Args:
            promotion (Promotion): Promotion object detailing the promotion to apply to the product.

        Returns:
            bool: True if the promotion is successfully added, False otherwise.
        """
        self.promotion = promotion

    def remove_promotion(self) -> None:
        """Remove any applied promotions from the product."""
        self.promotion = None

    @property
    def promotion_discount(self) -> int:
        """Compute the discount on the product with promotions applied.

        Returns:
            int: The discount on the product with promotions applied.
        """
        if not self.promotion:
            return 0

        return int(self.unit_price * self.promotion.percent_discount / 100)

    @property
    def promotion_price(self) -> Union[None, int]:
        """Compute the price of the product with promotions applied.

        Returns:
            int: The price of the product with promotions applied.
        """
        if not self.promotion:
            return self.unit_price

        return int(self.unit_price - self.promotion_discount)

    @property
    def promotion_message(self) -> Union[str, None]:
        """Get the message associated with an applied promotion.

        Returns:
            Union[str, None]: The message associated with an applied promotion. None if no promotion is applied.
        """
        if not self.promotion:
            return None

        return f"""{self.promotion.name}: {shoppingbasket._utils._currency_format(self.promotion_discount)}"""
