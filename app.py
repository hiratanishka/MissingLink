
import streamlit as st
from search_helper import suggest_next_detail
from data_loader import load_data
from data_cleaning import clean_records
from html import escape
from datetime import date
from search import make_location_index, find_by_location, linear_search
from match_score import calculate_score
from data_cleaning import clean_text
from check_differences import check_differences
from storage_service import save_local_dataset, open_local_dataset
from group_service import find_possible_groups

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

    records = st.session_state.records

    if not records:
        st.warning("Please load your dataset first.")

    else:
        st.write("Enter details to find possible matches.")

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=None,
            placeholder="Enter age"
        )

        gender = st.selectbox(
            "Gender",
            ["Unknown", "Male", "Female", "Other"]
        )

        location = st.text_input(
            "Missing Location"
        )

        missing_date = st.date_input(
            "Missing Since",
            value=None,
            max_value=date.today()
        )

        description = st.text_area(
            "Description",
            placeholder="Clothes, height, appearance..."
        )

        search_type = st.radio(
            "Search Type",
            ["All Records", "Same Location"]
        )

        min_score = st.slider(
            "Minimum Match Score",
            min_value=0,
            max_value=100,
            value=40
        )

        if st.button("Find Matches", type="primary"):

            person = {
                "Age": age,
                "Gender": (
                    "" if gender == "Unknown"
                    else gender.lower()
                ),
                "Missing Location": clean_text(location),
                "Missing Since": missing_date,
                "Description": clean_text(description)
            }

            suggestion = suggest_next_detail(
                person,
                records
            )

            st.session_state.search_suggestion = suggestion


            if not any([
                person["Age"] is not None,
                person["Gender"],
                person["Missing Location"],
                person["Missing Since"] is not None,
                person["Description"]
            ]):
                st.warning("Enter at least one detail.")

            else:
                if search_type == "Same Location":

                    if not person["Missing Location"]:
                        st.warning(
                            "Enter a location for Same Location search."
                        )
                        candidates = []

                    else:
                        index = make_location_index(records)

                        candidates = find_by_location(
                            index,
                            person["Missing Location"]
                        )

                else:
                    candidates = records

                results = linear_search(
                    candidates,
                    person,
                    calculate_score,
                    min_score
                )

                results.sort(
                    key=lambda item: item["score"],
                    reverse=True
                )

                st.session_state.search_results = results
        
        if "search_suggestion" in st.session_state:

            st.info(
                "Smart Search Helper: "
                + st.session_state.search_suggestion
            )

        if "search_results" in st.session_state:

            results = st.session_state.search_results

            st.subheader("Search Results")

            st.write(
                f"{len(results)} possible matching records found."
            )

            for item in results[:10]:

                record = item["record"]
                score = item["score"]

                with st.container(border=True):

                    st.subheader(
                        f"Case: {record.get('Case ID', 'Unknown')}"
                    )

                    st.metric("Match Score", f"{score}%")

                    st.write(
                        "Age:",
                        record.get("Age", "Unknown")
                    )

                    st.write(
                        "Gender:",
                        record.get("Gender", "Unknown")
                    )

                    st.write(
                        "Location:",
                        record.get("Missing Location", "Unknown")
                    )

                    st.write(
                        "Description:",
                        record.get("Description", "")
                    )

                    warnings = check_differences(
                        person,
                        record
                    )

                    if warnings:
                        st.warning(", ".join(warnings))

            st.caption(
                "These are possible matches, not confirmed identities."
            )


elif page == "Add Record":

    st.title("Add New Record")

    with st.form("add_record_form"):

        case_id = st.text_input("Case ID")
        age = st.number_input("Age", 0, 120, value=None)
        gender = st.selectbox(
            "Gender", ["Unknown", "Male", "Female", "Other"]
        )
        location = st.text_input("Missing Location")
        missing_date = st.date_input(
            "Missing Since", value=None
        )
        description = st.text_area("Description")

        submitted = st.form_submit_button("Add Record")

    if submitted:

        case_id = case_id.strip()

        existing_ids = {
            str(r.get("Case ID", "")).strip().lower()
            for r in st.session_state.records
        }

        if not case_id:
            st.error("Case ID is required.")

        elif case_id.lower() in existing_ids:
            st.error("Case ID already exists.")

        elif not location.strip():
            st.error("Missing Location is required.")

        else:
            new_record = {
                "Case ID": case_id,
                "Age": age,
                "Gender": "" if gender == "Unknown" else gender,
                "Missing Location": location,
                "Missing Since": missing_date,
                "Description": description
            }

            cleaned = clean_records([new_record])[0]
            st.session_state.records.append(cleaned)
            st.session_state.pop("search_results", None)

            st.success(f"Record {case_id} added successfully!")

    st.metric("Total Records", len(st.session_state.records))


elif page == "Saved Records":

    st.title("Saved Records")


    st.subheader("Local Storage")

    st.caption(
        "Save a working copy on this computer. "
        "Your original uploaded file is not overwritten."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Working Copy"):

            if not st.session_state.records:
                st.warning("No records available to save.")

            else:
                try:
                    path = save_local_dataset(
                        st.session_state.records
                    )
                    st.success(f"Saved to {path}")

                except Exception as error:
                    st.error(str(error))

    with col2:
        if st.button("Load Saved Copy"):

            try:
                records = open_local_dataset()

                if records:
                    st.session_state.records = records
                    st.session_state.dataset_name = "local_records.csv"
                    st.session_state.pop("search_results", None)
                    st.success(
                        f"{len(records)} saved records loaded."
                    )
                    st.rerun()

                else:
                    st.info("No saved records found.")

            except Exception as error:
                st.error(str(error))

    st.divider()


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

    st.write(
        "Find groups of records that may be related."
    )

    records = st.session_state.records

    if not records:
        st.warning("Please load records first.")

    else:
        min_score = st.slider(
            "Minimum Group Score",
            min_value=0,
            max_value=100,
            value=70
        )

        if st.button("Find Similar Groups"):

            with st.spinner("Checking possible groups..."):

                groups = find_possible_groups(
                    records,
                    min_score=min_score
                )

            st.session_state.similar_groups = groups

        if "similar_groups" in st.session_state:

            groups = st.session_state.similar_groups

            st.metric(
                "Possible Groups Found",
                len(groups)
            )

            if not groups:
                st.info("No possible groups found.")

            for group_number, group in enumerate(
                groups,
                start=1
            ):

                with st.expander(
                    f"Group {group_number} - {len(group)} records"
                ):

                    for record in group:

                        st.write(
                            "**Case ID:**",
                            record.get("Case ID", "")
                        )

                        st.write(
                            "**Age:**",
                            record.get("Age", "")
                        )

                        st.write(
                            "**Location:**",
                            record.get("Missing Location", "")
                        )

                        st.write(
                            "**Description:**",
                            record.get("Description", "")
                        )

                        st.divider()

            st.caption(
                "These are possible related groups, "
                "not confirmed matches. "
                "Human verification is required."
            )


elif page == "How It Works":
    st.title("How It Works")
