
import requests
import streamlit as st
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# Page Configuration
st.set_page_config(
    page_title="AI Data Annotation Tool",
    page_icon="🏷️",
    layout="wide"
)

# Application Header
st.title("🏷️ AI-Based Data Annotation Tool")
st.write("Welcome to our LLM-Based Data Annotation Tool!")

# Dynamic Dashboard
st.header("Dataset Dashboard")

try:
    dataset_response = requests.get(
        f"{API_URL}/datasets",
        timeout=60
    )
    dataset_response.raise_for_status()

    datasets = dataset_response.json()["datasets"]

    total_datasets = len(datasets)

    annotated_data = sum(
        item["annotated_records"] for item in datasets
    )

    pending_data = sum(
        item["pending_records"] for item in datasets
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Datasets", total_datasets)

    with col2:
        st.metric("Annotated Data", annotated_data)

    with col3:
        st.metric("Pending Data", pending_data)

except Exception as e:
        st.error(f"Dashboard error: {e}")
    

# Dataset Upload
st.divider()
st.header("Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

df = None

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# Dataset Preview
if df is not None:

    st.divider()
    st.subheader("Dataset Preview")

    st.write("Total Rows:", len(df))
    st.write("Total Columns:", len(df.columns))

    st.dataframe(
        df,
        use_container_width=True
    )

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
                [
                    "Not Annotated",
                    "Positive",
                    "Negative",
                    "Neutral"
                ],
                key=f"label_{index}"
            )

            if label != "Not Annotated":

                st.session_state.annotations[index] = label

            else:

                st.session_state.annotations.pop(
                    index,
                    None
                )

        annotated_count = len(st.session_state.annotations)
        pending_count = len(df) - annotated_count

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Manually Annotated Records", annotated_count)

        with col2:
            st.metric("Pending Records", pending_count)

    # AI Annotation
    st.divider()
    st.header("AI-Based Data Annotation")

    if st.button("Run AI Annotation", type="primary"):

        try:

            with st.spinner("AI is processing your dataset..."):

                response = requests.post(
                    f"{API_URL}/annotate-csv",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "text/csv"
                        )
                    },
                    timeout=120
                )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "AI annotation completed successfully!"
                )

                st.write(
                    "Dataset ID:",
                    result["dataset_id"]
                )

                st.write(
                    "Total Records:",
                    result["total_records"]
                )

                st.subheader("AI Annotation Results")

                results_df = pd.DataFrame(
                    result["results"]
                )

                st.dataframe(
                    results_df,
                    use_container_width=True
                )

            else:

                st.error(
                    f"Annotation failed: {response.text}"
                )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Backend connection error: {e}"
            )

# Dataset History
st.divider()
st.header("Dataset History")

try:

    history_response = requests.get(
        f"{API_URL}/datasets",
        timeout=60
    )

    history_response.raise_for_status()

    history_data = history_response.json()["datasets"]

    if history_data:

        history_df = pd.DataFrame(history_data)

        st.dataframe(
            history_df,
            use_container_width=True
        )

    else:

        st.info("No datasets uploaded yet.")

except requests.exceptions.RequestException:

    st.warning("Dataset history is currently unavailable.")

# Footer
st.divider()
st.caption("AI-Based Data Annotation Tool | Powered by FastAPI, Streamlit, SQLite and DistilBERT")

