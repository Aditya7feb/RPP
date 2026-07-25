# Mutual TLS Authentication Skill

**File:** `skills/authentication/mtls/README.md`

**Version:** 1.0.0

---

# Purpose

The Mutual TLS Authentication Skill is an Authentication-tier domain skill that
evaluates how an in-scope service enforces client-certificate (mutual TLS)
authentication within the Robust PenTest Platform (RPP).

It examines whether a service requires a client certificate where expected, how
strictly the presented certificate and its chain are validated, whether revocation
is checked, and whether the service falls back to weaker authentication, reporting
weaknesses such as optional client certificates, acceptance of untrusted or expired
certificates, and absent revocation checking.

The skill consumes the `service`, `endpoint`, and `certificate`
[Assets](../../../schemas/asset.md) produced by Discovery and the canonical
[TLS Connection](../../../schemas/tls-connection.md),
[Certificate](../../../schemas/certificate.md), and
[TLS Validation Result](../../../schemas/tls-validation-result.md)
representations. It drives the [TLS Client](../../shared/tls-client/README.md) and
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT open connections
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Mutual TLS Authentication Skill SHALL

- Evaluate client-certificate requirement, validation strictness, and revocation
  checking
- Detect fallback to weaker or absent authentication
- Consume `service`, `endpoint`, and `certificate` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for mutual TLS weaknesses
- Remain tool independent

---

# Non-Goals

The Mutual TLS Authentication Skill SHALL NOT

- Open TLS connections or perform HTTP input or output directly
- Discover services or certificates (that is Discovery)
- Analyze server-side TLS posture in general (that is TLS Analysis)
- Test authorization decisions (that is the Authorization tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared TLS and HTTP Clients; discovery and server-side TLS
posture belong to the Discovery tier; authorization testing belongs to a dedicated
skill.

---

# Design Principles

The Mutual TLS Authentication Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same service behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists private keys in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

Mutual TLS Authentication Skill

├── Policy Gate            → Policy Engine
├── Handshake Prober      → TLS Client
├── Application Prober    → HTTP Client
├── Validation Analyzer
├── Fallback Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the TLS and HTTP Clients to observe mutual TLS behavior. It
SHALL remain unaware of any transport implementation.

---

# Responsibilities

The Mutual TLS Authentication Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing client-certificate handshakes through the
  [TLS Client](../../shared/tls-client/README.md) and application behavior through
  the [HTTP Client](../../shared/http-client/README.md)
- Analyzing certificate and chain validation and revocation checking
- Detecting optional certificates and fallback to weaker authentication
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

Observe Client-Certificate Handshake (TLS Client)

↓

Observe Application Behavior (HTTP Client)

↓

Analyze Validation, Revocation, And Fallback

↓

Record Observations → Evidence

↓

Analyze For Mutual TLS Weaknesses

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

client_certificate_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope service endpoint expected to enforce mutual TLS.

`assets` reference the `service`, `endpoint`, and `certificate`
[Assets](../../../schemas/asset.md) under test.

`client_certificate_ref` MAY reference a managed test client certificate and key.
It SHALL be a reference, never inline key material.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types and SHALL NOT
persist private key material on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Client certificate not required where mutual TLS is expected
- Untrusted, self-signed, or expired client certificates accepted
- Client certificates from an unexpected certificate authority accepted
- Certificate subject or SAN not validated against the expected identity
- Revoked client certificates accepted due to absent revocation checking
- Fallback to unauthenticated or weaker authentication

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with private key material redacted.

---

# Policy Enforcement

The Mutual TLS Authentication Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Handshake and application probing are `active` actions; they SHALL proceed
only on an `allow` decision and within the attached rate ceiling. Where a decision
is `requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope services SHALL never be tested.

---

# Dependencies

The Mutual TLS Authentication Skill depends on

- [TLS Client](../../shared/tls-client/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [TLS Connection Schema](../../../schemas/tls-connection.md)
- [Certificate Schema](../../../schemas/certificate.md)
- [TLS Validation Result Schema](../../../schemas/tls-validation-result.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Mutual TLS Authentication Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- API and Cloud skills that rely on mutual TLS context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for mutual TLS weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Mutual TLS Authentication Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Redact private key material in all evidence
- Produce no Finding without supporting Evidence
- Reference managed certificates and keys, never inline key material
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `service` Assets expected to enforce mutual TLS
- Provide a managed test client certificate where required
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Open TLS connections or issue requests directly
- Bypass the Policy Engine
- Provide inline private key material
- Test out-of-scope services

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
- adr/ADR-001-mtls-authentication-skill.md

---

# Related Packages

- [TLS Client](../../shared/tls-client/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [TLS Analysis](../../discovery/tls-analysis/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [TLS Connection](../../../schemas/tls-connection.md)
- [Certificate](../../../schemas/certificate.md)
- [TLS Validation Result](../../../schemas/tls-validation-result.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Mutual TLS Authentication Skill](adr/ADR-001-mtls-authentication-skill.md)

---

# Future Extensions

Future versions MAY support

- Certificate-pinning evaluation
- Client-certificate lifecycle and rotation testing
- Correlation with server-side TLS posture from TLS Analysis
- Handoff of mutual TLS context to API and Cloud testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Mutual TLS Authentication Skill produces evidence-backed Findings for
client-certificate authentication weaknesses while acting strictly within scope and
Rules of Engagement through the Policy Engine, reusing canonical TLS and certificate
schemas, never persisting private key material, and never invoking tools directly.
