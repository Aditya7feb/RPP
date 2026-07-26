# ADR-001 — Content Security Policy Skill

**File:** `skills/web-security/csp/adr/ADR-001-content-security-policy-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates the strength and
correctness of an in-scope application's Content Security Policy (CSP). A CSP is a
defense-in-depth control that constrains the sources from which scripts and other
resources may load. Weak or misconfigured policies (CWE-693) — missing policies,
`unsafe-inline` or `unsafe-eval`, wildcard sources, and missing directives —
provide little protection against script injection.

The skill follows the Web Security-tier pattern established by the Clickjacking
skill: consume the `web-application` and `endpoint`
[Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-693.

CSP evaluation is response-based and non-intrusive. It is distinct from the
Clickjacking skill, which focuses on framing protection, and the XSS skill, which
tests script execution; the XSS skill consumes CSP context to assess exploitability.

---

# Decision

The platform SHALL provide a Content Security Policy Skill in the Web Security tier
that

- Observes the `Content-Security-Policy` header and meta policy through the HTTP
  Client
- Analyzes directive coverage, source-list strength, unsafe sources, known
  bypasses, and enforcement mode
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits Findings with Risk for CSP weaknesses, never without Evidence, classified
  with canonical weakness identifiers such as CWE-693

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT perform destructive exploitation.

---

# Alternatives Considered

## Folding CSP Into The XSS Skill

CSP evaluation could be part of the XSS skill.

Rejected because CSP is a distinct control with its own weakness taxonomy, and it
protects against more than cross-site scripting. Keeping it separate lets the XSS
skill consume CSP context while CSP evaluation remains focused and reusable.

## Folding Framing Protection Into CSP

`frame-ancestors` overlaps with the Clickjacking skill.

Rejected as a merge because framing protection also relies on `X-Frame-Options`,
which is independent of CSP. The Clickjacking skill owns framing protection; this
skill evaluates the full policy and MAY reference `frame-ancestors` strength.

## Executing Payloads To Prove Bypass

The skill could inject scripts to prove a CSP bypass.

Rejected because script execution belongs to the XSS skill and is intrusive. This
skill confirms policy weaknesses through analysis and evidence.

---

# Consequences

## Positive

- Produces evidence-backed CSP Findings
- Reuses the Web Security-tier skill pattern
- Provides CSP context that improves XSS exploitability assessment
- Remains non-intrusive and tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Overlaps conceptually with Clickjacking on `frame-ancestors`, requiring clear
  delineation

The negative consequences are outweighed by consistency and clarity.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-693
- Never perform destructive exploitation
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add nonce and hash-based strength grading, Trusted Types
evaluation, and reporting-endpoint configuration evaluation. These extensions SHALL
preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Content Security Policy README](../README.md)
- [Content Security Policy Interface](../interface.md)
- [Content Security Policy Execution Model](../execution.md)
- [Content Security Policy Error Model](../error-model.md)
- [Clickjacking](../../clickjacking/README.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Header Schema](../../../../schemas/http-header.md)
