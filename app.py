import streamlit as st
from collections import Counter
from html import escape
from datetime import datetime
from fast_results import top_matches
from merge_sort import merge_sort
from smart_case_page import show_smart_case_page
from search_helper import suggest_next_detail
from data_loader import load_data
from data_cleaning import clean_records
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


st.markdown(
    """
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
      background: #0b1020 !important; color: #edf3ff;
    }
    [data-testid="stHeader"] { border-bottom: 1px solid #1d2842 !important; }
    [data-testid="stToolbar"] { background: transparent !important; }
    .block-container { max-width: 1360px; padding-top: 1.6rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] { background: #10182b; border-right: 1px solid #26324d; }
    [data-testid="stSidebar"] h1 { font-size: 1.7rem; letter-spacing: -.04em; }
    [data-testid="stSidebar"] label { color: #c1cde4; }
    h1,h2,h3 { color: #f7f9ff !important; letter-spacing: -.025em; }
    .stButton button { border-radius: 12px; min-height: 42px; font-weight: 650; }
    .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
      color: white !important; border: 0 !important;
      background: linear-gradient(105deg,#2563eb,#7c3aed) !important;
    }
    div[data-testid="stMetric"] { border: 1px solid #273551; background: #17233c;
      border-radius: 16px; padding: 17px; }
    div[data-testid="stMetricValue"] { color: #b9adff; }
    div[data-testid="stForm"] { background: #121e33; border-radius: 18px;
      border: 1px solid #263552; padding: 18px; }
    div[data-testid="stAlert"] { border-radius: 13px; }
    .ml-topbar { display:flex; align-items:center; justify-content:space-between;
      gap:12px; margin-bottom:22px; }
    .ml-brand { display:flex; align-items:center; gap:13px; }
    .ml-brand-icon { width:52px; height:52px; display:flex; align-items:center;
      justify-content:center; border-radius:15px; border:1px solid #2563eb66;
      background:linear-gradient(135deg,#123a6b,#1b2750); font-size:25px; }
    .ml-brand h1 { margin:0 !important; font-size:32px !important; line-height:1.13; }
    .ml-sub { color:#95a4bf; font-size:13px; margin-top:4px; }
    .ml-chip { border:1px solid #185b58; background:#0c3638;
      color:#6ee7ba; padding:8px 12px; border-radius:12px;
      font-size:12px; font-weight:700; white-space:nowrap; }
    .ml-tabs { display:flex; gap:9px; margin: 0 0 23px; flex-wrap:wrap; }
    .ml-tag { border:1px solid #29334a; background:#141c2d; padding:8px 14px;
      color:#b9c6da; border-radius:11px; font-size:12px; font-weight:650; }
    .ml-tag-on { background:#152e58; border-color:#29599c; color:#b9d7ff; }
    .ml-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr));
      gap:13px; margin:8px 0 24px; }
    .ml-kpi { min-height:145px; border-radius:16px; padding:20px;
      border:1px solid #ffffff12; position:relative; overflow:hidden; }
    .ml-kpi-icon { display:inline-flex; align-items:center; justify-content:center;
      width:38px; height:38px; border-radius:10px;
      background:#00000035; font-size:20px; margin-bottom:13px; }
    .ml-kpi-name { color:#bdc9df; font-size:13px; margin-bottom:5px; }
    .ml-kpi-value { color:#fff; font-weight:780; font-size:29px;
      letter-spacing:-.04em; line-height:1.1; }
    .ml-kpi-extra { position:absolute; right:17px; top:17px; color:#75ddbd;
      background:#053b3b75; font-size:11px; padding:5px 8px;
      border-radius:8px; font-weight:650; }
    .ml-kpi-a {background:linear-gradient(120deg,#112744,#0b3454);}
    .ml-kpi-b {background:linear-gradient(120deg,#0c3036,#0d4140);}
    .ml-kpi-c {background:linear-gradient(120deg,#252047,#34245c);}
    .ml-kpi-d {background:linear-gradient(120deg,#38271e,#48291e);}
    .ml-kpi-e {background:linear-gradient(120deg,#382034,#4c2349);}
    .ml-kpi-f {background:linear-gradient(120deg,#1a284b,#213a67);}
    .ml-panel { border:1px solid #27314c; background:linear-gradient(128deg,#141b2c,#121a30);
      border-radius:18px; padding:24px; margin:12px 0 22px; }
    .ml-panel-title { font-size:18px; font-weight:750; color:#f2f6ff;
      margin:0 0 5px; }
    .ml-panel-sub { color:#9daac2; font-size:12px; margin-bottom:16px; }
    .ml-chart-svg { display:block; width:100%; height:auto; }
    .ml-row { display:flex; align-items:center; gap:12px; margin:12px 0; }
    .ml-loc-label { width:135px; flex-shrink:0; color:#d0ddf4;
      font-size:12px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .ml-track { flex:1; background:#28314a; height:11px; border-radius:30px; overflow:hidden; }
    .ml-fill { height:100%; border-radius:30px;
      background:linear-gradient(90deg,#2286ff,#34d8c4); }
    .ml-loc-count { width:55px; text-align:right; color:#f6f7ff;
      font-size:12px; font-weight:700; }
    .ml-note { padding:12px 16px; border:1px solid #324663;
      background:#14243a; border-radius:12px; font-size:12px; color:#b0c5df; }
    .ml-empty { color:#a8b7d1; padding:44px 12px; text-align:center; font-size:14px; }
    @media (max-width:800px) {
      .ml-grid {grid-template-columns:repeat(2,minmax(0,1fr));}
      .ml-kpi {min-height:130px;padding:15px;}
      .ml-kpi-value {font-size:24px;}
      .ml-brand h1 {font-size:25px !important;}
      .ml-panel {padding:15px;}
    }
    @media (max-width:480px) {
      .ml-grid {grid-template-columns:1fr;}
      .ml-topbar {align-items:flex-start;}
      .ml-chip {font-size:10px;}
    }
    </style>
    """,
    unsafe_allow_html=True
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
    records = st.session_state.records
    total = len(records)
    locations = Counter(
        str(record.get("Missing Location") or "").strip().title()
        for record in records
        if str(record.get("Missing Location") or "").strip()
    )
    complete_records = sum(
        all(record.get(k) is not None and str(record.get(k)).strip()
            for k in ("Age", "Gender", "Missing Location", "Missing Since", "Description"))
        for record in records
    )
    known_age = sum(record.get("Age") is not None for record in records)
    dated = sum(record.get("Missing Since") is not None for record in records)
    source_name = escape(st.session_state.dataset_name or "No dataset loaded")
    cards = [
        ("📁", "Total Records", f"{total:,}", "a", "Dataset size"),
        ("📍", "Locations Found", f"{len(locations):,}", "b", "Distinct places"),
        ("⚙️", "DSA Algorithms", "5", "c", "Implemented"),
        ("🪪", "Known Ages", f"{known_age:,}", "d", "Age available"),
        ("✅", "Complete Records", f"{complete_records:,}", "e", "Five fields filled"),
        ("📅", "Known Missing Dates", f"{dated:,}", "f", "Dates available"),
    ]
    cards_html = "".join(
        f'<div class="ml-kpi ml-kpi-{tone}">'
        f'<span class="ml-kpi-extra">{escape(extra)}</span>'
        f'<div class="ml-kpi-icon">{icon}</div>'
        f'<div class="ml-kpi-name">{escape(name)}</div>'
        f'<div class="ml-kpi-value">{escape(value)}</div></div>'
        for icon, name, value, tone, extra in cards
    )
    st.markdown(
        '<div class="ml-topbar"><div class="ml-brand">'
        '<div class="ml-brand-icon">🔎</div><div><h1>MissingLink Dashboard</h1>'
        '<div class="ml-sub">Case insights, data quality &amp; record discovery</div>'
        '</div></div><div class="ml-chip">✦ DSA-Powered</div></div>'
        '<div class="ml-tabs"><span class="ml-tag ml-tag-on">◉ Overview</span>'
        '<span class="ml-tag">✧ Record Insights</span>'
        '<span class="ml-tag">◈ Privacy-first</span></div>'
        f'<div class="ml-grid">{cards_html}</div>',
        unsafe_allow_html=True
    )

    months = Counter()
    for record in records:
        raw_date = record.get("Missing Since")
        if isinstance(raw_date, (date, datetime)):
            months[raw_date.strftime("%Y-%m")] += 1
        elif isinstance(raw_date, str):
            try:
                months[datetime.fromisoformat(raw_date).strftime("%Y-%m")] += 1
            except ValueError:
                pass
    ordered_months = sorted(months)
    if ordered_months:
        values = [months[m] for m in ordered_months]
        maximum = max(values) or 1
        min_x, max_x = 70, 1020
        chart_top, chart_bottom = 36, 260
        points = [
            (min_x + i * (max_x-min_x)/max(1,len(values)-1),
             chart_bottom - v/maximum*(chart_bottom-chart_top))
            for i,v in enumerate(values)
        ]
        if len(points) == 1:
            points = [(min_x, points[0][1]), (max_x,points[0][1])]
        path = " ".join(("M" if i==0 else "L")+f" {x:.1f} {y:.1f}"
                        for i,(x,y) in enumerate(points))
        area = path + f" L {points[-1][0]:.1f} {chart_bottom} L {points[0][0]:.1f} {chart_bottom} Z"
        grid = "".join(
            f'<line x1="65" y1="{y}" x2="1027" y2="{y}" stroke="#33415b" stroke-dasharray="4 5"/>'
            f'<text x="54" y="{y+4}" text-anchor="end" fill="#7d8ba8" font-size="12">{round(maximum*(chart_bottom-y)/(chart_bottom-chart_top))}</text>'
            for y in (36,92,148,204,260)
        )
        selected_ticks = sorted(set([0, len(ordered_months)-1] + list(range(0,len(ordered_months),max(1,len(ordered_months)//5)))))
        labels = "".join(
            f'<text x="{min_x+i*(max_x-min_x)/max(1,len(ordered_months)-1):.1f}" y="285" '
            f'fill="#8fa2c3" font-size="12" text-anchor="middle">{escape(ordered_months[i])}</text>'
            for i in selected_ticks
        )
        dots = "".join(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#59b4ff" stroke="#101a30" stroke-width="2"/>'
            for x,y in points[:80]
        )
        svg = (
            '<svg class="ml-chart-svg" viewBox="0 0 1080 315" role="img" aria-label="Records by missing month">'
            '<defs><linearGradient id="mlTrend" x1="0" x2="0" y1="0" y2="1">'
            '<stop offset="0%" stop-color="#248bff" stop-opacity=".42"/>'
            '<stop offset="100%" stop-color="#248bff" stop-opacity=".015"/>'
            '</linearGradient></defs>' + grid +
            f'<path d="{area}" fill="url(#mlTrend)"/>' +
            f'<path d="{path}" fill="none" stroke="#328eff" stroke-width="3" stroke-linejoin="round"/>' +
            dots + labels + '</svg>'
        )
    else:
        svg = '<div class="ml-empty">📈 &nbsp; Upload a CSV or Excel dataset with missing dates to see the monthly trend.</div>'
    st.markdown(
        '<div class="ml-panel"><div class="ml-panel-title">Missing Reports Trend</div>'
        '<div class="ml-panel-sub">Number of loaded records by missing month (not publication month)</div>'
        + svg + '</div>', unsafe_allow_html=True
    )

    if locations:
        largest = max(locations.values())
        location_bars = "".join(
            f'<div class="ml-row"><div class="ml-loc-label" title="{escape(place,quote=True)}">{escape(place)}</div>'
            f'<div class="ml-track"><div class="ml-fill" style="width:{100*count/largest:.1f}%"></div></div>'
            f'<div class="ml-loc-count">{count:,}</div></div>'
            for place,count in locations.most_common(6)
        )
    else:
        location_bars = '<div class="ml-empty">📍 &nbsp; Load records to see top missing locations.</div>'
    st.markdown(
        '<div class="ml-panel"><div class="ml-panel-title">Top Missing Locations</div>'
        '<div class="ml-panel-sub">Most frequent locations in the currently loaded records</div>'
        + location_bars + '</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="ml-note">🔐 &nbsp; Data source: <b>' + source_name + '</b>. '
        'Charts show dataset summaries, not verified identities or confirmed case links. '
        'Use the sidebar to search, add and compare records.</div>',
        unsafe_allow_html=True
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
                st.session_state.pop("search_results", None)
                st.session_state.pop("search_suggestion", None)
                st.session_state.pop("similar_groups", None)

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


        result_mode = st.radio(
            "Results Display",
            ["Top 10 Matches", "All Sorted Matches"]
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
            st.session_state.pop("search_results", None)

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
                        candidates = None

                    else:
                        index = make_location_index(records)

                        candidates = find_by_location(
                            index,
                            person["Missing Location"]
                        )

                else:
                    candidates = records

                if candidates is not None:
                    results = linear_search(
                        candidates,
                        person,
                        calculate_score,
                        min_score
                    )

                    if result_mode == "Top 10 Matches":
                        ranked_results = top_matches(
                            results,
                            limit=10
                        )
                    else:
                        ranked_results = merge_sort(results)

                    st.session_state.search_results = ranked_results
                    st.session_state.search_person = person.copy()

        
        if "search_suggestion" in st.session_state:

            st.info(
                "Smart Search Helper: "
                + st.session_state.search_suggestion
            )

        if "search_results" in st.session_state:

            results = st.session_state.search_results

            st.subheader("Search Results")

            st.write(
                f"Showing {len(results)} possible matching records."
            )
            st.caption(
                "Scores are heuristic ranking values, not identity probabilities."
            )

            
            for item in results:

                record = item["record"]
                score = item["score"]

                with st.container(border=True):

                    left, right = st.columns([3, 1])

                    with left:
                        st.subheader(
                            f"🔎 Case {record.get('Case ID', 'Unknown')}"
                        )

                    with right:
                        st.metric(
                            "Match Score",
                            f"{score:.1f}/100"
                        )

                    st.progress(
                        min(1.0, max(0.0, score / 100))
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            "**Age:**",
                            record.get("Age")
                            if record.get("Age") is not None
                            else "Unknown"
                        )

                        st.write(
                            "**Gender:**",
                            record.get("Gender") or "Unknown"
                        )

                    with col2:
                        st.write(
                            "**Location:**",
                            record.get("Missing Location") or "Unknown"
                        )

                        st.write(
                            "**Missing Since:**",
                            record.get("Missing Since") or "Unknown"
                        )

                    with st.expander("View Description"):
                        st.write(
                            record.get("Description")
                            or "No description available."
                        )

                    warnings = check_differences(
                        st.session_state.search_person,
                        record
                    )

                    if warnings:
                        st.warning(
                            "Review differences: "
                            + ", ".join(warnings)
                        )


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
            st.session_state.pop("search_suggestion", None)
            st.session_state.pop("similar_groups", None)

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
                    st.session_state.pop("search_suggestion", None)
                    st.session_state.pop("similar_groups", None)
                    st.success(
                        f"{len(records)} saved records loaded."
                    )

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

        display_rows = []
        for record in visible_records:
            display_rows.append({
                column: "" if record.get(column) is None
                else str(record.get(column))
                for column in columns
            })

        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True
        )


elif page == "Smart Case Link":
    show_smart_case_page(st.session_state.records)


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
    st.title("How MissingLink Works")
    st.caption("A DSA-based tool for reviewing possible links between reports.")

    st.subheader("1. Load and prepare records")
    st.write(
        "Upload an Excel or CSV file. The app validates the six required "
        "columns and standardizes the fields for searching."
    )

    st.subheader("2. Find possible matches")
    st.write(
        "Hash Map filters records by location when requested. Linear Search "
        "compares candidate records using a weighted heuristic Match Score."
    )

    st.subheader("3. Rank the results")
    st.write(
        "Min Heap returns up to ten highest-scoring records. "
        "Merge Sort orders all qualifying records by score."
    )

    st.subheader("4. Review possible connections")
    st.write(
        "Union-Find groups potentially related reports from the same location. "
        "Smart Case Link explores possible links across different locations. "
        "Smart Search Helper suggests missing search fields."
    )

    st.subheader("5. Save a working copy")
    st.write(
        "Use Saved Records to create or reopen a local CSV working copy. "
        "The source dataset is not overwritten. On a hosted deployment, "
        "the working copy is stored on the server, not a visitor's device."
    )

    st.warning(
        "All scores and groups are preliminary suggestions, not identity "
        "confirmations or calibrated probabilities. Human verification is required."
    )
