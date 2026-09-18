# Project Decisions

## Decision 1: Build an internal operations tool

I chose an internal supplier catalog exception desk instead of a complete
e-commerce platform because it is possible to demonstrate the full workflow
within a short build period.

## Decision 2: Use Streamlit for version one

Streamlit allows me to focus on the workflow and data handling instead of
spending most of the build time on frontend setup.

## Decision 3: Start with deterministic validation

Basic catalog checks such as missing fields, duplicate SKUs and invalid prices
should be predictable. AI assistance will be added only for tasks where language
generation or summarisation is useful.

## Decision 4: Keep a human in the loop

The tool will suggest actions and draft messages, but the operator must review
the result before marking an issue as resolved.