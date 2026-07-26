# ADR-001 — CORS Skill

**File:** `skills/web-security/cors/adr/ADR-001-cors-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application's Cross-Origin Resource Sharing (CORS) configuration safely restricts
which origins may read responses. Misconfigured CORS (CWE-942) — reflecting an
arbitrary `Origin`, allowing credentialed access from untrusted origins, accepting
the `null` origin, or combining a wildcard with credentials — enables cross-origin
theft of authenticated data.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-942.

CORS evaluation probes origin handling with benign untrusted origins and observes
response headers; it is confirmatory and non-destructive. It is distinct from the
CSP skill and the CSRF skill.

---

# Decision

The platform SHALL provide a CORS Skill in the Web Security tier that

- Observes cross-origin response headers, probing with benign untrusted origins,
  through the HTTP Client
- Analyzes origin reflection, `null` origin acceptance, credentialed access,
  wildcard-with-credentials, and permissive methods and headers
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits Findings with Risk for CORS weaknesses, never without Evidence, classified
  with canonical weakness identifiers such as CWE-942

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT perform destructive exploitation.

---

# Alternatives Considered

## Folding CORS Into CSP

CORS could be evaluated alongside CSP.

Rejected because CORS governs cross-origin read access while CSP governs resource
loading; they are distinct controls with distinct weakness taxonomies. Separate
skills keep each focused.

## Demonstrating Cross-Origin Theft

The skill could stage a cross-origin read from an attacker origin to prove impact.

Rejected because staging exploitation infrastructure is intrusive. The skill
confirms unsafe origin handling by observing response headers with benign probes.

## Treating CORS As An API-Only Concern

CORS could be evaluated only in the API Security tier.

Rejected because CORS applies to web applications and APIs alike. The skill evaluates
both, and API Security consumes its output.

---

# Consequences

## Positive

- Produces evidence-backed CORS Findings
- Reuses the Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Remains non-destructive and tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires benign test origins, which SHALL be used only for observation

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-942
- Use test origins only for observation, never for exploitation
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add preflight-behavior evaluation and origin-validation
logic-flaw classification, and MAY correlate credentialed-access impact with
authentication context. These extensions SHALL preserve the existing interface and
SHALL maintain backward compatibility.

---

# Related Documents

- [CORS README](../README.md)
- [CORS Interface](../interface.md)
- [CORS Execution Model](../execution.md)
- [CORS Error Model](../error-model.md)
- [Content Security Policy](../../csp/README.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Header Schema](../../../../schemas/http-header.md)
