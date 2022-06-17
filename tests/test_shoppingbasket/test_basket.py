"""Test suite for the basket module."""


import pytest
from shoppingbasket.basket import Basket


class Test_BasketInit:
    """Test suite for the Basket.__init__ method."""

    def test_empty_basket(self, basket: Basket):
        """Test creating an empty basket."""
        assert basket.contents == basket.invalid == []

        assert basket.promotion_discounts == {}


class Test_AddProduct:
    """Test suite for the Basket.add_product method."""

    @pytest.mark.parametrize(
        "name, unit_price",
        [
            ("SOUP", 65),
            ("breaD", 80),
            ("MILK", 130),
            ("APPLES", 100),
        ],
    )
    def test_valid_available_product(
        self,
        name: str,
        unit_price: int,
        basket: Basket,
    ):
        """Test example of a trying to add a valid and available product to the basket."""
        assert basket.add_product(name) is True
        assert len(basket.contents) == 1

        assert basket.subtotal == unit_price
        assert basket.total == unit_price

        assert basket.contents[0] == name.upper()
        assert basket.product_count.get(name.upper()) == 1

    @pytest.mark.parametrize(
        "name",
        [
            "TOMATOES",
            "CUCUMBER",
            "PEANUTS",
            "LAMB STEAK",
        ],
    )
    def test_invalid_product(
        self,
        name: str,
        basket: Basket,
    ):
        """Test example of trying to add a invalid products to the basket."""
        assert basket.add_product(name) is False
        assert len(basket.contents) == 0
        assert basket.subtotal == 0
        assert basket.total == 0
        assert len(basket.invalid) == 1
        assert basket.invalid[0] == name.upper()


class Test_ApplyPromotions:
    """Test suite for the Basket.apply_promotions method."""

    def test_apples_promotion(self, basket: Basket):
        """Test example of applying the apples promotion from a fresh basket."""
        basket.add_product("APPLES")
        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 1
        )
        assert basket.promotion_discounts.get("Apples 10% off") == 10
        assert basket.subtotal == 100
        assert basket.total_discount == 10
        assert basket.total == 90

        assert len(basket.contents) == 1
        assert len(basket.invalid) == 0
        assert basket.product_count.get("APPLES") == 1

    def test_apples_promotion_many_products(self, basket: Basket):
        """Test example of applying the apples promotion from a fresh basket when adding lots of other products too."""
        basket.add_product("APPLES")
        basket.add_product("APPLES")
        basket.add_product("APPLES")
        basket.add_product("MILK")
        basket.add_product("APPLES")
        basket.add_product("CHICKEN")
        basket.add_product("TEA")
        basket.add_product("TOMATOES")

        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 1
        )
        assert basket.promotion_discounts.get("Apples 10% off") == 40
        assert basket.subtotal == 530
        assert basket.total_discount == 40
        assert basket.total == 490

        assert len(basket.contents) == 5
        assert len(basket.invalid) == 3

        assert basket.product_count.get("APPLES") == 4
        assert basket.product_count.get("MILK") == 1
        assert basket.product_count.get("TOMATOES") is None
        assert basket.product_count.get("CHICKEN") is None
        assert basket.product_count.get("TEA") is None

    def test_soup_bread_promotion_v1(self, basket: Basket):
        """Test example of applying the soup_bread promotion from a fresh basket, whereby there is insufficient qualifying products purchased for a promotion to be applied."""
        basket.add_product("BREAD")
        basket.add_product("BREAD")
        basket.add_product("SOUP")

        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 0
        )
        assert (
            basket.promotion_discounts.get(
                "Purchase 2 tins of soup and get half price off bread"
            )
            == 0
        )
        assert basket.subtotal == 225
        assert basket.total_discount == 0
        assert basket.total == 225

        assert len(basket.contents) == 3
        assert len(basket.invalid) == 0

        assert basket.product_count.get("BREAD") == 2
        assert basket.product_count.get("SOUP") == 1

    def test_soup_bread_promotion_v2(self, basket: Basket):
        """Test example of applying the soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products purchased for a promotion to be applied once."""
        basket.add_product("BREAD")
        basket.add_product("BREAD")
        basket.add_product("SOUP")
        basket.add_product("SOUP")

        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 1
        )
        assert (
            basket.promotion_discounts.get(
                "Purchase 2 tins of soup and get half price off bread"
            )
            == 40
        )
        assert basket.subtotal == 290
        assert basket.total_discount == 40
        assert basket.total == 250

        assert len(basket.contents) == 4
        assert len(basket.invalid) == 0

        assert basket.product_count.get("BREAD") == 2
        assert basket.product_count.get("SOUP") == 2

    def test_soup_bread_promotion_v3(self, basket: Basket):
        """Test example of applying the soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products purchased for the promotion to be applied once."""
        basket.add_product("BREAD")
        basket.add_product("BREAD")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")

        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 1
        )
        assert (
            basket.promotion_discounts.get(
                "Purchase 2 tins of soup and get half price off bread"
            )
            == 40
        )
        assert basket.subtotal == 355
        assert basket.total_discount == 40
        assert basket.total == 315

        assert len(basket.contents) == 5
        assert len(basket.invalid) == 0

        assert basket.product_count.get("BREAD") == 2
        assert basket.product_count.get("SOUP") == 3

    def test_soup_bread_promotion_v4(self, basket: Basket):
        """Test example of applying the test soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products pruchased for the promotion to be applied twice."""
        basket.add_product("BREAD")
        basket.add_product("BREAD")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")

        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 1
        )
        assert (
            basket.promotion_discounts.get(
                "Purchase 2 tins of soup and get half price off bread"
            )
            == 80
        )
        assert basket.subtotal == 420
        assert basket.total_discount == 80
        assert basket.total == 340

        assert len(basket.contents) == 6
        assert len(basket.invalid) == 0

        assert basket.product_count.get("BREAD") == 2
        assert basket.product_count.get("SOUP") == 4

    def test_multiple_promotions(self, basket: Basket):
        """Test example of applying the multiple promotions from a fresh basket."""
        basket.add_product("BREAD")
        basket.add_product("BREAD")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("SOUP")
        basket.add_product("APPLES")
        basket.add_product("MILK")
        basket.add_product("SOUP")

        basket.apply_promotions()

        assert (
            sum(1 for discount in basket.promotion_discounts.values() if discount) == 2
        )
        assert (
            basket.promotion_discounts.get(
                "Purchase 2 tins of soup and get half price off bread"
            )
            == 80
        )
        assert basket.promotion_discounts.get("Apples 10% off") == 10

        assert basket.subtotal == 845
        assert basket.total_discount == 90
        assert basket.total == 755

        assert len(basket.contents) == 11
        assert len(basket.invalid) == 0

        assert basket.product_count.get("BREAD") == 2
        assert basket.product_count.get("SOUP") == 7
        assert basket.product_count.get("APPLES") == 1


class Test_EmptyBasket:
    """Test suite for the Basket.empty_basket method."""

    def test_empty_basket(self, basket: Basket):
        """Test example of adding some products to the basket and then emptying the basket.."""
        basket.add_product("APPLES")
        basket.add_product("APPLES")

        basket.apply_promotions()

        basket.empty_basket()

        assert basket.contents == basket.invalid == []

        assert basket.promotion_discounts == {}
