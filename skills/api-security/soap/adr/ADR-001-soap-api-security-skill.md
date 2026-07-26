# ADR-001 — SOAP API Security Skill

**File:** `skills/api-security/soap/adr/ADR-001-soap-api-security-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The API Security phase requires a domain skill that evaluates the security of an
in-scope SOAP web service. SOAP services are subject to distinct weaknesses: WSDL and
operation exposure, missing WS-Security enforcement, SOAP action and operation-level
authorization gaps, and message-integrity failures.

The skill follows the API Security-tier pattern established by the REST skill: consume
the `api` and `endpoint` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classified with canonical
identifiers and OWASP API Security Top 10 (2023) references.

SOAP messages are XML, so in-depth XML external entity testing is delegated to the
[XXE](../../../web-security/xxe/README.md) Web Security skill; the SOAP skill focuses
on service-boundary authentication, authorization, and exposure concerns.

---

# Decision

The platform SHALL provide a SOAP API Security Skill in the API Security tier that

- Submits bounded SOAP operations across two authorized controlled identities through
  the HTTP Client
- Analyzes WSDL exposure, WS-Security enforcement, action and operation-level
  authorization, and message integrity
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only minimal controlled
  confirmation recorded
- Emits Findings with Risk for SOAP security weaknesses, never without Evidence,
  classified with canonical identifiers and OWASP API Security Top 10 (2023)
  references

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output directly,
SHALL use only authorized controlled identities, and SHALL NOT enumerate or exfiltrate
other principals' data.

---

# Alternatives Considered

## Folding SOAP Into The REST Skill

SOAP could be tested by the REST API Security skill.

Rejected because SOAP has distinct WSDL, WS-Security, and SOAP-action semantics absent
from REST. A dedicated skill keeps each focused while both share the API Security-tier
pattern.

## Duplicating XML External Entity Testing

The skill could perform in-depth XXE testing on SOAP messages.

Rejected because XXE is owned by the dedicated XXE Web Security skill. The SOAP skill
refers external-entity testing to it and focuses on service-boundary concerns.

## Testing Generic Injection Here

The skill could test SQL and command injection against SOAP parameters.

Rejected because those injection classes are owned by dedicated Web Security skills.
The SOAP skill references them rather than duplicating them.

---

# Consequences

## Positive

- Produces evidence-backed SOAP-specific Findings aligned to OWASP API Security
- Reuses the API Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Delegates XXE cleanly to the dedicated skill

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires two authorized controlled test identities

The negative consequences are outweighed by safety and clarity.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Use only authorized controlled identities for authorization testing
- Confirm enforcement gaps with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Refer in-depth external-entity testing to the XXE skill
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers and OWASP API Security references
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add WS-Policy and WS-Trust evaluation, SOAP action spoofing
evaluation, and attachment-handling safety evaluation. These extensions SHALL preserve
the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [SOAP API Security README](../README.md)
- [SOAP API Security Interface](../interface.md)
- [SOAP API Security Execution Model](../execution.md)
- [SOAP API Security Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [XML External Entity](../../../web-security/xxe/README.md)
