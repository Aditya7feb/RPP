# Content Security Policy Skill

**File:** `skills/web-security/csp/README.md`

**Version:** 1.0.0

---

# Purpose

The Content Security Policy Skill is a Web-Security-tier domain skill that evaluates
the strength and correctness of an in-scope web application's Content Security
Policy (CSP) within the Robust PenTest Platform (RPP).

It examines whether a CSP is present, whether its directives meaningfully constrain
script and resource loading, and whether known bypasses are permitted, reporting
weaknesses such as a missing policy, `unsafe-inline` or `unsafe-eval` script
sources, overly broad source lists, and missing `object-src` or `base-uri`
restrictions (CWE-693).

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Content Security Policy Skill SHALL

- Evaluate CSP presence, directive coverage, and source-list strength
- Identify known CSP bypasses and weakening directives
- Consume `web-application` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for CSP weaknesses
- Remain tool independent

---

# Non-Goals

The Content Security Policy Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Evaluate framing protection in isolation (that is the Clickjacking skill)
- Test for cross-site scripting execution (that is the XSS skill)
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; framing-only and script-execution testing belong to dedicated skills.

---

# Design Principles

The Content Security Policy Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same policy content
- Conservative — it confirms weaknesses without disruptive exploitation
- Non-destructive — it observes policy without harming the target
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Content Security Policy Skill

├── Policy Gate            → Policy Engine
├── Response Prober       → HTTP Client
├── Directive Analyzer
├── Source Strength Analyzer
├── Bypass Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe the policy. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Content Security Policy Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing the `Content-Security-Policy` header and meta policy through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing directive coverage, source-list strength, and known bypasses
- Detecting `unsafe-inline`, `unsafe-eval`, wildcard sources, and missing
  directives
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

Observe Content Security Policy (HTTP Client)

↓

Analyze Directives, Sources, And Bypasses

↓

Record Observations → Evidence

↓

Analyze For CSP Weaknesses

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
[Assets](../../../schemas/asset.md) under test.

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

- No Content Security Policy present on sensitive responses (CWE-693)
- `unsafe-inline` or `unsafe-eval` permitted in `script-src`
- Wildcard or overly broad source lists that neutralize the policy
- Missing `object-src`, `base-uri`, or `frame-ancestors` restrictions
- Policies trivially bypassable through allow-listed hosts or schemes
- Report-only policies deployed where enforcement is expected

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Content Security Policy Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Response probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope applications SHALL never be tested.

---

# Dependencies

The Content Security Policy Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Header Schema](../../../schemas/http-header.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Content Security Policy Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- The XSS skill, which uses CSP context to assess exploitability
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for CSP weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Content Security Policy Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-693
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and sensitive endpoints
- Rely on the skill for CSP evaluation rather than ad hoc checks
- Treat produced Findings as inputs to XSS exploitability and remediation
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
- adr/ADR-001-content-security-policy-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Clickjacking](../clickjacking/README.md)
- XSS (Web Security tier, planned)

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

- [ADR-001 — Content Security Policy Skill](adr/ADR-001-content-security-policy-skill.md)

---

# Future Extensions

Future versions MAY support

- Nonce and hash-based policy strength grading
- Trusted Types and `require-trusted-types-for` evaluation
- CSP reporting-endpoint configuration evaluation
- Correlation of CSP strength with XSS exploitability

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Content Security Policy Skill produces evidence-backed Findings for CSP
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming weaknesses without disruptive exploitation, and never
invoking tools directly.
