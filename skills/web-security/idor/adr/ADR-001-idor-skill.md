# ADR-001 — Insecure Direct Object Reference Skill

**File:** `skills/web-security/idor/adr/ADR-001-idor-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application enforces per-object authorization on object references. Insecure direct
object references (CWE-639) allow one principal to access another principal's
resources by changing an identifier, a leading cause of broken object-level
authorization.

Confirming IDOR safely requires demonstrating unauthorized access without exposing
real users' data. The skill therefore uses two authorized, controlled test identities
and confirms that one can access the other's object with a minimal read, never
enumerating or exfiltrating other principals' data.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-639.

---

# Decision

The platform SHALL provide an Insecure Direct Object Reference Skill in the Web
Security tier that

- Requests object references across two authorized controlled identities through the
  HTTP Client
- Analyzes whether per-object authorization is enforced and whether identifiers are
  predictable
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only minimal controlled
  confirmation recorded
- Emits Findings with Risk for IDOR weaknesses, never without Evidence, classified
  with canonical weakness identifiers such as CWE-639

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, SHALL use only authorized controlled identities, and SHALL NOT enumerate or
exfiltrate other principals' data.

---

# Alternatives Considered

## Enumerating Object Identifiers To Prove Impact

The skill could enumerate identifiers to show broad exposure.

Rejected because enumeration exposes real users' data and is intrusive. Two
controlled identities and a minimal read confirm the weakness safely.

## Testing With A Single Identity

The skill could infer IDOR from one identity's behavior.

Rejected because confirming unauthorized cross-principal access requires comparing two
identities. Two controlled identities provide reliable, privacy-preserving
confirmation.

## Folding IDOR Into Authentication Testing

IDOR could be part of the Authentication tier.

Rejected because IDOR is an object-level authorization weakness, distinct from
authentication. It belongs to the Web Security tier and MAY consume authentication
context.

---

# Consequences

## Positive

- Produces evidence-backed IDOR Findings without exposing real users' data
- Reuses the Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms unauthorized access with minimal, controlled reads

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires two authorized controlled test identities

The negative consequences are outweighed by safety and privacy preservation.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Use only authorized controlled identities and their own references
- Confirm unauthorized access with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Reference managed identities, never inline credentials
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-639
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add vertical privilege-escalation object-access modeling and
object-identifier-pattern classification. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Insecure Direct Object Reference README](../README.md)
- [Insecure Direct Object Reference Interface](../interface.md)
- [Insecure Direct Object Reference Execution Model](../execution.md)
- [Insecure Direct Object Reference Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
