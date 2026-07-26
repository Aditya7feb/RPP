# ADR-001 — XML External Entity Skill

**File:** `skills/web-security/xxe/adr/ADR-001-xxe-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application unsafely processes XML external entities. XML external entity injection
(CWE-611) can lead to file disclosure, server-side request forgery, and denial of
service depending on parser configuration.

Confirming XXE safely requires demonstrating external-entity resolution without
reading sensitive files. The skill therefore confirms resolution using a bounded,
non-sensitive entity or an out-of-band interaction to a controlled collector, and
SHALL NOT read sensitive files.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-611.

---

# Decision

The platform SHALL provide an XML External Entity Skill in the Web Security tier that

- Submits bounded entity probes referencing non-sensitive or controlled resources and
  observes resolution through the HTTP Client
- Analyzes in-band and out-of-band resolution signals
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the high impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only non-sensitive resolution
  recorded
- Emits Findings with Risk for XXE weaknesses, never without Evidence, classified
  with canonical weakness identifiers such as CWE-611

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT read, exfiltrate, or modify sensitive files.

---

# Alternatives Considered

## Folding XXE Into SSRF

XXE can be a vector for server-side request forgery.

Rejected as a merge because XXE is a distinct XML-parsing weakness with file-
disclosure and denial-of-service impacts beyond request forgery. The SSRF skill owns
general request forgery; this skill owns XML entity processing and MAY reference SSRF
where an XXE enables it.

## Reading A Sensitive File To Prove Impact

The skill could resolve an entity to a sensitive file to demonstrate disclosure.

Rejected because reading sensitive files is intrusive. A non-sensitive marker or
out-of-band interaction confirms resolution safely.

## Testing Entity Expansion By Default

The skill could test billion-laughs entity expansion.

Rejected as a default because entity-expansion testing risks denial of service.
Expansion exposure is deferred to a stricter, explicitly approved future capability.

---

# Consequences

## Positive

- Produces evidence-backed XXE Findings safely
- Reuses the Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms resolution without touching sensitive data

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Blind confirmation requires an authorized out-of-band collector

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm resolution using non-sensitive or controlled resources only
- Never read, exfiltrate, or modify sensitive files
- Reference managed markers and authorized collectors only
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-611
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add parameter-entity and blind-XXE confirmation via richer
out-of-band channels and document-type-definition configuration analysis. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [XML External Entity README](../README.md)
- [XML External Entity Interface](../interface.md)
- [XML External Entity Execution Model](../execution.md)
- [XML External Entity Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
