# Metric Profile Checklist

Use this before optimizing, fixing, or expanding an eval suite for a RAG app,
agent, workflow, chat system, or domain assistant.

Do not optimize cost before this checklist is complete. If the metric profile is
missing, the RCA can accidentally make the system cheaper while it stops
measuring the failure mode.

## Required Case Fields

Every meaningful case or production segment should define:

- `risk_profile`: the risk being tested, such as `pii_disclosure`,
  `stale_policy`, `malicious_use`, `brand_and_tone`, `multi_source_rag`,
  `tool_loop`, or `low_risk_faq`
- `quality_dimensions`: the dimensions that must not regress, such as
  `answer_quality`, `retrieval_quality`, `safety`, `privacy`,
  `agent_performance`, `source_authority`, `brand`, and `cost`
- `galileo_metrics`: the Galileo metrics intended to measure the case
- `expected_decision`: the expected route, refusal, action, or answer type
- `required_citations`: sources that must be retrieved, used, or cited
- `forbidden_citations`: stale, untrusted, irrelevant, or unsafe sources
- `required_tools`: tools or workflow steps required for this risk profile
- `required_answer_terms`: obligations that must appear in the answer
- `forbidden_answer_terms`: unsafe, stale, private, or misleading claims
- `must_abstain`: whether the correct behavior is to refuse, clarify, or defer
- `must_be_permission_safe`: whether permission/role safety is required

## Metric Mapping

### Answer Quality

- Use `correctness`, `ground_truth_adherence`, `instruction_adherence`, and
  `completeness` when the answer must match an expected decision or contract.
- Add a custom metric when the desired behavior is domain-specific and generic
  answer metrics cannot see it.

### RAG Grounding

- Use `context_relevance` when retrieval may miss required context.
- Use `context_adherence` when the answer may hallucinate or ignore retrieved
  context.
- Use `chunk_attribution_utilization` when the RCA needs to know which chunks
  influenced the answer or whether useful chunks were ignored.
- Track required and forbidden citations locally when source authority matters.

### Safety And Compliance

- Use `prompt_injection` for retrieved instructions, jailbreaks, or
  instruction-conflict cases.
- Use `input_pii` and `output_pii` for privacy and data-disclosure cases.
- Use toxicity, tone, or custom policy metrics for malicious-use, brand, or
  compliance-sensitive cases.
- Keep deterministic gates for permission safety, abstention correctness, and
  forbidden answer terms.

### Agent Performance

- Use `agent_efficiency`, `agent_flow`, `tool_selection_quality`, and
  `tool_error_rate` when the system plans, calls tools, retries, routes, or
  performs multi-step work.
- Track tool-call count, retry count, span count, self-check count, rerank
  count, and agent steps locally for tokenomics RCA.

### Cost And Latency

- Track `average_cost`, `average_latency`, input/output/total tokens, retrieved
  context tokens, retrieved document count, tool-call count, and evaluator cost.
- Compare cost only after the relevant quality, safety, grounding, and
  performance metrics are named.
- Require a segment-level acceptance gate for mixed traffic. A cheaper aggregate
  run is not acceptable if a high-risk segment regresses.

## Acceptance Gate

Before keeping a fix or cost-reduction candidate, state:

1. Which case or segment is being optimized.
2. Which metrics prove quality, safety, grounding, and performance.
3. Which cost metrics should move.
4. Which metrics are higher-is-better and which are lower-is-better.
5. Which segment-level acceptance gate prevents hidden regressions.
6. Which metric gap remains if Galileo or the local packet cannot measure the
   risk directly.

Use `assets/metric-profile-template.md` when writing this into an RCA artifact,
fixture README, or eval dataset proposal.
