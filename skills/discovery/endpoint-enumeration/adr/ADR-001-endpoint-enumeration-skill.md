# ADR-001 — Endpoint Enumeration Skill

**File:** `skills/discovery/endpoint-enumeration/adr/ADR-001-endpoint-enumeration-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that reveals the endpoint and
parameter surface of an in-scope web application. Applications expose endpoints and
parameters through rendered pages, client-side scripts, forms, and dynamic
requests. Enumerating these seeds targeted Web Security testing.

This work is active and subject to scope and Rules of Engagement. The skill follows
the Discovery-skill pattern: consume shared infrastructure, consult the Policy
Engine before every action, and produce canonical domain objects along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

The skill is distinct from [Content Discovery](../../content-discovery/README.md),
which enumerates content by wordlist, and from
[API Discovery](../../api-discovery/README.md), which locates API specifications.

---

# Decision

The platform SHALL provide an Endpoint Enumeration Skill in the Discovery tier
that

- Extracts endpoints and parameters through the
  [Browser](../../../shared/browser/README.md) and
  [HTTP Client](../../../shared/http-client/README.md)
- Mines additional parameters within bounds
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every action and proceeds only on `allow`, within the attached rate ceiling
- Produces canonical `endpoint` [Assets](../../../../schemas/asset.md) enriched
  with parameter facts and their relationships
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for hidden-parameter exposure, never without
  Evidence

The skill SHALL be tool independent, SHALL NOT test parameters for
vulnerabilities, and SHALL NOT perform HTTP or browser input or output directly.

---

# Alternatives Considered

## Folding Into Content Discovery

Endpoint enumeration could be part of Content Discovery.

Rejected because endpoint and parameter enumeration interprets application
behavior — rendered content, scripts, and dynamic requests — while Content
Discovery enumerates content by wordlist. The signals and techniques differ.

## Testing Parameters During Enumeration

The skill could test discovered parameters for vulnerabilities.

Rejected because parameter testing is intrusive and belongs to the Web Security
tier. Discovery reveals and records the surface, reporting only behavioral
exposure as Findings.

## Unbounded Parameter Mining

The skill could mine parameters without bounds.

Rejected because unbounded mining is noisy and risks disruption. Mining is
bounded and governed by the policy rate ceiling.

---

# Consequences

## Positive

- Produces an evidence-backed map of the endpoint and parameter surface
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Seeds Web Security testing with canonical endpoint Assets
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine, HTTP Client, and Browser
- Parameter mining requires careful bounding and confidence grading

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every action
- Bound request volume and rate
- Produce only canonical domain objects
- Back every Finding with Evidence
- Redact client-side secrets in evidence per Rules of Engagement
- Never act on out-of-scope applications
- Never perform HTTP or browser input or output directly

---

# Future Compatibility

Future versions MAY add source-map correlation, traffic-replay-driven discovery,
and parameter-type inference. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Endpoint Enumeration README](../README.md)
- [Endpoint Enumeration Interface](../interface.md)
- [Endpoint Enumeration Execution Model](../execution.md)
- [Endpoint Enumeration Error Model](../error-model.md)
- [Browser](../../../shared/browser/README.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
