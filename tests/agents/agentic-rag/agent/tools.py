"""Deterministic tools used by the agentic RAG fixture."""

from __future__ import annotations

from typing import Any

from agent.data import load_accounts, load_audit_logs, load_tickets
from agent.embeddings import EmbeddingStore
from agent.retrieval import rerank_evidence, search_chunks


def fetch_account(account_id: str | None) -> dict[str, Any] | None:
    if not account_id:
        return None
    return load_accounts().get(account_id)


def search_tickets(account_id: str | None, query: str) -> list[dict[str, Any]]:
    if not account_id:
        return []
    terms = set(query.lower().split())
    results = []
    for ticket in load_tickets():
        haystack = f"{ticket['title']} {ticket['text']}".lower()
        if ticket["account_id"] == account_id and any(term.strip("?.!,") in haystack for term in terms):
            results.append(ticket)
    return results


def inspect_audit_log(account_id: str | None, user_id: str | None) -> dict[str, Any]:
    if not account_id or not user_id:
        return {"events": [], "identity_seen": False}
    for item in load_audit_logs():
        if item["account_id"] == account_id and item["user_id"] == user_id:
            return {"events": item["events"], "identity_seen": bool(item["events"])}
    return {"events": [], "identity_seen": False}


def search_kb(
    query: str,
    *,
    top_k: int,
    embedding_store: EmbeddingStore,
    actor_role: str,
    enforce_permissions: bool,
) -> dict[str, Any]:
    return search_chunks(
        query,
        top_k=top_k,
        embedding_store=embedding_store,
        actor_role=actor_role,
        enforce_permissions=enforce_permissions,
    )


def rerank(chunks: list[dict[str, Any]], query: str, risk: str, limit: int) -> list[dict[str, Any]]:
    return rerank_evidence(chunks, query, risk)[:limit]

