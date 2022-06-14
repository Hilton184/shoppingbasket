"""Test suite for the catalog module."""


from shoppingbasket.catalog import Catalog, CatalogType


class Test_CatalogInit:
    """Test suite for the Catalog.__init__ method."""

    def test_init_product_catalog(self, product_json_data_filepath: str):
        """Test initialisation of product catalog."""
        product_catalog = Catalog(CatalogType.PRODUCTS, product_json_data_filepath)
        assert product_catalog.catalog_type == "PRODUCTS"
        assert product_catalog.file_path == product_json_data_filepath

    def test_init_promotion_catalog(self, promotion_json_data_filepath: str):
        """Test initialisation of promotion catalog."""
        promotion_catalog = Catalog(
            CatalogType.PROMOTIONS, promotion_json_data_filepath
        )
        assert promotion_catalog.catalog_type == "PROMOTIONS"
        assert promotion_catalog.file_path == promotion_json_data_filepath


class Test_CatalogByName:
    """Test suite for the Catalog.by_name property."""

    def test_by_name_product_catalog(self, product_json_data_filepath: str):
        """Test by_name property of product catalog."""
        product_catalog = Catalog(CatalogType.PRODUCTS, product_json_data_filepath)

        by_name = product_catalog.by_name

        for product in ["SOUP", "BREAD", "MILK", "APPLES"]:
            assert product in by_name

        assert by_name["SOUP"]["unit_price"] == 65
        assert by_name["SOUP"]["available"] is True
        assert by_name["SOUP"]["id"] == 1
        assert by_name["SOUP"]["name"] == "SOUP"

    def test_by_name_promotion_catalog(self, promotion_json_data_filepath: str):
        """Test by_name property of promotion catalog."""
        promotion_catalog = Catalog(
            CatalogType.PROMOTIONS, promotion_json_data_filepath
        )

        by_name = promotion_catalog.by_name

        for promotion in [
            "Apples 10% off",
            "Purchase 2 tins of soup and get half price off bread",
        ]:
            assert promotion in by_name

        assert by_name["Apples 10% off"]["id"] == 1
        assert by_name["Apples 10% off"]["name"] == "Apples 10% off"
        assert by_name["Apples 10% off"]["active"] is True
        assert by_name["Apples 10% off"]["qualifying_product_id"] == 4
        assert by_name["Apples 10% off"]["qualifying_product_quantity"] == 1
        assert by_name["Apples 10% off"]["discounted_product_id"] == 4
        assert by_name["Apples 10% off"]["percent_discount"] == 10


class Test_CatalogByID:
    """Test suite for the Catalog.by_id property."""

    def test_by_id_product_catalog(self, product_json_data_filepath: str):
        """Test by_id property of product catalog."""
        product_catalog = Catalog(CatalogType.PRODUCTS, product_json_data_filepath)

        by_id = product_catalog.by_id

        for product in [1, 2, 3, 4]:
            assert product in by_id

        assert by_id[2]["unit_price"] == 80
        assert by_id[2]["available"] is True
        assert by_id[2]["id"] == 2
        assert by_id[2]["name"] == "BREAD"

    def test_by_id_promotion_catalog(self, promotion_json_data_filepath: str):
        """Test by_id property of promotion catalog."""
        promotion_catalog = Catalog(
            CatalogType.PROMOTIONS, promotion_json_data_filepath
        )

        by_id = promotion_catalog.by_id

        for promotion in [1, 2]:
            assert promotion in by_id

        assert by_id[2]["id"] == 2
        assert (
            by_id[2]["name"] == "Purchase 2 tins of soup and get half price off bread"
        )
        assert by_id[2]["active"] is True
        assert by_id[2]["qualifying_product_id"] == 1
        assert by_id[2]["qualifying_product_quantity"] == 2
        assert by_id[2]["discounted_product_id"] == 2
        assert by_id[2]["percent_discount"] == 50
