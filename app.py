import streamlit as st

from services.data_loader import load_catalog, load_demo_catalog

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

if "catalog" in st.session_state:
    catalog = st.session_state["catalog"]

    st.success(f"Loaded {len(catalog)} product records.")

    st.markdown("### Catalog preview")
    st.dataframe(catalog, use_container_width=True)
else:
    st.markdown(
        """
        Upload a CSV file or click **Load demo catalog** to begin.
        """
    )