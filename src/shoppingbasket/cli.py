"""Command line interface utility for the shoppingbasket module."""


from typing import Iterable

import click

import shoppingbasket._utils
from shoppingbasket.basket import Basket


def _handle_invalid_products_output(basket: Basket) -> None:
    for product in basket.invalid:
        print(
            f"""Product "{product}" is an invalid product. It has not been added to the basket."""
        )


def _handle_primary_output(basket: Basket) -> None:
    print(f"Subtotal: {shoppingbasket._utils._currency_format(basket.subtotal)}")

    if not basket.total_discount:
        print("(No offers available)")

    for promotion, discount in basket.promotion_discounts.items():

        if discount:
            print(f"{promotion}: -{shoppingbasket._utils._currency_format(discount)}")

    print(f"Total price: {shoppingbasket._utils._currency_format(basket.total)}")


@click.command()
@click.argument("products", nargs=-1)
def main(products: Iterable):
    """Entrypoint for running the command line utility of the shoppingbasket package. Specify one or more products (via the PRODUCTS positional argument) to add to the basket."""
    products = [*products]

    basket = Basket()

    for product_name in products:
        basket.add_product(product_name)

    basket.apply_promotions()

    _handle_invalid_products_output(basket)

    _handle_primary_output(basket)
