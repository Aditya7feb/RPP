# ADR-001 — Open Redirect Skill

**File:** `skills/web-security/open-redirect/adr/ADR-001-open-redirect-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application performs unsafe redirects to attacker-controllable destinations. Open
redirection (CWE-601) enables phishing, credential harvesting, and token leakage by
sending victims from a trusted origin to an untrusted one.

The skill follows the Web Security-tier pattern: consume the `web-application` and
`endpoint` [Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-601. It reuses the canonical
[HTTP Redirect](../../../../schemas/http-redirect.md) representation.

Confirming an open redirect requires observing that a user-controlled value reaches
the redirect target. The skill SHALL confirm this using a benign controlled probe
destination and SHALL NOT follow a redirect into a harmful destination.

---

# Decision

The platform SHALL provide an Open Redirect Skill in the Web Security tier that

- Observes redirect responses, supplying a benign controlled destination through
  candidate parameters, through the HTTP Client
- Analyzes which parameters control the redirect target and whether destinations are
  validated
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with sensitive tokens redacted
- Emits Findings with Risk for open-redirect weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-601

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT follow a redirect into a harmful destination or harm third
parties.

---

# Alternatives Considered

## Folding Open Redirect Into SSRF

Open redirect could be part of the SSRF skill.

Rejected because open redirect concerns client-side redirection to an untrusted
origin, while SSRF concerns server-side requests to internal resources. The threat
models and impacts differ; separate skills keep each focused, though redirect sinks
MAY feed SSRF analysis.

## Following Redirects To A Live Destination

The skill could follow the redirect to demonstrate impact.

Rejected because following a redirect into a live untrusted destination is unsafe and
may harm third parties. The skill confirms redirection using a benign controlled
destination only.

## Treating Open Redirect As An XSS Sink Only

Open redirect could be evaluated within the XSS skill.

Rejected because open redirect is a distinct weakness with impact independent of
script execution, though `javascript:` redirect sinks MAY be referenced to the XSS
skill.

---

# Consequences

## Positive

- Produces evidence-backed open-redirect Findings
- Reuses the Web Security-tier skill pattern and canonical redirect schema
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Remains non-destructive and tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires a benign controlled probe destination

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm redirection using benign controlled destinations only
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-601
- Never follow a redirect into a harmful destination
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add redirect-chain evaluation and token-leakage classification,
and MAY correlate redirect sinks with XSS and SSRF exploitability. These extensions
SHALL preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Open Redirect README](../README.md)
- [Open Redirect Interface](../interface.md)
- [Open Redirect Execution Model](../execution.md)
- [Open Redirect Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Redirect Schema](../../../../schemas/http-redirect.md)
