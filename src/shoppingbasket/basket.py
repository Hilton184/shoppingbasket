"""Module for the Basket class - with functionality to add products, determine the basket total, apply promotions to the products in the basket and more."""

import collections
from typing import Counter, Dict, List, Union

from shoppingbasket.data import PRODUCTS, PROMOTIONS


class Basket:
    """Blueprint for Basket object."""

    PRODUCTS = PRODUCTS
    PROMOTIONS = PROMOTIONS

    def __init__(
        self,
    ) -> None:
        """Create a Basket object with no contents.

        Available products and their price per unit in pence are defined in the PRODUCTS and PROMOTIONS class variable.

        Available promotions and requird details are defined in the PROMOTIONS class variable.
        """
        self.contents: List[str] = []
        self.invalid: List[str] = []

        self.promotion_discounts: Dict[str, int] = {}

    @property
    def product_count(self) -> Counter[str]:
        """Count the number of each product in the basket.

        Returns:
            Counter: Key value pairs, with keys product name and value the quantity of that product in the basket.
        """
        return collections.Counter(self.contents)

    @property
    def subtotal(self) -> int:
        """Compute the cost of the basket before taking into account any applied promotions.

        Returns:
            int: The cost of the basket before taking into account any applied promotions.
        """
        return sum(self.PRODUCTS.get(product) for product in self.contents)

    @property
    def total_discount(self) -> int:
        """Compute the total discount on the basket due the applied promotions.

        Returns:
            int: The total discount on the basket due to promotions.
        """
        return sum(discount for discount in self.promotion_discounts.values())

    @property
    def total(self) -> int:
        """Compute the cost of the basket after taking into account any applied promotions.

        Returns:
            int: The cost of the basket after after taking into account any applied promotions.
        """
        return self.subtotal - self.total_discount

    def add_product(self, product: str) -> bool:
        """Add a product to the contents of the basket.

        Args:
            product: The name of the product to add to the basket.

        Returns:
            bool: True if the product is successfully added, False otherwise.
        """
        product_upper = product.upper()

        if product_upper in self.PRODUCTS:
            self.contents.append(product_upper)
            return True

        self.invalid.append(product)
        return False

    def empty_basket(self) -> None:
        """Empty the basket."""
        self.contents = []
        self.invalid = []
        self.promotion_discounts = {}

    def apply_promotions(self) -> None:
        """Apply each promotion from self.PROMOTIONS to the products in the basket."""
        for promotion, promotion_details in self.PROMOTIONS.items():
            self.apply_promotion(promotion, promotion_details)

    def apply_promotion(
        self, promotion_name: str, promotion_details: Dict[str, Union[str, int]]
    ):
        """Apply the promotion to the products in the basket.

        Args:
            promotion_name (str): The name of the promotion to apply.
            promotion_details (Dict[str, Union[str, int]]): Details of the promotion to be applied. Keys should include qualifying_product, discounted_product, qualifying_product_quantity and percent_discount.
        """
        qualifying_product_count = self.product_count[
            promotion_details["qualifying_product"]
        ]
        discounted_product_count = self.product_count[
            promotion_details["discounted_product"]
        ]

        qualifying_product_quantity = promotion_details["qualifying_product_quantity"]
        percent_discount = promotion_details["percent_discount"]
        unit_price = self.PRODUCTS[promotion_details["discounted_product"]]

        num_allowed_discounts = qualifying_product_count // qualifying_product_quantity

        discounts_applied = min(num_allowed_discounts, discounted_product_count)

        self.promotion_discounts[promotion_name] = int(
            discounts_applied * unit_price * percent_discount / 100
        )
