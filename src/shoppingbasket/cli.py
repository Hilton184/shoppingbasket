"""Command line interface utility for the shoppingbasket module."""


import click

import shoppingbasket._utils
from shoppingbasket.basket import Basket
from shoppingbasket.catalog import Catalog, CatalogType


def _handle_invalid_products_output(basket: Basket) -> None:
    for product in basket.invalid_products:
        print(
            f"""Product "{product}" is an invalid product as it is not in the product data."""
        )

    for product in basket.unavailable_products:
        print(f"""Product "{product}" is unavailable for purchase.""")


def _handle_primary_output(basket: Basket) -> None:
    print(f"Subtotal: {shoppingbasket._utils._currency_format(basket.subtotal)}")

    if not basket.promoted_products:
        print("(No offers available)")

    for product in basket.promoted_products:
        print(product.promotion_message)

    print(f"Total price: {shoppingbasket._utils._currency_format(basket.total)}")


@click.command()
@click.option(
    "--products-catalog-filepath",
    help="The relative filepath from the current working directory, to the JSON file dataset containing valid purchasable products and their attributes. Default handled in package internals to look in data/products.json, relative to the current working directory.",
)
@click.option(
    "--promotions-catalog-filepath",
    help="The relative filepath from the current working directory, to the JSON file dataset containing product promotions and their attributes. Default handled in package internals to look in data/promotions.json, relative to the current working directory.",
)
@click.argument("products", nargs=-1)
def main(
    products_catalog_filepath: str, promotions_catalog_filepath: str, products: str
):
    """Entrypoint for running the command line utility of the shoppingbasket package. Specify one or more products (via the PRODUCTS positional argument) to add to the basket."""
    products = [*products]

    products_catalog = Catalog(CatalogType.PRODUCTS, products_catalog_filepath)
    promotions_catalog = Catalog(CatalogType.PROMOTIONS, promotions_catalog_filepath)
    basket = Basket(products_catalog, promotions_catalog)

    for product_name in products:
        basket.add_product(product_name)

    basket.apply_promotions()

    _handle_invalid_products_output(basket)

    _handle_primary_output(basket)
