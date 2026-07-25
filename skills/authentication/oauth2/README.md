# OAuth2 Authentication Skill

**File:** `skills/authentication/oauth2/README.md`

**Version:** 1.0.0

---

# Purpose

The OAuth2 Authentication Skill is an Authentication-tier domain skill that
evaluates how an in-scope application implements OAuth2 authorization flows within
the Robust PenTest Platform (RPP).

It examines grant types, redirect-URI validation, state-parameter usage, PKCE
enforcement, token handling, and scope enforcement, reporting weaknesses such as
open redirect-URI acceptance, missing anti-forgery state, absent PKCE on
Authorization Code clients, and insecure token transport.

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The OAuth2 Authentication Skill SHALL

- Evaluate grant types, redirect-URI validation, state usage, and PKCE enforcement
- Evaluate token handling, scope enforcement, and transport
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for OAuth2 weaknesses
- Remain tool independent

---

# Non-Goals

The OAuth2 Authentication Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Evaluate OpenID Connect identity-layer specifics (that is the OIDC skill)
- Validate JWT structure and signatures in depth (that is the JWT skill)
- Test authorization decisions of protected resources (that is the Authorization
  tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; identity-layer, token-format, and authorization testing belong to dedicated
skills.

---

# Design Principles

The OAuth2 Authentication Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same authorization-server behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists tokens or client secrets in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

OAuth2 Authentication Skill

├── Policy Gate            → Policy Engine
├── Flow Prober           → HTTP Client
├── Redirect Analyzer
├── State And PKCE Analyzer
├── Token Handling Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe OAuth2 flows. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The OAuth2 Authentication Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing authorization and token flows through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing redirect-URI validation, state usage, and PKCE enforcement
- Analyzing token handling, scope enforcement, and transport
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

Observe Authorization And Token Flows (HTTP Client)

↓

Analyze Redirect, State, PKCE, And Token Handling

↓

Record Observations → Evidence

↓

Analyze For OAuth2 Weaknesses

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

client_credentials_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope OAuth2 authorization server or client application base
URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test.

`client_credentials_ref` MAY reference managed test client credentials. It SHALL be
a reference, never inline secrets.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. Where it confirms a distinct authenticated
identity context, it MAY record an `identity`
[Asset](../../../schemas/asset.md) with provenance. It SHALL NOT invent other Asset
types and SHALL NOT persist tokens or client secrets on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Redirect URIs validated loosely, permitting open redirection or token leakage
- Missing or unvalidated anti-forgery `state` parameter
- PKCE not enforced for Authorization Code clients, which SHOULD apply to both
  public and confidential clients per current OAuth security guidance
- Implicit grant or other discouraged grant types offered
- Access or refresh tokens transported or stored insecurely
- Excessive or unenforced scopes granted

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with tokens and client secrets redacted.

---

# Policy Enforcement

The OAuth2 Authentication Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Flow testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope targets SHALL never be tested.

---

# Dependencies

The OAuth2 Authentication Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The OAuth2 Authentication Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- The OIDC skill, which builds on OAuth2 flow context
- API Security skills that build on token handling
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for OAuth2 weaknesses
- Observations and Evidence references
- Optional `identity` Assets for confirmed authenticated contexts

Outputs SHALL remain implementation independent.

---

# Security Principles

The OAuth2 Authentication Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Redact tokens and client secrets in all evidence
- Produce no Finding without supporting Evidence
- Reference managed credentials, never inline secrets
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and managed client credentials
- Rely on the skill for OAuth2 flow evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide inline client secrets
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
- adr/ADR-001-oauth2-authentication-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [JWT Authentication](../jwt/README.md)
- OIDC (Authentication tier, planned)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [HTTP Redirect](../../../schemas/http-redirect.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — OAuth2 Authentication Skill](adr/ADR-001-oauth2-authentication-skill.md)

---

# Future Extensions

Future versions MAY support

- Device-authorization and client-credentials grant evaluation
- Token-introspection and revocation-endpoint analysis
- Rich authorization-request (PAR and JAR) evaluation
- Handoff of flow context to OIDC and API Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant OAuth2 Authentication Skill produces evidence-backed Findings for OAuth2
flow weaknesses while acting strictly within scope and Rules of Engagement through
the Policy Engine, never persisting tokens or client secrets, and never invoking
tools directly.
