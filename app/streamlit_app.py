import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.triage.agent import TriageAgent
from src.tam.account_service import AccountService
from src.tam.summarizer import TicketSummarizer
from src.utils.data_loader import (
    load_tickets,
    load_accounts,
)


st.set_page_config(
    page_title="Zycus AI Support Triage",
    page_icon="AI",
    layout="wide",
)


@st.cache_resource
def get_agent():
    return TriageAgent()


@st.cache_resource
def get_account_service():
    return AccountService()


@st.cache_resource
def get_summarizer():
    return TicketSummarizer()


@st.cache_data
def get_tickets():
    return load_tickets()


@st.cache_data
def get_accounts():
    return load_accounts()


def display_risk(result):
    st.subheader("Risk Assessment")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Risk Level",
            result.risk_level.upper(),
        )

    with col2:
        st.metric(
            "High Risk",
            "Yes" if result.is_high_risk else "No",
        )

    if result.risk_reasons:
        st.write("Risk Indicators")

        for reason in result.risk_reasons:
            st.write(f"- {reason}")
    else:
        st.info(
            "No high-risk indicators detected."
        )


def display_ticket_triage():
    st.header("Task 1: Intelligent Ticket Triage")

    st.write(
        "Analyze a support ticket using customer context, "
        "risk detection, knowledge-base retrieval, and "
        "structured AI triage."
    )

    tickets = get_tickets()

    if not tickets:
        st.error("No tickets were found.")
        return

    st.subheader("Ticket Selection")

    col1, col2 = st.columns(2)

    with col1:
        search_text = st.text_input(
            "Search tickets",
            placeholder="Enter ticket ID or subject",
            key="ticket_search",
        )

    with col2:
        category_filter = st.selectbox(
            "Filter by category",
            options=[
                "All",
                "billing",
                "authentication",
                "technical",
                "onboarding",
                "general",
            ],
            key="ticket_category_filter",
        )

    filtered_tickets = tickets

    if search_text:
        search_lower = search_text.lower()

        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if (
                search_lower
                in str(
                    ticket.get(
                        "ticket_id",
                        "",
                    )
                ).lower()
                or search_lower
                in str(
                    ticket.get(
                        "subject",
                        "",
                    )
                ).lower()
            )
        ]

    if category_filter != "All":
        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if category_filter.lower()
            in (
                f"{ticket.get('subject', '')} "
                f"{ticket.get('description', '')}"
            ).lower()
        ]

    if not filtered_tickets:
        st.warning(
            "No tickets match the selected filters."
        )
        return

    ticket_options = {
        (
            f"{ticket.get('ticket_id', 'Unknown')} - "
            f"{ticket.get('subject', 'No subject')}"
        ): ticket.get("ticket_id")
        for ticket in filtered_tickets
    }

    selected_ticket = st.selectbox(
        "Select a support ticket",
        options=list(ticket_options.keys()),
        key="selected_ticket",
    )

    selected_ticket_id = ticket_options[
        selected_ticket
    ]

    if st.button(
        "Analyze Ticket",
        type="primary",
        use_container_width=True,
        key="analyze_ticket",
    ):
        with st.spinner(
            "Analyzing ticket..."
        ):
            try:
                agent = get_agent()

                result = agent.triage(
                    selected_ticket_id
                )

                context = agent.build_context(
                    selected_ticket_id
                )

                st.session_state[
                    "triage_result"
                ] = result

                st.session_state[
                    "triage_context"
                ] = context

            except Exception as exc:
                st.error(
                    f"Unable to analyze ticket: {exc}"
                )
                return

    if "triage_result" not in st.session_state:
        st.info(
            "Select a ticket and click "
            "'Analyze Ticket' to begin."
        )
        return

    result = st.session_state[
        "triage_result"
    ]

    context = st.session_state[
        "triage_context"
    ]

    st.success(
        "Ticket analysis completed."
    )

    st.divider()

    st.header("Ticket Details")

    ticket = context.get("ticket")

    if ticket:
        st.write(
            f"**Ticket ID:** "
            f"{ticket.get('ticket_id', 'N/A')}"
        )

        st.write(
            f"**Subject:** "
            f"{ticket.get('subject', 'No subject')}"
        )

        description = ticket.get(
            "description"
        )

        if description:
            st.write(
                f"**Description:** {description}"
            )
        else:
            st.write(
                "**Description:** N/A"
            )

    else:
        st.warning(
            "Ticket information is unavailable."
        )

    st.divider()

    st.header("Customer Context")

    account = context.get("account")

    if account:
        st.write(
            f"**Account ID:** "
            f"{account.get('account_id', 'N/A')}"
        )

        st.write(
            f"**Customer:** "
            f"{account.get('customer_name', 'N/A')}"
        )

        st.write(
            f"**Plan:** "
            f"{account.get('plan', 'N/A')}"
        )

        st.write(
            f"**Status:** "
            f"{account.get('status', 'N/A')}"
        )

        st.write(
            f"**Account Summary:** "
            f"{account.get('summary', 'N/A')}"
        )

    else:
        st.info(
            "Account information is not available "
            "for this ticket."
        )

    st.divider()

    st.header("Risk Assessment")

    display_risk(result)

    st.divider()

    st.header("Customer Summary")

    summary = context.get("summary")

    if summary:
        if isinstance(summary, dict):
            st.write(
                f"**Ticket Summary:** "
                f"{summary.get('ticket_summary', 'N/A')}"
            )

            st.write(
                f"**History Summary:** "
                f"{summary.get('history_summary', 'N/A')}"
            )

            st.write(
                f"**Account Available:** "
                f"{summary.get('account_available', False)}"
            )
        else:
            st.write(summary)
    else:
        st.info(
            "No customer summary is available."
        )

    account_tickets = context.get(
        "account_tickets",
        [],
    )

    if account_tickets:
        st.subheader(
            "Previous Ticket History"
        )

        for previous_ticket in account_tickets:
            st.write(
                f"- "
                f"{previous_ticket.get('ticket_id', 'N/A')}: "
                f"{previous_ticket.get('subject', 'No subject')}"
            )
    else:
        st.write(
            "No previous ticket history available."
        )

    st.divider()

    st.header("Triage Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Product Area",
            result.product_area,
        )

    with col2:
        st.metric(
            "Issue Category",
            result.category,
        )

    with col3:
        st.metric(
            "Priority",
            result.priority,
        )

    st.write(
        f"**Sentiment:** {result.sentiment}"
    )

    st.write(
        f"**Known Issue:** "
        f"{'Yes' if result.known_issue else 'No'}"
    )

    st.subheader("Triage Reasoning")

    st.write(result.reasoning)

    st.divider()

    st.header("Responder Routing")

    st.write(
        f"**Recommended Team:** "
        f"{result.recommended_team}"
    )

    st.subheader(
        "Recommended Action"
    )

    st.write(        result.recommended_action
    )

    st.divider()

    st.header("Draft First Response")

    st.write(
        result.first_response
    )

    st.divider()

    st.header("AI Response")

    st.write(
        result.response
    )

    st.divider()

    st.header("Knowledge Sources")

    if result.knowledge_sources:
        for source in result.knowledge_sources:
            st.write(
                f"- `{source}`"
            )
    else:
        st.info(
            "No knowledge-base sources found."
        )


def display_account_health():
    st.header("Task 2: TAM Account Health")

    st.write(
        "Generate a deterministic account brief using "
        "the customer account summary and support tickets "
        "from the last 90 days."
    )

    accounts = get_accounts()

    if not accounts:
        st.error("No accounts were found.")
        return

    account_options = {
        (
            f"{account.get('account_id', 'Unknown')} - "
            f"{account.get('customer_name', 'Unknown customer')}"
        ): account.get("account_id")
        for account in accounts
    }

    selected_account = st.selectbox(
        "Select a customer account",
        options=list(account_options.keys()),
        key="selected_account",
    )

    selected_account_id = account_options[
        selected_account
    ]

    if st.button(
        "Generate Account Health Brief",
        type="primary",
        use_container_width=True,
        key="generate_account_brief",
    ):
        with st.spinner(
            "Generating account health brief..."
        ):
            try:
                account_service = (
                    get_account_service()
                )

                summarizer = get_summarizer()

                account = (
                    account_service.get_account(
                        selected_account_id
                    )
                )

                account_tickets = (
                    account_service.get_account_tickets(
                        selected_account_id
                    )
                )

                brief = (
                    summarizer.generate_account_brief(
                        account_id=selected_account_id,
                        account=account,
                        tickets=account_tickets,
                    )
                )

                st.session_state[
                    "account_brief"
                ] = brief

                st.session_state[
                    "account_health_account"
                ] = account

            except Exception as exc:
                st.error(
                    f"Unable to generate account brief: {exc}"
                )
                return

    if "account_brief" not in st.session_state:
        st.info(
            "Select an account and click "
            "'Generate Account Health Brief' "
            "to begin."
        )
        return

    brief = st.session_state[
        "account_brief"
    ]

    account = st.session_state.get(
        "account_health_account"
    )

    st.success(
        "Account health brief generated successfully."
    )

    st.divider()

    st.header("Account Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Account ID",
            brief["account_id"],
        )

    with col2:
        customer_name = "Unknown customer"

        if account:
            customer_name = account.get(
             "customer_name",
                account.get(
                    "name",
                    account.get(
                        "customer",
                        brief.get(
                            "account_name",
                            "Unknown customer",
                        ),
                    ),
                ),
            )

        st.metric(
            "Customer",
            str(customer_name),
        )

    with col3:
        account_status = "Unknown"

        if account:
            account_status = account.get(
                "status",
                account.get(
                    "account_status",
                    account.get(
                        "health_status",
                        "Unknown",
                    ),
                ),
            )

        if account_status == "Unknown":
            summary_text = str(
                account.get("summary", "")
                if account
                else ""
            ).lower()

            if "at risk" in summary_text:
                account_status = "At Risk"

        st.metric(
            "Account Status",
            str(account_status),
        )
    if account:
        account_summary = account.get(
            "summary"
        )

        if account_summary:
            st.write(
                f"**Account Summary:** "
                f"{account_summary}"
            )

    st.divider()

    st.header("Last 90 Days")

    st.metric(
        "Support Tickets",
        brief["recent_ticket_count"],
    )

    st.divider()

    st.header("Executive Summary")

    st.write(
        brief["executive_summary"]
    )

    st.divider()

    st.header("Open Risks & Flagged Issues")

    open_risks = brief[
        "open_risks"
    ]

    if not open_risks:
        st.info(
            "No open risks or flagged issues."
        )
    else:
        for risk in open_risks:
            risk_type = risk.get(
                "type",
                "Risk",
            )

            st.subheader(
                risk_type
            )

            ticket_id = risk.get(
                "ticket_id"
            )

            if ticket_id:
                st.write(
                    f"**Ticket:** {ticket_id}"
                )

            st.write(
                f"**Reason:** "
                f"{risk.get('reason', 'N/A')}"
            )

            quote = risk.get(
                "quote"
            )

            if quote:
                st.write(
                    f'**Direct ticket quote:** "{quote}"'
                )

    st.divider()

    st.header(
        "Recommended Talking Points"
    )

    talking_points = brief[
        "recommended_talking_points"
    ]

    for point in talking_points:
        st.write(
            f"- {point}"
        )


def main():
    st.title(
        "Zycus AI Support Triage"
    )

    st.write(
        "Production-oriented AI support tooling for "
        "Technical Support and Technical Account Management."
    )

    tab1, tab2 = st.tabs(
        [
            "Ticket Triage",
            "TAM Account Health",
        ]
    )

    with tab1:
        display_ticket_triage()

    with tab2:
        display_account_health()


if __name__ == "__main__":
    main()