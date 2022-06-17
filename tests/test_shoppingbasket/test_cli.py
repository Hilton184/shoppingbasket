"""Test suite for the cli module."""


from click.testing import CliRunner
from shoppingbasket.cli import main


class Test_MainFunction:
    """Test CLI interface with shoppingbasket package."""

    def test_single_available_product_no_promotion(self):
        """Test single product."""
        products_list = ["MILK"]

        runner = CliRunner()

        response = runner.invoke(main, products_list)

        assert (
            response.output
            == "Subtotal: £1.30\n(No offers available)\nTotal price: £1.30\n"
        )
        assert response.exit_code == 0

    def test_single_available_product_on_promotion(self):
        """Test single product on promotion."""
        products_list = ["APPLES"]

        runner = CliRunner()

        response = runner.invoke(main, products_list)

        assert (
            response.output
            == "Subtotal: £1.00\nApples 10% off: -10p\nTotal price: 90p\n"
        )
        assert response.exit_code == 0

    def test_several_available_products(self):
        """Test several available products including promotions."""
        products_list = ["APPLES", "MILK", "SOUP", "BREAD"]

        runner = CliRunner()

        response = runner.invoke(main, products_list)

        assert (
            response.output
            == "Subtotal: £3.75\nApples 10% off: -10p\nTotal price: £3.65\n"
        )
        assert response.exit_code == 0

    def test_several_available_products_with_soup_promo(self):
        """Test several available products including several promotions."""
        products_list = ["APPLES", "MILK", "SOUP", "BREAD", "SOUP"]

        runner = CliRunner()

        response = runner.invoke(main, products_list)

        assert (
            response.output
            == "Subtotal: £4.40\nApples 10% off: -10p\nPurchase 2 tins of soup and get half price off bread: -40p\nTotal price: £3.90\n"
        )
        assert response.exit_code == 0

    def test_several_available_products_with_soup_promo_and_invalid_products(
        self,
    ):
        """Test several available products including several promotions including invalid products."""
        products_list = [
            "apples",
            "MILK",
            "SOup",
            "bread",
            "SOUP",
            "TOMATOES",
            "CHICKEN",
            "cucumber",
            "tEa",
        ]

        runner = CliRunner()

        response = runner.invoke(main, products_list)

        assert response.exit_code == 0

        assert (
            """Product "TOMATOES" is an invalid product. It has not been added to the basket."""
            in response.output
        )
        assert (
            """Product "CHICKEN" is an invalid product. It has not been added to the basket."""
            in response.output
        )
        assert (
            """Product "cucumber" is an invalid product. It has not been added to the basket."""
            in response.output
        )
        assert (
            """Product "tEa" is an invalid product. It has not been added to the basket."""
            in response.output
        )

        assert (
            "Subtotal: £4.40\nApples 10% off: -10p\nPurchase 2 tins of soup and get half price off bread: -40p\nTotal price: £3.90\n"
            in response.output
        )
