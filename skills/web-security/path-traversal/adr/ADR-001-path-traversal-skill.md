# ADR-001 — Path Traversal Skill

**File:** `skills/web-security/path-traversal/adr/ADR-001-path-traversal-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application allows access to files outside an intended directory. Path traversal
(CWE-22) enables reading configuration, source, or credential files by escaping a
base directory through traversal sequences.

Confirming traversal safely requires reaching a location outside the intended base
without reading sensitive data. The skill therefore confirms traversal by reading a
non-sensitive marker resource and SHALL NOT read or exfiltrate sensitive files.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-22.

---

# Decision

The platform SHALL provide a Path Traversal Skill in the Web Security tier that

- Injects bounded traversal and encoded-traversal probes targeting a non-sensitive
  marker through the HTTP Client
- Analyzes canonicalization adequacy and marker reads outside the intended base
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only non-sensitive marker reads
  recorded
- Emits Findings with Risk for path traversal weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-22

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT read, exfiltrate, or modify sensitive files.

---

# Alternatives Considered

## Reading A Known Sensitive File To Prove Impact

The skill could read a well-known sensitive file to demonstrate impact.

Rejected because reading sensitive files is intrusive and may expose confidential
data. A non-sensitive marker confirms traversal safely.

## Folding Path Traversal Into File Upload Or Inclusion

Path traversal could be part of a broader file-handling skill.

Rejected because path traversal is a distinct weakness with its own probe strategy.
Separate skills keep each focused, though traversal sinks MAY feed inclusion and
upload analysis.

## Unbounded Traversal Depth

The skill could attempt arbitrary traversal depth.

Rejected because unbounded depth is noisy and unnecessary. Depth is bounded by
configuration.

---

# Consequences

## Positive

- Produces evidence-backed path traversal Findings safely
- Reuses the Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms traversal without touching sensitive data

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires a non-sensitive marker resource for confirmation

The negative consequences are outweighed by safety and clarity.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm traversal using non-sensitive markers only
- Never read, exfiltrate, or modify sensitive files
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-22
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add absolute-path and null-byte classification and
archive-extraction traversal evaluation. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Path Traversal README](../README.md)
- [Path Traversal Interface](../interface.md)
- [Path Traversal Execution Model](../execution.md)
- [Path Traversal Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
