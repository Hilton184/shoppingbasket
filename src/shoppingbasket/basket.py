"""Module for the Basket class - with functionality to add products, determine the basket total, apply promotions to the Products in the basket and more."""

from typing import List

from shoppingbasket.catalog import Catalog
from shoppingbasket.product import Product
from shoppingbasket.promotion import Promotion


class Basket:
    """Blueprint for Basket object."""

    def __init__(
        self,
        product_catalog: Catalog,
        promotion_catalog: Catalog,
    ) -> None:
        """Create a Basket object, with the product catalog and promotion catalog defining the valid products and promotions.

        Args:
            product_catalog (Catalog): Catalog of products.
            promotion_catalog (Catalog): Catalog of promotions.

        """
        self.product_catalog = product_catalog
        self.promotion_catalog = promotion_catalog

        self.contents: List[Product] = []
        self.promoted_products: List[Product] = []
        self.unavailable_products: List[str] = []
        self.invalid_products: List[str] = []

    def __repr__(self) -> str:
        """Developer friendly representation of object."""
        return f"Basket(contents={self.contents})"

    @staticmethod
    def _product_in_catalog(product_name: str, product_catalog: Catalog) -> bool:
        """Check whether the product is in the product catalog.

        Args:
            product_name (str): The name of the product to lookup in the product catalog.
            product_catalog (Catalog): The product catalog of the valid products.

        Returns:
            bool: Whether or not the product is in the product catalog.
        """
        if product_name.upper() in product_catalog.by_name:
            return True

        return False

    @staticmethod
    def _product_available(product_name: str, product_catalog: Catalog) -> bool:
        """Check whether the product is available.

        Args:
            product_name (str): The name of the product to check for availability.
            product_catalog (Catalog): The product catalog of the valid products.

        Returns:
            bool: Whether or not the product is available.
        """
        return product_catalog.by_name[product_name.upper()]["available"]

    @staticmethod
    def _create_product_object(product_name: str, product_catalog: Catalog) -> Product:
        """Create a Product object from the name of a product.

        Args:
            product_name (str): The name of the product.
            product_catalog (Catalog): The product catalog of the valid products.

        Returns:
            Product: Product object.
        """
        product_details = product_catalog.by_name[product_name.upper()]

        product = Product(
            product_details["name"],
            product_details["id"],
            product_details["unit_price"],
            product_details["available"],
        )
        return product

    def add_product(self, product_name: str) -> bool:
        """Add a product to the contents of the basket.

        Args:
            product (Product): Product to add to the contents of the basket.

        Returns:
            bool: True if the product is successfully added, False otherwise.
        """
        if not self._product_in_catalog(product_name, self.product_catalog):
            self.invalid_products.append(product_name)
            return False

        if not self._product_available(product_name, self.product_catalog):
            self.unavailable_products.append(product_name)
            return False

        product = self._create_product_object(product_name, self.product_catalog)

        self.contents.append(product)

        return True

    @property
    def subtotal(self) -> int:
        """Compute the cost of the basket before any promotions have been applied.

        Returns:
            int: The cost of the basket before any promotions have been applied.
        """
        return sum(product.unit_price for product in self.contents)

    def _create_promotion_object(self, promotion_id: int) -> Promotion:
        """Create a Promotion object from the id of a promotion.

        Args:
            promotion_id (int): The id of the promotion.

        Returns:
            Product: Promotion object.
        """
        promotion_details = self.promotion_catalog.by_id[promotion_id]

        promotion = Promotion(
            promotion_details["id"],
            promotion_details["name"],
            promotion_details["active"],
            promotion_details["qualifying_product_id"],
            promotion_details["qualifying_product_quantity"],
            promotion_details["discounted_product_id"],
            promotion_details["percent_discount"],
        )

        return promotion

    def _compute_qualifying_discounts(self, promotion: Promotion) -> int:
        """Compute the total number of times a promotion can be applied to the basket based on the qualifying product purchase quantity.

        Args:
            promotion (Promotion): The promotion for which the number of times the promotion can be applied is to be determined.

        Returns:
            int: The number of times the promotion can be applied, based on the qualifying product purchase quantity.
        """
        qualifying_product_count = sum(
            1 for item in self.contents if item.id == promotion.qualifying_product_id
        )

        return qualifying_product_count // promotion.qualifying_product_quantity

    def _apply_qualifying_discounts(
        self, promotion: Promotion, qualifying_discounts: int
    ):
        """Apply the qualifying discounts on the products in the basket to be discounted in line with the promotion.

        Args:
            promotion (Promotion): The promotion to apply.
            qualifying_discounts (int): The number of times to apply the promotion.
        """
        items_eligible_for_discount = [
            item for item in self.contents if item.id == promotion.discounted_product_id
        ]

        for item in items_eligible_for_discount:
            if qualifying_discounts < 1:
                break

            item.apply_promotion(promotion)
            qualifying_discounts -= 1
            self.promoted_products.append(item)

    def apply_promotion(self, promotion: Promotion):
        """Apply <promotion> to the products in the basket.

        Args:
            promotion (Promotion): Promotion to apply to the products in the basket.
        """
        if not promotion.active:
            return None

        qualifying_discounts = self._compute_qualifying_discounts(promotion)

        self._apply_qualifying_discounts(promotion, qualifying_discounts)

    def apply_promotions(self) -> None:
        """Loop through the products in the basket and apply promotions to the products."""
        self.reset_promotions()

        for id in self.promotion_catalog.by_id:
            promotion = self._create_promotion_object(id)
            self.apply_promotion(promotion)

    @property
    def total(self) -> int:
        """Compute the cost of the basket after promotions have been applied.

        Returns:
            int: The cost of the basket after promotions have been applied.
        """
        return sum(product.promotion_price for product in self.contents)

    def reset_promotions(self) -> None:
        """Reset the basket and its contents to remove any applied promotions."""
        self.promoted_products = []

        for item in self.contents:
            item.remove_promotion()

    def empty_basket(self) -> None:
        """Empty the basket."""
        self.reset_promotions()
        self.contents = []
        self.invalid_products = []
        self.unavailable_products = []
