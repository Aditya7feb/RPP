# ADR-001 — CSRF Protection Skill

**File:** `skills/authentication/csrf/adr/ADR-001-csrf-protection-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Authentication phase requires a domain skill that evaluates whether an in-scope
web application defends state-changing requests against Cross-Site Request Forgery.
CSRF weaknesses — absent tokens, unvalidated tokens, tokens not bound to the
session, and unsafe cross-origin acceptance — allow an attacker to induce
authenticated victims to perform unwanted state changes.

The skill follows the Authentication-tier pattern established by the Session
Management skill: consume the `web-application` and `endpoint`
[Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline. It reuses the
canonical [HTTP Session](../../../../schemas/http-session.md) and
[HTTP Cookie](../../../../schemas/http-cookie.md) schemas.

Because confirming CSRF touches state-changing endpoints, the skill SHALL confirm
weaknesses without executing harmful state changes.

---

# Decision

The platform SHALL provide a CSRF Protection Skill in the Authentication tier that

- Observes anti-CSRF token issuance and validation, session binding, and origin
  protections through the HTTP Client
- Consults the Policy Engine before every target-facing action and proceeds only
  on `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Confirms weaknesses without executing harmful state changes
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with tokens redacted
- Emits Findings with Risk for CSRF weaknesses, never without Evidence

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT persist tokens or secrets.

---

# Alternatives Considered

## Folding CSRF Testing Into Session Management

CSRF testing could be part of the Session Management skill.

Rejected because CSRF concerns request-forgery defenses on state-changing
endpoints, a distinct concern from session lifecycle. Separate skills keep each
focused, though both reuse the session and cookie schemas.

## Demonstrating Impact By Executing State Changes

The skill could execute a forged state change to demonstrate impact.

Rejected because executing harmful state changes risks disruption. The skill
confirms the absence or non-validation of protections with evidence, deferring any
demonstration to explicitly authorized testing.

## Treating CSRF As A Web Security Concern Only

CSRF could be tested solely in the Web Security tier.

Rejected because CSRF defense is fundamentally an authentication-context concern
tied to session-bound tokens; placing it in the Authentication tier aligns it with
session and cookie evaluation while Web Security builds on its output.

---

# Consequences

## Positive

- Produces evidence-backed CSRF Findings
- Reuses the Authentication-tier skill pattern and canonical session schemas
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms weaknesses without disruptive state changes

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Testing state-changing endpoints requires careful approval gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm weaknesses without executing harmful state changes
- Back every Finding with Evidence
- Redact anti-CSRF tokens in evidence
- Reference managed credentials, never inline secrets
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add double-submit and synchronizer-token differentiation,
SameSite policy-strength grading, and cross-application CSRF evaluation. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [CSRF Protection README](../README.md)
- [CSRF Protection Interface](../interface.md)
- [CSRF Protection Execution Model](../execution.md)
- [CSRF Protection Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Session Schema](../../../../schemas/http-session.md)
- [HTTP Cookie Schema](../../../../schemas/http-cookie.md)
