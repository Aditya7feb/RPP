# REST API Security Skill

**File:** `skills/api-security/rest/README.md`

**Version:** 1.0.0

---

# Purpose

The REST API Security Skill is an API-Security-tier domain skill that evaluates the
security of an in-scope REST API within the Robust PenTest Platform (RPP).

It focuses on API-specific weaknesses drawn from the OWASP API Security Top 10 (2023)
— broken object level authorization, broken function level authorization, broken
object property level authorization (mass assignment and excessive data exposure),
and unrestricted resource consumption — reporting weaknesses confirmed through
bounded, non-destructive verification.

The skill consumes the `api` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The REST API Security Skill SHALL

- Evaluate object-level and function-level authorization on REST operations
- Evaluate object property level authorization, including mass assignment and
  excessive data exposure
- Evaluate resource-consumption controls such as pagination and rate limiting
- Consume `api` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for API security weaknesses
- Remain tool independent

---

# Non-Goals

The REST API Security Skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints (that is Discovery)
- Test generic injection such as SQL, command, or template injection (those are Web
  Security skills)
- Test cross-site scripting or request forgery (those are Web Security skills)
- Enumerate or exfiltrate other principals' data beyond minimal confirmation
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; generic injection and client-side weaknesses belong to Web Security skills.

---

# Design Principles

The REST API Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same API behavior
- Conservative — it confirms authorization gaps with minimal, controlled reads
- Privacy-preserving — it uses only authorized controlled identities
- Tool independent

---

# Architecture

```
API Security Agent

↓

REST API Security Skill

├── Policy Gate            → Policy Engine
├── Operation Prober      → HTTP Client
├── Object Authorization Analyzer
├── Function Authorization Analyzer
├── Property Authorization Analyzer
├── Resource Consumption Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe API authorization behavior. It SHALL
remain unaware of any transport implementation.

---

# Responsibilities

The REST API Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Exercising REST operations across two controlled identities through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing object-level, function-level, and property-level authorization
- Analyzing resource-consumption controls
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive API Target And Assets

↓

Consult Policy Engine (per action)

↓

Exercise Operations Across Controlled Identities (HTTP Client)

↓

Analyze Object, Function, And Property Authorization

↓

Record Observations → Evidence

↓

Analyze For API Security Weaknesses

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

specification_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope REST API base URL.

`assets` reference the `api` and `endpoint`
[Assets](../../../schemas/asset.md) under test.

`identities_ref` MAY reference two authorized, controlled test identities used for
authorization testing. It SHALL be a reference, never inline credentials.

`specification_ref` MAY reference a discovered API specification that enumerates
operations and properties.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It MAY enrich `endpoint`
[Assets](../../../schemas/asset.md) with operation and property facts and SHALL NOT
invent Asset types.

---

# Produced Findings

These weaknesses align with the OWASP API Security Top 10 (2023), primarily API1
(BOLA), API3 (BOPLA), and API5 (BFLA), and with the OWASP Top 10 (2021) category
A01:2021 – Broken Access Control. These references are informational and do not change
capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Broken object level authorization on a REST resource (CWE-639)
- Broken function level authorization on a privileged operation (CWE-285)
- Mass assignment permitting modification of protected properties (CWE-915)
- Excessive data exposure returning more than the caller requires (CWE-213)
- Unrestricted resource consumption due to missing pagination or rate limiting
  (CWE-770)

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

The REST API Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. API testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted. The
skill SHALL use only authorized controlled identities and SHALL NOT enumerate or
exfiltrate other principals' data. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The REST API Security Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Transaction Schema](../../../schemas/http-transaction.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The REST API Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The API Security Agent and API-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for API security weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The REST API Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Use only authorized controlled identities for authorization testing
- Confirm authorization gaps with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Reference managed identities, never inline credentials
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and OWASP API Security references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` Assets, a discovered specification, and two controlled
  identities
- Rely on the skill for API-specific authorization evaluation
- Route generic injection and client-side testing to Web Security skills
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
- adr/ADR-001-rest-api-security-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [API Discovery](../../discovery/api-discovery/README.md)
- [Insecure Direct Object Reference](../../web-security/idor/README.md)

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

- [ADR-001 — REST API Security Skill](adr/ADR-001-rest-api-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Sensitive business-flow abuse evaluation
- Specification-driven operation and property modeling
- API inventory and versioning-exposure evaluation
- Correlation with Discovery API inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant REST API Security Skill produces evidence-backed Findings for
API-specific authorization and resource-consumption weaknesses while acting strictly
within scope and Rules of Engagement through the Policy Engine, using only controlled
identities, and never enumerating others' data or invoking tools directly.
