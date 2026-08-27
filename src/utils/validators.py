REQUIRED_TICKET_FIELDS = {
    "ticket_id",
    "account_id",
    "company",
    "subject",
    "body",
    "product",
    "product_area",
    "category",
    "urgency",
    "status",
    "plan_tier",
    "created_at",
}

REQUIRED_ACCOUNT_FIELDS = {
    "account_id",
    "company",
    "tam",
    "plan_tier",
    "arr_usd",
    "seats_licensed",
    "seats_active",
    "products",
    "health_status",
    "usage_trend",
    "open_tickets",
    "p1_tickets_last_30d",
    "renewal_date",
    "last_qbr_date",
    "escalation_notes",
}

def validate_records(
    records: list[dict],
    required_fields: set[str],
    record_type: str,
) -> None:
    """Validate that every record contains required fields."""

    if not records:
        raise ValueError(f"No {record_type} records found.")

    for index, record in enumerate(records):
        missing = required_fields - record.keys()

        if missing:
            raise ValueError(
                f"{record_type} record {index} is missing fields: "
                f"{sorted(missing)}"
            )