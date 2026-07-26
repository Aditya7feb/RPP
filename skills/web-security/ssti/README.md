# Server-Side Template Injection Skill

**File:** `skills/web-security/ssti/README.md`

**Version:** 1.0.0

---

# Purpose

The Server-Side Template Injection Skill is a Web-Security-tier domain skill that
evaluates whether an in-scope web application evaluates user-controllable input as a
server-side template expression within the Robust PenTest Platform (RPP).

It examines whether input reaches a template engine and is evaluated, reporting
weaknesses confirmed through bounded expression-evaluation markers where injection is
possible (CWE-1336).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Server-Side Template Injection Skill SHALL

- Evaluate injection points for server-side template expression evaluation
- Confirm evaluation using bounded, non-destructive expression markers
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for template injection weaknesses
- Remain tool independent

---

# Non-Goals

The Server-Side Template Injection Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test client-side template injection or cross-site scripting (that is the XSS skill)
- Test other injection classes such as SQL or command injection (those are dedicated
  skills)
- Escalate to code execution or run system commands
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; client-side and other injection classes belong to dedicated skills; code
execution is prohibited.

---

# Design Principles

The Server-Side Template Injection Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms evaluation with bounded expression markers, not code
  execution
- Non-destructive — its markers cause no harmful side effects
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Server-Side Template Injection Skill

├── Policy Gate            → Policy Engine
├── Injection Prober      → HTTP Client
├── Evaluation Analyzer
├── Engine Fingerprint Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe evaluation behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Server-Side Template Injection Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Injecting bounded expression markers and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing whether markers are evaluated and which engine class is indicated
- Confirming evaluation without escalating to code execution
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

Inject Bounded Expression Markers (HTTP Client)

↓

Observe Evaluation And Engine Indicators

↓

Record Observations → Evidence

↓

Analyze For Template Injection Weaknesses

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

`target` SHALL be an in-scope web application or API base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test, including candidate parameters.

`payload_set_ref` MAY reference a managed set of bounded expression markers. It SHALL
be a reference, never inline code-execution payloads.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with OWASP Top 10 (2021) category A03:2021 – Injection. This
category reference is informational and does not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Server-side template injection where a bounded expression marker is evaluated
  (CWE-1336)
- Input rendered by a template engine without safe handling
- A template engine class indicated by evaluation behavior, informing exploitability

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with the evaluated marker recorded and sensitive content redacted.

---

# Policy Enforcement

The Server-Side Template Injection Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Injection probing is an `active`, high-impact action; it SHALL proceed only
on an `allow` decision and within the attached rate ceiling, and SHALL commonly
require approval under the Rules of Engagement. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted. The
skill SHALL confirm evaluation without escalating to code execution, and SHALL never
test out-of-scope targets.

---

# Dependencies

The Server-Side Template Injection Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Server-Side Template Injection Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for template injection weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Server-Side Template Injection Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm evaluation with bounded expression markers only
- Never escalate to code execution or run system commands
- Reference managed marker sets, never inline code-execution payloads
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-1336
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and candidate parameters
- Provide a managed bounded expression-marker set
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide code-execution payloads
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
- adr/ADR-001-ssti-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Command Injection](../command-injection/README.md)
- [Cross-Site Scripting](../xss/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Server-Side Template Injection Skill](adr/ADR-001-ssti-skill.md)

---

# Future Extensions

Future versions MAY support

- Engine-specific evaluation modeling
- Sandbox-escape exposure assessment under stricter approval
- Blind confirmation via out-of-band channels
- Correlation of template sinks with command-injection exploitability

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Server-Side Template Injection Skill produces evidence-backed Findings for
template injection weaknesses while acting strictly within scope and Rules of
Engagement through the Policy Engine, confirming evaluation with bounded expression
markers, and never escalating to code execution or invoking tools directly.
