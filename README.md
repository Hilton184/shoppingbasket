# shoppingbasket

[![Continuous Integration](https://github.com/Hilton184/shoppingbasket/actions/workflows/ci.yml/badge.svg)](https://github.com/Hilton184/shoppingbasket)                [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

shoppingbasket is a Python library with functionality for calculating the price of baskets of products, including functionality to account for product promotions.

You can use the functionality of the shoppingbasket package directly from the command line, using the command line program `ShoppingBasket`. Installation and usage instructions for both the shoppingbasket python package and the ShoppingBasket command line utility are provided.


---
## data

Usage of the shoppingbasket python package and ShoppingBasket command line utility requires a products dataset and a promotions dataset to work.

By default, the program will look in a `data` directory, relative to the current working directory, as is the case from the root of this repository.

This `data` directory should contain two JSON files; a `products.json` and a `promotions.json`. These files should provide in JSON format the details about the products and promotions for use with the package. These files should be in the same format as in the example `products.json` and `promotions.json` files in this repository. Note that prices should be in pence.

Both the python package and command line utility allow the user to override this default behaviour.

---
## Installation

To install and run the code locally:
1) Ensure you have Python and git installed. The shoppingbasket library requires python>=3.8.
2) Clone this repository using the command `git clone https://github.com/Hilton184/shoppingbasket.git`.
3) Run the command `pip install dist/shoppingbasket-0.1.0-py3-none-any.whl` from the root directory of the cloned repository.
4) The shoppingbasket package should now be installed.
    - Confirm this is the case by running the command `pip show shoppingbasket`.
    - Confirm you have access to the ShoppingBasket command line utility by running the command `ShoppingBasket --help`

---
## CLI Example Usage

```bash
# Assuming products data and promotions data are stored in data/products.json and data/promotions.json respectively, relative to the current working directory:

# if no offers are available, this is made explicitly clear.
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
# > Apples 10% off: 10p
# > Total price: £3.65

# if several offers are available, they are logged to the output as each offer is applied.
ShoppingBasket milk bread soup apples soup
# > Subtotal: £4.40
# > Apples 10% off: 10p
# > Purchase 2 tins of soup and get half price off bread: 40p
# > Total price: £3.90

# if several offers are available, they are logged to the output as each offer is applied, including for the same offer being applied multiple times when applicable.
ShoppingBasket milk bread soup apples soup apples
# > Subtotal: £4.90
# > Apples 10% off: 10p
# > Apples 10% off: 10p
# > Purchase 2 tins of soup and get half price off bread: 40p
# > Apples 10% off: 10p
# > Total price: £4.80

# if an offer is invalid because it is not part of the products.json data file, the program will specify so and the product will not be added to the basket.
ShoppingBasket milk bread soup apples chicken
# > Product "chicken" is an invalid product as it is not in the products data.
# > Subtotal: £3.75
# > Apples 10% off: 10p
# > Total price: £3.65

# if an offer is unavailable because it is part of the products.json data file but the file states the product is unavailable, the program will specify so and the product will not be added to the basket.
ShoppingBasket milk bread soup apples tomatoes
# > Product "tomatoes" is unavailable for purchase.
# > Subtotal: £3.75
# > Apples 10% off: 10p
# > Total price: £3.65

# if the JSON data is not stored in the default location, you must specify the location using the --products-catalog-filepath and --promotions-catalog-filepath command line options. For example:

ShoppingBasket --products-catalog-filepath subfolder/subfolder2/products.json --promotions-catalog-filepath subfolder/subfolder2/products.json milk
# > Subtotal: £1.30
# > (No offers available)
# > Total price: £1.30
```

## Python Example Usage

Documentation generated automatically from module, class and function docstrings can be found at `docs/shoppingbasket`. This is HTML documentation so is best viewed in a browser like Google Chrome.

Nevertheless, some example using of the shoppingbasket package directly in a python script is provided below:

```python
# Assuming products data and promotions data are stored in data/products.json and data/promotions.json respectively, relative to the current working directory:

# Assuming products data and promotions data are stored in data/products.json and data/promotions.json respectively, relative to the current working directory.

from shoppingbasket.basket import Basket
from shoppingbasket.catalog import Catalog, CatalogType

products_catalog = Catalog(CatalogType.PRODUCTS)
promotions_catalog = Catalog(CatalogType.PROMOTIONS)

basket = Basket(products_catalog, promotions_catalog)

products_to_add = ["APPLES", "breAD", "milk", "soup", "tomatoes", "chicken"]

# add product to the basket basket.add_product. This method looks up the product name in basket.products_catalog. If product is unavailable or invalid, the product is not added to the basket.
for product in products_to_add:
    basket.add_product(product)

# Get a list of Product objects for the products successfully added to the basket
basket.contents

# Get the names of each product part of the basket contents.
[product.name for product in basket.contents]  # ["APPLES", "BREAD", "MILK", "SOUP"]

# Compute the initial cost of the basket
basket.subtotal  # 375

# Compute the cost of the basket after any applied promotions are taken into account
basket.total  # 375 (since no promotions yet applied)

# Get the names of each products not added to the contents of the basket due to unavailability
basket.unavailable_products  # ["tomatoes"]

# Get the names of each products not added to the contents of the basket due to invalidity (not in products.json)
basket.invalid_products  # ["chicken"]

# Get the products for which promotions have been applied
basket.promoted_products  # []


# Loop through the promotions in the promotions catalog and apply any promotions that are active
basket.apply_promotions()
[product.name for product in basket.promoted_products]  # ["APPLES"]
basket.subtotal  # 375
basket.total  # 365


# Reset the applied promotions for a basket...
basket.reset_promotions()
[product.name for product in basket.contents]  # ["APPLES", "BREAD", "MILK", "SOUP"]
basket.promoted_products  # []
basket.subtotal  # 375
basket.total  # 375


# Empty a basket completely
basket.empty_basket
basket.contents  # []
basket.promoted_products  # []
basket.subtotal  # 375
basket.total  # 375


# if the JSON data is not stored in the default location, you must specify the location when creating the catalog objects. For example:

products_catalog = Catalog(
    CatalogType.PRODUCTS, file_path="subfolder/subfolder2/products.json"
)
promotions_catalog = Catalog(
    CatalogType.PROMOTIONS, file_path="subfolder/subfolder2/promotions.json"
)
```


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
