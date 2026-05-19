# Tokenomics RCA

Use this sub-workflow when the user asks to reduce cost, latency, token usage,
model spend, retry waste, retrieval bloat, or evaluation cost for any RAG,
agent, workflow, or chat implementation.

Tokenomics RCA is not generic cost cutting. The goal is to reduce spend while
preserving measured behavior.

## Evidence To Read

Start from `.galileo/current/debug-packet.json` and, when available,
`.galileo/current/verification-debug-packet.json`.

Before proposing cost reductions, complete the metric-profile checklist in
`references/metric-profile-checklist.md` for the case, route, or segment being
optimized. Use `assets/metric-profile-template.md` when the profile needs to be
written into an RCA artifact.

Read these Galileo evidence fields when present:

- `average_cost`, `total_cost`, or cost charts/alerts
- `average_latency`, `total_latency`, span `duration_ns`, or time to first token
- `average_num_input_tokens`, `average_num_output_tokens`,
  `average_num_total_tokens`
- `total_responses`, trace count, session count, and span counts by type
- LLM span model names, input/output/total tokens, duration, status code, and
  tool definitions passed to the model
- retriever span document counts, retrieved context size, status, and metadata
- retrieved source IDs, source authority, and forbidden retrieved sources when
  privacy, prompt injection, stale policy, or source authority is part of the
  quality contract
- tool span counts, arguments, status, duration, and error patterns
- agent tool loops: LLM span count, tool-call count, retry count, failed-call
  share, and whether each step advances the task
- configured quality metrics such as tool selection, action completion,
  correctness, groundedness, context adherence, instruction adherence, safety,
  or custom domain metrics
- case-specific metric profiles that map each fixture or route to the quality,
  safety, performance, and cost metrics that can detect its failure mode
- RAG answer-quality metrics such as completeness, groundedness, and context
  relevance when reducing retrieved context
- multi-hop and case-level RAG results when context pruning could remove one
  of several required sources or obligations
- metric direction: higher-is-better quality metrics such as groundedness and
  lower-is-better quality metrics such as `tool_error_rate`, toxicity,
  hallucination, or policy violation rate
- log-stream metric sampling settings when the cost includes evaluation cost
- evaluator cost metrics, metric sampling rate, and whether sampled quality
  still represents the route, segment, or task being optimized

Galileo can surface cost, latency, and status as default alert metrics; trace
and span logging can include duration and token counts; and log-stream metric
sampling controls the cost of LLM-based evaluation in production.

## RCA Questions

Answer these in order before proposing a fix:

1. **What got expensive?**
   - cost, latency, input tokens, output tokens, total tokens, request volume,
     evaluator cost, or failures/retries
2. **Where did it happen?**
   - route, trace, session, span type, agent node, model, tool, retriever,
     customer segment, or metric job
   - check segment evidence before trusting an aggregate improvement
3. **Did the spend buy quality?**
   - compare cost drivers with the active quality metrics and Galileo rationales
   - confirm whether each quality gate is higher-is-better or lower-is-better
   - confirm the active metrics actually cover the case risk: grounding,
     correctness, privacy, malicious use, prompt injection, brand tone, tool
     flow, or cost
4. **What is the smallest fix surface?**
   - prompt/context, retriever, model routing, tool policy, retry control,
     caching, output contract, evaluator sampling, or instrumentation
5. **How will we prove it?**
   - require before/after packets with cost deltas and quality deltas

## Evidence To Cost Mapping

| Signal | Likely Waste Pattern | Practical Fix Surface |
| --- | --- | --- |
| High `total_responses` or repeated LLM spans | planning loop, retry loop, unnecessary decomposition | merge steps, add early exit, tighten retry policy, deterministic router |
| High agent step, rerank, planner, or self-check count | one-size-fits-all agent control flow | risk-aware routing, skip self-check on low-risk paths, rerank only for ambiguity/conflict |
| High input tokens | bloated prompt, repeated policies, long history, over-retrieval | prompt compression, history pruning, static prefix caching, lower retriever `top_k` |
| High output tokens | verbose final answer, oversized JSON, unnecessary explanation | concise answer contract, smaller schema, lower max output cap |
| High latency with high output tokens | generation-bound latency | shorter output, streaming, chunked response only when needed |
| High retriever span count or context size | over-retrieval or duplicated context | dedupe, rerank, reduce `top_k`, strip boilerplate, context compression |
| High tool count with weak quality | helper-tool overuse or wrong actions | tool gating, schema tightening, tool-selection eval, remove redundant tools |
| Tool errors or status failures | wasted retries and failed side effects | validate inputs earlier, cap retries, improve error handling |
| Expensive model on simple spans | overpowered model routing | route classification, extraction, or formatting to cheaper model after eval |
| High LLM-judge spend | metrics too broad in production | metric sampling, metric filters, code-based metric, narrower eval slice |
| Cost spike on one segment | production-specific route or customer behavior | segment-specific packet, targeted eval case, route-specific guardrail |
| Lower `total_responses` without per-trace efficiency movement | traffic volume changed, not necessarily waste | segment by workload, compare cost per successful task, avoid treating traffic volume alone as a kept optimization |
| Aggregate quality holds but one segment drops | hidden segment regression | reject the candidate, add segment-specific evals, or route the optimization only to safe segments |

## Fix Surface Recipes

### Prompt And Context

- Move stable instructions, tool schemas, and examples to a stable prefix that
  can benefit from provider prompt caching when supported.
- Remove duplicated policy text, obsolete examples, and old conversation turns.
- Keep dynamic request and retrieved context separate from stable instructions.
- Verify with input token deltas and the relevant quality metric.

### RAG Retrieval

- Count retrieved chunks, document tokens, duplicate sources, and retrieved
  context actually cited or used.
- Lower `top_k` only when context relevance, groundedness, and answer quality do
  not regress.
- Do not judge retrieval safety only from final citations. If an untrusted,
  stale, or injected document enters context, record that as source-authority
  evidence even when the final answer avoided citing it.
- Verify multi-hop and case-level policy questions, not only easy single-source
  questions; an aggregate score can hide a missing source in one high-risk case.
- Prefer dedupe/rerank before summarizing context; summarization can hide needed
  evidence.
- Preserve source IDs so cost reductions remain auditable.
- Do not rely on local deterministic scoring alone after retrieval pruning;
  Galileo quality metrics can catch missing operational clauses that still pass
  coarse term/source checks.

### Agent And Tool Workflows

- Count LLM, tool, retriever, and workflow spans.
- Count agent steps, planner spans, rerank passes, and self-check spans.
- Check whether each tool call advances the task or only gathers unused context.
- Compare low-risk and high-risk routes separately; cost reductions are only
  safe if high-risk routes keep their permission, source-authority, and
  abstention gates.
- Require case-specific metric profiles for mixed agentic RAG suites. A legal
  hold case, a PII case, a malicious-use case, and a low-risk FAQ should not be
  considered equally measured by the same minimal metric list.
- Fix wrong or redundant tools before optimizing model choice; correctness often
  removes wasted steps.
- Use deterministic gates for clear policy constraints rather than asking the
  model to rediscover the same rule every run.

### Model Routing

- Identify spans whose task is classification, routing, extraction, formatting,
  or validation.
- Try cheaper or lower-latency models only for those bounded spans.
- Keep the stronger model for synthesis, high-risk decisions, or ambiguous user
  intent until evals prove otherwise.
- Verify by segment, not only by aggregate.

### Evaluation Cost

- In development, full metric coverage is usually useful.
- In production, configure metric sampling for costly LLM-based metrics while
  preserving all traces.
- Prefer code-based metrics for deterministic contracts.
- Use metric filters so final-answer metrics do not run on every intermediate
  LLM span in a multi-agent workflow.
- Keep route and segment coverage explicit when reducing evaluator cost; cheap
  sampling is not a win if it hides the failure mode being monitored.

## Derived Metrics

Compute these when the packet has enough evidence:

- cost per successful task
- cost per passing eval
- cost per session
- latency per successful task
- input-token share and output-token share
- retriever token share
- retry or failed-call cost share
- tool-call count per successful task
- evaluator cost share
- quality delta per cost delta

Use `scripts/compare_tokenomics_packets.py` to calculate before/after deltas
from two compact packets. Run it without `--quality-metrics` first so it can
infer custom non-cost quality metrics that exist in both packets, then inspect
the `Quality metrics compared` line. Pass explicit quality metrics when the
packet contains numeric fields that should be excluded or when the inferred set
misses the intended gate. Pass lower-is-better quality metrics explicitly when
the name does not already encode direction:

```bash
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py baseline.json verification.json
python3 skills/eval-engineer/scripts/compare_tokenomics_packets.py baseline.json verification.json --quality-metrics average_groundedness,tool_error_rate --lower-is-better-quality-metrics tool_error_rate
```

Do not let wall-clock fields such as `wall_time_ns`, duration fields, token
counts, latency, or cost become quality metrics. They can prove efficiency
movement, but they should not reject a candidate as a quality regression.

## Artifact Workflow

1. Write `.galileo/current/cost-diagnosis.md` using
   `assets/cost-diagnosis-template.md`.
2. Write `.galileo/current/tokenomics-fix-plan.md` using
   `assets/tokenomics-fix-plan-template.md`.
3. Write `.galileo/current/quality-preserving-verification-plan.md` using
   `assets/quality-preserving-verification-template.md`.
4. Run the smallest local or Galileo verification that exercises the suspected
   cost driver.
5. Compare baseline and verification packets.
6. Keep the change only if cost, latency, or token usage improves and the named
   quality metrics do not regress.

## Stop Conditions

Do not optimize yet when:

- the packet lacks cost, token, latency, or span attribution
- the quality metric is missing or outside the behavior being optimized
- the proposed fix would remove evidence needed for safety, compliance,
  correctness, or grounding
- the cost spike is caused by traffic volume rather than per-trace waste and no
  segment is identified
- the only improvement is lower traffic volume or response count, without
  improved cost, latency, token, retry, tool, or evaluator efficiency
- evaluation cost is high but metric sampling/filtering is not yet understood

In those cases, improve instrumentation, packet shape, segmentation, or metric
configuration first.

## Keep Criteria

Keep a tokenomics change only when the after packet proves:

- target cost, token, latency, or evaluation spend moved in the intended
  direction
- target quality metrics stayed flat or improved
- no safety, grounding, correctness, or tool metrics regressed
- the change is bounded to one fix surface
- remaining risks are captured as follow-up eval gaps
