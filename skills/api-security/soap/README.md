# SOAP API Security Skill

**File:** `skills/api-security/soap/README.md`

**Version:** 1.0.0

---

# Purpose

The SOAP API Security Skill is an API-Security-tier domain skill that evaluates the
security of an in-scope SOAP web service within the Robust PenTest Platform (RPP).

It focuses on SOAP-specific weaknesses — WSDL and operation exposure, WS-Security
enforcement, SOAP action and message-level authorization, and XML message-handling
safety — reporting weaknesses confirmed through bounded, non-destructive verification
aligned to the OWASP API Security Top 10 (2023).

The skill consumes the `api` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The SOAP API Security Skill SHALL

- Evaluate WSDL and operation exposure
- Evaluate WS-Security enforcement and message-level authentication
- Evaluate SOAP action and operation-level authorization across identities
- Evaluate XML message-handling safety at the service boundary
- Consume `api` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for SOAP security weaknesses
- Remain tool independent

---

# Non-Goals

The SOAP API Security Skill SHALL NOT

- Perform HTTP input or output directly
- Discover services or endpoints (that is Discovery)
- Perform in-depth XML external entity testing (that is the XXE Web Security skill)
- Test generic injection such as SQL or command injection (those are Web Security
  skills)
- Enumerate or exfiltrate other principals' data beyond minimal confirmation
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; XML external entity testing belongs to the XXE skill; generic injection belongs
to Web Security skills.

The authentication boundary is explicit. This skill verifies authentication
*presence* and *enforcement* on the SOAP surface — whether WS-Security or an
equivalent control is required and enforced for a given operation — and it verifies
authorization *behavior* across identities. The correctness of the underlying
authentication mechanisms and protocols (OAuth2, OIDC, JWT, SAML, mTLS, Sessions, and
API Keys) is owned by the Authentication tier, which SHALL evaluate protocol
correctness. This skill SHALL NOT assess authentication-protocol correctness.

---

# Design Principles

The SOAP API Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same service behavior
- Conservative — it confirms authorization and enforcement gaps with minimal reads
- Privacy-preserving — it uses only authorized controlled identities
- Tool independent

---

# Architecture

```
API Security Agent

↓

SOAP API Security Skill

├── Policy Gate            → Policy Engine
├── Operation Prober      → HTTP Client
├── WSDL Exposure Analyzer
├── WS-Security Analyzer
├── Action Authorization Analyzer
├── Message Safety Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe SOAP behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The SOAP API Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting bounded SOAP operations across two controlled identities through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing WSDL exposure, WS-Security enforcement, and action authorization
- Confirming enforcement gaps with minimal, controlled reads
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Service Target And Assets

↓

Consult Policy Engine (per action)

↓

Submit Bounded Operations Across Controlled Identities (HTTP Client)

↓

Analyze WSDL Exposure, WS-Security, And Action Authorization

↓

Record Observations → Evidence

↓

Analyze For SOAP Security Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced Finding SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

assets:

identities_ref:

wsdl_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope SOAP service endpoint URL.

`assets` reference the `api` and `endpoint`
[Assets](../../../schemas/asset.md) under test.

`identities_ref` MAY reference two authorized, controlled test identities. It SHALL be
a reference, never inline credentials.

`wsdl_ref` MAY reference a discovered WSDL that enumerates operations and bindings.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It MAY enrich the `api`
[Asset](../../../schemas/asset.md) with operation facts and SHALL NOT invent Asset
types.

---

# Produced Findings

These weaknesses align with the OWASP API Security Top 10 (2023), primarily API2
(Broken Authentication), API5 (BFLA), and API8 (Security Misconfiguration), and with
the OWASP Top 10 (2021) categories A05:2021 – Security Misconfiguration and A01:2021 –
Broken Access Control. These references are informational and do not change capability
scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- WSDL and operation detail publicly exposed without authentication (CWE-200)
- WS-Security not enforced, permitting unauthenticated message processing (CWE-306)
- SOAP action or operation-level authorization not enforced across identities
  (CWE-285)
- Message-level signature or integrity not validated (CWE-347)
- Verbose SOAP faults disclosing implementation detail (CWE-209)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only minimal controlled confirmation recorded and sensitive content redacted.

---

# OWASP API Security Top 10 (2023) Coverage Boundaries

The following OWASP API Security Top 10 (2023) categories are intentionally delegated
or deferred rather than assessed by this skill; no capability is lost.

- API6:2023 (Unrestricted Access to Sensitive Business Flows) SHALL be deferred to the
  future Business Logic capability, whose evaluation depends on per-application
  workflow modeling.
- API9:2023 (Improper Inventory Management) SHALL be primarily owned by API Discovery
  in the Discovery tier, which inventories `api` and `endpoint` Assets.
- API10:2023 (Unsafe Consumption of APIs) SHALL be deferred to a future API Security
  extension.

---

# Policy Enforcement

The SOAP API Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Operation probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted. The
skill SHALL use only authorized controlled identities and SHALL NOT enumerate or
exfiltrate other principals' data. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The SOAP API Security Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Transaction Schema](../../../schemas/http-transaction.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The SOAP API Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The API Security Agent and API-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for SOAP security weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The SOAP API Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Use only authorized controlled identities for authorization testing
- Confirm enforcement gaps with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Reference managed identities, never inline credentials
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and OWASP API Security references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` Assets, a discovered WSDL, and two controlled identities
- Rely on the skill for SOAP-specific evaluation
- Route XML external entity and generic injection testing to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Enumerate or exfiltrate other principals' data
- Test out-of-scope targets

---

# Documentation Requirements

This skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-soap-api-security-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [API Discovery](../../discovery/api-discovery/README.md)
- [XML External Entity](../../web-security/xxe/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — SOAP API Security Skill](adr/ADR-001-soap-api-security-skill.md)

---

# Future Extensions

Future versions MAY support

- WS-Policy and WS-Trust evaluation
- SOAP action spoofing and routing evaluation
- Attachment-handling safety evaluation
- Correlation with Discovery API inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SOAP API Security Skill produces evidence-backed Findings for
SOAP-specific weaknesses while acting strictly within scope and Rules of Engagement
through the Policy Engine, using only controlled identities, and never enumerating
others' data or invoking tools directly.
