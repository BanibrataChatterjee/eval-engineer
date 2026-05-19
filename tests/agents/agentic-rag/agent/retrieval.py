"""Chunking, retrieval, and evidence reranking for the agentic RAG fixture."""

from __future__ import annotations

import re
from typing import Any

from agent.data import load_documents
from agent.embeddings import EmbeddingStore, cosine_similarity


def _terms(values: list[str] | str) -> set[str]:
    if isinstance(values, str):
        values = [values]
    return set(re.findall(r"[a-zA-Z0-9]+", " ".join(values).lower()))


def chunk_documents() -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for doc in load_documents():
        paragraphs = [part.strip() for part in doc["text"].split("\n\n") if part.strip()]
        for index, text in enumerate(paragraphs):
            chunk = dict(doc)
            chunk["chunk_id"] = f"{doc['doc_id']}#{index + 1}"
            chunk["text"] = text
            chunks.append(chunk)
    return chunks


def search_chunks(
    query: str,
    *,
    top_k: int,
    embedding_store: EmbeddingStore,
    actor_role: str = "support",
    enforce_permissions: bool = True,
) -> dict[str, Any]:
    chunks = chunk_documents()
    if enforce_permissions:
        chunks = [
            chunk
            for chunk in chunks
            if actor_role in chunk.get("allowed_roles", []) or "support" in chunk.get("allowed_roles", [])
        ]
    texts = [f"{chunk['title']} {' '.join(chunk.get('tags', []))} {chunk['text']}" for chunk in chunks]
    query_vector = embedding_store.embed_texts([query])[0]
    chunk_vectors = embedding_store.embed_texts(texts)

    scored = []
    query_terms = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
    for chunk, vector in zip(chunks, chunk_vectors):
        tag_hits = len(query_terms & _terms(chunk.get("tags", [])))
        score = cosine_similarity(query_vector, vector) + (tag_hits * 0.08)
        scored.append((score, chunk))
    scored.sort(key=lambda item: (-item[0], -item[1].get("authority", 0), item[1]["doc_id"]))
    selected = [dict(chunk, retrieval_score=round(score, 6)) for score, chunk in scored[:top_k]]
    return {
        "chunks": selected,
        "cache_hits": embedding_store.stats["cache_hits"],
        "cache_misses": embedding_store.stats["computed"],
    }


def rerank_evidence(chunks: list[dict[str, Any]], query: str, risk: str) -> list[dict[str, Any]]:
    query_terms = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))

    def rank_key(chunk: dict[str, Any]) -> tuple[float, str, str]:
        tag_hits = len(query_terms & _terms(chunk.get("tags", [])))
        status_bonus = 0 if chunk.get("status") == "current" else -20
        trusted_bonus = -50 if chunk.get("status") == "untrusted" else 0
        risk_bonus = 5 if risk in {"high", "regulated"} and chunk.get("authority", 0) >= 90 else 0
        retrieval_score = chunk.get("retrieval_score", 0.0) * 100
        return (
            retrieval_score + chunk.get("authority", 0) + status_bonus + trusted_bonus + risk_bonus + (tag_hits * 10),
            chunk.get("effective_date", ""),
            chunk["doc_id"],
        )

    deduped: dict[str, dict[str, Any]] = {}
    for chunk in chunks:
        existing = deduped.get(chunk["doc_id"])
        if existing is None or rank_key(chunk) > rank_key(existing):
            deduped[chunk["doc_id"]] = chunk
    return sorted(deduped.values(), key=rank_key, reverse=True)
