import sys
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.triage.agent import TriageAgent
from src.tam.account_service import AccountService
from src.tam.summarizer import TicketSummarizer


TASK1_CASES_FILE = BASE_DIR / "task1_cases.json"
TASK2_CASES_FILE = BASE_DIR / "task2_cases.json"
REPORT_FILE = BASE_DIR / "eval_report.json"


VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}

VALID_CATEGORIES = {
    "billing",
    "authentication",
    "technical",
    "onboarding",
    "general",
}


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_text(value):
    return (
        isinstance(value, str)
        and bool(value.strip())
    )


def evaluate_triage_case(agent, case):
    test_id = case["test_id"]
    ticket_id = case["ticket_id"]

    criteria = case.get(
        "acceptance_criteria",
        {},
    )

    checks = {}

    try:
        result = agent.triage(ticket_id)

        if "category" in criteria:
            checks["category"] = (
                result.category
                == criteria["category"]
            )

        if "category_in" in criteria:
            checks["category"] = (
                result.category
                in criteria["category_in"]
            )

        if criteria.get("valid_priority"):
            checks["valid_priority"] = (
                result.priority
                in VALID_PRIORITIES
            )

        if "priority_in" in criteria:
            checks["priority"] = (
                result.priority
                in criteria["priority_in"]
            )

        if criteria.get("has_product_area"):
            checks["has_product_area"] = check_text(
                result.product_area
            )

        if criteria.get("has_reasoning"):
            checks["has_reasoning"] = check_text(
                result.reasoning
            )

        if criteria.get("has_recommended_team"):
            checks["has_recommended_team"] = check_text(
                result.recommended_team
            )

        if criteria.get("has_first_response"):
            checks["has_first_response"] = check_text(
                result.first_response
            )

        if criteria.get("has_knowledge_sources"):
            checks["has_knowledge_sources"] = isinstance(
                result.knowledge_sources,
                list,
            )

        if "high_risk" in criteria:
            checks["high_risk"] = (
                result.is_high_risk
                == criteria["high_risk"]
            )

        if criteria.get("handles_missing_description"):
            context = agent.build_context(ticket_id)

            ticket = context.get("ticket")

            checks["handles_missing_description"] = (
                ticket is not None
            )

        quality_score = (
            sum(checks.values()) / len(checks)
            if checks
            else 0.0
        )

        passed = quality_score >= 0.80

        return {
            "test_id": test_id,
            "task": "Task 1 - Intelligent Ticket Triage",
            "name": case.get(
                "name",
                test_id,
            ),
            "ticket_id": ticket_id,
            "adversarial": case.get(
                "adversarial",
                False,
            ),
            "passed": passed,
            "quality_score": round(
                quality_score,
                2,
            ),
            "checks": checks,
        }

    except Exception as exc:
        return {
            "test_id": test_id,
            "task": "Task 1 - Intelligent Ticket Triage",
            "name": case.get(
                "name",
                test_id,
            ),
            "ticket_id": ticket_id,
            "adversarial": case.get(
                "adversarial",
                False,
            ),
            "passed": False,
            "quality_score": 0.0,
            "checks": {},
            "error": str(exc),
        }


def evaluate_account_case(
    account_service,
    summarizer,
    case,
):
    test_id = case["test_id"]
    account_id = case["account_id"]

    criteria = case.get(
        "acceptance_criteria",
        {},
    )

    checks = {}

    try:
        account = account_service.get_account(
            account_id
        )

        checks["account_loaded"] = (
            account is not None
        )

        tickets = account_service.get_account_tickets(
            account_id
        )

        checks["tickets_loaded"] = isinstance(
            tickets,
            list,
        )

        brief = summarizer.generate_account_brief(
            account_id=account_id,
            account=account,
            tickets=tickets,
        )

        checks["brief_generated"] = (
            isinstance(brief, dict)
        )

        required_fields = [
            "account_id",
            "account_name",
            "recent_ticket_count",
            "executive_summary",
            "open_risks",
            "recommended_talking_points",
        ]

        for field in required_fields:
            checks[f"has_{field}"] = (
                field in brief
            )

        if "account_id" in brief:
            checks["account_id_match"] = (
                brief["account_id"]
                == account_id
            )

        if criteria.get("has_executive_summary"):
            checks["has_executive_summary"] = check_text(
                brief.get("executive_summary")
            )

        if criteria.get("has_open_risks"):
            checks["has_open_risks"] = isinstance(
                brief.get("open_risks"),
                list,
            )

        if criteria.get("has_talking_points"):
            talking_points = brief.get(
                "recommended_talking_points",
                [],
            )

            checks["has_talking_points"] = (
                isinstance(
                    talking_points,
                    list,
                )
                and len(talking_points) > 0
            )

        if criteria.get("has_recent_ticket_count"):
            checks["has_recent_ticket_count"] = (
                isinstance(
                    brief.get(
                        "recent_ticket_count"
                    ),
                    int,
                )
            )

        if criteria.get("deterministic"):
            brief_again = summarizer.generate_account_brief(
                account_id=account_id,
                account=account,
                tickets=tickets,
            )

            checks["deterministic"] = (
                brief == brief_again
            )

        if criteria.get("risk_quotes_from_tickets"):
            valid_quotes = True

            ticket_text = " ".join(
                (
                    str(
                        ticket.get(
                            "subject",
                            "",
                        )
                    )
                    + " "
                    + str(
                        ticket.get(
                            "description",
                            "",
                        )
                    )
                ).lower()
                for ticket in tickets
            )

            for risk in brief.get(
                "open_risks",
                [],
            ):
                quote = risk.get(
                    "quote",
                    "",
                )

                if quote:
                    if quote.lower() not in ticket_text:
                        valid_quotes = False
                        break

            checks["risk_quotes_from_tickets"] = (
                valid_quotes
            )

        quality_score = (
            sum(checks.values()) / len(checks)
            if checks
            else 0.0
        )

        passed = quality_score >= 0.80

        return {
            "test_id": test_id,
            "task": "Task 2 - TAM Account Health",
            "name": case.get(
                "name",
                test_id,
            ),
            "account_id": account_id,
            "adversarial": case.get(
                "adversarial",
                False,
            ),
            "passed": passed,
            "quality_score": round(
                quality_score,
                2,
            ),
            "checks": checks,
        }

    except Exception as exc:
        return {
            "test_id": test_id,
            "task": "Task 2 - TAM Account Health",
            "name": case.get(
                "name",
                test_id,
            ),
            "account_id": account_id,
            "adversarial": case.get(
                "adversarial",
                False,
            ),
            "passed": False,
            "quality_score": 0.0,
            "checks": {},
            "error": str(exc),
        }


def create_summary(results):
    total = len(results)

    passed = sum(
        result["passed"]
        for result in results
    )

    failed = total - passed

    quality_score = (
        sum(
            result["quality_score"]
            for result in results
        )
        / total
        if total
        else 0.0
    )

    task1_results = [
        result
        for result in results
        if result["task"].startswith("Task 1")
    ]

    task2_results = [
        result
        for result in results
        if result["task"].startswith("Task 2")
    ]

    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "overall_quality_score": round(
            quality_score,
            2,
        ),
        "task_1": {
            "total": len(task1_results),
            "passed": sum(
                r["passed"]
                for r in task1_results
            ),
            "quality_score": round(
                (
                    sum(
                        r["quality_score"]
                        for r in task1_results
                    )
                    / len(task1_results)
                    if task1_results
                    else 0.0
                ),
                2,
            ),
        },
        "task_2": {
            "total": len(task2_results),
            "passed": sum(
                r["passed"]
                for r in task2_results
            ),
            "quality_score": round(
                (
                    sum(
                        r["quality_score"]
                        for r in task2_results
                    )
                    / len(task2_results)
                    if task2_results
                    else 0.0
                ),
                2,
            ),
        },
    }


def run_evaluation():
    print("=" * 70)
    print("ZYCUS AI SUPPORT - EVALUATION HARNESS")
    print("=" * 70)

    task1_cases = load_json(
        TASK1_CASES_FILE
    )

    task2_cases = load_json(
        TASK2_CASES_FILE
    )

    print(
        f"\nTask 1 cases: {len(task1_cases)}"
    )

    print(
        f"Task 2 cases: {len(task2_cases)}"
    )

    agent = TriageAgent()
    account_service = AccountService()
    summarizer = TicketSummarizer()

    results = []

    print("\n" + "-" * 70)
    print("TASK 1 - INTELLIGENT TICKET TRIAGE")
    print("-" * 70)

    for case in task1_cases:
        result = evaluate_triage_case(
            agent,
            case,
        )

        results.append(result)

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"{status} | "
            f"{result['test_id']} | "
            f"{result['name']} | "
            f"score={result['quality_score']:.2f}"
        )

    print("\n" + "-" * 70)
    print("TASK 2 - TAM ACCOUNT HEALTH")
    print("-" * 70)

    for case in task2_cases:
        result = evaluate_account_case(
            account_service,
            summarizer,
            case,
        )

        results.append(result)

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"{status} | "
            f"{result['test_id']} | "
            f"{result['name']} | "
            f"score={result['quality_score']:.2f}"
        )

    summary = create_summary(results)

    report = {
        "evaluation_metadata": {
            "generated_at": datetime.now().isoformat(),
            "dataset": (
                "Provided synthetic Zycus mock dataset"
            ),
            "external_data_used": False,
        },
        "summary": summary,
        "results": results,
    }

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
        )

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Total tests: "
        f"{summary['total_tests']}"
    )

    print(
        f"Passed: "
        f"{summary['passed']}"
    )

    print(
        f"Failed: "
        f"{summary['failed']}"
    )

    print(
        f"Overall quality score: "
        f"{summary['overall_quality_score']:.2f}"
    )

    print(
        f"\nReport written to: "
        f"{REPORT_FILE}"
    )

    print("=" * 70)

    return report


if __name__ == "__main__":
    run_evaluation()
