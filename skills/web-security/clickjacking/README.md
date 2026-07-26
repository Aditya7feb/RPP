# Clickjacking Skill

**File:** `skills/web-security/clickjacking/README.md`

**Version:** 1.0.0

---

# Purpose

The Clickjacking Skill is a Web-Security-tier domain skill that evaluates whether an
in-scope web application defends against UI redress (clickjacking) attacks within
the Robust PenTest Platform (RPP).

It examines whether responses instruct browsers to prevent framing, reporting
weaknesses such as an absent or permissive `X-Frame-Options` header, a missing or
weak Content Security Policy `frame-ancestors` directive, and sensitive
state-changing pages that are framable by untrusted origins (CWE-1021).

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Clickjacking Skill SHALL

- Evaluate framing-protection headers and directives on in-scope responses
- Identify sensitive pages framable by untrusted origins
- Consume `web-application` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for clickjacking weaknesses
- Remain tool independent

---

# Non-Goals

The Clickjacking Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Evaluate the full Content Security Policy (that is the CSP skill)
- Evaluate cross-origin resource sharing (that is the CORS skill)
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; full CSP and CORS evaluation belong to dedicated skills.

---

# Design Principles

The Clickjacking Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same response behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Non-destructive — it observes framing controls without harming the target
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Clickjacking Skill

├── Policy Gate            → Policy Engine
├── Response Prober       → HTTP Client
├── Framing Control Analyzer
├── Sensitivity Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe framing controls. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Clickjacking Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing response headers through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing `X-Frame-Options` and CSP `frame-ancestors` directives
- Identifying sensitive state-changing pages that are framable
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

Observe Response Framing Controls (HTTP Client)

↓

Analyze Framing Protection And Page Sensitivity

↓

Record Observations → Evidence

↓

Analyze For Clickjacking Weaknesses

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

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application base URL.

`assets` reference the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) under test, including sensitive state-changing
pages.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with OWASP Top 10 (2021) category A04:2021 – Insecure Design.
This category reference is informational and does not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Sensitive pages served without `X-Frame-Options` or CSP `frame-ancestors`
  (CWE-1021)
- Permissive framing controls that allow untrusted origins to frame the page
- Inconsistent framing protection across sensitive endpoints

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Clickjacking Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Response probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope applications SHALL never be tested.

---

# Dependencies

The Clickjacking Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Header Schema](../../../schemas/http-header.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Clickjacking Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for clickjacking weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Clickjacking Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Produce no Finding without supporting Evidence
- Preserve auditability
- Classify weaknesses using canonical weakness identifiers such as CWE-1021

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and sensitive endpoints
- Rely on the skill for framing-protection evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Attempt destructive exploitation
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
- adr/ADR-001-clickjacking-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- CSP (Web Security tier, planned)
- CORS (Web Security tier, planned)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [HTTP Header](../../../schemas/http-header.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Clickjacking Skill](adr/ADR-001-clickjacking-skill.md)

---

# Future Extensions

Future versions MAY support

- Frame-busting script robustness evaluation
- Nested-framing and double-framing evaluation
- Correlation with CSP `frame-ancestors` strength grading
- Handoff of framable sensitive pages to reporting prioritization

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Clickjacking Skill produces evidence-backed Findings for UI redress
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming weaknesses without disruptive exploitation, and never
invoking tools directly.
