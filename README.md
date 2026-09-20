# CatalogOps AI

CatalogOps AI is a human-in-the-loop supplier catalog operations desk.

It helps an operations user review supplier product data, identify catalog
exceptions, draft follow-up messages and track issues toward resolution.

## Problem

Supplier catalogs often contain missing product details, duplicate SKUs,
invalid prices, incomplete stock values and missing supplier contacts. These
issues slow down product listing and require manual checking and follow-up.

## What the app does

- Loads a fictional supplier catalog.
- Accepts supplier CSV uploads.
- Validates required product fields.
- Detects duplicate SKUs.
- Identifies invalid prices and stock values.
- Checks supplier email formats.
- Classifies exceptions by severity.
- Filters issues by severity, type and status.
- Shows an exception review panel.
- Drafts editable supplier follow-up messages.
- Tracks operator notes, status and update time.
- Exports clean catalogs and exception reports.

## AI-assisted workflow

The application uses a human-in-the-loop model:

1. Deterministic rules detect data problems.
2. AI assistance summarises the issue and drafts a message.
3. The operator reviews and edits the draft.
4. The operator chooses a status and adds a note.
5. The operator saves or exports the result.

No messages are sent automatically.

## Current AI mode

The current prototype uses a local fallback AI service. It does not require an
external API key and remains usable when external AI services are unavailable.

## Demo

[Open the live demo] (https://myd65hutt9yzrhalht8ob2.streamlit.app/)

## Screenshots

### Dashboard

![CatalogOps AI dashboard](screenshots/dashboard.png)

### Exception review

![Exception review panel](screenshots/exception-review.png)
![Exception review panel](screenshots/exception-review0.png)
![Exception review panel](screenshots/exception-review-operatornote.png)

### Saved review
![Exception review panel](screenshots/saved-review.png)
### Exports

![Export reports](screenshots/exports.png)
## Technology

- Python
- Streamlit
- Pandas
- Git and GitHub
- Pytest

## Project structure

```text
catalogops-ai/
├── app.py
├── README.md
├── DECISIONS.md
├── pytest.ini
├── requirements.txt
├── data/
│   └── sample_supplier_catalog.csv
├── services/
│   ├── ai_assistant.py
│   ├── data_loader.py
│   ├── exporter.py
│   ├── validation_rules.py
│   └── validator.py
└── tests/
    └── test_validator.py
```

## Data and privacy

The repository uses fictional supplier data only.

Do not upload real customer, supplier, payment or personal information to the
public demo.

## Limitations

- Reviews are stored in Streamlit session state.
- The current AI service uses a local fallback.
- Supplier messages are drafted but never sent.
- The application is a portfolio prototype, not a production operations system.

## What I learned

- Deterministic rules are useful for predictable data-quality checks.
- AI is useful for drafting and explanation.
- Human review is important when outputs may affect suppliers or customers.
- A small complete workflow is more useful than an unfinished complex system.
"""