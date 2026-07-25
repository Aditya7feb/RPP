# JWT Authentication Skill

**File:** `skills/authentication/jwt/README.md`

**Version:** 1.0.0

---

# Purpose

The JWT Authentication Skill is an Authentication-tier domain skill that evaluates
how an in-scope application issues, transports, and validates JSON Web Tokens
within the Robust PenTest Platform (RPP).

It examines token structure, signing algorithm, signature validation, claim
validation, and transport, reporting weaknesses such as unsigned-token acceptance,
algorithm confusion, weak signing secrets, absent expiry validation, and sensitive
data disclosed in token payloads.

The skill consumes the `api`, `endpoint`, and `web-application`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The JWT Authentication Skill SHALL

- Evaluate token structure, signing algorithm, signature validation, and claims
- Evaluate token transport and payload confidentiality
- Consume `api`, `endpoint`, and `web-application` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for JWT weaknesses
- Remain tool independent

---

# Non-Goals

The JWT Authentication Skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints (that is Discovery)
- Test OAuth2 or OIDC flows that carry JWTs (those are dedicated skills)
- Test authorization decisions (that is the Authorization tier)
- Recover signing secrets through unbounded brute force
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; protocol-flow and authorization testing belong to dedicated skills.

---

# Design Principles

The JWT Authentication Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists token secrets or full tokens in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

JWT Authentication Skill

├── Policy Gate            → Policy Engine
├── Token Prober          → HTTP Client
├── Structure Analyzer
├── Signature Analyzer
├── Claim Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe token handling. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The JWT Authentication Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing token issuance and acceptance through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing token structure, algorithm, signature validation, and claims
- Detecting unsigned-token acceptance, algorithm confusion, and weak validation
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

Observe Token Issuance And Acceptance (HTTP Client)

↓

Analyze Structure, Signature, And Claims

↓

Record Observations → Evidence

↓

Analyze For JWT Weaknesses

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

token_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope API or application base URL.

`assets` reference the `api`, `endpoint`, and `web-application`
[Assets](../../../schemas/asset.md) under test.

`token_ref` MAY reference a managed test token required to observe acceptance
behavior. It SHALL be a reference, never an inline token.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. Where it confirms a distinct authenticated
identity context, it MAY record an `identity`
[Asset](../../../schemas/asset.md) with provenance. It SHALL NOT invent other Asset
types and SHALL NOT persist token secrets on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Unsigned tokens accepted (`alg` of `none`)
- Algorithm confusion, such as an asymmetric key accepted as an HMAC secret
- Weak or guessable HMAC signing secrets
- Signatures not verified by the server
- Absent or unenforced expiry, issuer, or audience claims
- Sensitive data disclosed in the token payload
- Tokens transmitted over cleartext transport

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with token secrets redacted.

---

# Policy Enforcement

The JWT Authentication Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Token testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Secret-recovery checks SHALL be bounded by configuration and the Rules of
Engagement. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The JWT Authentication Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The JWT Authentication Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- OAuth2 and OIDC skills that build on token-validation context
- API Security skills that build on token handling
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for JWT weaknesses
- Observations and Evidence references
- Optional `identity` Assets for confirmed authenticated contexts

Outputs SHALL remain implementation independent.

---

# Security Principles

The JWT Authentication Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Bound any secret-recovery check by configuration and Rules of Engagement
- Redact token secrets and full tokens in all evidence
- Produce no Finding without supporting Evidence
- Reference managed tokens, never inline token material
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` Assets and a managed test token
- Rely on the skill for JWT evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide inline token material
- Request unbounded secret brute force
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
- adr/ADR-001-jwt-authentication-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Session Management](../sessions/README.md)
- [API Key Authentication](../api-keys/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — JWT Authentication Skill](adr/ADR-001-jwt-authentication-skill.md)

---

# Future Extensions

Future versions MAY support

- JWE encrypted-token evaluation
- Key-rotation and JWKS-endpoint analysis
- Nested and chained token evaluation
- Handoff of token context to OAuth2, OIDC, and API Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant JWT Authentication Skill produces evidence-backed Findings for JWT
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, bounding any secret-recovery check, never persisting token secrets,
and never invoking tools directly.
