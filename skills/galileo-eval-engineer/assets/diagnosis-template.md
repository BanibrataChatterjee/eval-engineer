# Diagnosis

## RCA Summary

State the most likely root cause in one or two sentences. Include whether this
appears to be an app failure, metric issue, dataset issue, integration issue, or
insufficient-evidence case.

## Evidence Source

Name the source type: controlled experiment, production log stream, or mixed.
Include the time window, filters, dataset row, case ID, session, or experiment
identity needed to reproduce the investigation.

## Evidence Links

- Galileo project:
- Log stream:
- Experiment:
- Session:
- Debug packet:
- Verification packet:
- Trace IDs:
- Span IDs:
- Metrics:
- Dataset rows:

## Metric Contract

Name the selected metric or metrics. Explain what each metric measures, why it
is relevant to this failure, and what it does not prove.

## Failure Pattern

Describe the repeated behavior, affected workflow, frequency or sample size,
and which traces/sessions support the claim.

## Expected Versus Actual

- Expected:
- Actual:
- First divergent trace/span/session:

## Metric Reading

List the relevant metric values and explain what each metric does and does not
prove.

## Uncertainty

Call out missing data, weak evidence, conflicting metrics, or follow-up queries
needed before changing code.
