import re

import pandas as pd

from services.validation_rules import REQUIRED_COLUMNS


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_columns(catalog: pd.DataFrame) -> list[str]:
    """Return required columns missing from the catalog."""
    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in catalog.columns
    ]


def validate_catalog(catalog: pd.DataFrame) -> list[dict]:
    """Return one exception record for each catalog problem."""
    exceptions = []

    missing_columns = validate_columns(catalog)

    if missing_columns:
        return [
            {
                "sku": "N/A",
                "issue_type": "Missing columns",
                "severity": "high",
                "issue_description": (
                    "The catalog is missing required columns: "
                    + ", ".join(missing_columns)
                ),
                "suggested_action": "Ask the supplier to provide the missing columns.",
                "status": "Open",
            }
        ]

    duplicate_skus = (
        catalog["sku"]
        .astype(str)
        .str.strip()
        .value_counts()
    )

    duplicate_skus = set(
        duplicate_skus[duplicate_skus > 1].index
    )

    for index, row in catalog.iterrows():
        sku = str(row.get("sku", "")).strip()
        name = str(row.get("name", "")).strip()
        category = str(row.get("category", "")).strip()
        supplier_email = str(row.get("supplier_email", "")).strip()

        price = pd.to_numeric(row.get("price"), errors="coerce")
        stock = pd.to_numeric(row.get("stock"), errors="coerce")

        if not sku or sku.lower() == "nan":
            exceptions.append(
                {
                    "sku": "N/A",
                    "issue_type": "Missing SKU",
                    "severity": "high",
                    "issue_description": "The product does not have a SKU.",
                    "suggested_action": "Ask the supplier to provide a unique SKU.",
                    "status": "Open",
                }
            )
            continue

        if sku in duplicate_skus:
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Duplicate SKU",
                    "severity": "high",
                    "issue_description": "This SKU appears more than once.",
                    "suggested_action": "Ask the supplier to confirm the correct SKU.",
                    "status": "Open",
                }
            )

        if not name or name.lower() == "nan":
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Missing product name",
                    "severity": "medium",
                    "issue_description": "The product name is missing.",
                    "suggested_action": "Ask the supplier to provide the product name.",
                    "status": "Open",
                }
            )

        if not category or category.lower() == "nan":
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Missing category",
                    "severity": "medium",
                    "issue_description": "The product category is missing.",
                    "suggested_action": "Ask the supplier to confirm the product category.",
                    "status": "Open",
                }
            )

        if pd.isna(price):
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Invalid price",
                    "severity": "high",
                    "issue_description": "The price is missing or is not a number.",
                    "suggested_action": "Ask the supplier to confirm the price and currency.",
                    "status": "Open",
                }
            )
        elif price <= 0:
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Invalid price",
                    "severity": "high",
                    "issue_description": "The price must be greater than zero.",
                    "suggested_action": "Ask the supplier to provide a valid positive price.",
                    "status": "Open",
                }
            )

        if pd.isna(stock):
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Invalid stock",
                    "severity": "medium",
                    "issue_description": "The stock value is missing or invalid.",
                    "suggested_action": "Ask the supplier to confirm the stock quantity.",
                    "status": "Open",
                }
            )
        elif stock < 0:
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Invalid stock",
                    "severity": "medium",
                    "issue_description": "Stock cannot be negative.",
                    "suggested_action": "Ask the supplier to confirm the stock quantity.",
                    "status": "Open",
                }
            )

        if not supplier_email or supplier_email.lower() == "nan":
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Missing supplier email",
                    "severity": "high",
                    "issue_description": "The supplier email is missing.",
                    "suggested_action": "Ask the supplier to provide a contact email.",
                    "status": "Open",
                }
            )
        elif not EMAIL_PATTERN.match(supplier_email):
            exceptions.append(
                {
                    "sku": sku,
                    "issue_type": "Invalid supplier email",
                    "severity": "high",
                    "issue_description": "The supplier email format is invalid.",
                    "suggested_action": "Ask the supplier to confirm a valid email address.",
                    "status": "Open",
                }
            )

    return exceptions