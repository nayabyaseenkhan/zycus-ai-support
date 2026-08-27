import streamlit as st

from src.triage.agent import TriageAgent


st.set_page_config(
    page_title="Zycus AI Support",
    layout="wide",
)


@st.cache_resource
def get_agent() -> TriageAgent:
    """Create and cache the triage agent."""
    return TriageAgent()


def main():
    """Run the Streamlit application."""

    st.title("Zycus AI Support Triage")

    st.write(
        "Analyze customer support tickets using customer context, "
        "risk detection, knowledge-base retrieval, and AI triage."
    )

    agent = get_agent()

    tickets = agent.account_service.tickets

    if not tickets:
        st.error("No support tickets are available.")
        return

    # Ticket search
    search_text = st.text_input(
        "Search tickets",
        placeholder="Enter ticket ID or subject",
    )

    # Ticket category filter
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
    )

    # Apply search filter
    filtered_tickets = tickets

    if search_text:
        search_text = search_text.lower()

        filtered_tickets = [
            ticket
            for ticket in filtered_tickets
            if (
                search_text
                in str(
                    ticket.get("ticket_id", "")
                ).lower()
                or search_text
                in str(
                    ticket.get("subject", "")
                ).lower()
            )
        ]

    # Apply category filter
    if category_filter != "All":
        filtered_tickets = [
        ticket
        for ticket in filtered_tickets
        if agent.classify_category(ticket)
        == category_filter
    ]

    if not filtered_tickets:
        st.warning(
            "No tickets match the selected filters."
        )
        return

    # Ticket selection
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
    )

    ticket_id = ticket_options[selected_ticket]

    # Analyze selected ticket
    if st.button(
        "Analyze Ticket",
        type="primary",
    ):

        with st.spinner(
            "Analyzing support ticket..."
        ):

            context = agent.build_context(
                ticket_id=ticket_id,
                top_k=3,
            )

            result = agent.triage(
                ticket_id=ticket_id,
                top_k=3,
            )

        ticket = context["ticket"]
        account = context["account"]
        summary = context["summary"]

        st.success(
            "Ticket analysis completed."
        )

        # Ticket details
        st.subheader("Ticket Details")

        st.write(
            f"Ticket ID: "
            f"{ticket.get('ticket_id', 'N/A')}"
        )

        st.write(
            f"Subject: "
            f"{ticket.get('subject', 'N/A')}"
        )

        st.write(
            f"Description: "
            f"{ticket.get('description', 'N/A')}"
        )

        # Customer context
        st.subheader("Customer Context")

        if account:
            st.write(
                f"Account ID: "
                f"{account.get('account_id', 'N/A')}"
            )

            st.write(
                f"Customer: "
                f"{account.get('name', 'N/A')}"
            )
        else:
            st.warning(
                "Account information is not available "
                "for this ticket."
            )

        # Risk assessment
        st.subheader("Risk Assessment")

        if result.is_high_risk:
            st.error(
                f"Risk Level: {result.risk_level}"
            )
        else:
            st.success(
                f"Risk Level: {result.risk_level}"
            )

        if result.risk_reasons:
            st.write("Risk Reasons:")

            for reason in result.risk_reasons:
                st.write(reason)
        else:
            st.write(
                "No high-risk indicators detected."
            )

        # Customer summary
        st.subheader("Customer Summary")

        st.write(
            summary.get(
                "ticket_summary",
                "No ticket summary available.",
            )
        )

        st.write("Previous Ticket History")

        st.write(
            summary.get(
                "history_summary",
                "No previous history available.",
            )
        )

        # Triage result
        st.subheader("Triage Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Category",
                result.category,
            )

        with col2:
            st.metric(
                "Priority",
                result.priority,
            )

        with col3:
            st.metric(
                "Sentiment",
                result.sentiment,
            )

        # Recommended action
        st.subheader("Recommended Action")

        st.info(
            result.recommended_action
        )

        # AI response
        st.subheader("AI Response")

        st.write(
            result.response
        )

        # Knowledge sources
        st.subheader("Knowledge Sources")

        if result.knowledge_sources:
            for source in result.knowledge_sources:
                st.write(source)
        else:
            st.write(
                "No relevant knowledge sources found."
            )


if __name__ == "__main__":
    main()