# Insecure Deserialization Skill

**File:** `skills/web-security/deserialization/README.md`

**Version:** 1.0.0

---

# Purpose

The Insecure Deserialization Skill is a Web-Security-tier domain skill that evaluates
whether an in-scope web application unsafely deserializes user-controllable data
within the Robust PenTest Platform (RPP).

It examines whether serialized input is accepted and processed by an unsafe
deserializer, reporting weaknesses confirmed through bounded out-of-band and
differential signals where insecure deserialization is possible (CWE-502).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Insecure Deserialization Skill SHALL

- Evaluate endpoints that accept serialized input for unsafe deserialization
- Confirm processing using bounded, non-destructive out-of-band and differential
  signals
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for insecure deserialization weaknesses
- Remain tool independent

---

# Non-Goals

The Insecure Deserialization Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test other injection classes such as command injection (that is a dedicated skill)
- Deliver a functional gadget chain or execute code
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; other injection classes belong to dedicated skills; code execution is
prohibited.

---

# Design Principles

The Insecure Deserialization Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms unsafe deserialization with bounded probes, not gadget
  chains
- Non-destructive — its probes cause no harmful side effects
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Insecure Deserialization Skill

├── Policy Gate            → Policy Engine
├── Serialized Prober     → HTTP Client
├── Out-Of-Band Analyzer
├── Differential Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe deserialization behavior. It SHALL
remain unaware of any transport implementation.

---

# Responsibilities

The Insecure Deserialization Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting bounded serialized probes and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing out-of-band interaction and differential signals
- Confirming unsafe processing without delivering a gadget chain
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

Submit Bounded Serialized Probes (HTTP Client)

↓

Observe Out-Of-Band And Differential Signals

↓

Record Observations → Evidence

↓

Analyze For Insecure Deserialization Weaknesses

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

payload_set_ref:

collector_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL that accepts serialized
input.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test.

`payload_set_ref` MAY reference a managed set of bounded, non-destructive serialized
probes. It SHALL be a reference, never a functional gadget chain.

`collector_ref` MAY reference a controlled out-of-band collector used to confirm
processing.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with OWASP Top 10 (2021) category A08:2021 – Software and Data
Integrity Failures. This category reference is informational and does not change
capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Insecure deserialization confirmed by an out-of-band interaction (CWE-502)
- Serialized input processed by an unsafe deserializer without type restrictions
- Differential behavior indicating serialized-object processing

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only bounded probe interaction recorded and sensitive content redacted.

---

# Policy Enforcement

The Insecure Deserialization Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Serialized probing is an `active`, high-impact action; it SHALL proceed only
on an `allow` decision and within the attached rate ceiling, and SHALL commonly
require approval under the Rules of Engagement. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted. The
skill SHALL confirm unsafe processing without delivering a gadget chain, and SHALL
never test out-of-scope targets.

---

# Dependencies

The Insecure Deserialization Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Timing Schema](../../../schemas/http-timing.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Insecure Deserialization Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- API Security skills that process serialized payloads
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for insecure deserialization weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Insecure Deserialization Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm unsafe processing with bounded, non-destructive probes only
- Never deliver a functional gadget chain or execute code
- Reference managed probe sets and authorized collectors only
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-502
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets that accept serialized input
- Provide a managed bounded probe set and a controlled collector where permitted
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Deliver functional gadget chains
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
- adr/ADR-001-deserialization-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Command Injection](../command-injection/README.md)
- [XML External Entity](../xxe/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [HTTP Timing](../../../schemas/http-timing.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Insecure Deserialization Skill](adr/ADR-001-deserialization-skill.md)

---

# Future Extensions

Future versions MAY support

- Format-specific serialized-object modeling
- Blind confirmation via richer out-of-band channels
- Type-restriction and allow-list evaluation
- Correlation of deserialization with command-injection exploitability

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Insecure Deserialization Skill produces evidence-backed Findings for
insecure deserialization weaknesses while acting strictly within scope and Rules of
Engagement through the Policy Engine, confirming unsafe processing with bounded
probes, and never delivering a gadget chain or invoking tools directly.
