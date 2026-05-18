# Tokenomics Fix Plan

## Bounded Change

Describe the smallest proposed cost-reduction change and the exact fix surface:
prompt/context, retriever, model routing, tool policy, retry control, caching,
output contract, metric sampling, metric filtering, or instrumentation.

## Evidence Behind The Change

Link the change to Galileo cost, token, latency, span, trace, session, or metric
evidence.

## Quality Guardrail

Name the metrics and local checks that must stay flat or improve.

## Expected Cost Movement

- Cost:
- Latency:
- Input tokens:
- Output tokens:
- Total tokens:
- Responses or span count:
- Evaluation metric cost:

## Editable Files

List files allowed by `.galileo/config.yml`.

## Non-Goals

State what should not be optimized or changed in this iteration.

## Risk

Describe likely regressions, including correctness, grounding, safety, tool
selection, answer completeness, and observability loss.

## Rollback Criteria

State which quality regression, missing evidence, cost non-improvement, or
instrumentation loss would make this change unsafe to keep.

