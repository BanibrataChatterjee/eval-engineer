# Agentic RAG Case Resolution

This fixture is a realistic case-resolution agent for testing Eval Engineer
against RAG plus agent workflows. It is intentionally more complex than the
policy RAG fixture: the agent plans, calls deterministic account/ticket/audit
tools, retrieves a chunked knowledge corpus through cached embeddings, reranks
evidence for high-risk cases, synthesizes structured decisions, and records
tokenomics metrics.

The default lane is deterministic so tests stay stable. Embeddings can use a
local hash provider or OpenAI with a local cache. Final generation is
deterministic by default; the realistic surface is the agent control flow,
tooling, retrieval, permissions, source authority, and tokenomics tradeoff.

The suite has 14 cases. It covers enterprise refund, legal hold export, SSO
permission, prompt injection, stale policy conflict, missing account context,
low-risk FAQ, ticket conflict, unclear export, malicious credential social
engineering, PII disclosure, brand-safe response, multi-source information
integration, and counterfactual untrusted-context handling.

Each case declares a `risk_profile`, `quality_dimensions`, and
`galileo_metrics` list so the metric contract is explicit across safety,
performance, answer quality, retrieval grounding, and cost.

## Modes

- `baseline_safe`: broad retrieval, rerank, all relevant tools, self-check.
- `cheap_unsafe`: low `top_k`, no rerank, minimal tools, no self-check.
- `adaptive`: risk-aware path; low-risk cases stay cheap, high-risk cases use
  rerank, account/ticket/audit tools, and self-check when needed.

The expected tokenomics result is that `cheap_unsafe` reduces cost but is
rejected for quality regressions, while `adaptive` reduces cost against
`baseline_safe` and preserves quality.

## Commands

Run local evals:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/agentic-rag/eval/evaluate.py --mode baseline_safe
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/agentic-rag/eval/evaluate.py --mode cheap_unsafe
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/agentic-rag/eval/evaluate.py --mode adaptive
```

Run with cached OpenAI embeddings:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/agentic-rag/eval/evaluate.py --mode adaptive --embedding-provider openai --cache-path tests/agents/agentic-rag/index/openai-embedding-cache.json
```

Compare curated packets:

```bash
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py tests/agents/agentic-rag/galileo/fixtures/baseline-safe-debug-packet.json tests/agents/agentic-rag/galileo/fixtures/cheap-unsafe-debug-packet.json --quality-metrics average_case_success,average_citation_recall,average_permission_safety,average_injection_resistance,average_source_authority,average_abstention_correctness
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py tests/agents/agentic-rag/galileo/fixtures/baseline-safe-debug-packet.json tests/agents/agentic-rag/galileo/fixtures/adaptive-debug-packet.json --quality-metrics average_case_success,average_citation_recall,average_permission_safety,average_injection_resistance,average_source_authority,average_abstention_correctness
```
