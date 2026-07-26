# Cross-Site Scripting Skill

**File:** `skills/web-security/xss/README.md`

**Version:** 1.0.0

---

# Purpose

The Cross-Site Scripting Skill is a Web-Security-tier domain skill that evaluates
whether an in-scope web application is vulnerable to cross-site scripting (XSS)
within the Robust PenTest Platform (RPP).

It examines reflected, stored, and DOM-based injection points, reporting weaknesses
where user-controllable input reaches an HTML, attribute, JavaScript, or URL sink
without adequate encoding or sanitization, allowing script execution in a victim's
browser (CWE-79).

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and the
[Browser](../../shared/browser/README.md) and SHALL NOT issue requests or render
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Cross-Site Scripting Skill SHALL

- Evaluate reflected, stored, and DOM-based XSS injection points
- Confirm script execution using bounded, non-destructive marker payloads
- Consume `web-application` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for XSS weaknesses
- Remain tool independent

---

# Non-Goals

The Cross-Site Scripting Skill SHALL NOT

- Perform HTTP input or output or browser rendering directly
- Discover applications or endpoints (that is Discovery)
- Evaluate the Content Security Policy in isolation (that is the CSP skill)
- Test server-side template injection (that is the SSTI skill)
- Deliver a real payload to third parties or perform destructive exploitation
- Invoke command-line tools or parse their output

Transport and rendering belong to the shared HTTP Client and Browser; discovery
belongs to the Discovery tier; CSP and template-injection testing belong to
dedicated skills.

---

# Design Principles

The Cross-Site Scripting Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms execution with bounded marker payloads, not weaponized
  payloads
- Non-destructive — its markers cause no harmful side effects
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Cross-Site Scripting Skill

├── Policy Gate            → Policy Engine
├── Injection Prober      → HTTP Client
├── Rendering Observer    → Browser
├── Context Analyzer
├── Encoding Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client and Browser to observe injection and
rendering behavior. It SHALL remain unaware of any transport or rendering
implementation.

---

# Responsibilities

The Cross-Site Scripting Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Injecting bounded marker payloads and observing reflection through the
  [HTTP Client](../../shared/http-client/README.md)
- Observing marker execution through the
  [Browser](../../shared/browser/README.md) for DOM-based and rendered contexts
- Analyzing output context and encoding adequacy
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

Inject Bounded Marker Payloads (HTTP Client)

↓

Observe Reflection And Rendering (HTTP Client / Browser)

↓

Analyze Output Context And Encoding

↓

Record Observations → Evidence

↓

Analyze For XSS Weaknesses

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

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application base URL.

`assets` reference the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) under test, including candidate parameters and
sinks.

`payload_set_ref` MAY reference a managed set of bounded, non-destructive marker
payloads. It SHALL be a reference, never inline weaponized payloads.

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

- Reflected XSS where input reaches a sink without adequate encoding (CWE-79)
- Stored XSS where persisted input executes when later rendered
- DOM-based XSS where client-side code passes input to a dangerous sink
- Context-inappropriate encoding that fails to neutralize injection
- Sinks exploitable despite partial filtering

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with the confirming marker recorded and sensitive content redacted.

---

# Policy Enforcement

The Cross-Site Scripting Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Injection and rendering are `active` actions; they SHALL proceed only on an
`allow` decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Stored-XSS testing, which persists input, SHALL be treated as higher impact and
SHALL require approval where the Rules of Engagement so specify. Out-of-scope
applications SHALL never be tested.

---

# Dependencies

The Cross-Site Scripting Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Browser](../../shared/browser/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Cross-Site Scripting Skill SHALL NOT depend on other domain skills. It MAY
consume Content Security Policy context produced by the CSP skill to assess
exploitability, without taking a package dependency on it.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for XSS weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Cross-Site Scripting Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm execution with bounded, non-destructive marker payloads only
- Reference managed payload sets, never inline weaponized payloads
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-79
- Treat stored-injection testing as higher impact and gate it accordingly
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and candidate parameters and sinks
- Provide a managed bounded marker payload set
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests or drive the browser directly
- Bypass the Policy Engine
- Provide inline weaponized payloads
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
- adr/ADR-001-xss-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Browser](../../shared/browser/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Content Security Policy](../csp/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Cross-Site Scripting Skill](adr/ADR-001-xss-skill.md)

---

# Future Extensions

Future versions MAY support

- Mutation and template-based context-aware payload synthesis
- Blind and out-of-band XSS confirmation via controlled collectors
- Framework-specific sink modeling
- Correlation of CSP strength with XSS exploitability grading

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Cross-Site Scripting Skill produces evidence-backed Findings for XSS
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming execution with bounded non-destructive markers, and never
invoking tools directly or delivering weaponized payloads.
