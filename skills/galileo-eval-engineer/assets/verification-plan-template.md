# Verification Plan

## Baseline

Name the baseline run, session, experiment, metric values, and trace/span
evidence.

## Evidence Source

Name whether the baseline came from a controlled experiment, production log
stream, or mixed source. Preserve the experiment, session, trace, log-stream,
time-window, filter, or dataset identity needed for comparison.

## Commands

List exact local or Galileo commands from `.galileo/config.yml` when available.

## Verification Mode

Choose the verification mode:

- experiment-origin RCA: run a fresh controlled experiment and compare
  `debug-packet.json` to `verification-debug-packet.json`
- log-stream-origin RCA: fetch a fresh production slice when safe and create or
  update a controlled eval case for recurrence
- mixed RCA: use log streams for production relevance and experiments for
  controlled improvement

## Galileo Comparison

Define the before/after comparison: experiments, sessions, metrics, traces, and
expected direction of movement. Use `.galileo/current/debug-packet.json` for the
baseline/current packet and `.galileo/current/verification-debug-packet.json`
for the after-change packet when working in the current set.

## Regression Check

Name the local suite, broader experiment, or log-stream slice that should not
regress.

## Success Criteria

State what must improve, what must not regress, and which grounded evidence will
prove it.

## Follow-Up

List candidate eval cases, monitoring queries, or log-stream slices to inspect
after the fix.
