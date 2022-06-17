# shoppingbasket

[![Continuous Integration](https://github.com/Hilton184/shoppingbasket/actions/workflows/ci.yml/badge.svg)](https://github.com/Hilton184/shoppingbasket)                [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

shoppingbasket is a Python library with functionality for calculating the price of baskets of products, including functionality to account for product promotions.

You can use the functionality of the shoppingbasket package directly from the command line, using the command line program `ShoppingBasket`. Installation and usage instructions for both the shoppingbasket python package and the ShoppingBasket command line utility are provided.

---

## Installation

To install and run the code locally:
1) Ensure you have Python and git installed. The shoppingbasket library requires python>=3.8.
2) Clone this repository using the command `git clone https://github.com/Hilton184/shoppingbasket.git`.
3) Run the command `pip install .` from the root directory of the cloned repository.
4) The shoppingbasket package should now be installed.
    - Confirm this is the case by running the command `pip show shoppingbasket`.
    - Confirm you have access to the ShoppingBasket command line utility by running the command `ShoppingBasket --help`

---
## CLI Example Usage

```bash
ShoppingBasket milk bread soup
# > Subtotal: £2.75
# > (No offers available)
# > Total price: £2.75

# the PRODUCTS argument is case-insensitive.
ShoppingBasket miLK BREAD soup
# > Subtotal: £2.75
# > (No offers available)
# > Total price: £2.75

# if offers are available, a brief description of the offer and the discount obtained is provided.
ShoppingBasket milk bread soup apples
# > Subtotal: £3.75
# > Apples 10% off: -10p
# > Total price: £3.65

# if several offers are available, they are logged to the output as each offer is applied.
ShoppingBasket milk bread soup apples soup
# > Subtotal: £4.40
# > Apples 10% off: -10p
# > Purchase 2 tins of soup and get half price off bread: -40p
# > Total price: £3.90

# if several offers are available, they are logged to the output as each offer is applied. If the same offer is applied multiple times, the discounts are totalled for each promotion.
ShoppingBasket milk bread soup apples soup apples
# > Subtotal: £4.90
# > Apples 10% off: -30p
# > Purchase 2 tins of soup and get half price off bread: -40p
# > Total price: £4.80

# if an offer is invalid because it is not part of the PRODUCTS data structure defined in data.py, the program will specify so and the product will not be added to the basket.
ShoppingBasket milk bread soup apples chicken
# > Product "chicken" is an invalid product. It has not been added to the basket.
# > Subtotal: £3.75
# > Apples 10% off: -10p
# > Total price: £3.65

# if an offer is unavailable because it is part of the products.json data file but the file states the product is unavailable, the program will specify so and the product will not be added to the basket.
ShoppingBasket milk bread soup apples tomatoes
# > Product "tomatoes" is an invalid product. It has not been added to the basket.
# > Subtotal: £3.75
# > Apples 10% off: -10p
# > Total price: £3.65
```

## Python Example Usage

Documentation generated automatically from module, class and function docstrings can be found at `docs/shoppingbasket`. This is HTML documentation so is best viewed in a browser like Google Chrome.

Nevertheless, some example using of the shoppingbasket package directly in a python script is provided below:

```python
from shoppingbasket.basket import Basket

basket = Basket()

products_to_add = ["APPLES", "breAD", "milk", "soup", "tomatoes", "chicken"]

# add product to the basket basket.add_product. This method looks up the product name in basket.PRODUCTS data structure. If product is invalid, the product is not added to the basket.
for product in products_to_add:
    basket.add_product(product)

# Get a list of the products successfully added to the basket
basket.contents

# Compute the initial cost of the basket
basket.subtotal  # 375

# Compute the cost of the basket after any applied promotions are taken into account
basket.total  # 375 (since no promotions yet applied)

# Get the names of each products not added to the contents of the basket as they are invalid
basket.invalid  # ["tomatoes, "chicken"]

# Get the promotions which have been applied and the discount provided
basket.promotion_discounts  # {}

# Loop through the promotions in the basket.PROMOTIONS data structure and apply each promotion to the basket.
basket.apply_promotions()
basket.promotion_discounts # {Apples 10% off: 10, "Purchase 2 tins of soup and get half price off bread": 0}
basket.subtotal  # 375
basket.total  # 365
basket.total_discount # 10

# Empty a basket
basket.empty_basket
basket.contents  # []
basket.promotion_discounts # {}
basket.subtotal  # 375
basket.total  # 375
```

---
## Additional Information

The products and promotions taken into account by the program are defined in `data.py`, in the `PRODUCTS` and `PROMOTIONS` data structures. The `shoppingbasket` package and `ShoppingBasket` program only allow products defined in the PRODUCTS data structure to be added to a basket, and only apply promotions defined in the PROMOTIONS data structure. The maintainers of the package will keep these structures up to date with the available products and promotions.

---
## Contributing

The python packaging and dependency management tool `poetry` is used for this project. To contribute, in addition to having python and git installed, ensure you have poetry installed on your system too.

- Run command `poetry install` to install the required packages for testing and development based on the `poetry.lock` file.
- If adding new dependencies, run command `poetry add <package>` to ensure the package is added as a project dependency.
- If an existing dependency is no longer required, run command `poetry remove <package>`.
- Run command `poetry update` to ensure the `project.lock` file is updated as and when required.
- Run command `poetry build` to build the package locally.

### Formatting

The `black` package is used to auto-format code. This is checked as part of the CI process, so make sure you format your code using blacklocally.

### Linting

The `flake8` package is used to lint code. This is checked as part of the CI process, so make sure you lint your code using flake8 locally. Exceptions: E501, W503.

### Testing

The `pytest` package is used to write unit tests. Ensure all tests are passing by running the command `pytest`. Run command `pytest --cov --cov-report html` to run the test suite and generate an interactive HTML coverage report.

### Documentation

The `pdoc3` package is used to automatically generate documentation from the source code. The docstrings written at a module, class and function level ensure this generated documentation can effectively detail the use and applications of the package.

To automatically generate documentation, run `pdoc --html --output-dir docs src/shoppingbasket --force`. This will generate html documentation in the folder `docs/shoppingbasket`. This documentation can be viewed interactively using a browser (i.e open with Google Chrome).

Alternatively, run `pdoc3 --http : src/shoppingbasket` from the root directory on the command line to run a local HTTP server hosting the interactive documentation, with live development reload functionality built in.
