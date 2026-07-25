# ADR-001 — Clickjacking Skill

**File:** `skills/web-security/clickjacking/adr/ADR-001-clickjacking-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
web application defends against UI redress (clickjacking) attacks. Clickjacking
(CWE-1021) allows an attacker to frame a target page beneath a deceptive overlay and
trick a victim into performing unintended actions. Defenses are the
`X-Frame-Options` header and the Content Security Policy `frame-ancestors`
directive.

This is the first skill in the Web Security tier. It establishes the pattern for
that tier: consume the `web-application` and `endpoint`
[Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-1021.

Clickjacking is header-and-configuration based and non-intrusive, making it a
suitable first Web Security skill. It is distinct from the CSP skill, which
evaluates the full Content Security Policy, and the CORS skill, which evaluates
cross-origin resource sharing.

---

# Decision

The platform SHALL provide a Clickjacking Skill in the Web Security tier that

- Observes framing-protection headers and directives through the HTTP Client
- Identifies sensitive pages framable by untrusted origins
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits Findings with Risk for clickjacking weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-1021

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT perform destructive exploitation.

---

# Alternatives Considered

## Folding Clickjacking Into The CSP Skill

Clickjacking could be part of the CSP skill.

Rejected because framing protection also relies on `X-Frame-Options`, which is
independent of CSP, and clickjacking is a distinct weakness class. The CSP skill
evaluates the full policy; this skill focuses on framing protection and page
sensitivity.

## Demonstrating Impact With A Framing Proof-Of-Concept

The skill could host a framing page to demonstrate exploitation.

Rejected because hosting exploitation infrastructure is intrusive and unnecessary.
The skill confirms the absence or weakness of framing controls with evidence.

## Treating Clickjacking As An Authentication Concern

Clickjacking could be placed with session or CSRF skills.

Rejected because clickjacking is a response-hardening web-security weakness distinct
from authentication. Placing it in the Web Security tier preserves layering.

---

# Consequences

## Positive

- Produces evidence-backed clickjacking Findings
- Establishes the reusable Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Remains non-intrusive and tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Overlaps conceptually with CSP `frame-ancestors`, requiring clear delineation

The negative consequences are outweighed by consistency and clarity.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-1021
- Never perform destructive exploitation
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add frame-busting robustness evaluation and nested-framing
evaluation, and MAY correlate with CSP `frame-ancestors` strength grading. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [Clickjacking README](../README.md)
- [Clickjacking Interface](../interface.md)
- [Clickjacking Execution Model](../execution.md)
- [Clickjacking Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Header Schema](../../../../schemas/http-header.md)
