# ADR-001 — Structured Logging Abstraction

**File:** `skills/shared/logging/adr/ADR-001-structured-logging-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

Every component of the Robust PenTest Platform produces operational output:
lifecycle transitions, network activity, execution progress, and
security-relevant observations. Without a shared mechanism, this output would be

- Unstructured and difficult to correlate
- Inconsistent across packages
- At risk of leaking secrets such as credentials and tokens
- Impossible to trace end-to-end across an assessment

Before this decision, components could emit ad hoc log output directly. That
approach produced inconsistent formats, no correlation, and no guaranteed
redaction.

The platform requires a single, canonical, implementation-independent mechanism
to emit structured, correlated, redacted log events.

---

# Decision

The platform SHALL provide a dedicated Logging shared skill that centralizes all
operational logging behind a stable interface.

The Logging shared skill SHALL

- Compose canonical [Log Event](../../../../schemas/log-event.md) records
- Inject correlation identifiers from execution context
- Redact secrets before emission, unconditionally
- Grade events by severity and category
- Route events to configured sinks through adapters
- Preserve an accurate audit trail

Consumers SHALL emit operational logs exclusively through the
[Logging Interface](../interface.md). Sink implementations SHALL remain hidden
behind adapters so that consumers remain unaware of destinations.

Logging SHALL be expressed through a canonical schema, consistent with the
platform's schema-first architecture, and SHALL NOT replace the
[Finding schema](../../../../schemas/finding.md) or the
[Evidence](../../evidence/README.md) shared package.

---

# Alternatives Considered

## Ad Hoc Per-Component Logging

Each component could emit its own output.

Rejected because it produces inconsistent formats, no correlation, and no
guaranteed redaction, risking credential leakage.

## Logging As Evidence

Log output could serve as the evidence record.

Rejected because logging and evidence have different lifecycles and guarantees.
Evidence is authoritative and reference-linked; logs are observability records.
Conflating them would weaken both.

## Log Severity As Risk

Security risk could be encoded in log severity.

Rejected because operational severity and security risk are distinct. Risk is
expressed by the Finding schema; log severity reflects operational significance
only. A `security_event` category preserves audit relevance without implying a
confirmed finding.

---

# Consequences

## Positive

- Uniform, structured, correlated logging across every package
- Guaranteed redaction of secrets before emission
- End-to-end traceability across an assessment
- Sink independence through adapters
- Clear separation between logs, evidence, and findings

## Negative

- Consumers MUST route logs through the interface
- An additional shared dependency is introduced
- Mandatory redaction adds minor composition overhead

The negative consequences are outweighed by the safety, consistency, and
observability benefits.

---

# Compliance

Consumers SHALL

- Emit structured events through the Logging Interface
- Never place secrets in messages or attributes
- Use `security_event` for audit-relevant observations rather than findings
- Rely on automatic correlation injection

All packages SHOULD depend on the Logging shared skill for operational output
and SHALL NOT emit unstructured output directly.

---

# Future Compatibility

Future versions MAY introduce sampling, distributed trace propagation, and
per-category structured payloads. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Logging README](../README.md)
- [Logging Interface](../interface.md)
- [Logging Execution Model](../execution.md)
- [Logging Error Model](../error-model.md)
- [Log Event Schema](../../../../schemas/log-event.md)
- [Evidence](../../evidence/README.md)
- [Finding Schema](../../../../schemas/finding.md)
