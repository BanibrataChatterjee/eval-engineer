# Policy RAG Reference

This fixture is a deterministic RAG-style agent for exercising Eval Engineer
beyond tool-calling agents. It produces stable retrieval, answer-quality, and
tokenomics evidence across easy single-source questions and harder multi-source
policy questions.

The runner supports three retrieval modes:

- `wide`: baseline mode that sends all policy documents as context.
- `focused`: risky cheap mode that routes to one scored document.
- `balanced`: quality-preserving mode that uses route-aware document pairs for
  multi-source questions.

The tokenomics expectation is that `focused` can reduce input tokens and
estimated cost but should be rejected on the harder suite because it drops
required sources. `balanced` should reduce cost versus `wide` while preserving
the deterministic local answer score across all six cases.

## Commands

Run local evals:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/policy-rag/eval/evaluate.py --mode wide
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/policy-rag/eval/evaluate.py --mode focused
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/policy-rag/eval/evaluate.py --mode balanced
```

Create Galileo log streams:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/policy-rag/galileo/run_log_stream.py --mode wide
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/policy-rag/galileo/run_log_stream.py --mode focused
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 tests/agents/policy-rag/galileo/run_log_stream.py --mode balanced
```

Compare before and after packets with the tokenomics skill helper:

```bash
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py <baseline-packet.json> <verification-packet.json> --quality-metrics average_completeness_gpt,average_groundedness,average_context_relevance
```

Compare the curated hard-suite packets:

```bash
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py tests/agents/policy-rag/galileo/fixtures/hard-wide-baseline-debug-packet.json tests/agents/policy-rag/galileo/fixtures/hard-focused-risky-debug-packet.json --quality-metrics average_local_answer_score
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py tests/agents/policy-rag/galileo/fixtures/hard-wide-baseline-debug-packet.json tests/agents/policy-rag/galileo/fixtures/hard-balanced-verification-debug-packet.json --quality-metrics average_local_answer_score
```

Curated packet fixtures live under `galileo/fixtures/`; generated fetched
packets and raw run outputs stay ignored.

The first completed RCA is recorded in
`tests/agents/policy-rag/galileo/reports/tokenomics-rca-2026-05-14.md`.
