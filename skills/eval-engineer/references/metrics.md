# Galileo Metrics Reference

Eval Engineer should choose metrics from the failure contract, not from the
first reference agent. Agent metrics are appropriate for tool-calling failures,
but they are not the default for every AI system.

Docs source: `https://docs.galileo.ai/sdk-api/metrics/metrics`.

## Selection Rule

Start with the question:

```text
What behavior are we trying to improve or verify?
```

Then choose the smallest metric set that directly measures that behavior.
For test suites, write a case-specific metric profile using
`references/metric-profile-checklist.md` and pass the
full expected-output contract to Galileo. The contract should include expected
decision, required
and forbidden citations, required tools, answer constraints,
abstention/permission requirements, risk profile, and quality dimensions. A
generic "quality" string is not enough for grounded RCA.

Examples:

- Wrong tool, wrong arguments, unnecessary tool calls: tool/agent metrics.
- Unsupported final answer: correctness, context adherence, or custom policy
  metric.
- RAG retrieved irrelevant context: context relevance or context precision.
- RAG answer ignores retrieved context: context adherence or chunk attribution
  utilization.
- Output misses required instructions: instruction adherence.
- Output is incomplete: completeness.
- Safety/privacy issue: PII, toxicity, bias, prompt injection, or tone metrics.
- SQL generation issue: SQL correctness, SQL adherence, SQL efficiency, or SQL
  injection.
- Visual output issue: visual quality or visual fidelity.
- Domain-specific rule: custom metric.

## Metric Families

### Agent And Tool Behavior

Use these when the failure is about an agent workflow, action progress, tool
choice, tool arguments, or tool execution.

- `action_advancement`
- `action_completion`
- `agent_efficiency`
- `agent_flow`
- `tool_error_rate`
- `tool_selection_quality`

### Response Quality

Use these when the final answer or model response is the thing being judged.

- `correctness`
- `instruction_adherence`
- `completeness`
- `conversation_quality`
- `ground_truth_adherence`
- `uncertainty`

### RAG And Context Use

Use these when the issue involves retrieved context, grounding, source use, or
closed-domain hallucination.

- `context_adherence`
- `context_relevance`
- `context_precision`
- `chunk_attribution_utilization`

Use `context_relevance` to decide whether retrieval found enough context.
Use `context_adherence` to decide whether the answer stayed grounded in that
context. Use `chunk_attribution_utilization` when the RCA needs to know which
retrieved chunks influenced the answer or whether useful chunks were ignored.

### Safety, Security, And Style

Use these for harmful, private, biased, injected, or tone-related behavior.

- `input_pii`
- `output_pii`
- `input_toxicity`
- `output_toxicity`
- `input_sexism`
- `output_sexism`
- `prompt_injection`
- `input_tone`
- `output_tone`
- `prompt_perplexity`
- `user_intent_change`

### Text Overlap And Ground Truth

Use these when the dataset has an authoritative reference output. Galileo's
docs call out that BLEU, ROUGE, and ground-truth adherence need ground truth in
the experiment dataset.

- `bleu`
- `rouge`
- `ground_truth_adherence`

### SQL

Use these for text-to-SQL and query generation workflows.

- `sql_correctness`
- `sql_adherence`
- `sql_efficiency`
- `sql_injection`

### Vision

Use these for visual or multimodal output quality.

- `visual_quality`
- `visual_fidelity`

### Custom Metrics

Use custom metrics when the desired behavior is domain-specific and no preset
metric measures it cleanly. A policy-answer check, compliance rubric, or
business-process assertion may be better as a custom metric than as a generic
response-quality metric.

## Luna Metrics

Do not use Luna metric variants unless the workspace has Luna-2 enabled and the
user explicitly wants that path. Prefer non-Luna preset metrics for the current
Eval Engineer reference testbeds.

## SDK Drift

The docs may list metrics that the installed SDK enum does not expose yet. When
that happens:

1. Confirm the installed enum with `GalileoMetrics`.
2. Prefer enum constants when available.
3. Use exact metric strings only as a compatibility fallback.
4. Record the fallback and reason in `.galileo/learnings.md`.

## Current Fixture

The current support-agent fixture is tool-calling, so its starter metrics are
agent/tool metrics:

- `agentic_workflow_success`
- `agentic_session_success`
- `tool_selection_quality`
- `tool_error_rate`

Those metrics are fixture-specific, not a general recommendation for all Eval
Engineer use cases.

The agentic RAG fixture uses a broader profile because it tests ambiguity,
privacy, malicious use, prompt injection, stale sources, brand tone,
multi-source integration, counterfactual context, tool flow, and cost. That is
the pattern to copy: map each case to the metrics that can actually detect its
failure mode, then compare cost changes only against the relevant quality and
safety gates.
