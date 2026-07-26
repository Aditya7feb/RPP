# ADR-001 — Insecure Deserialization Skill

**File:** `skills/web-security/deserialization/adr/ADR-001-deserialization-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application unsafely deserializes user-controllable data. Insecure deserialization
(CWE-502) can lead to remote code execution when untrusted serialized objects are
processed by an unsafe deserializer.

Confirming this weakness safely requires demonstrating that serialized input is
processed without delivering a functional gadget chain. The skill therefore confirms
unsafe processing using bounded, non-destructive probes — an out-of-band interaction
to a controlled collector, corroborated by response and timing differentials — and
SHALL NOT deliver a gadget chain or execute code.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-502. It reuses the canonical
[HTTP Timing](../../../../schemas/http-timing.md) representation.

---

# Decision

The platform SHALL provide an Insecure Deserialization Skill in the Web Security tier
that

- Submits bounded serialized probes and observes out-of-band and differential signals
  through the HTTP Client
- Confirms unsafe processing without delivering a gadget chain
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the high impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only bounded probe interaction
  recorded
- Emits Findings with Risk for insecure deserialization weaknesses, never without
  Evidence, classified with canonical weakness identifiers such as CWE-502

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT deliver a functional gadget chain or execute code.

---

# Alternatives Considered

## Delivering A Gadget Chain To Prove Impact

The skill could deliver a functional gadget chain to demonstrate code execution.

Rejected because gadget chains are dangerous and could be abused. Bounded probes with
out-of-band and differential confirmation prove unsafe processing safely.

## Relying Solely On Response Differentials

The skill could infer deserialization from differentials alone.

Rejected as a default because differentials are noisy. Out-of-band confirmation is the
primary signal where an authorized collector is available, corroborated by bounded
differentials.

## Combining All Injection Classes

Deserialization could share a skill with command and template injection.

Rejected because deserialization has distinct serialized-input semantics and
safe-probe strategies. Separate skills keep each focused.

---

# Consequences

## Positive

- Produces evidence-backed deserialization Findings safely
- Reuses the Web Security-tier skill pattern and canonical timing schema
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms unsafe processing without gadget chains

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Reliable confirmation benefits from an authorized out-of-band collector

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm unsafe processing with bounded, non-destructive probes only
- Never deliver a functional gadget chain or execute code
- Reference managed probe sets and authorized collectors only
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-502
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add format-specific serialized-object modeling and type-restriction
evaluation. These extensions SHALL preserve the existing interface and SHALL maintain
backward compatibility.

---

# Related Documents

- [Insecure Deserialization README](../README.md)
- [Insecure Deserialization Interface](../interface.md)
- [Insecure Deserialization Execution Model](../execution.md)
- [Insecure Deserialization Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Timing Schema](../../../../schemas/http-timing.md)
