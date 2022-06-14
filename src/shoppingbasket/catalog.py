"""Interface for extracting availability, pricing and configuration data from JSON data files turning into Python Catalog objects."""

import json
import os
from enum import Enum
from typing import Dict, List, Optional


class CatalogType(Enum):
    """Blueprint for CatalogType Enum object. Value of each Enum should correspond to the default relative filepath to use when extracting required data. This default is only used if file_path is not specified in Catalog class."""

    PRODUCTS = "data/products.json"
    PROMOTIONS = "data/promotions.json"


class Catalog:
    """Blueprint for Catalog class."""

    def __init__(
        self, catalog_type: CatalogType, file_path: Optional[str] = None
    ) -> None:
        """Initialize a Catalog object of a specific type.

        Args:
            catalog_type (CatalogType): CatalogType object specifying the type of Catalog object to create.
            file_path (Optional[str], optional): Relative filepath to the JSON file to be loaded. Defaults to None. If None, will attempt to access data from the default relative file path as specified in the CatalogType object.
        """
        if not file_path:
            file_path = os.path.abspath(os.path.join(os.getcwd(), catalog_type.value))

        self.catalog_type = catalog_type.name
        self.file_path = file_path

        data = self._load_data()

        self.data = self._validate_data(self.catalog_type, data)

    def _load_data(self) -> List[Dict]:
        """Load data from <self.file_path> to get the dataset as a list of items, where each item is a dictionary of item properties."""
        with open(self.file_path) as f:
            data = json.load(f)
        return data

    def _validate_data(self, catalog_type: str, data: Dict) -> None:
        """Validate the data to ensure it is in the correct format for use in the program."""
        if not data.get(self.catalog_type.lower()):
            raise Exception(
                f"""{catalog_type} data JSON missing "{self.catalog_type.lower()}" key."""
            )

        if catalog_type == CatalogType.PRODUCTS.name:
            return self._validate_product_data(data)
        elif catalog_type == CatalogType.PROMOTIONS.name:
            return self._validate_promotion_data(data)

    def _validate_product_data(self, data: Dict) -> Dict:
        """Validate the product data to ensure it is in the correct format for use in the program."""
        required_keys = ["id", "name", "unit_price", "available"]

        for product in data[self.catalog_type.lower()]:
            if not all(key in product for key in required_keys):
                raise Exception(
                    f"Products data JSON missing some required keys. Required keys are {required_keys}. Product {product} detected to be missing some required keys."
                )

            product["name"] = product["name"].upper()

        return data.get(self.catalog_type.lower())

    def _validate_promotion_data(self, data: Dict) -> None:
        """Validate the promotion data to ensure it is in the correct format for use in the program."""
        required_keys = [
            "id",
            "name",
            "active",
            "qualifying_product_id",
            "qualifying_product_quantity",
            "discounted_product_id",
            "percent_discount",
        ]

        for promotion in data[self.catalog_type.lower()]:
            if not all(key in promotion for key in required_keys):
                raise Exception(
                    f"Promotion data JSON missing some required keys. Required keys are {required_keys}. Product {promotion} detected to be missing some required keys."
                )

        return data.get(self.catalog_type.lower())

    @property
    def by_name(self) -> Dict:
        """Get the catalog as a dictionary, with keys corresponding to the name of each item in the catalog.

        Returns:
            Dict: A dictionary representation of the items in the catalog, with keys corresponding to the name of each item in the catalog.
        """
        return {x["name"]: x for x in self.data}

    @property
    def by_id(self) -> Dict:
        """Get the catalog as a dictionary, with keys corresponding to the id of each item in the catalog.

        Returns:
            Dict: A dictionary representation of the items in the catalog, with keys corresponding to the id of each item in the catalog.
        """
        return {x["id"]: x for x in self.data}
