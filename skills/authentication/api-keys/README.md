# API Key Authentication Skill

**File:** `skills/authentication/api-keys/README.md`

**Version:** 1.0.0

---

# Purpose

The API Key Authentication Skill is an Authentication-tier domain skill that
evaluates how an in-scope application issues, transports, and validates API keys
within the Robust PenTest Platform (RPP).

It examines where API keys are placed, how they are transmitted, whether they are
exposed to clients, and whether the server validates them correctly, reporting
weaknesses such as keys in URLs, keys embedded in client-side code, cleartext
transport, and absent validation or scoping.

The skill consumes the `api`, `endpoint`, and `web-application`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The API Key Authentication Skill SHALL

- Evaluate API key placement, transport, exposure, and validation
- Consume `api`, `endpoint`, and `web-application` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for API key weaknesses
- Remain tool independent

---

# Non-Goals

The API Key Authentication Skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints (that is Discovery)
- Test OAuth2, OIDC, or JWT bearer tokens (those are dedicated skills)
- Test authorization decisions (that is the Authorization tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; token-protocol and authorization testing belong to dedicated skills.

---

# Design Principles

The API Key Authentication Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists key material in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

API Key Authentication Skill

├── Policy Gate            → Policy Engine
├── Key Placement Prober   → HTTP Client
├── Exposure Analyzer
├── Validation Analyzer
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe API key handling. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The API Key Authentication Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing API key placement and transport through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing client-side exposure and server-side validation
- Detecting keys in URLs, keys in client code, and weak validation
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Target And Assets

↓

Consult Policy Engine (per action)

↓

Observe API Key Placement And Transport (HTTP Client)

↓

Analyze Client Exposure And Server Validation

↓

Record Observations → Evidence

↓

Analyze For API Key Weaknesses

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

api_key_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope API or application base URL.

`assets` reference the `api`, `endpoint`, and `web-application`
[Assets](../../../schemas/asset.md) under test.

`api_key_ref` MAY reference a managed test API key. It SHALL be a reference, never
an inline key.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types and SHALL NOT
persist API key material on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- API keys transmitted in URLs or query strings
- API keys embedded in client-side code or public artifacts
- API keys transmitted over cleartext transport
- Missing or weak server-side key validation
- Keys without scope, expiry, or rotation
- Keys accepted without rate limiting contrary to Rules of Engagement

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with key material redacted.

---

# Policy Enforcement

The API Key Authentication Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Key testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope targets SHALL never be tested.

---

# Dependencies

The API Key Authentication Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The API Key Authentication Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- API Security skills that build on key-handling context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for API key weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The API Key Authentication Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Redact API key material in all evidence
- Produce no Finding without supporting Evidence
- Reference managed keys, never inline key material
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` Assets and a managed test key
- Rely on the skill for API key evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide inline key material
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
- adr/ADR-001-api-key-authentication-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Session Management](../sessions/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — API Key Authentication Skill](adr/ADR-001-api-key-authentication-skill.md)

---

# Future Extensions

Future versions MAY support

- Key-rotation and revocation testing
- Key-scope and least-privilege evaluation
- Correlation of exposed keys with discovered client artifacts
- Handoff of key context to API Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant API Key Authentication Skill produces evidence-backed Findings for API
key weaknesses while acting strictly within scope and Rules of Engagement through
the Policy Engine, never persisting key material or invoking tools directly.
