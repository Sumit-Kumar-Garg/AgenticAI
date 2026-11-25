
import streamlit as st
import requests

# -------------------------------------------------
# Configuration
# -------------------------------------------------

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Hotel Support AI",
    page_icon="🏨",
    layout="wide"
)

# -------------------------------------------------
# Session state
# -------------------------------------------------

if "investigation" not in st.session_state:
    st.session_state.investigation = None

if "review_result" not in st.session_state:
    st.session_state.review_result = None

if "audit_records" not in st.session_state:
    st.session_state.audit_records = None

if "current_ticket_id" not in st.session_state:
    st.session_state.current_ticket_id = ""


# -------------------------------------------------
# API helper
# -------------------------------------------------

def api_request(method, endpoint, payload=None):

    url = f"{API_BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, timeout=60)

        elif method == "POST":
            response = requests.post(
                url,
                json=payload,
                timeout=120
            )

        else:
            raise ValueError("Unsupported HTTP method")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        st.error(f"API request failed: {error}")

        if getattr(error, "response", None) is not None:
            st.error(error.response.text)

        return None


# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("🏨 Hotel Support AI Platform")

st.caption(
    "AI-powered ticket investigation, "
    "knowledge retrieval and human review"
)

st.divider()


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("Support Operations")

st.sidebar.markdown(
    """
    **Available modules**

    - Ticket Investigation
    - AI Recommendation
    - Human Review
    - Audit History
    """
)

st.sidebar.caption("Backend: FastAPI")
st.sidebar.caption("AI Engine: Gemini")
st.sidebar.caption("Orchestration: LangGraph")


# -------------------------------------------------
# Ticket Queue
# -------------------------------------------------

st.header("1. Support Ticket Queue")

filter_col, limit_col = st.columns(2)

with filter_col:
    selected_status = st.selectbox(
        "Filter by Status",
        ["OPEN", "CLOSED", "ALL"]
    )

with limit_col:
    selected_limit = st.selectbox(
        "Maximum Tickets",
        [50, 100, 200, 500],
        index=1
    )

if st.button("Refresh Ticket Queue"):

    with st.spinner("Loading support tickets..."):

        queue_result = api_request(
            "GET",
            f"/tickets?status={selected_status}"
            f"&limit={selected_limit}"
        )

    if queue_result:
        st.session_state.ticket_queue = queue_result

if "ticket_queue" not in st.session_state:
    st.session_state.ticket_queue = None

queue = st.session_state.ticket_queue

if queue:

    tickets = queue.get("tickets", [])

    total = len(tickets)

    open_count = sum(
        1 for t in tickets
        if t["status"].upper() == "OPEN"
    )

    high_priority_count = sum(
        1 for t in tickets
        if t["priority"].upper() in ["HIGH", "CRITICAL"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Tickets Loaded", total)
    col2.metric("Open Tickets", open_count)
    col3.metric("High/Critical Priority", high_priority_count)

    st.subheader("Ticket List")

    if tickets:

        st.dataframe(
            tickets,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No tickets found for this filter.")

# -------------------------------------------------
# Ticket Investigation
# -------------------------------------------------

st.header("1. Ticket Investigation")

available_ticket_ids = []

if st.session_state.ticket_queue:
    available_ticket_ids = [
        ticket["ticket_id"]
        for ticket in st.session_state.ticket_queue.get(
            "tickets", []
        )
    ]

if available_ticket_ids:
    ticket_id = st.selectbox(
        "Select Ticket for Investigation",
        available_ticket_ids
    )
else:
    ticket_id = st.text_input(
        "Enter Ticket ID",
        value="TKT00001",
        placeholder="Example: TKT00001"
    )

if st.button(
    "Investigate Ticket",
    type="primary"
):

    if not ticket_id.strip():
        st.warning("Please enter a ticket ID.")

    else:
        st.session_state.investigation = None
        st.session_state.review_result = None
        st.session_state.audit_records = None

        with st.spinner(
            "Investigating ticket using AI agents..."
        ):

            result = api_request(
                "POST",
                "/tickets/investigate",
                {"ticket_id": ticket_id.strip()}
            )

        if result:
            st.session_state.investigation = result
            st.session_state.current_ticket_id = ticket_id.strip()


# -------------------------------------------------
# Investigation Result
# -------------------------------------------------

investigation = st.session_state.investigation

if investigation:

    st.divider()
    st.header("2. Investigation Results")

    status = investigation.get("status", "UNKNOWN")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Ticket ID",
            investigation.get("ticket_id", "N/A")
        )

    with col2:
        st.metric(
            "Workflow Status",
            status
        )

    analysis = (
        investigation.get("review_request", {}).get("analysis")
        or investigation.get("analysis")
        or {}
    )

    warnings = (
        investigation.get("review_request", {}).get(
            "data_integrity_warnings", []
        )
        or investigation.get("data_integrity_warnings", [])
    )

    st.subheader("AI Analysis")

    if analysis:

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Category**")
            st.info(analysis.get("category", "N/A"))

        with col2:
            confidence = analysis.get("confidence", 0)
            st.write("**AI Confidence**")
            st.progress(
                max(0.0, min(1.0, float(confidence)))
            )
            st.write(f"{confidence:.0%}")

        st.write("**Likely Root Cause**")
        st.write(
            analysis.get("likely_root_cause", "Not available")
        )

        st.write("**Recommended Action**")
        st.success(
            analysis.get("recommended_action", "Not available")
        )

        st.write("**Reasoning**")
        st.write(
            analysis.get("reasoning", "Not available")
        )

        st.write("**Supporting Knowledge Articles**")
        articles = analysis.get("supporting_articles", [])

        if articles:
            for article in articles:
                st.write(f"- {article}")
        else:
            st.write("No supporting articles returned.")

    if warnings:
        st.subheader("Data Integrity Warnings")

        for warning in warnings:
            st.warning(warning)

    # -------------------------------------------------
    # Human Review
    # -------------------------------------------------

    if status == "PENDING_HUMAN_REVIEW":

        st.divider()
        st.header("3. Human Review")

        st.warning(
            "This ticket requires a human decision."
        )

        thread_id = investigation.get("thread_id")

        st.caption(f"Workflow thread: {thread_id}")

        with st.form("human_review_form"):

            reviewer = st.text_input(
                "Reviewer",
                value="support-manager"
            )

            decision = st.radio(
                "Review Decision",
                ["Approve", "Reject"],
                horizontal=True
            )

            comment = st.text_area(
                "Reviewer Comment",
                placeholder="Enter review comments..."
            )

            submitted = st.form_submit_button(
                "Submit Review",
                type="primary"
            )

            if submitted:

                payload = {
                    "approved": decision == "Approve",
                    "reviewer": reviewer,
                    "comment": comment
                }

                with st.spinner("Submitting human decision..."):

                    result = api_request(
                        "POST",
                        f"/tickets/review/{thread_id}",
                        payload
                    )

                if result:
                    st.session_state.review_result = result
                    st.session_state.investigation["status"] = (
                        result.get("status", "UNKNOWN")
                    )

                    st.success(
                        f"Review completed: {result.get('status')}"
                    )

                    st.rerun()

    elif status == "AUTO_RECOMMENDED":

        st.divider()

        st.success(
            "Recommendation passed the configured "
            "automation guardrails."
        )

        st.caption(
            "No refund, cancellation or other external "
            "business operation has been executed."
        )

    # -------------------------------------------------
    # Review Result
    # -------------------------------------------------

    if st.session_state.review_result:

        st.subheader("Review Decision")

        st.json(st.session_state.review_result)


# -------------------------------------------------
# Audit History
# -------------------------------------------------

st.divider()
st.header("4. Ticket Audit History")

audit_ticket_id = st.text_input(
    "Ticket ID for audit history",
    value=(
        st.session_state.current_ticket_id
        or ticket_id
    ),
    key="audit_ticket_input"
)

if st.button("Load Audit History"):

    if audit_ticket_id.strip():

        with st.spinner("Loading audit history..."):

            audit = api_request(
                "GET",
                f"/tickets/{audit_ticket_id.strip()}/audit"
            )

        if audit:
            st.session_state.audit_records = audit

if st.session_state.audit_records:

    audit = st.session_state.audit_records

    st.metric(
        "Total Human Reviews",
        audit.get("total_reviews", 0)
    )

    records = audit.get("audit_records", [])

    if records:
        st.dataframe(
            records,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No human review records found.")
