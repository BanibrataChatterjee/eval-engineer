# Fix Plan

## Bounded Change

Describe the smallest proposed change. Name the prompt, tool description,
retriever, guardrail, dataset, metric, or product surface to edit.

## Fix Surface

Classify the fix surface: prompt, tool schema, retriever/ranker/query rewrite,
context assembly, deterministic guardrail, safety or policy filter, adapter/SDK
wiring, metric configuration, custom metric/rubric, or dataset/scorer
normalization.

## Evidence Behind The Change

Link the change back to the traces, spans, sessions, metrics, or datasets that
justify it.

## Metric Contract

State which metric should move after the fix and which related behavior remains
outside that metric's contract.

## Editable Files

List files allowed by `.galileo/config.yml`.

## Non-Goals

State what should not be changed in this iteration.

## Risk

Describe likely regressions and what evidence would reveal them.
