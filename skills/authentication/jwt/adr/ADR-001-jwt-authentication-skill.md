# ADR-001 — JWT Authentication Skill

**File:** `skills/authentication/jwt/adr/ADR-001-jwt-authentication-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates how an in-scope
application issues and validates JSON Web Tokens. JWTs are a widespread stateless
authentication mechanism whose weaknesses — unsigned-token acceptance, algorithm
confusion, weak signing secrets, absent signature or claim validation, and
sensitive payload disclosure — directly undermine authentication.

The skill follows the Authentication-tier pattern established by the Session
Management skill: consume the `api`, `endpoint`, and `web-application`
[Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

Because some JWT checks touch weak-secret analysis, the skill SHALL bound such
analysis by configuration and the Rules of Engagement, avoiding unbounded brute
force.

---

# Decision

The platform SHALL provide a JWT Authentication Skill in the Authentication tier
that

- Observes token issuance and acceptance and analyzes structure, signature, and
  claims through the HTTP Client
- Consults the Policy Engine before every target-facing action and proceeds only
  on `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Bounds any weak-secret analysis by configuration and Rules of Engagement
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with token secrets redacted
- Emits Findings with Risk for JWT weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, SHALL NOT persist token secrets, and SHALL NOT recover secrets through
unbounded brute force.

---

# Alternatives Considered

## Testing JWTs Within OAuth2 And OIDC Skills

JWT validation could be tested only where JWTs appear in OAuth2 or OIDC flows.

Rejected because JWTs are used as bearer tokens independently of those protocols.
A dedicated skill evaluates JWT validation wherever tokens are used, and the OAuth2
and OIDC skills build on its output.

## Unbounded Secret Recovery

The skill could brute force signing secrets to demonstrate weakness.

Rejected because unbounded brute force is disruptive and unsafe. Weak-secret
analysis is bounded by configuration and Rules of Engagement, confirming weakness
without exhaustive recovery.

## Defining A New Token Schema

The skill could define a canonical JWT schema.

Rejected because a token is not a canonical assessment Asset; the skill records
findings and evidence, optionally an `identity` Asset, reusing existing schemas.

---

# Consequences

## Positive

- Produces evidence-backed JWT Findings
- Reuses the Authentication-tier skill pattern
- Bounds sensitive secret analysis safely
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Bounded secret analysis requires careful configuration and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Bound weak-secret analysis by configuration and Rules of Engagement
- Back every Finding with Evidence
- Redact token secrets and full tokens in evidence
- Reference managed tokens, never inline token material
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add JWE encrypted-token evaluation, JWKS-endpoint analysis, and
nested-token evaluation. These extensions SHALL preserve the existing interface and
SHALL maintain backward compatibility.

---

# Related Documents

- [JWT Authentication README](../README.md)
- [JWT Authentication Interface](../interface.md)
- [JWT Authentication Execution Model](../execution.md)
- [JWT Authentication Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
