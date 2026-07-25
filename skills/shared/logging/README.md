# Logging Shared Skill

**File:** `skills/shared/logging/README.md`

**Version:** 1.0.0

---

# Purpose

The Logging Shared Skill provides the canonical, implementation-independent
mechanism for emitting structured, correlated log events within the Robust
PenTest Platform (RPP).

Rather than allowing individual skills and shared packages to emit ad hoc log
output, this shared skill centralizes structured logging, correlation,
redaction, severity handling, and log observability.

All packages SHALL emit operational logs through this shared skill.

---

# Goals

The Logging Shared Skill SHALL

- Abstract logging behind a stable interface
- Produce structured [Log Event](../../../schemas/log-event.md) records
- Correlate events with assessment, task, and execution context
- Redact secrets before emission
- Grade events by severity and category
- Route events to configured sinks
- Integrate with platform observability

---

# Non-Goals

The Logging Shared Skill SHALL NOT

- Detect vulnerabilities
- Produce security findings
- Interpret log content as risk
- Perform target-facing network operations
- Persist evidence as a substitute for the Evidence package

Logging records what happened. It SHALL NOT replace the
[Finding schema](../../../schemas/finding.md) or the
[Evidence](../evidence/README.md) shared package.

---

# Design Principles

The Logging Shared Skill SHALL be

- Structured
- Correlatable
- Deterministic in field composition
- Transport independent
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill or Shared Package

↓

Logging Shared Skill

├── Event Builder
├── Correlation Injector
├── Redaction Filter
├── Severity Gate
├── Sink Router
├── Event Manager

↓

Configured Sinks
```

The Logging Shared Skill composes and routes events but SHALL remain unaware of
sink implementations.

---

# Responsibilities

The Logging Shared Skill is responsible for

- Composing structured [Log Event](../../../schemas/log-event.md) records
- Injecting correlation identifiers from execution context
- Applying redaction before emission
- Enforcing severity and category gating
- Routing events to configured sinks
- Linking events to evidence where applicable

---

# Logging Lifecycle

```
Receive Log Request

↓

Compose Event

↓

Inject Correlation

↓

Apply Redaction

↓

Evaluate Severity Gate

├── Below Threshold → Drop

└── At/Above Threshold → Route To Sinks

↓

Emit Event
```

Redaction SHALL always precede routing.

---

# Correlation

The Logging Shared Skill SHALL inject correlation identifiers from the execution
context, including assessment, task, request, execution, and span identifiers,
as defined in the [Log Event schema](../../../schemas/log-event.md).

Correlation enables end-to-end tracing across packages.

---

# Redaction

The Logging Shared Skill SHALL redact secret material before any event is
emitted.

Redaction SHALL apply to messages, attributes, and extensions.

Redacted fields SHALL be recorded in the event `redaction.fields` list.

Secrets SHALL never reach a sink.

---

# Severity And Category

The Logging Shared Skill SHALL grade every event by

- `severity` reflecting operational significance
- `category` reflecting the nature of the event

`security_event` category SHALL denote a security-relevant observation for
audit purposes and SHALL NOT be treated as a confirmed finding.

---

# Sinks

The Logging Shared Skill SHALL route events to configured sinks.

Sink implementations SHALL be hidden behind adapters. Consumers SHALL remain
unaware of whether events are routed to files, streams, collectors, or platform
services.

---

# Evidence Linkage

Where an event corresponds to captured evidence, the Logging Shared Skill SHOULD
set `evidence_ref` to link the event to evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

# Events

The Logging Shared Skill emits structured
[Log Event](../../../schemas/log-event.md) records. It SHOULD also expose
internal counters for observability, including emitted, dropped, and redacted
event counts.

---

# Dependencies

The Logging Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Log Event Schema](../../../schemas/log-event.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Logging Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Every package MAY consume the Logging Shared Skill, including

- All shared packages
- All discovery, authentication, web-security, API, and cloud skills
- Agent framework components

---

# Outputs

Typical outputs MAY include

- Structured log events routed to sinks
- Correlation-linked traces
- Log metrics

Outputs SHALL remain implementation independent.

---

# Security Principles

The Logging Shared Skill SHALL

- Redact secrets before emission
- Never route secret material to any sink
- Preserve an accurate audit trail
- Distinguish operational severity from security risk
- Bound log volume to prevent resource exhaustion

Logging sensitive material can cause credential leakage. The shared skill SHALL
enforce redaction unconditionally.

---

# Best Practices

Consumers SHOULD

- Emit structured events rather than free-form strings
- Rely on automatic correlation injection
- Reference evidence rather than embedding large payloads
- Use `security_event` for audit-relevant observations
- Choose severity by operational significance

---

# Anti-Patterns

Consumers SHOULD NOT

- Emit secrets or credentials
- Use logging to store findings
- Emit unstructured, uncorrelated output
- Duplicate evidence in log attributes
- Bypass the shared skill with direct output

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-structured-logging-abstraction.md

---

# Related Shared Packages

- [Evidence](../evidence/README.md)
- [HTTP Client](../http-client/README.md)
- [Retry](../retry/README.md)
- [Rate Limiter](../rate-limiter/README.md)

---

# Canonical Schemas

- [Log Event](../../../schemas/log-event.md)
- [Evidence](../../../schemas/evidence.md)
- [Execution State](../../../schemas/execution-state.md)

---

# Architecture Decisions

- [ADR-001 — Structured Logging Abstraction](adr/ADR-001-structured-logging-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Sampling and adaptive verbosity
- Distributed trace propagation standards
- Structured log schemas per category
- Log-derived metrics pipelines

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Logging Shared Skill provides a structured, correlated, and
implementation-independent logging abstraction for the Robust PenTest Platform.

It enables consistent observability across every package while enforcing
redaction, preserving auditability, and never leaking secrets.
