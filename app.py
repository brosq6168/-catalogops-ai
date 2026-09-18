import streamlit as st

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

st.markdown("### What this prototype will do")

st.write(
    """
    - Upload supplier catalog files
    - Detect missing or inconsistent product data
    - Classify exceptions by severity
    - Draft supplier follow-up messages
    - Track issue status
    - Export reports
    """
)