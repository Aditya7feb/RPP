# ADR-001 — API Key Authentication Skill

**File:** `skills/authentication/api-keys/adr/ADR-001-api-key-authentication-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates how an in-scope
application handles API keys. API keys are a common authentication mechanism whose
weaknesses — keys in URLs, keys embedded in client code, cleartext transport, and
absent server-side validation or scoping — expose credentials and enable
unauthorized access.

The skill follows the Authentication-tier pattern established by the Session
Management skill: consume the `api`, `endpoint`, and `web-application`
[Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

---

# Decision

The platform SHALL provide an API Key Authentication Skill in the Authentication
tier that

- Observes API key placement, transport, exposure, and validation through the HTTP
  Client
- Consults the Policy Engine before every target-facing action and proceeds only
  on `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with key material redacted
- Emits Findings with Risk for API key weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT persist key material.

---

# Alternatives Considered

## Folding API Key Testing Into API Discovery

Key testing could be part of API Discovery.

Rejected because API Discovery locates API surfaces, while key testing evaluates an
authentication mechanism requiring credential handling and active validation.
Keeping it in the Authentication tier preserves layering.

## Testing All Token Types In One Skill

A single skill could test API keys, JWTs, and OAuth2 tokens.

Rejected because each mechanism has distinct semantics and weaknesses. Separate
skills keep each focused and independently reusable.

## Exploiting Confirmed Weaknesses

The skill could use exposed keys to access protected functionality.

Rejected because Authentication-tier testing confirms weaknesses with evidence
without disruptive exploitation. Exploitation belongs to later, explicitly
authorized testing.

---

# Consequences

## Positive

- Produces evidence-backed API key Findings
- Reuses the Authentication-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Active validation testing requires careful key handling and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Redact key material in evidence
- Reference managed keys, never inline key material
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add key-rotation and revocation testing, key-scope evaluation,
and correlation of exposed keys with discovered client artifacts. These extensions
SHALL preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [API Key Authentication README](../README.md)
- [API Key Authentication Interface](../interface.md)
- [API Key Authentication Execution Model](../execution.md)
- [API Key Authentication Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
