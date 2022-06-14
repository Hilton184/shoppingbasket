"""Helper functions for shoppingbasket package."""


def _currency_format(pence: int) -> str:
    if pence >= 100:
        return f"£{pence/100:.2f}"
    else:
        return f"{pence}p"
