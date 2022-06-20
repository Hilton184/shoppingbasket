"""Test suite for the _utils module."""
import pytest
from shoppingbasket._utils import _currency_format


class Test_CurrencyFormat:
    """Test suite for the _currency_format function."""

    @pytest.mark.parametrize(
        "input,expected",
        [
            (0, "0p"),
            (5, "5p"),
            (20, "20p"),
            (54, "54p"),
            (99, "99p"),
            (100, "£1.00"),
            (120, "£1.20"),
            (125, "£1.25"),
            (199, "£1.99"),
            (805, "£8.05"),
            (999, "£9.99"),
            (1000, "£10.00"),
            (1200, "£12.00"),
            (1330, "£13.30"),
            (1405, "£14.05"),
            (1598, "£15.98"),
            (9999, "£99.99"),
        ],
    )
    def test_currency_format(self, input: int, expected: str):
        """Test _currency_format for numbers 0 through 9999."""
        assert _currency_format(input) == expected
