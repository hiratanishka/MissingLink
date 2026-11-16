
import streamlit as st
from data_loader import load_data
from data_cleaning import clean_records
from html import escape

st.set_page_config(
    page_title="MissingLink",
    page_icon="🔍",
    layout="wide"
)

if "records" not in st.session_state:
    st.session_state.records = []

if "dataset_name" not in st.session_state:
    st.session_state.dataset_name = ""

st.sidebar.title("MissingLink")
st.sidebar.caption("Missing Person Search System")

page = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "Load Data",
        "Find Person",
        "Add Record",
        "Saved Records",
        "Smart Case Link",
        "Similar Groups",
        "How It Works"
    ]
)

if page == "Home":

    st.title("Welcome to MissingLink")

    st.write(
        "Find similar missing-person records "
        "using simple and efficient DSA algorithms."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
    "Loaded Records",
    len(st.session_state.records)
  )
    col2.metric("Search Results", "Top 10")
    col3.metric("DSA Algorithms", "5")

    st.divider()

    st.subheader("What can you do?")

    left, right = st.columns(2)

    with left:
        st.info(
            "Load Data\n\n"
            "Use your own Excel or CSV dataset."
        )

        st.info(
            "Find Person\n\n"
            "Search for the best possible matches."
        )

    with right:
        st.success(
            "Smart Case Link\n\n"
            "Find possible links between reports."
        )

        st.success(
            "Smart Search Helper\n\n"
            "Find which detail to check next."
        )

    st.warning(
        "MissingLink suggests possible matches. "
        "Human verification is required."
    )



elif page == "Load Data":

    st.title("Load Your Data")

    st.write(
        "Upload your own missing-person records."
    )

    st.info(
        "Your data stays on your computer "
        "when you run MissingLink locally."
    )

    uploaded_file = st.file_uploader(
        "Choose Excel or CSV file",
        type=["xlsx", "csv"]
    )

    st.subheader("Required Columns")

    st.write(
        "Case ID, Age, Gender, Missing Location, "
        "Missing Since, Description"
    )

    if uploaded_file is not None:

        st.write("Selected file:", uploaded_file.name)

        if st.button("Load Records"):

            try:

                uploaded_file.seek(0)

                raw_records = load_data(
                    uploaded_file,
                    uploaded_file.name
                )

                records = clean_records(raw_records)

                st.session_state.records = records

                st.session_state.dataset_name = (
                    uploaded_file.name
                )

                st.success(
                    f"{len(records)} records loaded successfully!"
                )

            except Exception as error:

                st.error(str(error))

    if st.session_state.records:

        st.subheader("Current Dataset")

        st.write(
            "File:",
            st.session_state.dataset_name
        )

        st.metric(
            "Total Records",
            len(st.session_state.records)
        )


    st.title("Load Your Data")

    st.write(
        "Upload your own missing-person records "
        "to start searching."
    )

    st.info(
        "Your data is processed locally when "
        "MissingLink runs on your computer."
    )

    uploaded_file = st.file_uploader(
        "Choose your dataset",
        type=["csv", "xlsx"]
    )

    st.subheader("Required Columns")

    st.write(
        "Case ID, Age, Gender, Missing Location, "
        "Missing Since, Description"
    )

    if uploaded_file is not None:

        st.success(
            f"Selected file: {uploaded_file.name}"
        )

        st.caption(
            "Data loading will be connected after "
            "the data module is merged."
        )


elif page == "Find Person":
    st.title("Find Person")

elif page == "Add Record":
    st.title("Add Record")


elif page == "Saved Records":

    st.title("Saved Records")

    records = st.session_state.records

    if not records:

        st.info(
            "Please load a dataset first."
        )

    else:

        st.metric("Total Records", len(records))

        columns = [
            "Case ID",
            "Age",
            "Gender",
            "Missing Location",
            "Missing Since",
            "Description"
        ]

        page_size = 20

        total_pages = (
            len(records) + page_size - 1
        ) // page_size

        page_number = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            step=1
        )

        start = (page_number - 1) * page_size

        visible_records = records[
            start:start + page_size
        ]

        table = "<table><thead><tr>"

        for column in columns:
            table += f"<th>{escape(column)}</th>"

        table += "</tr></thead><tbody>"

        for record in visible_records:

            table += "<tr>"

            for column in columns:

                value = record.get(column)

                if value is None:
                    value = ""

                table += (
                    f"<td>{escape(str(value))}</td>"
                )

            table += "</tr>"

        table += "</tbody></table>"

        st.markdown(
            table,
            unsafe_allow_html=True
        )


elif page == "Smart Case Link":
    st.title("Smart Case Link")

elif page == "Similar Groups":
    st.title("Similar Groups")

elif page == "How It Works":
    st.title("How It Works")
