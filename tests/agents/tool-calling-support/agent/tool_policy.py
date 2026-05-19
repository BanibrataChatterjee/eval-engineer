"""Policy-derived tool availability rules for the support-agent fixture."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


EEA_UK_REGIONS = {
    "austria",
    "belgium",
    "bulgaria",
    "croatia",
    "cyprus",
    "czech republic",
    "denmark",
    "estonia",
    "finland",
    "france",
    "germany",
    "greece",
    "hungary",
    "iceland",
    "ireland",
    "italy",
    "latvia",
    "liechtenstein",
    "lithuania",
    "luxembourg",
    "malta",
    "netherlands",
    "norway",
    "poland",
    "portugal",
    "romania",
    "slovakia",
    "slovenia",
    "spain",
    "sweden",
    "united kingdom",
    "uk",
    "eea",
    "eu",
}

REFUND_TERMS = ("refund", "money back", "reimburse", "charge back", "chargeback")
CANCEL_TERMS = ("cancel", "cancellation", "terminate")
LEGAL_DATA_TERMS = (
    "gdpr",
    "delete my data",
    "data deletion",
    "data export",
    "data access",
    "legal hold",
    "subpoena",
)


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _is_eea_or_uk(region: Any) -> bool:
    return str(region or "").strip().lower() in EEA_UK_REGIONS


def requires_wire_refund_billing_intake(user_message: str, account_context: dict[str, Any]) -> bool:
    """Return true when policy makes billing escalation the only valid first tool."""
    text = user_message.lower()
    asks_for_refund = _contains_any(text, REFUND_TERMS)
    asks_for_cancellation = _contains_any(text, CANCEL_TERMS)
    payment_method = str(account_context.get("payment_method", "")).lower()
    region = account_context.get("billing_region")

    return (
        asks_for_refund
        and asks_for_cancellation
        and payment_method == "wire_transfer"
        and not _is_eea_or_uk(region)
        and not _contains_any(text, LEGAL_DATA_TERMS)
    )


def select_tools_for_context(
    tools: list[dict[str, Any]],
    user_message: str,
    account_context: dict[str, Any],
) -> list[dict[str, Any]]:
    """Apply deterministic policy gates before exposing tools to the model."""
    if requires_wire_refund_billing_intake(user_message, account_context):
        selected = []
        for tool in tools:
            if tool.get("name") != "escalate_to_billing":
                continue
            billing_tool = deepcopy(tool)
            reason_schema = billing_tool["input_schema"]["properties"]["reason"]
            reason_schema["enum"] = ["wire_transfer_issue"]
            reason_schema["description"] = (
                "Use `wire_transfer_issue` for non-EEA/UK wire-transfer "
                "cancellation+refund handling."
            )
            selected.append(billing_tool)
        return selected
    return tools
