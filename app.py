import streamlit as st
import pandas as pd
from services.annotation_service
import mock_annotate

st.set_page_config(
    page_title="AI Data Annotation Tool",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ AI-Based Data Annotation Tool")
st.write("Welcome to our LLM-Based Data Annotation Tool!")

# Dataset upload
st.header("Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file,header=None)
        df.columns = ["Text"]
        st.success("Dataset uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# Dashboard
st.header("Dataset Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Datasets", 1 if df is not None else 0)

with col2:
    st.metric("Annotated Data", 0)

with col3:
    st.metric(
        "Pending Data",
        len(df) if df is not None else 0
    )

# Dataset preview
if df is not None:
    st.divider()

    st.subheader("Dataset Preview")

    st.write("Total Rows:", len(df))
    st.write("Total Columns:", len(df.columns))

    st.dataframe(df, width="stretch")

    st.info("Your dataset is ready for annotation!")

    # Manual Annotation
    st.divider()
    st.header("Manual Data Annotation")

    if len(df.columns) == 0:
        st.warning("Your dataset has no columns.")
    else:
        text_column = st.selectbox(
            "Select text column",
            df.columns
        )

        if "annotations" not in st.session_state:
            st.session_state.annotations = {}

        for index, row in df.iterrows():
            st.subheader(f"Record {index + 1}")
            st.write(row[text_column])

            label = st.selectbox(
                "Choose label",
                ["Not Annotated", "Positive", "Negative", "Neutral"],
                key=f"label_{index}"
            )

            if label != "Not Annotated":
                st.session_state.annotations[index] = label
            else:
                st.session_state.annotations.pop(index, None)

        annotated_count = len(st.session_state.annotations)
        pending_count = len(df) - annotated_count

        st.divider()
        st.metric("Annotated Records", annotated_count)
        st.metric("Pending Records", pending_count)

        if st.button("Save Annotations"):
            st.success("Annotations saved successfully!")