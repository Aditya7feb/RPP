# ADR-001 — Cross-Site Scripting Skill

**File:** `skills/web-security/xss/adr/ADR-001-xss-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application is vulnerable to cross-site scripting (XSS). XSS (CWE-79) allows an
attacker to execute script in a victim's browser through reflected, stored, or
DOM-based injection, leading to session theft, account takeover, and content
manipulation.

Confirming XSS requires injecting input and observing whether it executes.
Reflected and stored contexts require observing responses, while DOM-based contexts
require observing client-side rendering. The skill therefore drives both the
[HTTP Client](../../../shared/http-client/README.md) and the
[Browser](../../../shared/browser/README.md), making it the first Web Security skill
to depend on the Browser.

The skill follows the Web Security-tier pattern: consume the `web-application` and
`endpoint` [Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-79.

Because exploitation could be harmful, the skill confirms execution using bounded,
non-destructive marker payloads drawn from a managed set, never weaponized payloads,
and treats stored-injection testing as higher impact.

---

# Decision

The platform SHALL provide a Cross-Site Scripting Skill in the Web Security tier that

- Injects bounded marker payloads through the HTTP Client and observes execution
  through the Browser
- Analyzes output context and encoding adequacy for reflected, stored, and DOM-based
  contexts
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  gating stored-injection testing accordingly
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with the confirming marker recorded
- Emits Findings with Risk for XSS weaknesses, never without Evidence, classified
  with canonical weakness identifiers such as CWE-79

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output or
browser rendering directly, and SHALL NOT deliver weaponized payloads or perform
destructive exploitation.

---

# Alternatives Considered

## Using Only The HTTP Client

XSS could be confirmed from responses alone.

Rejected because DOM-based XSS executes only in the browser and reflected execution
is best confirmed by rendering. Depending on the Browser enables reliable,
low-false-positive confirmation.

## Injecting Weaponized Payloads

The skill could inject full exploitation payloads to demonstrate impact.

Rejected because weaponized payloads are harmful and unnecessary for confirmation.
Bounded, non-destructive markers confirm execution safely.

## Folding CSP Evaluation Into XSS

CSP strength could be evaluated here.

Rejected because CSP is a distinct control owned by the CSP skill. This skill MAY
consume CSP context to grade exploitability without a package dependency.

---

# Consequences

## Positive

- Produces evidence-backed XSS Findings across reflected, stored, and DOM contexts
- Reuses the Web Security-tier skill pattern and adds Browser-based confirmation
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms execution safely with bounded markers

## Negative

- Introduces a dependency on the Browser in addition to the HTTP Client
- Stored-injection testing requires careful approval gating

The negative consequences are outweighed by confirmation reliability and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm execution with bounded, non-destructive markers only
- Reference managed payload sets, never inline weaponized payloads
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-79
- Gate stored-injection testing per the Rules of Engagement
- Never act on out-of-scope targets
- Never issue HTTP requests or render directly

---

# Future Compatibility

Future versions MAY add context-aware payload synthesis, blind and out-of-band
confirmation via controlled collectors, and framework-specific sink modeling. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [Cross-Site Scripting README](../README.md)
- [Cross-Site Scripting Interface](../interface.md)
- [Cross-Site Scripting Execution Model](../execution.md)
- [Cross-Site Scripting Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Browser](../../../shared/browser/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Content Security Policy](../../csp/README.md)
