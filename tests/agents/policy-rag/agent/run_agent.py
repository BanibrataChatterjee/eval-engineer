#!/usr/bin/env python3
"""Run the deterministic policy RAG reference implementation."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).parent
MODEL_NAME = "gpt-4o-mini"
INPUT_TOKEN_COST = 0.00000015
OUTPUT_TOKEN_COST = 0.0000006


def load_knowledge_base() -> list[dict[str, Any]]:
    return json.loads((BASE_DIR / "knowledge_base.json").read_text(encoding="utf-8"))


def estimate_tokens(text: str) -> int:
    """Approximate token count deterministically for local tokenomics checks."""
    return max(1, int(len(re.findall(r"\S+", text)) * 1.35))


def _by_id(docs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {doc["id"]: doc for doc in docs}


def _ordered_docs(docs_by_id: dict[str, dict[str, Any]], ids: list[str]) -> list[dict[str, Any]]:
    return [docs_by_id[doc_id] for doc_id in ids if doc_id in docs_by_id]


def retrieve_documents(question: str, mode: str = "wide") -> list[dict[str, Any]]:
    docs = load_knowledge_base()
    if mode == "wide":
        return docs
    docs_by_id = _by_id(docs)
    lower = question.lower()

    if mode == "balanced":
        if "enterprise" in lower and "refund" in lower:
            return _ordered_docs(docs_by_id, ["refund-exceptions", "billing-refunds"])
        if "legal hold" in lower or "subpoena" in lower:
            return _ordered_docs(docs_by_id, ["privacy-export", "security-data"])
        if "promo" in lower or "promotional" in lower or "trial" in lower:
            return _ordered_docs(docs_by_id, ["trial-extension"])
        if "enterprise" in lower and ("cancel" in lower or "cancellation" in lower):
            return _ordered_docs(docs_by_id, ["enterprise-cancellation", "plan-limits"])

    terms = {term.lower() for term in re.findall(r"[a-zA-Z]+", question)}
    scored = []
    for doc in docs:
        tags = set(doc.get("tags", []))
        title_terms = {term.lower() for term in re.findall(r"[a-zA-Z]+", doc["title"])}
        text_terms = {term.lower() for term in re.findall(r"[a-zA-Z]+", doc["text"])}
        score = len(terms & tags) * 3 + len(terms & title_terms) * 2 + len(terms & text_terms)
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    limit = 1 if mode == "focused" else 2
    return [doc for _, doc in scored[:limit]] or docs[:1]


def build_prompt(question: str, docs: list[dict[str, Any]]) -> str:
    context = "\n\n".join(f"[{doc['id']}] {doc['text']}" for doc in docs)
    return (
        "Answer the support policy question using only the policy context. "
        "Be concise and include the policy source id.\n\n"
        f"<policy_context>\n{context}\n</policy_context>\n\n"
        f"<question>{question}</question>"
    )


def synthesize_answer(question: str, docs: list[dict[str, Any]]) -> str:
    lower = question.lower()
    doc_ids = {doc["id"] for doc in docs}
    if "enterprise" in lower and "refund" in lower and "ach" in lower:
        if {"refund-exceptions", "billing-refunds"} <= doc_ids:
            return (
                "Enterprise ACH refunds above $5,000 require a billing ticket "
                "and account manager approval before the refund timeline starts. "
                "After approval, ACH refunds process in 7-14 business days. "
                "Source: refund-exceptions, billing-refunds"
            )
        source = next((doc for doc in docs if doc["id"] in {"refund-exceptions", "billing-refunds"}), docs[0])
        return source["text"] + " Source: " + source["id"]
    if "ach" in lower and "refund" in lower:
        source = next((doc for doc in docs if doc["id"] == "billing-refunds"), docs[0])
        return "ACH refunds process in 7-14 business days. Source: " + source["id"]
    if "enterprise" in lower and ("cancel" in lower or "cancellation" in lower):
        source = next((doc for doc in docs if doc["id"] == "enterprise-cancellation"), docs[0])
        return (
            "Enterprise cancellations must be routed to the assigned account manager; "
            "support should not cancel them directly from chat. Source: "
            + source["id"]
        )
    if "legal hold" in lower or "subpoena" in lower:
        if {"privacy-export", "security-data"} <= doc_ids:
            return (
                "Data exports for legal hold must be handled by compliance and "
                "are not self-serve; compliance also handles legal hold and "
                "subpoena data requests after identity verification. "
                "Source: privacy-export, security-data"
            )
        source = next((doc for doc in docs if doc["id"] in {"privacy-export", "security-data"}), docs[0])
        return source["text"] + " Source: " + source["id"]
    if "delete" in lower or "gdpr" in lower or "data" in lower:
        source = next((doc for doc in docs if doc["id"] == "security-data"), docs[0])
        return "Data deletion and GDPR requests must be escalated to compliance after identity verification. Source: " + source["id"]
    if "trial" in lower or "extension" in lower or "promotional" in lower:
        source = next((doc for doc in docs if doc["id"] == "trial-extension"), docs[0])
        return "Trial extensions are not available after a promotional extension in the last 90 days. Source: " + source["id"]
    source = docs[0]
    return source["text"] + " Source: " + source["id"]


def answer_question(question: str, mode: str = "wide") -> dict[str, Any]:
    start = time.perf_counter_ns()
    docs = retrieve_documents(question, mode=mode)
    retrieval_duration_ns = time.perf_counter_ns() - start
    prompt = build_prompt(question, docs)
    answer = synthesize_answer(question, docs)
    input_tokens = estimate_tokens(prompt)
    output_tokens = estimate_tokens(answer)
    total_tokens = input_tokens + output_tokens
    estimated_cost = input_tokens * INPUT_TOKEN_COST + output_tokens * OUTPUT_TOKEN_COST

    return {
        "question": question,
        "answer": answer,
        "mode": mode,
        "model": MODEL_NAME,
        "retrieved_documents": docs,
        "retrieved_document_ids": [doc["id"] for doc in docs],
        "prompt": prompt,
        "metrics": {
            "retrieval_duration_ns": retrieval_duration_ns,
            "llm_duration_ns": max(1_000_000, total_tokens * 90_000),
            "total_duration_ns": retrieval_duration_ns + max(1_000_000, total_tokens * 90_000),
            "num_input_tokens": input_tokens,
            "num_output_tokens": output_tokens,
            "num_total_tokens": total_tokens,
            "estimated_cost": estimated_cost,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--mode", choices=("wide", "focused", "balanced"), default="wide")
    args = parser.parse_args()
    print(json.dumps(answer_question(args.question, mode=args.mode), indent=2))


if __name__ == "__main__":
    main()
