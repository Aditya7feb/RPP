# ADR-001 — Unrestricted File Upload Skill

**File:** `skills/web-security/file-upload/adr/ADR-001-file-upload-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application safely restricts uploaded files. Unrestricted file upload (CWE-434) can
lead to remote code execution when dangerous file types are accepted and served
executably from a web-accessible location.

Confirming this weakness safely requires demonstrating weak validation without
uploading a functional web shell. The skill therefore uploads inert, non-executable
marker files and analyzes type, content, and storage handling, never uploading or
executing functional malicious payloads.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-434.

---

# Decision

The platform SHALL provide an Unrestricted File Upload Skill in the Web Security tier
that

- Submits inert, non-executable marker files and observes validation through the HTTP
  Client
- Analyzes type, content, and storage validation and unsafe content-type serving
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only inert marker uploads recorded
- Emits Findings with Risk for file upload weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-434

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT upload or execute functional malicious payloads or web
shells.

---

# Alternatives Considered

## Uploading A Web Shell To Prove Impact

The skill could upload a functional web shell to demonstrate execution.

Rejected because uploading a functional web shell is dangerous and could be abused.
Inert markers confirm weak validation safely; execution impact is inferred from
storage and content-type analysis.

## Folding Path Traversal Into File Upload

Upload paths sometimes allow traversal.

Rejected as a merge because path traversal is a distinct weakness owned by the Path
Traversal skill. This skill focuses on type, content, and storage validation and MAY
reference traversal where an upload path enables it.

## Testing Only Extension Filtering

The skill could test only extension-based filtering.

Rejected because content and storage handling are equally important. The skill
evaluates type, content, and storage together.

---

# Consequences

## Positive

- Produces evidence-backed file upload Findings safely
- Reuses the Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms weak validation without uploading malicious payloads

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Impact inference requires careful storage and content-type analysis

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm weak validation with inert, non-executable markers only
- Never upload or execute functional malicious payloads
- Reference managed marker sets, never functional malicious payloads
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-434
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add magic-byte validation modeling and parser-exposure evaluation
for images and documents. These extensions SHALL preserve the existing interface and
SHALL maintain backward compatibility.

---

# Related Documents

- [Unrestricted File Upload README](../README.md)
- [Unrestricted File Upload Interface](../interface.md)
- [Unrestricted File Upload Execution Model](../execution.md)
- [Unrestricted File Upload Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
