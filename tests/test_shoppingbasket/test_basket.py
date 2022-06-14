"""Test suite for the basket module."""

from typing import Tuple

import pytest
from shoppingbasket.basket import Basket
from shoppingbasket.catalog import Catalog
from shoppingbasket.product import Product
from shoppingbasket.promotion import Promotion


class Test_BasketInit:
    """Test suite for the Basket.__init__ method."""

    def test_empty_basket(self, fresh_basket: Basket):
        """Test creating an empty basket."""
        assert (
            fresh_basket.contents
            == fresh_basket.promoted_products
            == fresh_basket.unavailable_products
            == fresh_basket.invalid_products
            == []
        )


class Test_ProductInCatalog:
    """Test suite for the Basket._product_in_catalog static method."""

    @pytest.mark.parametrize("name", ["APPLES", "soup", "breAD", "MILK"])
    def test_valid_available_product(
        self,
        name: str,
        catalogs: Tuple[Catalog],
    ):
        """Test example of a valid available product and see if it is found in the catalog."""
        product_catalog, _ = catalogs

        assert Basket._product_in_catalog(name, product_catalog) is True

    @pytest.mark.parametrize("name", ["TOMAtoes", "CucumBeR", "peanuts", "LAMB STEAK"])
    def test_valid_unavailable_product(
        self,
        name: str,
        catalogs: Tuple[Catalog],
    ):
        """Test example of a valid unavailable product and see if it is found in the catalog."""
        product_catalog, _ = catalogs

        assert Basket._product_in_catalog(name, product_catalog) is True

    @pytest.mark.parametrize("name", ["chicken", "tea", "COFFEE"])
    def test_invalid_product(
        self,
        name: str,
        catalogs: Tuple[Catalog],
    ):
        """Test example of an invalid product and confirm it is not found in the catalog."""
        product_catalog, _ = catalogs

        assert Basket._product_in_catalog(name, product_catalog) is False


class Test_ProductAvailable:
    """Test suite for the Basket._product_available static method. This method only gets called for products which are valid."""

    @pytest.mark.parametrize("name", ["APPLES", "soup", "breAD", "MILK"])
    def test_valid_available_product(self, name: str, catalogs: Tuple[Catalog]):
        """Test example of a valid available product and confirm the product is available."""
        product_catalog, _ = catalogs

        assert Basket._product_available(name, product_catalog) is True

    @pytest.mark.parametrize("name", ["TOMAtoes", "CucumBeR", "peanuts", "LAMB STEAK"])
    def test_valid_unavailable_product(self, name: str, catalogs: Tuple[Catalog]):
        """Test example of a valid unavailable product and confirm the product is unavailable."""
        product_catalog, _ = catalogs

        assert Basket._product_available(name, product_catalog) is False


class Test_AddProduct:
    """Test suite for the Basket.add_product method."""

    @pytest.mark.parametrize(
        "name,id, unit_price, available,",
        [
            ("SOUP", 1, 65, True),
            ("breaD", 2, 80, True),
            ("MILK", 3, 130, True),
            ("APPLES", 4, 100, True),
        ],
    )
    def test_valid_available_product(
        self,
        name: str,
        id: int,
        unit_price: int,
        available: bool,
        fresh_basket: Basket,
    ):
        """Test example of a trying to add a valid and available product to the basket."""
        assert fresh_basket.add_product(name) is True
        assert len(fresh_basket.contents) == 1

        assert fresh_basket.subtotal == unit_price
        assert fresh_basket.total == unit_price

        assert fresh_basket.contents[0] == Product(name, id, unit_price, available)

    @pytest.mark.parametrize(
        "name",
        [
            "TOMATOES",
            "CUCUMBER",
            "PEANUTS",
            "LAMB STEAK",
        ],
    )
    def test_valid_unavailable_product(
        self,
        name: str,
        fresh_basket: Basket,
    ):
        """Test example of trying to add a valid but unavailable product to the basket."""
        assert fresh_basket.add_product(name) is False
        assert len(fresh_basket.contents) == 0
        assert fresh_basket.subtotal == 0
        assert fresh_basket.total == 0
        assert len(fresh_basket.unavailable_products) == 1
        assert fresh_basket.unavailable_products[0] == name

    @pytest.mark.parametrize(
        "name",
        [
            "CHICKEN",
            "TEA",
        ],
    )
    def test_invalid_product(
        self,
        name: str,
        fresh_basket: Basket,
    ):
        """Test example of trying to add an invalid product to the basket."""
        assert fresh_basket.add_product(name) is False
        assert len(fresh_basket.contents) == 0
        assert fresh_basket.subtotal == 0
        assert fresh_basket.total == 0
        assert len(fresh_basket.invalid_products) == 1
        assert fresh_basket.invalid_products[0] == name


class Test_ApplyPromotions:
    """Test suite for the Basket.apply_promotions method."""

    def test_apples_promotion(self, fresh_basket: Basket, apples_promotion: Promotion):
        """Test example of applying the test apples promotion from a fresh basket."""
        fresh_basket.add_product("APPLES")
        fresh_basket.apply_promotions()
        assert fresh_basket.contents[0].promotion == apples_promotion
        assert len(fresh_basket.promoted_products) == 1
        assert fresh_basket.subtotal == 100
        assert fresh_basket.total == 90

    def test_apples_promotion_many_products(
        self, fresh_basket: Basket, apples_promotion: Promotion
    ):
        """Test example of applying the test apples promotion from a fresh basket."""
        fresh_basket.add_product("APPLES")
        fresh_basket.add_product("APPLES")
        fresh_basket.add_product("APPLES")
        fresh_basket.add_product("MILK")
        fresh_basket.add_product("APPLES")
        fresh_basket.add_product("CHICKEN")
        fresh_basket.add_product("TEA")
        fresh_basket.add_product("TOMATOES")

        fresh_basket.apply_promotions()

        assert (
            fresh_basket.contents[0].promotion
            == fresh_basket.contents[1].promotion
            == fresh_basket.contents[2].promotion
            == fresh_basket.contents[4].promotion
            == apples_promotion
        )

        assert fresh_basket.contents[3].promotion is None

        assert len(fresh_basket.promoted_products) == 4
        assert len(fresh_basket.invalid_products) == 2
        assert len(fresh_basket.unavailable_products) == 1

        assert len(fresh_basket.contents) == 5

        assert fresh_basket.subtotal == 530
        assert fresh_basket.total == 490

    def test_soup_bread_promotion_v1(
        self, fresh_basket: Basket, soup_bread_promotion: Promotion
    ):
        """Test example of applying the test soup_bread promotion from a fresh basket, whereby there is insufficient qualifying products purchased for a promotion to be applied."""
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("SOUP")

        fresh_basket.apply_promotions()

        assert (
            fresh_basket.contents[0].promotion
            == fresh_basket.contents[1].promotion
            == fresh_basket.contents[2].promotion
            is None
        )
        assert len(fresh_basket.promoted_products) == 0
        assert fresh_basket.subtotal == 225
        assert fresh_basket.total == 225

    def test_soup_bread_promotion_v2(
        self, fresh_basket: Basket, soup_bread_promotion: Promotion
    ):
        """Test example of applying the test soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products purchased for a promotion to be applied."""
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")

        fresh_basket.apply_promotions()

        assert fresh_basket.contents[0].promotion == soup_bread_promotion

        assert (
            fresh_basket.contents[1].promotion
            == fresh_basket.contents[2].promotion
            == fresh_basket.contents[3].promotion
            is None
        )

        assert len(fresh_basket.promoted_products) == 1

        assert fresh_basket.subtotal == 290
        assert fresh_basket.total == 250

    def test_soup_bread_promotion_v3(
        self, fresh_basket: Basket, soup_bread_promotion: Promotion
    ):
        """Test example of applying the test soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products purchased for only 1 promotion to be applied."""
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")

        fresh_basket.apply_promotions()

        assert fresh_basket.contents[0].promotion == soup_bread_promotion

        assert (
            fresh_basket.contents[1].promotion
            == fresh_basket.contents[2].promotion
            == fresh_basket.contents[3].promotion
            == fresh_basket.contents[4].promotion
            is None
        )

        assert len(fresh_basket.promoted_products) == 1

        assert fresh_basket.subtotal == 355
        assert fresh_basket.total == 315

    def test_soup_bread_promotion_v4(
        self, fresh_basket: Basket, soup_bread_promotion: Promotion
    ):
        """Test example of applying the test soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products purchased for only 1 promotion to be applied."""
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")

        fresh_basket.apply_promotions()

        assert fresh_basket.contents[0].promotion == soup_bread_promotion
        assert fresh_basket.contents[1].promotion == soup_bread_promotion

        assert (
            fresh_basket.contents[2].promotion
            == fresh_basket.contents[3].promotion
            == fresh_basket.contents[4].promotion
            == fresh_basket.contents[5].promotion
            is None
        )

        assert len(fresh_basket.promoted_products) == 2

        assert fresh_basket.subtotal == 420
        assert fresh_basket.total == 340

    def test_soup_bread_promotion_v5(
        self, fresh_basket: Basket, soup_bread_promotion: Promotion
    ):
        """Test example of applying the test soup_bread promotion from a fresh basket, whereby there are sufficient qualifying products purchased for only 1 promotion to be applied."""
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("BREAD")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")
        fresh_basket.add_product("SOUP")

        fresh_basket.apply_promotions()

        assert fresh_basket.contents[0].promotion == soup_bread_promotion
        assert fresh_basket.contents[1].promotion == soup_bread_promotion

        assert (
            fresh_basket.contents[2].promotion
            == fresh_basket.contents[3].promotion
            == fresh_basket.contents[4].promotion
            == fresh_basket.contents[5].promotion
            == fresh_basket.contents[6].promotion
            == fresh_basket.contents[7].promotion
            == fresh_basket.contents[8].promotion
            is None
        )

        assert len(fresh_basket.promoted_products) == 2

        assert fresh_basket.subtotal == 615
        assert fresh_basket.total == 535


class Test_EmptyBasket:
    """Test suite for the Basket.empty_basket method."""

    def test_empty_basket(self, fresh_basket: Basket, apples_promotion: Promotion):
        """Test example of applying the test apples promotion from a fresh basket."""
        fresh_basket.add_product("APPLES")
        fresh_basket.apply_promotions()

        fresh_basket.empty_basket()

        assert (
            fresh_basket.contents
            == fresh_basket.invalid_products
            == fresh_basket.unavailable_products
            == []
        )
