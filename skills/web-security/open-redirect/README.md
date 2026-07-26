# Open Redirect Skill

**File:** `skills/web-security/open-redirect/README.md`

**Version:** 1.0.0

---

# Purpose

The Open Redirect Skill is a Web-Security-tier domain skill that evaluates whether an
in-scope web application performs unsafe redirects to attacker-controllable
destinations within the Robust PenTest Platform (RPP).

It examines redirect parameters and flows, reporting weaknesses where a
user-controllable value determines the redirect target without validation, allowing
redirection to an untrusted external origin (CWE-601).

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Open Redirect Skill SHALL

- Evaluate redirect parameters and flows for unsafe destination handling
- Identify redirects to untrusted external origins from user-controllable input
- Consume `web-application` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for open-redirect weaknesses
- Remain tool independent

---

# Non-Goals

The Open Redirect Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test server-side request forgery (that is the SSRF skill)
- Test cross-site scripting via redirect sinks (that is the XSS skill)
- Complete a redirect into a malicious destination or harm any third party
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; SSRF and script-execution testing belong to dedicated skills.

---

# Design Principles

The Open Redirect Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same redirect behavior
- Conservative — it confirms redirection without following into harmful
  destinations
- Non-destructive — it uses benign, controlled probe destinations
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Open Redirect Skill

├── Policy Gate            → Policy Engine
├── Redirect Prober       → HTTP Client
├── Parameter Analyzer
├── Destination Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe redirect behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Open Redirect Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing redirect responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing redirect parameters and destination validation
- Detecting redirection to untrusted origins from user-controllable input
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

Observe Redirect Responses (HTTP Client)

↓

Analyze Redirect Parameters And Destination Validation

↓

Record Observations → Evidence

↓

Analyze For Open-Redirect Weaknesses

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

probe_destination:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application base URL.

`assets` reference the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) under test, including candidate redirect
parameters.

`probe_destination` MAY reference a benign, controlled destination used to confirm
redirection without harming third parties.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- A user-controllable parameter that determines an unvalidated redirect target
  (CWE-601)
- Redirection to an untrusted external origin accepted
- Weak destination validation based on substring, prefix, or suffix matching
- Redirects that leak sensitive tokens in the destination URL

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Open Redirect Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Redirect probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
The skill SHALL confirm redirection using a benign controlled destination and SHALL
NOT follow a redirect into a harmful destination. Out-of-scope targets SHALL never
be tested.

---

# Dependencies

The Open Redirect Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Open Redirect Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for open-redirect weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Open Redirect Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm redirection using benign controlled destinations only
- Never follow a redirect into a harmful destination or harm third parties
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-601
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and candidate redirect parameters
- Provide a benign controlled probe destination
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Use live malicious destinations
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
- adr/ADR-001-open-redirect-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- SSRF (Web Security tier, planned)
- XSS (Web Security tier, planned)

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

- [ADR-001 — Open Redirect Skill](adr/ADR-001-open-redirect-skill.md)

---

# Future Extensions

Future versions MAY support

- Redirect-chain and multi-hop redirect evaluation
- Token-leakage-through-redirect classification
- Correlation of redirect sinks with XSS and SSRF exploitability
- Handoff of redirect context to reporting prioritization

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Open Redirect Skill produces evidence-backed Findings for open-redirect
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming redirection with benign controlled destinations, and never
invoking tools directly or harming third parties.
