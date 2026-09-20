def draft_supplier_message(exception: dict) -> str:
    sku = exception.get("sku", "the product")
    description = exception.get(
        "issue_description",
        "The catalog record needs clarification.",
    )

    return (
        f"Subject: Clarification needed for {sku}\n\n"
        "Hello,\n\n"
        f"We are reviewing the catalog record for {sku}. "
        f"{description} "
        "Please confirm the correct information so we can "
        "complete the catalog record.\n\n"
        "Kind regards,\n"
        "Catalog Operations"
    )


def summarize_exception(exception: dict) -> str:
    issue_type = exception.get("issue_type", "Catalog issue")
    severity = exception.get("severity", "unknown")
    action = exception.get("suggested_action", "Review the record.")

    return (
        f"{issue_type} ({severity} priority). "
        f"Recommended action: {action}"
    )


def get_ai_mode() -> str:
    """Return the AI mode currently used by the application."""
    return "Fallback mode"
