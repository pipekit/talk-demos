# Trace Context Beyond HTTP: Environment Variables as OpenTelemetry Propagation Carriers

[![Pipekit Logo](https://raw.githubusercontent.com/pipekit/talk-demos/main/assets/images/pipekit-logo.png)](https://pipekit.io?utm_campaign=talk-demos)


## The talk
The slide deck for this talk can be found [here](assets/slide-deck.pdf).

The demos and slide source for this talk live in [pellared/otel-env-car-talk](https://github.com/pellared/otel-env-car-talk).

## Abstract

Distributed traces usually carry context in HTTP headers or message metadata, but CI jobs, workflow engines, and build tools also cross process boundaries. This talk shows how OpenTelemetry propagators use environment variables as carriers so launched CLIs, containers, and subprocesses can continue the same trace without a network handoff or custom format.

Starting from a broken HTTP-to-CLI trace, we show how injecting `TRACEPARENT` and extracting it in the child preserves parentage. Captured Argo examples connect a workflow to its workload, reveal timing inside a Docker build, and derive table-level lineage from instrumented SQL spans in a batch pipeline. The carrier supports multiple propagation formats; instrumentation creates spans and records the evidence for lineage. Attendees leave with a practical model for consistent names, safe inherited context, and interoperable process launches. Trace-derived lineage does not replace dedicated lineage tools.

## Details
- **Event:** [Observability Summit Europe 2026](https://events.linuxfoundation.org/observability-summit-europe/program/schedule/)
- **Speakers:** Robert Pająk, Splunk; Alan Clucas, Pipekit
- **Date:** Monday, October 5, 2026
- **Time:** 14:40 - 15:05 CEST
- **Location:** South Hall 3 A, Prague
