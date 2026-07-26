# ADR-001 — REST API Security Skill

**File:** `skills/api-security/rest/adr/ADR-001-rest-api-security-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The API Security phase requires a domain skill that evaluates the security of an
in-scope REST API. REST APIs are subject to a distinct weakness taxonomy captured by
the OWASP API Security Top 10 (2023) — most prominently broken object level
authorization (API1), broken object property level authorization including mass
assignment and excessive data exposure (API3), broken function level authorization
(API5), and unrestricted resource consumption (API4).

These weaknesses are API-specific and differ from the generic injection and
client-side weaknesses owned by the Web Security tier. The REST API Security skill
therefore focuses on API authorization and resource-consumption concerns and delegates
generic injection, cross-site scripting, and request forgery to the Web Security
skills.

This is the first skill in the API Security tier. It establishes the pattern for that
tier: consume the `api` and `endpoint` [Assets](../../../../schemas/asset.md) produced
by Discovery, consult the [Policy Engine](../../../shared/policy-engine/README.md)
before every target-facing action, drive the
[HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline. Authorization testing
uses two authorized controlled identities and confirms gaps with minimal reads,
consistent with the privacy-preserving methodology of the IDOR skill.

---

# Decision

The platform SHALL provide a REST API Security Skill in the API Security tier that

- Exercises REST operations across two authorized controlled identities through the
  HTTP Client
- Analyzes object level, function level, and object property level authorization and
  resource-consumption controls
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only minimal controlled
  confirmation recorded
- Emits Findings with Risk for API security weaknesses, never without Evidence,
  classified with canonical identifiers and OWASP API Security Top 10 (2023)
  references

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output directly,
SHALL use only authorized controlled identities, and SHALL NOT enumerate or exfiltrate
other principals' data.

---

# Alternatives Considered

## Folding API Security Into Web Security

REST API weaknesses could be tested by the Web Security skills.

Rejected because API-specific weaknesses — object, function, and property level
authorization and resource consumption — have a distinct taxonomy (OWASP API Security
Top 10) not covered by the generic Web Security skills. Separate tiers keep each
focused; generic injection is delegated to Web Security.

## Enumerating Objects To Prove Impact

The skill could enumerate objects to show broad exposure.

Rejected because enumeration exposes real users' data. Two controlled identities and
minimal reads confirm authorization gaps safely, consistent with the IDOR skill.

## Testing Generic Injection Here

The skill could test SQL, command, and template injection against API parameters.

Rejected because those injection classes are owned by dedicated Web Security skills.
The REST API Security skill references them rather than duplicating them.

---

# Consequences

## Positive

- Produces evidence-backed API-specific Findings aligned to OWASP API Security Top 10
- Establishes the reusable API Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms authorization gaps without exposing real users' data

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires two authorized controlled test identities

The negative consequences are outweighed by safety and clarity.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Use only authorized controlled identities for authorization testing
- Confirm authorization gaps with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers and OWASP API Security references
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add sensitive business-flow abuse evaluation and
specification-driven operation modeling. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [REST API Security README](../README.md)
- [REST API Security Interface](../interface.md)
- [REST API Security Execution Model](../execution.md)
- [REST API Security Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [API Discovery](../../../discovery/api-discovery/README.md)
