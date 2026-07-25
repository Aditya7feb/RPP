# ADR-001 — OAuth2 Authentication Skill

**File:** `skills/authentication/oauth2/adr/ADR-001-oauth2-authentication-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates how an in-scope
application implements OAuth2 authorization flows. OAuth2 is a widely deployed
delegation protocol whose weaknesses — loose redirect-URI validation, missing
anti-forgery `state`, absent PKCE on public clients, discouraged grant types, and
insecure token handling — enable token theft and account compromise.

The skill follows the Authentication-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline. It reuses the canonical
[HTTP Redirect](../../../../schemas/http-redirect.md) representation for redirect
analysis.

The skill focuses on OAuth2 authorization behavior. Identity-layer specifics belong
to the OIDC skill, and in-depth JWT validation belongs to the JWT skill; both build
on this skill's output.

---

# Decision

The platform SHALL provide an OAuth2 Authentication Skill in the Authentication tier
that

- Observes authorization and token flows through the HTTP Client
- Analyzes redirect-URI validation, `state` usage, PKCE enforcement, grant-type
  hygiene, token transport, and scope enforcement
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with tokens and client secrets
  redacted
- Emits Findings with Risk for OAuth2 weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT persist tokens or client secrets.

---

# Alternatives Considered

## Combining OAuth2 And OIDC

OAuth2 and OpenID Connect could be a single skill.

Rejected because OIDC adds an identity layer (ID tokens, UserInfo, discovery) atop
OAuth2. Separating them keeps each focused; the OIDC skill depends on OAuth2 flow
context conceptually and is documented as a distinct skill.

## Validating JWTs In Depth Here

The skill could fully validate access-token JWTs.

Rejected because in-depth JWT structure and signature validation belong to the JWT
skill. This skill evaluates OAuth2 flow behavior and token handling, referencing JWT
findings where relevant.

## Exploiting Confirmed Weaknesses

The skill could complete a token-theft chain to demonstrate impact.

Rejected because Authentication-tier testing confirms weaknesses with evidence
without disruptive exploitation. Exploitation belongs to later, explicitly
authorized testing.

---

# Consequences

## Positive

- Produces evidence-backed OAuth2 Findings
- Reuses the Authentication-tier skill pattern and canonical redirect schema
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Keeps OAuth2, OIDC, and JWT concerns cleanly separated

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Flow testing requires careful credential handling and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Redact tokens and client secrets in evidence
- Reference managed credentials, never inline secrets
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add device-authorization and client-credentials grant
evaluation, token-introspection and revocation analysis, and rich
authorization-request evaluation. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [OAuth2 Authentication README](../README.md)
- [OAuth2 Authentication Interface](../interface.md)
- [OAuth2 Authentication Execution Model](../execution.md)
- [OAuth2 Authentication Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Redirect Schema](../../../../schemas/http-redirect.md)
