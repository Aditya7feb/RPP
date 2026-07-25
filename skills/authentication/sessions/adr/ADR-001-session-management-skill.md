# ADR-001 — Session Management Skill

**File:** `skills/authentication/sessions/adr/ADR-001-session-management-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates how an in-scope web
application manages sessions. Session management is a frequent source of
weaknesses — insecure cookie attributes, session fixation, predictable
identifiers, and absent invalidation — that undermine authentication regardless of
credential strength.

This is the first skill in the Authentication tier. It establishes the pattern for
that tier: consume the `web-application` and `endpoint`
[Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

The skill reuses the canonical
[HTTP Session](../../../../schemas/http-session.md) and
[HTTP Cookie](../../../../schemas/http-cookie.md) schemas rather than defining new
representations.

---

# Decision

The platform SHALL provide a Session Management Skill in the Authentication tier
that

- Observes session issuance, cookie attributes, and lifecycle through the HTTP
  Client
- Consults the Policy Engine before every target-facing action and proceeds only
  on `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Reuses the canonical HTTP Session and HTTP Cookie schemas
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with secrets redacted
- Emits Findings with Risk for session-management weaknesses, never without
  Evidence
- MAY record an `identity` Asset for a confirmed authenticated context

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT persist session secrets.

---

# Alternatives Considered

## Folding Session Testing Into Discovery

Session testing could be part of Content Discovery.

Rejected because session management is an authentication concern that requires
authenticated states and credential handling, which are out of scope for
Discovery. Keeping it in the Authentication tier preserves layering.

## Defining New Session And Cookie Representations

The skill could define its own session and cookie models.

Rejected because canonical HTTP Session and HTTP Cookie schemas already exist.
Reuse avoids duplication and keeps evidence interoperable.

## Exploiting Confirmed Weaknesses

The skill could exploit weaknesses such as fixation to demonstrate impact.

Rejected because Discovery-adjacent authentication testing confirms weaknesses with
evidence without disruptive exploitation. Exploitation belongs to later, explicitly
authorized testing.

---

# Consequences

## Positive

- Produces evidence-backed session-management Findings
- Establishes the reusable Authentication-tier skill pattern
- Reuses canonical session and cookie schemas
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Authenticated testing requires careful credential handling and approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Reuse canonical session and cookie schemas
- Back every Finding with Evidence
- Redact session identifiers and secrets in evidence
- Reference managed credentials, never inline secrets
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add single-sign-on session evaluation, token-binding analysis,
and concurrent-session testing. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Session Management README](../README.md)
- [Session Management Interface](../interface.md)
- [Session Management Execution Model](../execution.md)
- [Session Management Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Session Schema](../../../../schemas/http-session.md)
- [HTTP Cookie Schema](../../../../schemas/http-cookie.md)
