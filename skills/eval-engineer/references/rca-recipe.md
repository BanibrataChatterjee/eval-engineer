# Galileo RCA Recipe

This recipe turns Galileo evidence into a bounded diagnose/fix/verify loop for
agents, RAG apps, workflows, and future AI systems. Use it when a metric,
trace, session, experiment, or log stream shows degraded behavior and the next
action is unclear.

## 1. Start From Fetched Evidence

Use a compact debug packet as the first reasoning surface. A packet should carry
the experiment or log-stream identity, aggregate metrics, trace/span IDs,
dataset or expected behavior, actual output, and metric rationales.

Do not rely on runner stdout as the final source of truth when metrics are
settling. Prefer a fetched packet tied to stable trace, span, session, dataset,
and experiment IDs.

First classify the evidence source:

- controlled experiment: best for known samples, regression cases, and
  before/after verification
- production log stream: best for recurring live failures, user/session slices,
  and discovery of new eval cases
- mixed: production packet for discovery plus experiment packet for controlled
  verification

If the packet does not say where evidence came from, identify that uncertainty
before editing code.

## 2. Name The Metric Contract

Before proposing a fix, state exactly what the selected metric measures and why
it is the right metric for this failure mode.

Examples:

- A tool-selection metric can prove that the chosen tool and arguments are
  policy-aligned.
- A groundedness metric can prove that an answer is supported by retrieved
  context.
- A response-quality metric can prove the final text follows policy or user
  intent.
- A safety metric can prove private, toxic, injected, or otherwise unsafe
  behavior was detected.
- A custom metric can prove a domain-specific business or compliance rule.

If the observed failure is outside the metric's contract, do not call the app
fixed. Create a separate metric, eval, or follow-up for the uncovered behavior.
If the metric is too broad to produce an actionable fix, use the metric as a
smoke test and add a narrower reference-backed, context-backed, or custom eval.

## 3. Compare Expected And Actual Behavior

Extract a compact failure contract:

- expected behavior or ground truth
- actual behavior
- metric value and rationale
- first trace/span where behavior diverged
- dataset row, case ID, production session identity, or log-stream slice
- uncertainty: app bug, metric issue, dataset issue, integration issue, or
  insufficient evidence

Keep each RCA claim grounded in Galileo IDs or links. If a claim cannot be tied
to a trace, span, metric, dataset, experiment, session, or log stream, mark it
as an inference.

## 4. Classify The Fix Surface

Pick the smallest fix surface that matches the evidence:

- prompt or instruction when the model ignored an explicit policy
- tool schema when the tool contract is ambiguous or too permissive
- retriever, ranker, query rewrite, or chunking when RAG context is missing,
  irrelevant, or poorly attributed
- context assembly when the right source exists but is not available to the
  model at answer time
- deterministic guardrail when a model repeatedly selects disallowed actions
- safety or policy filter when the failure is risk-control behavior, not
  generation quality
- adapter or SDK wiring when trace/tool schemas, enum constraints, callbacks,
  scorer jobs, or parallel tool behavior distort what is being evaluated
- metric configuration when the metric is missing, failing, or judging the
  wrong behavior
- custom metric or rubric when the desired behavior is domain-specific and no
  preset metric measures it cleanly
- dataset or scorer normalization when the expected output shape is too narrow
  for semantically correct behavior

Do not keep widening prompts when Galileo shows the model can still violate the
same policy. Escalate from prompt to schema, guardrail, or adapter fixes when
the traces justify it.

## 5. Prove One Narrow Improvement

Verification needs both local and Galileo evidence when possible:

- run the smallest local case that exercises the failure
- run the broader local suite for regressions
- run a fresh Galileo experiment, fetch a fresh log-stream packet, or both
- compare before and after metric values
- compare expected and actual outputs
- compare the first failing span/rationale

Choose verification mode from the evidence source:

- experiment-origin RCA: verify with a fresh controlled experiment and compare
  baseline `debug-packet.json` to `verification-debug-packet.json`
- log-stream-origin RCA: verify with a fresh production slice when safe, and
  create or update a controlled eval case for recurrence
- mixed RCA: use the log stream to prove production relevance and the experiment
  to prove controlled improvement

A successful code diff, prompt diff, local score, or experiment creation is not
enough by itself. The fetched after packet must show the target metric and trace
behavior improved.

## 6. Preserve The Learning

Record only reusable lessons:

- what Galileo showed that local tests hid
- what the metric did and did not cover
- what fix surface actually worked
- what integration behavior affected scoring
- what new eval or metric is needed next
- which production failures should become controlled regression cases

Keep fixture-specific details in reports and current artifacts. Keep durable
patterns in the skill reference and `.galileo/learnings.md`.

## Common Galileo Lessons

- Fetched packets are better RCA inputs than transient runner output.
- Metric presence is not the same as metric coverage; inspect trace/span status
  and rationales.
- A metric can pass while another behavior remains wrong. Treat that as a new
  metric/eval gap, not as evidence that the whole user experience is fixed.
- If no spans are scored, diagnose metric coverage or output normalization
  before diagnosing app behavior.
- If provider behavior is unstable across runs, compare traces before changing
  the app again. The fix may belong in tool availability, schema constraints,
  adapter wiring, or provider-specific execution settings.
