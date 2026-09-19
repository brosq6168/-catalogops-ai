import pandas as pd
import streamlit as st

from services.data_loader import load_catalog, load_demo_catalog
from services.validator import validate_catalog


st.set_page_config(
    page_title="CatalogOps AI",
    page_icon="📦",
    layout="wide",
)

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

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload supplier CSV",
        type=["csv"],
    )

with col2:
    if st.button("Load demo catalog"):
        st.session_state["catalog"] = load_demo_catalog()

if uploaded_file is not None:
    st.session_state["catalog"] = load_catalog(uploaded_file)

if "catalog" not in st.session_state:
    st.markdown(
        "Upload a CSV file or click **Load demo catalog** to begin."
    )
    st.stop()

catalog = st.session_state["catalog"]
exceptions = validate_catalog(catalog)

st.success(f"Loaded {len(catalog)} product records.")

metric_columns = st.columns(4)

with metric_columns[0]:
    st.metric("Products", len(catalog))

with metric_columns[1]:
    st.metric("Exceptions", len(exceptions))

with metric_columns[2]:
    high_priority = sum(
        issue["severity"] == "high"
        for issue in exceptions
    )
    st.metric("High priority", high_priority)

with metric_columns[3]:
    st.metric(
        "Products without issues",
        max(len(catalog) - len(set(issue["sku"] for issue in exceptions)), 0),
    )

st.markdown("### Catalog preview")
st.dataframe(catalog, use_container_width=True)

st.markdown("### Detected exceptions")

if exceptions:
    exceptions_df = pd.DataFrame(exceptions)
    st.dataframe(exceptions_df, use_container_width=True)
else:
    st.success("No catalog exceptions found.")