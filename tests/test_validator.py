from services.data_loader import load_demo_catalog
from services.validator import validate_catalog


def test_demo_catalog_has_exceptions():
    catalog = load_demo_catalog()
    issues = validate_catalog(catalog)
    assert len(issues) == 9


def test_clean_catalog_has_no_exceptions():
    import pandas as pd

    catalog = pd.DataFrame([
        {
            "sku": "TEST-001",
            "name": "Sample Product",
            "category": "Tools",
            "price": 10.00,
            "currency": "EUR",
            "stock": 5,
            "supplier_email": "supplier@example.com",
        }
    ])

    assert validate_catalog(catalog) == []
