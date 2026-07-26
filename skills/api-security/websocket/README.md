# WebSocket API Security Skill

**File:** `skills/api-security/websocket/README.md`

**Version:** 1.0.0

---

# Purpose

The WebSocket API Security Skill is an API-Security-tier domain skill that evaluates
the security of an in-scope WebSocket API within the Robust PenTest Platform (RPP).

It focuses on WebSocket-specific weaknesses — Cross-Site WebSocket Hijacking (CSWSH)
and missing Origin validation, missing handshake authentication, missing
message-level authorization, and cleartext transport — reporting weaknesses confirmed
through bounded, non-destructive verification aligned to the OWASP API Security Top 10
(2023) and the OWASP Top 10 (2021).

The skill consumes the `api` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[WebSocket Client](../../shared/websocket-client/README.md) and SHALL NOT open
connections directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The WebSocket API Security Skill SHALL

- Evaluate Origin validation on the WebSocket handshake
- Evaluate authentication on the WebSocket handshake
- Evaluate message-level authorization across identities
- Evaluate transport security for WebSocket connections
- Consume `api` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for WebSocket security weaknesses
- Remain tool independent

---

# Non-Goals

The WebSocket API Security Skill SHALL NOT

- Open WebSocket connections or send or receive frames directly
- Discover endpoints (that is Discovery)
- Analyze general server-side TLS posture (that is TLS Analysis)
- Test generic injection such as SQL, command, or cross-site scripting within message
  payloads (those are Web Security skills)
- Enumerate or exfiltrate other principals' data beyond minimal confirmation
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared WebSocket Client; discovery belongs to the Discovery
tier; general TLS posture belongs to TLS Analysis; generic injection belongs to Web
Security skills.

The authentication boundary is explicit. This skill verifies authentication
*presence* and *enforcement* on the WebSocket surface — whether the handshake requires
and enforces authentication — and it verifies authorization *behavior* across
identities. The correctness of the underlying authentication mechanisms and protocols
(OAuth2, OIDC, JWT, SAML, mTLS, Sessions, and API Keys) is owned by the Authentication
tier, which SHALL evaluate protocol correctness. This skill SHALL NOT assess
authentication-protocol correctness.

---

# Design Principles

The WebSocket API Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same API behavior
- Conservative — it confirms hijacking and authorization gaps with bounded probes
- Privacy-preserving — it uses only authorized controlled identities
- Tool independent

---

# Architecture

```
API Security Agent

↓

WebSocket API Security Skill

├── Policy Gate               → Policy Engine
├── Handshake Prober          → WebSocket Client
├── Origin Validation Analyzer
├── Handshake Authentication Analyzer
├── Message Authorization Analyzer
├── Transport Analyzer
├── Weakness Analyzer
├── Evidence Recorder         → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the WebSocket Client to observe handshake and message
behavior. It SHALL remain unaware of any transport implementation.

---

# Responsibilities

The WebSocket API Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Performing bounded handshakes and message exchanges across two controlled
  identities through the [WebSocket Client](../../shared/websocket-client/README.md)
- Analyzing Origin validation, handshake authentication, message authorization, and
  transport security
- Confirming gaps with minimal, controlled exchanges
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

Perform Bounded Handshakes And Messages Across Controlled Identities (WebSocket Client)

↓

Analyze Origin, Authentication, Authorization, And Transport

↓

Record Observations → Evidence

↓

Analyze For WebSocket Security Weaknesses

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

allowed_origins_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope WebSocket endpoint.

`assets` reference the `api` and `endpoint`
[Assets](../../../schemas/asset.md) under test.

`identities_ref` MAY reference two authorized, controlled test identities by reference
only, never inline credentials.

`allowed_origins_ref` MAY reference the set of legitimate Origins expected to be
accepted, enabling detection of missing Origin validation.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It MAY enrich the `api`
[Asset](../../../schemas/asset.md) with endpoint facts and SHALL NOT invent Asset
types.

---

# Produced Findings

These weaknesses align with the OWASP API Security Top 10 (2023), primarily API2
(Broken Authentication), API1/API5 (Broken Object/Function Level Authorization), and
API8 (Security Misconfiguration), and with the OWASP Top 10 (2021) categories
A01:2021 – Broken Access Control and A05:2021 – Security Misconfiguration. These
references are informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Missing Origin validation on the handshake enabling Cross-Site WebSocket Hijacking
  (CWE-1385, a specialization of CWE-346)
- WebSocket handshake accepted without authentication (CWE-306)
- Message-level authorization not enforced across identities (CWE-285)
- WebSocket connection established over cleartext transport (CWE-319)
- Verbose error or close-frame detail disclosing implementation information (CWE-209)

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

The WebSocket API Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Handshake and message exchange are `active` actions; they SHALL proceed only
on an `allow` decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Message exchanges SHALL be bounded to avoid denial of service, and the skill SHALL use
only authorized controlled identities. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The WebSocket API Security Skill depends on

- [WebSocket Client](../../shared/websocket-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The WebSocket API Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The API Security Agent and API-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for WebSocket security weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The WebSocket API Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound message exchanges to avoid denial of service
- Use only authorized controlled identities for authorization testing
- Confirm hijacking and authorization gaps with minimal, controlled exchanges only
- Never enumerate or exfiltrate other principals' data
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and OWASP API Security references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` and `endpoint` Assets, the set of allowed Origins, and two
  controlled identities
- Rely on the skill for WebSocket-specific evaluation
- Route general TLS posture and generic payload injection testing to the dedicated
  skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Open WebSocket connections directly
- Bypass the Policy Engine
- Send unbounded message volumes
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
- adr/ADR-001-websocket-api-security-skill.md

---

# Related Packages

- [WebSocket Client](../../shared/websocket-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [API Discovery](../../discovery/api-discovery/README.md)
- [TLS Analysis](../../discovery/tls-analysis/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — WebSocket API Security Skill](adr/ADR-001-websocket-api-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Subprotocol-specific abuse evaluation
- Compression-extension abuse evaluation
- Long-lived connection authorization drift evaluation
- Correlation with Discovery API inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant WebSocket API Security Skill produces evidence-backed Findings for
WebSocket-specific weaknesses while acting strictly within scope and Rules of
Engagement through the Policy Engine, bounding message exchanges, using only
controlled identities, and never denying service or invoking tools directly.
