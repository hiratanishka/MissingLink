
import streamlit as st

from smart_case_link import find_case_links


def show_smart_case_page(records):

    st.title("Smart Case Link")

    st.write(
        "Find possible links between reports "
        "from different locations."
    )

    if not records:
        st.warning("Please load records first.")
        return

    case_options = {
        f"{i + 1}: {r.get('Case ID', 'Unknown')}": i
        for i, r in enumerate(records)
    }

    selected = st.selectbox(
        "Choose a record",
        list(case_options.keys())
    )

    min_score = st.slider(
        "Minimum Link Score",
        0,
        100,
        55
    )

    if st.button("Find Possible Links"):

        index = case_options[selected]
        person = records[index]

        candidates = [
            record
            for i, record in enumerate(records)
            if i != index
        ]

        links = find_case_links(
            person,
            candidates,
            min_score=min_score
        )

        st.metric("Possible Links", len(links))

        if not links:
            st.info("No possible cross-location links found.")

        for item in links[:10]:

            record = item["record"]

            with st.container(border=True):

                st.subheader(
                    f"Case {record.get('Case ID', 'Unknown')}"
                )

                st.write(
                    "Location:",
                    record.get("Missing Location", "")
                )

                st.write(
                    "Age:",
                    record.get("Age", "")
                )

                st.write(
                    "Description:",
                    record.get("Description", "")
                )

                st.write(
                    "Similarity Score:",
                    item["score"]
                )

    st.caption(
        "Possible links require human verification. "
        "A similarity score is not an identity probability."
    )
