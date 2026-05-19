"""Cached embedding support for the agentic RAG fixture."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any


DEFAULT_CACHE_PATH = Path(__file__).resolve().parents[1] / "index" / "embedding-cache.json"
DEFAULT_DETERMINISTIC_MODEL = "local-hash-v1"
DEFAULT_OPENAI_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 96


class EmbeddingStore:
    """Small local cache around deterministic or OpenAI embeddings."""

    def __init__(
        self,
        cache_path: str | Path | None = None,
        provider: str = "deterministic",
        model: str | None = None,
    ) -> None:
        self.cache_path = Path(cache_path) if cache_path else DEFAULT_CACHE_PATH
        self.provider = provider
        self.model = model or (DEFAULT_OPENAI_MODEL if provider == "openai" else DEFAULT_DETERMINISTIC_MODEL)
        self.stats = {"computed": 0, "cache_hits": 0}
        self._cache = self._read_cache()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float] | None] = []
        missing: list[tuple[int, str, str]] = []
        for index, text in enumerate(texts):
            key = self._cache_key(text)
            cached = self._cache.get(key)
            if cached is None:
                vectors.append(None)
                missing.append((index, key, text))
            else:
                vectors.append(cached)
                self.stats["cache_hits"] += 1

        if missing:
            computed = self._compute_embeddings([text for _, _, text in missing])
            for (index, key, _), vector in zip(missing, computed):
                self._cache[key] = vector
                vectors[index] = vector
                self.stats["computed"] += 1
            self._write_cache()

        return [vector for vector in vectors if vector is not None]

    def _cache_key(self, text: str) -> str:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return f"{self.provider}:{self.model}:{digest}"

    def _read_cache(self) -> dict[str, list[float]]:
        if not self.cache_path.exists():
            return {}
        try:
            return json.loads(self.cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.cache_path.with_name(
            f".{self.cache_path.name}.{os.getpid()}.{id(self)}.tmp"
        )
        tmp_path.write_text(json.dumps(self._cache, sort_keys=True), encoding="utf-8")
        tmp_path.replace(self.cache_path)

    def _compute_embeddings(self, texts: list[str]) -> list[list[float]]:
        if self.provider == "openai":
            return self._compute_openai_embeddings(texts)
        return [_deterministic_embedding(text) for text in texts]

    def _compute_openai_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings.")
        from openai import OpenAI

        response = OpenAI().embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]


def _deterministic_embedding(text: str) -> list[float]:
    vector = [0.0] * VECTOR_SIZE
    for token in re.findall(r"[a-zA-Z0-9]+", text.lower()):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "big") % VECTOR_SIZE
        sign = 1 if digest[2] % 2 == 0 else -1
        vector[index] += sign * (1.0 + min(len(token), 12) / 12)
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [round(value / norm, 8) for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    return sum(a * b for a, b in zip(left, right))
