"""Test suite for the product module."""


import pytest
from shoppingbasket.product import Product
from shoppingbasket.promotion import Promotion


class Test_ProductInit:
    """Test suite for the Basket.__init__ method."""

    @pytest.mark.parametrize(
        "name,id, unit_price, available,",
        [
            ("SOUP", 1, 65, True),
            ("breaD", 2, 80, True),
            ("MILK", 3, 130, True),
            ("APPLES", 4, 100, True),
            ("TOMATOES", 5, 50, False),
            ("CUCUMBER", 6, 90, False),
            ("PEANUTS", 7, 210, False),
            ("LAMB STEAK", 8, 450, False),
            ("CHICKEN", 9, 620, True),
            ("TEA", 10, 140, False),
        ],
    )
    def test_init(self, id: int, name: str, unit_price: int, available: bool):
        """Test creating a product."""
        product = Product(name, id, unit_price, available)

        assert product.name == name.upper()
        assert product.id == id
        assert product.unit_price == unit_price
        assert product.available == available
        assert product.promotion is None


class Test_ProductEq:
    """Test suite for the Basket.__eq__ method."""

    def test_equal_products(self):
        """Test equality of two Product objects that should be deemed equal."""
        product1 = Product("SOUP", 1, 65, True)
        product2 = Product("SOUP", 1, 65, True)

        assert product1 == product2

    def test_inequal_products(self):
        """Test equality of two Product objects that should not be deemed equal."""
        product1 = Product("SOUP", 1, 65, True)
        product2 = Product("MILK", 3, 130, True)

        assert product1 != product2

    def test_incorrect_type_comparison(self):
        """Test equality of Product object with another type."""
        product1 = Product("SOUP", 1, 65, True)

        assert product1 != "SOUP"


class Test_ApplyPromotion:
    """Test suite for the Basket.apply_promotion method."""

    def test_apply_promotion(self, apples_promotion: Promotion):
        """Test applying Promotion to Product."""
        product = Product("APPLES", 4, 100, True)
        product.apply_promotion(apples_promotion)

        assert product.promotion == apples_promotion
        assert product.promotion_discount == 10
        assert apples_promotion.name in product.promotion_message
        assert product.promotion_price == 90

    def test_remove_promotion(self, apples_promotion: Promotion):
        """Test applying and then removing a promotion from a Product."""
        product = Product("APPLES", 4, 100, True)
        product.apply_promotion(apples_promotion)
        product.remove_promotion()

        assert product.promotion is None
        assert product.promotion_discount == 0
        assert product.promotion_message is None
        assert product.promotion_price == product.unit_price
