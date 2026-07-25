# CSRF Protection Skill

**File:** `skills/authentication/csrf/README.md`

**Version:** 1.0.0

---

# Purpose

The CSRF Protection Skill is an Authentication-tier domain skill that evaluates
whether an in-scope web application defends state-changing requests against
Cross-Site Request Forgery within the Robust PenTest Platform (RPP).

It examines whether state-changing endpoints require and correctly validate
anti-CSRF tokens, whether tokens are bound to the session, and whether
same-site and origin protections are present, reporting weaknesses such as missing
tokens, tokens that are not validated, and unsafe cross-origin acceptance.

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery and the canonical
[HTTP Session](../../../schemas/http-session.md) and
[HTTP Cookie](../../../schemas/http-cookie.md) representations. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The CSRF Protection Skill SHALL

- Evaluate anti-CSRF token presence, validation, and session binding
- Evaluate same-site and origin-based protections
- Consume `web-application` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for CSRF weaknesses
- Remain tool independent

---

# Non-Goals

The CSRF Protection Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Execute forged state changes beyond safe confirmation
- Test authorization decisions (that is the Authorization tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; authorization testing belongs to a dedicated skill.

---

# Design Principles

The CSRF Protection Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms weaknesses without executing harmful state changes
- Credential-safe — it never persists tokens or secrets in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

CSRF Protection Skill

├── Policy Gate            → Policy Engine
├── Token Prober          → HTTP Client
├── Validation Analyzer
├── Origin Protection Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe CSRF defenses. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The CSRF Protection Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing token issuance and validation on state-changing endpoints through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing token session binding and same-site and origin protections
- Detecting missing, unvalidated, or replayable tokens
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Application Target And Assets

↓

Consult Policy Engine (per action)

↓

Observe Token Issuance And Validation (HTTP Client)

↓

Analyze Session Binding And Origin Protections

↓

Record Observations → Evidence

↓

Analyze For CSRF Weaknesses

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

credentials_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application base URL.

`assets` reference the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md), including state-changing endpoints under test.

`credentials_ref` MAY reference managed test credentials required to reach
authenticated state-changing endpoints. It SHALL be a reference, never inline
secrets.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types and SHALL NOT
persist tokens or secrets on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- State-changing endpoints that require no anti-CSRF token
- Anti-CSRF tokens that are not validated by the server
- Tokens not bound to the session or replayable across sessions
- Unsafe cross-origin acceptance without same-site or origin checks
- State-changing operations reachable by safe HTTP methods

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with tokens redacted.

---

# Policy Enforcement

The CSRF Protection Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. CSRF testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
The skill SHALL confirm weaknesses without executing harmful state changes, and
SHALL never test out-of-scope applications.

---

# Dependencies

The CSRF Protection Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Session Schema](../../../schemas/http-session.md)
- [HTTP Cookie Schema](../../../schemas/http-cookie.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The CSRF Protection Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- Web Security skills that build on request-forgery context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for CSRF weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The CSRF Protection Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without executing harmful state changes
- Redact anti-CSRF tokens in all evidence
- Produce no Finding without supporting Evidence
- Reference managed credentials, never inline secrets
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and state-changing endpoints
- Provide managed test credentials for authenticated endpoints
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Execute harmful state changes to demonstrate impact
- Test out-of-scope applications

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
- adr/ADR-001-csrf-protection-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Session Management](../sessions/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [HTTP Session](../../../schemas/http-session.md)
- [HTTP Cookie](../../../schemas/http-cookie.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — CSRF Protection Skill](adr/ADR-001-csrf-protection-skill.md)

---

# Future Extensions

Future versions MAY support

- Double-submit and synchronizer-token pattern differentiation
- SameSite policy-strength grading
- Cross-application CSRF evaluation
- Handoff of request-forgery context to Web Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant CSRF Protection Skill produces evidence-backed Findings for CSRF
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming weaknesses without executing harmful state changes, and
never persisting tokens or invoking tools directly.
