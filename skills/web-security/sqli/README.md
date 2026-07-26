# SQL Injection Skill

**File:** `skills/web-security/sqli/README.md`

**Version:** 1.0.0

---

# Purpose

The SQL Injection Skill is a Web-Security-tier domain skill that evaluates whether an
in-scope web application is vulnerable to SQL injection (SQLi) within the Robust
PenTest Platform (RPP).

It examines whether user-controllable input alters the structure of backend SQL
queries, reporting weaknesses confirmed through error-based, boolean-based, and
time-based signals where input is not safely parameterized (CWE-89).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The SQL Injection Skill SHALL

- Evaluate injection points for error-based, boolean-based, and time-based SQLi
- Confirm injection using bounded, non-destructive probes
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for SQL injection weaknesses
- Remain tool independent

---

# Non-Goals

The SQL Injection Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test other injection classes such as command or template injection (those are
  dedicated skills)
- Extract, modify, or destroy database contents
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; other injection classes belong to dedicated skills; data exfiltration and
modification are prohibited.

---

# Design Principles

The SQL Injection Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms injectability without extracting or altering data
- Non-destructive — its probes cause no data loss and bound time-based delays
- Tool independent

---

# Architecture

```
Web Security Agent

↓

SQL Injection Skill

├── Policy Gate            → Policy Engine
├── Injection Prober      → HTTP Client
├── Error Signal Analyzer
├── Boolean Signal Analyzer
├── Time Signal Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe injection signals. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The SQL Injection Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Injecting bounded probes and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing error-based, boolean-based, and time-based injection signals
- Confirming injectability without extracting or altering data
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

Inject Bounded Probes (HTTP Client)

↓

Observe Error, Boolean, And Time Signals

↓

Record Observations → Evidence

↓

Analyze For SQL Injection Weaknesses

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

`payload_set_ref` MAY reference a managed set of bounded, non-destructive probes. It
SHALL be a reference, never inline data-extraction payloads.

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

- Error-based SQL injection where malformed input yields database errors (CWE-89)
- Boolean-based blind SQL injection where true and false conditions diverge
- Time-based blind SQL injection where a bounded delay is induced
- Injection points that are not safely parameterized

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with the confirming signal recorded and sensitive content redacted.

---

# Policy Enforcement

The SQL Injection Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Injection probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Time-based probes SHALL bound induced delays to avoid disruption. The skill SHALL
NOT extract, modify, or destroy data, and SHALL never test out-of-scope targets.

---

# Dependencies

The SQL Injection Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Timing Schema](../../../schemas/http-timing.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The SQL Injection Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- API Security skills that build on injection context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for SQL injection weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The SQL Injection Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm injectability without extracting, modifying, or destroying data
- Bound time-based probe delays to avoid disruption
- Reference managed probe sets, never inline data-extraction payloads
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-89
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and candidate parameters
- Provide a managed bounded probe set
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide data-extraction or destructive payloads
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
- adr/ADR-001-sql-injection-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Cross-Site Scripting](../xss/README.md)
- Command Injection (Web Security tier, planned)

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

- [ADR-001 — SQL Injection Skill](adr/ADR-001-sql-injection-skill.md)

---

# Future Extensions

Future versions MAY support

- Second-order and stored SQL injection confirmation
- Out-of-band confirmation via controlled collectors
- Database-technology-aware signal modeling
- Bounded, authorized data-shape confirmation under stricter approval

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SQL Injection Skill produces evidence-backed Findings for SQL injection
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming injectability without extracting or altering data, and
never invoking tools directly.
