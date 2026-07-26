# ADR-001 — SQL Injection Skill

**File:** `skills/web-security/sqli/adr/ADR-001-sql-injection-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application is vulnerable to SQL injection (SQLi). SQLi (CWE-89) allows an attacker
to alter backend query structure through unsafe handling of user input, leading to
authentication bypass, data disclosure, and data modification.

Confirming SQLi requires injecting input and observing error-based, boolean-based,
or time-based signals. The skill follows the Web Security-tier pattern: consume the
`web-application`, `endpoint`, and `api` [Assets](../../../../schemas/asset.md)
produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-89. It reuses the canonical
[HTTP Timing](../../../../schemas/http-timing.md) representation for time-based
signals.

Because SQLi can be highly destructive, the skill confirms injectability using
bounded, non-destructive probes and SHALL NOT extract, modify, or destroy data.
Time-based probes SHALL bound induced delays to avoid disruption.

---

# Decision

The platform SHALL provide a SQL Injection Skill in the Web Security tier that

- Injects bounded probes and observes error-based, boolean-based, and time-based
  signals through the HTTP Client
- Confirms injectability without extracting, modifying, or destroying data
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with the confirming signal recorded
- Emits Findings with Risk for SQL injection weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-89

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT extract, modify, or destroy data.

---

# Alternatives Considered

## Combining All Injection Classes

SQLi, command injection, and template injection could share one skill.

Rejected because each injection class has distinct signals, contexts, and safe-probe
strategies. Separate skills keep each focused and independently governable.

## Extracting Data To Prove Impact

The skill could extract records to demonstrate impact.

Rejected because data extraction is intrusive and may expose sensitive data.
Confirming injectability through bounded signals is sufficient and safe; any
authorized data-shape confirmation is deferred to a stricter, explicitly approved
future capability.

## Unbounded Time-Based Delays

The skill could induce large delays to make blind injection obvious.

Rejected because unbounded delays risk disruption and denial of service. Delays are
bounded and confirmed through repeated measurement.

---

# Consequences

## Positive

- Produces evidence-backed SQLi Findings across error, boolean, and time signals
- Reuses the Web Security-tier skill pattern and canonical timing schema
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms injectability safely without touching data

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Time-based confirmation requires careful bounding and noise reduction

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm injectability without extracting or altering data
- Bound time-based probe delays
- Reference managed probe sets, never inline data-extraction payloads
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-89
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add second-order confirmation, out-of-band confirmation via
controlled collectors, and database-technology-aware signal modeling. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [SQL Injection README](../README.md)
- [SQL Injection Interface](../interface.md)
- [SQL Injection Execution Model](../execution.md)
- [SQL Injection Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Timing Schema](../../../../schemas/http-timing.md)
