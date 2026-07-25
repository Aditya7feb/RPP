# Session Management Skill

**File:** `skills/authentication/sessions/README.md`

**Version:** 1.0.0

---

# Purpose

The Session Management Skill is an Authentication-tier domain skill that evaluates
the security of an in-scope web application's session management within the Robust
PenTest Platform (RPP).

It examines how session identifiers are issued, transported, protected, renewed,
and terminated, and reports weaknesses such as insecure cookie attributes, session
fixation, predictable identifiers, and absent invalidation on logout.

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery and the canonical
[HTTP Session](../../../schemas/http-session.md) and
[HTTP Cookie](../../../schemas/http-cookie.md) representations. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Session Management Skill SHALL

- Evaluate session identifier issuance, transport, protection, renewal, and
  termination
- Consume `web-application` and `endpoint` Assets and canonical HTTP Session and
  Cookie representations
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for session-management weaknesses
- Remain tool independent

---

# Non-Goals

The Session Management Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test authentication token formats such as JWT (that is the JWT skill)
- Test authorization decisions (that is the Authorization tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; token-format and authorization testing belong to dedicated skills.

---

# Design Principles

The Session Management Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists session secrets in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

Session Management Skill

├── Policy Gate            → Policy Engine
├── Session Prober         → HTTP Client
├── Cookie Analyzer
├── Lifecycle Analyzer
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk · (optional) identity Assets
```

The skill orchestrates the HTTP Client to observe session behavior. It SHALL
remain unaware of any transport implementation.

---

# Responsibilities

The Session Management Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing session issuance and cookie attributes through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing [HTTP Cookie](../../../schemas/http-cookie.md) attributes and
  [HTTP Session](../../../schemas/http-session.md) lifecycle
- Detecting session fixation, predictable identifiers, and absent invalidation
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

Observe Session Issuance And Cookies (HTTP Client)

↓

Analyze Cookie Attributes And Session Lifecycle

↓

Record Observations → Evidence

↓

Analyze For Session-Management Weaknesses

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
[Assets](../../../schemas/asset.md) under test.

`credentials_ref` MAY reference managed test credentials required to reach
authenticated session states. It SHALL be a reference, never inline secrets.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. Where it confirms a distinct authenticated
identity context, it MAY record an `identity`
[Asset](../../../schemas/asset.md) with provenance. It SHALL NOT invent other
Asset types and SHALL NOT persist session secrets on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Session cookies missing `Secure`, `HttpOnly`, or `SameSite` attributes
- Session identifiers transmitted over cleartext transport
- Session fixation — the identifier is not rotated after authentication
- Predictable or low-entropy session identifiers
- Sessions not invalidated on logout or after timeout
- Overly long session lifetimes contrary to Rules of Engagement

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with session secrets redacted.

---

# Policy Enforcement

The Session Management Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Session testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope applications SHALL never be tested.

---

# Dependencies

The Session Management Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Session Schema](../../../schemas/http-session.md)
- [HTTP Cookie Schema](../../../schemas/http-cookie.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Session Management Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- Web Security skills that build on session context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for session-management weaknesses
- Observations and Evidence references
- Optional `identity` Assets for confirmed authenticated contexts

Outputs SHALL remain implementation independent.

---

# Security Principles

The Session Management Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Redact session identifiers and secrets in all evidence
- Produce no Finding without supporting Evidence
- Reference managed credentials, never inline secrets
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and managed test credentials
- Rely on the skill for session-management evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide inline credentials or secrets
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
- adr/ADR-001-session-management-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- JWT (Authentication tier, planned)
- CSRF (Authentication tier, planned)

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

- [ADR-001 — Session Management Skill](adr/ADR-001-session-management-skill.md)

---

# Future Extensions

Future versions MAY support

- Cross-application single-sign-on session evaluation
- Session-binding and token-binding analysis
- Concurrent-session and session-revocation testing
- Handoff of authenticated contexts to Web Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Session Management Skill produces evidence-backed Findings for
session-management weaknesses while acting strictly within scope and Rules of
Engagement through the Policy Engine, consuming canonical Session and Cookie
representations, and never persisting session secrets or invoking tools directly.
