# ADR-001 — Mutual TLS Authentication Skill

**File:** `skills/authentication/mtls/adr/ADR-001-mtls-authentication-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates how an in-scope
service enforces client-certificate (mutual TLS) authentication. Mutual TLS is used
to authenticate clients at the transport layer; weaknesses — optional client
certificates, acceptance of untrusted or expired certificates, absent revocation
checking, and fallback to weaker authentication — undermine that guarantee.

The skill follows the Authentication-tier pattern: consume the `service`,
`endpoint`, and `certificate` [Assets](../../../../schemas/asset.md) produced by
Discovery, consult the [Policy Engine](../../../shared/policy-engine/README.md)
before every target-facing action, drive the shared clients, and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

Unlike other Authentication skills, mutual TLS operates at the transport layer, so
this skill additionally depends on the
[TLS Client](../../../shared/tls-client/README.md) and reuses the canonical
[TLS Connection](../../../../schemas/tls-connection.md),
[Certificate](../../../../schemas/certificate.md), and
[TLS Validation Result](../../../../schemas/tls-validation-result.md) schemas. It is
distinct from [TLS Analysis](../../../discovery/tls-analysis/README.md), which
evaluates server-side TLS posture.

---

# Decision

The platform SHALL provide a Mutual TLS Authentication Skill in the Authentication
tier that

- Observes client-certificate handshakes through the TLS Client and application
  behavior through the HTTP Client
- Consults the Policy Engine before every target-facing action and proceeds only
  on `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Reuses the canonical TLS Connection, Certificate, and TLS Validation Result
  schemas
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with private key material redacted
- Emits Findings with Risk for mutual TLS weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT open connections or perform HTTP
input or output directly, and SHALL NOT persist private key material.

---

# Alternatives Considered

## Folding Mutual TLS Into TLS Analysis

Mutual TLS could be evaluated within TLS Analysis.

Rejected because TLS Analysis evaluates server-side TLS posture during Discovery,
while mutual TLS is a client-authentication mechanism requiring managed client
certificates and authenticated probing. Keeping it in the Authentication tier
preserves layering, while both reuse the same canonical TLS schemas.

## Depending Only On The HTTP Client

The skill could rely on HTTP behavior alone.

Rejected because client-certificate handshakes are a transport-layer concern
observable only through the TLS Client. Depending on the TLS Client is necessary
and consistent with the shared-infrastructure model.

## Exploiting Accepted Certificates

The skill could use an accepted untrusted certificate to access protected
functionality.

Rejected because Authentication-tier testing confirms weaknesses with evidence
without disruptive exploitation. Exploitation belongs to later, explicitly
authorized testing.

---

# Consequences

## Positive

- Produces evidence-backed mutual TLS Findings
- Reuses the Authentication-tier skill pattern and canonical TLS schemas
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Remains tool independent

## Negative

- Introduces dependencies on the Policy Engine, TLS Client, and HTTP Client
- Client-certificate testing requires careful key handling and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Reuse canonical TLS and certificate schemas
- Back every Finding with Evidence
- Redact private key material in evidence
- Reference managed certificates and keys, never inline key material
- Never act on out-of-scope services
- Never open connections or issue requests directly

---

# Future Compatibility

Future versions MAY add certificate-pinning evaluation and client-certificate
lifecycle testing, and MAY correlate with server-side TLS posture from TLS Analysis.
These extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [Mutual TLS Authentication README](../README.md)
- [Mutual TLS Authentication Interface](../interface.md)
- [Mutual TLS Authentication Execution Model](../execution.md)
- [Mutual TLS Authentication Error Model](../error-model.md)
- [TLS Client](../../../shared/tls-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [TLS Validation Result Schema](../../../../schemas/tls-validation-result.md)
