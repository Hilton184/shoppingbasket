"""Test suite for the promotion module."""

from shoppingbasket.promotion import Promotion


class Test_PromotionInit:
    """Test suite for the Promotion.__init__ method."""

    def test_init(self):
        """Test creating a Promotion."""
        (
            id,
            name,
            active,
            qualifying_product_id,
            qualifying_product_quantity,
            discounted_product_id,
            percent_discount,
        ) = (1, "Apples 10% off", True, 4, 1, 4, 10)

        promotion = Promotion(
            id,
            name,
            active,
            qualifying_product_id,
            qualifying_product_quantity,
            discounted_product_id,
            percent_discount,
        )

        assert promotion.id == id
        assert promotion.name == name
        assert promotion.active == active
        assert promotion.qualifying_product_id == qualifying_product_id
        assert promotion.qualifying_product_quantity == qualifying_product_quantity
        assert promotion.discounted_product_id == discounted_product_id
        assert promotion.percent_discount == percent_discount
