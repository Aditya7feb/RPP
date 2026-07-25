# ADR-001 — SAML Authentication Skill

**File:** `skills/authentication/saml/adr/ADR-001-saml-authentication-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates how an in-scope
service provider implements SAML-based single sign-on. SAML remains widely used for
enterprise federation, and its assertion-processing weaknesses — unsigned-assertion
acceptance, signature stripping, XML signature wrapping, and absent audience,
recipient, or replay protections — allow authentication bypass and identity
spoofing.

The skill follows the Authentication-tier pattern: consume the `web-application`,
`endpoint`, and `identity` [Assets](../../../../schemas/asset.md) produced by
Discovery and prior Authentication skills, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

This is the final skill of the Authentication tier. It is distinct from the OAuth2
and OIDC skills, which evaluate token-based federation.

---

# Decision

The platform SHALL provide a SAML Authentication Skill in the Authentication tier
that

- Observes assertion consumption through the HTTP Client
- Analyzes signature validation, signature wrapping and stripping, audience and
  recipient restrictions, replay protection, and transport security
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with assertions and signing material
  redacted
- Emits Findings with Risk for SAML weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT persist assertions or signing material.

---

# Alternatives Considered

## Combining SAML With OAuth2 And OIDC

A single federated-identity skill could cover SAML, OAuth2, and OIDC.

Rejected because SAML is XML-assertion based with distinct signature and wrapping
weaknesses unrelated to token-based flows. A dedicated skill keeps each protocol
focused.

## Providing Generic XML-Signature Analysis Infrastructure

Signature-wrapping analysis could be delivered as shared infrastructure.

Rejected for now because only this skill requires it. Consistent with the
shared-infrastructure rule, such a capability would be extracted only when a second
consumer emerges.

## Exploiting Confirmed Weaknesses

The skill could forge an authenticated session to demonstrate impact.

Rejected because Authentication-tier testing confirms weaknesses with evidence
without disruptive exploitation. Exploitation belongs to later, explicitly
authorized testing.

---

# Consequences

## Positive

- Produces evidence-backed SAML Findings
- Completes the Authentication tier with consistent structure
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Assertion testing requires careful managed-material handling and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Redact assertions and signing material in evidence
- Reference managed assertions and keys, never inline material
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add identity-provider-initiated flow evaluation, metadata trust
evaluation, and single-logout evaluation. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [SAML Authentication README](../README.md)
- [SAML Authentication Interface](../interface.md)
- [SAML Authentication Execution Model](../execution.md)
- [SAML Authentication Error Model](../error-model.md)
- [OIDC Authentication](../../oidc/README.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
