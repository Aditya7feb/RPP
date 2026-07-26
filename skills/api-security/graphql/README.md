# GraphQL API Security Skill

**File:** `skills/api-security/graphql/README.md`

**Version:** 1.0.0

---

# Purpose

The GraphQL API Security Skill is an API-Security-tier domain skill that evaluates the
security of an in-scope GraphQL API within the Robust PenTest Platform (RPP).

It focuses on GraphQL-specific weaknesses — introspection exposure, unbounded query
depth and complexity (resource consumption), field- and object-level authorization,
and batching abuse — reporting weaknesses confirmed through bounded, non-destructive
verification aligned to the OWASP API Security Top 10 (2023).

The skill consumes the `api` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The GraphQL API Security Skill SHALL

- Evaluate introspection exposure and schema disclosure
- Evaluate query depth and complexity controls for resource consumption
- Evaluate field- and object-level authorization across identities
- Evaluate batching and alias-based amplification controls
- Consume `api` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for GraphQL security weaknesses
- Remain tool independent

---

# Non-Goals

The GraphQL API Security Skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints (that is Discovery)
- Test generic injection such as SQL, command, or template injection (those are Web
  Security skills)
- Test cross-site scripting or request forgery (those are Web Security skills)
- Execute unbounded depth or complexity queries that could deny service
- Enumerate or exfiltrate other principals' data beyond minimal confirmation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; generic injection and client-side weaknesses belong to Web Security skills;
denial of service is prohibited.

---

# Design Principles

The GraphQL API Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same API behavior
- Conservative — it confirms depth and complexity gaps with bounded probes, not
  denial of service
- Privacy-preserving — it uses only authorized controlled identities
- Tool independent

---

# Architecture

```
API Security Agent

↓

GraphQL API Security Skill

├── Policy Gate            → Policy Engine
├── Query Prober          → HTTP Client
├── Introspection Analyzer
├── Depth Complexity Analyzer
├── Field Authorization Analyzer
├── Batching Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe GraphQL behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The GraphQL API Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting bounded GraphQL queries across two controlled identities through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing introspection, depth and complexity, authorization, and batching
- Confirming resource-consumption gaps with bounded probes only
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

Submit Bounded Queries Across Controlled Identities (HTTP Client)

↓

Analyze Introspection, Depth, Authorization, And Batching

↓

Record Observations → Evidence

↓

Analyze For GraphQL Security Weaknesses

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

scope_id:

roe_id:
```

`target` SHALL be an in-scope GraphQL API endpoint URL.

`assets` reference the `api` and `endpoint`
[Assets](../../../schemas/asset.md) under test.

`identities_ref` MAY reference two authorized, controlled test identities used for
authorization testing. It SHALL be a reference, never inline credentials.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It MAY enrich the `api`
[Asset](../../../schemas/asset.md) with schema facts and SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with the OWASP API Security Top 10 (2023), primarily API4
(Unrestricted Resource Consumption), API1 (BOLA), API3 (Broken Object Property Level
Authorization), API5 (BFLA), and API8 (Security Misconfiguration), and with the OWASP
Top 10 (2021) categories A05:2021 – Security Misconfiguration and A01:2021 – Broken
Access Control. These references are informational and do not change capability scope.

Because GraphQL exposes data at field granularity, field-level authorization and
field-level data exposure are Broken Object Property Level Authorization (API3:2023)
concerns in addition to object-level authorization (API1:2023). The skill evaluates
both object-level and field-level (property-level) authorization; it does not thereby
expand its capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Introspection enabled in a production environment, disclosing the full schema
  (CWE-200)
- Missing query depth or complexity limits enabling resource exhaustion (CWE-770)
- Object-level authorization not enforced across identities (CWE-285, API1:2023)
- Field-level (property-level) authorization not enforced, exposing fields the caller
  is not entitled to read (CWE-285, API3:2023)
- Batching or alias-based query amplification without controls (CWE-770)
- Verbose errors disclosing schema or implementation detail (CWE-209)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only bounded, minimal confirmation recorded and sensitive content redacted.

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

The GraphQL API Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Query probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Depth and complexity probes SHALL be bounded to avoid denial of service, and the
skill SHALL use only authorized controlled identities. Out-of-scope targets SHALL
never be tested.

---

# Dependencies

The GraphQL API Security Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Transaction Schema](../../../schemas/http-transaction.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The GraphQL API Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The API Security Agent and API-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for GraphQL security weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The GraphQL API Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound depth and complexity probes to avoid denial of service
- Use only authorized controlled identities for authorization testing
- Confirm authorization gaps with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and OWASP API Security references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` Assets and two controlled identities
- Rely on the skill for GraphQL-specific evaluation
- Route generic injection and client-side testing to Web Security skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Execute unbounded depth or complexity queries
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
- adr/ADR-001-graphql-api-security-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [API Discovery](../../discovery/api-discovery/README.md)
- [REST API Security](../rest/README.md)

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

- [ADR-001 — GraphQL API Security Skill](adr/ADR-001-graphql-api-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Schema-driven authorization modeling
- Subscription and mutation-specific evaluation
- Persisted-query and cost-analysis evaluation
- Correlation with Discovery API inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant GraphQL API Security Skill produces evidence-backed Findings for
GraphQL-specific weaknesses while acting strictly within scope and Rules of Engagement
through the Policy Engine, bounding depth and complexity probes, using only controlled
identities, and never denying service or invoking tools directly.
