
import streamlit as st

st.set_page_config(
    page_title="MissingLink",
    page_icon="🔍",
    layout="wide"
)

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

    col1.metric("Saved Records", "0")
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

elif page == "Smart Case Link":
    st.title("Smart Case Link")

elif page == "Similar Groups":
    st.title("Similar Groups")

elif page == "How It Works":
    st.title("How It Works")
