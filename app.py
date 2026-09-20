from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from services.data_loader import load_catalog, load_demo_catalog
from services.exporter import dataframe_to_csv_bytes
from services.validator import validate_catalog


st.set_page_config(
    page_title="CatalogOps AI",
    page_icon="📦",
    layout="wide",
)

STATUS_OPTIONS = [
    "Open",
    "Needs supplier clarification",
    "Contacted",
    "Resolved",
    "Blocked",
]


def load_new_catalog(catalog: pd.DataFrame) -> None:
    """Start a new catalog review session."""
    st.session_state["catalog"] = catalog
    st.session_state["exceptions"] = validate_catalog(catalog)


def save_exception_review(
    exception: dict,
    message: str,
    status: str,
    note: str,
) -> None:
    """Save review values to one exception."""
    exception["supplier_message"] = message
    exception["status"] = status
    exception["notes"] = note
    exception["reviewed"] = True
    exception["updated_at"] = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")


st.title("CatalogOps AI")
st.subheader("Supplier Catalog Exception Desk")

st.write(
    "Upload a supplier catalog, review data exceptions, "
    "and help close operational issues."
)

st.info(
    "Prototype mode: this application uses fictional demo data "
    "and does not contact real suppliers."
)

st.markdown("### Load a catalog")

load_columns = st.columns(2)

with load_columns[0]:
    uploaded_file = st.file_uploader(
        "Upload supplier CSV",
        type=["csv"],
    )

with load_columns[1]:
    if st.button("Load demo catalog"):
        load_new_catalog(load_demo_catalog())
        st.session_state["loaded_source"] = "demo"

if uploaded_file is not None:
    uploaded_name = uploaded_file.name

    if (
        st.session_state.get("loaded_source")
        != f"upload:{uploaded_name}"
    ):
        load_new_catalog(load_catalog(uploaded_file))
        st.session_state["loaded_source"] = (
            f"upload:{uploaded_name}"
        )

if "catalog" not in st.session_state:
    st.markdown(
        "Upload a CSV file or click **Load demo catalog** to begin."
    )
    st.stop()

catalog = st.session_state["catalog"]
exceptions = st.session_state["exceptions"]

st.success(f"Loaded {len(catalog)} product records.")

status_counts = pd.Series(
    [
        issue.get("status", "Open")
        for issue in exceptions
    ],
    dtype="object",
).value_counts()

metrics = st.columns(5)

with metrics[0]:
    st.metric("Products", len(catalog))

with metrics[1]:
    st.metric("Exceptions", len(exceptions))

with metrics[2]:
    st.metric(
        "High priority",
        sum(
            issue.get("severity") == "high"
            for issue in exceptions
        ),
    )

with metrics[3]:
    st.metric(
        "Reviewed",
        sum(
            issue.get("reviewed", False)
            for issue in exceptions
        ),
    )

with metrics[4]:
    st.metric(
        "Resolved",
        status_counts.get("Resolved", 0),
    )

st.markdown("### Catalog preview")
st.dataframe(catalog, use_container_width=True)

st.markdown("### Exception review")

if not exceptions:
    st.success("No catalog exceptions found.")
    st.stop()

exceptions_df = pd.DataFrame(exceptions)

filter_columns = st.columns(3)

with filter_columns[0]:
    severity_options = ["All"] + sorted(
        exceptions_df["severity"].unique().tolist()
    )
    selected_severity = st.selectbox(
        "Filter by severity",
        severity_options,
    )

with filter_columns[1]:
    issue_options = ["All"] + sorted(
        exceptions_df["issue_type"].unique().tolist()
    )
    selected_issue_type = st.selectbox(
        "Filter by issue type",
        issue_options,
    )

with filter_columns[2]:
    selected_status = st.selectbox(
        "Filter by status",
        ["All"] + STATUS_OPTIONS,
    )

filtered = exceptions_df.copy()

if selected_severity != "All":
    filtered = filtered[
        filtered["severity"] == selected_severity
    ]

if selected_issue_type != "All":
    filtered = filtered[
        filtered["issue_type"] == selected_issue_type
    ]

if selected_status != "All":
    filtered = filtered[
        filtered["status"] == selected_status
    ]

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)

if filtered.empty:
    st.warning("No exceptions match the selected filters.")
    st.stop()

selected_index = st.selectbox(
    "Select an exception to review",
    filtered.index.tolist(),
    format_func=lambda index: (
        f"{exceptions[index]['sku']} — "
        f"{exceptions[index]['issue_type']}"
    ),
)

selected_exception = exceptions[selected_index]

left, right = st.columns(2)

with left:
    st.markdown("#### Exception details")
    st.write(f"**SKU:** {selected_exception['sku']}")
    st.write(f"**Issue:** {selected_exception['issue_type']}")
    st.write(f"**Severity:** {selected_exception['severity']}")
    st.write(
        f"**Description:** "
        f"{selected_exception['issue_description']}"
    )
    st.write(
        f"**Suggested action:** "
        f"{selected_exception['suggested_action']}"
    )

with right:
    st.markdown("#### Operator review")

    default_message = (
        f"Subject: Clarification needed for "
        f"{selected_exception['sku']}\n\n"
        "Hello,\n\n"
        f"We are reviewing the catalog record for "
        f"{selected_exception['sku']}. "
        f"{selected_exception['issue_description']} "
        "Please confirm the correct information so we can "
        "complete the catalog record.\n\n"
        "Kind regards,\n"
        "Catalog Operations"
    )

    message = st.text_area(
        "Supplier follow-up draft",
        value=selected_exception.get(
            "supplier_message",
            default_message,
        ),
        key=f"message_{selected_index}",
        height=220,
    )

    current_status = selected_exception.get("status", "Open")

    status = st.selectbox(
        "Status",
        STATUS_OPTIONS,
        index=(
            STATUS_OPTIONS.index(current_status)
            if current_status in STATUS_OPTIONS
            else 0
        ),
        key=f"status_{selected_index}",
    )

    note = st.text_area(
        "Operator note",
        value=selected_exception.get("notes", ""),
        key=f"note_{selected_index}",
        height=120,
    )

    if st.button(
        "Save review",
        type="primary",
        key=f"save_{selected_index}",
    ):
        save_exception_review(
            selected_exception,
            message,
            status,
            note,
        )

        st.session_state["exceptions"] = exceptions
        st.session_state["last_saved_index"] = selected_index

        st.success(
            f"Review saved for {selected_exception['sku']}."
        )

st.markdown("### Saved review status")

reviewed = [
    issue
    for issue in exceptions
    if issue.get("reviewed", False)
]

summary = st.columns(4)

with summary[0]:
    st.metric("Reviewed exceptions", len(reviewed))

with summary[1]:
    st.metric("Open", status_counts.get("Open", 0))

with summary[2]:
    st.metric("Contacted", status_counts.get("Contacted", 0))

with summary[3]:
    st.metric("Blocked", status_counts.get("Blocked", 0))

if reviewed:
    reviewed_df = pd.DataFrame(
        [
            {
                "sku": issue["sku"],
                "issue_type": issue["issue_type"],
                "severity": issue["severity"],
                "status": issue.get("status", "Open"),
                "operator_note": issue.get("notes", ""),
                "updated_at": issue.get("updated_at", ""),
            }
            for issue in reviewed
        ]
    )

    st.dataframe(
        reviewed_df,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No saved reviews yet.")

st.markdown("### Export reports")

affected_skus = {
    issue["sku"]
    for issue in exceptions
    if issue["sku"] != "N/A"
}

clean_catalog = catalog.copy()

if "sku" in clean_catalog.columns:
    clean_catalog = clean_catalog[
        ~clean_catalog["sku"].astype(str).isin(affected_skus)
    ]

exceptions_report = pd.DataFrame(exceptions)

reviewed_report = pd.DataFrame(
    [
        {
            "sku": issue["sku"],
            "issue_type": issue["issue_type"],
            "severity": issue["severity"],
            "status": issue.get("status", "Open"),
            "supplier_message": issue.get(
                "supplier_message",
                "",
            ),
            "operator_note": issue.get("notes", ""),
            "updated_at": issue.get("updated_at", ""),
        }
        for issue in reviewed
    ]
)

export_columns = st.columns(3)

with export_columns[0]:
    st.download_button(
        "Download clean catalog",
        data=dataframe_to_csv_bytes(clean_catalog),
        file_name="clean_catalog.csv",
        mime="text/csv",
    )

with export_columns[1]:
    st.download_button(
        "Download exception report",
        data=dataframe_to_csv_bytes(exceptions_report),
        file_name="exception_report.csv",
        mime="text/csv",
    )

with export_columns[2]:
    st.download_button(
        "Download reviewed exceptions",
        data=dataframe_to_csv_bytes(reviewed_report),
        file_name="reviewed_exceptions.csv",
        mime="text/csv",
    )