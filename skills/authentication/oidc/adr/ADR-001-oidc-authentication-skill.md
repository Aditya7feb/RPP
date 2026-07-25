# ADR-001 — OIDC Authentication Skill

**File:** `skills/authentication/oidc/adr/ADR-001-oidc-authentication-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates the OpenID Connect
identity layer that many applications build atop OAuth2. OIDC introduces ID tokens,
a `nonce`, a discovery document, JWKS, and a UserInfo endpoint. Weaknesses —
unvalidated ID token signatures, missing nonce, absent audience or issuer checks,
and insecure UserInfo handling — allow identity spoofing and replay.

The skill follows the Authentication-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

OIDC builds on OAuth2 authorization behavior evaluated by the
[OAuth2 Authentication](../../oauth2/README.md) skill and on token validation
evaluated by the JWT skill, but SHALL NOT take a package dependency on either;
it focuses on the identity layer.

---

# Decision

The platform SHALL provide an OIDC Authentication Skill in the Authentication tier
that

- Observes discovery, ID token, and UserInfo behavior through the HTTP Client
- Analyzes ID token signature validation, audience and issuer validation, nonce
  enforcement, and identity-claim verification
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with ID tokens and secrets redacted
- Emits Findings with Risk for OIDC weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT persist ID tokens or secrets.

---

# Alternatives Considered

## Combining OIDC With OAuth2

OIDC could be folded into the OAuth2 skill.

Rejected because the identity layer — ID tokens, nonce, discovery, UserInfo — is a
distinct concern with distinct weaknesses. Separate skills keep each focused; OIDC
builds on OAuth2 output conceptually without a package dependency.

## Fully Validating ID Token JWTs Here

The skill could perform in-depth JWT structure and signature analysis.

Rejected because in-depth JWT validation belongs to the JWT skill. This skill
evaluates whether the relying party validates ID tokens correctly, referencing JWT
findings where relevant.

## Exploiting Confirmed Weaknesses

The skill could forge an identity to demonstrate impact.

Rejected because Authentication-tier testing confirms weaknesses with evidence
without disruptive exploitation. Exploitation belongs to later, explicitly
authorized testing.

---

# Consequences

## Positive

- Produces evidence-backed OIDC Findings
- Reuses the Authentication-tier skill pattern
- Keeps OAuth2, OIDC, and JWT concerns cleanly separated
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Identity-flow testing requires careful credential handling and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Redact ID tokens and secrets in evidence
- Reference managed credentials, never inline secrets
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add front-channel and back-channel logout evaluation,
pairwise-subject evaluation, and federation trust evaluation. These extensions SHALL
preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [OIDC Authentication README](../README.md)
- [OIDC Authentication Interface](../interface.md)
- [OIDC Authentication Execution Model](../execution.md)
- [OIDC Authentication Error Model](../error-model.md)
- [OAuth2 Authentication](../../oauth2/README.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
