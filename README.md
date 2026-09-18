# CatalogOps AI

CatalogOps AI is a small AI-assisted operations prototype for reviewing supplier
catalogs, identifying data problems and helping an operator close exceptions.

## Problem

Supplier catalog files can contain missing product details, duplicate SKUs,
invalid prices, incomplete supplier contacts and other issues. These problems
slow down product listings and require manual follow-up.

## Solution

CatalogOps AI allows an operator to:

1. Upload a supplier CSV file.
2. Validate product records.
3. Identify and classify catalog exceptions.
4. Review the issue and suggested action.
5. Draft an editable supplier follow-up message.
6. Track the issue status.
7. Export a clean catalog and exception report.

## Intended user

A supplier or catalog operations specialist who needs to review product data
quickly and follow up on missing information.

## Project type

Portfolio prototype using fictional supplier data. It is not a production
e-commerce system and does not send real supplier emails or process real
payments.

## Main design principle

Automation should reduce repetitive work while keeping a human responsible for
reviewing and closing each exception.

## Version-one scope

### Included

- Uploading a supplier CSV.
- Loading sample demo data.
- Checking required catalog fields.
- Detecting duplicate SKUs.
- Detecting missing product names.
- Detecting missing categories.
- Detecting invalid or missing prices.
- Detecting invalid stock values.
- Detecting missing supplier emails.
- Assigning issue severity.
- Showing an exception table.
- Drafting editable supplier follow-up messages.
- Updating exception status.
- Exporting a clean catalog.
- Exporting an exception report.

### Not included

- User accounts or authentication.
- Real supplier emails.
- Real payment processing.
- Real supplier data.
- Automatic purchasing.
- Fully autonomous AI agents.
- Complex machine-learning model training.
- Multi-user collaboration.
- Production-grade security or scaling.
