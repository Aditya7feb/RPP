# Command Injection Skill

**File:** `skills/web-security/command-injection/README.md`

**Version:** 1.0.0

---

# Purpose

The Command Injection Skill is a Web-Security-tier domain skill that evaluates whether
an in-scope web application passes user-controllable input into operating-system
command execution within the Robust PenTest Platform (RPP).

It examines whether input reaches a command interpreter without safe handling,
reporting weaknesses confirmed through bounded time-based and out-of-band signals
where injection is possible (CWE-78).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Command Injection Skill SHALL

- Evaluate injection points for operating-system command injection
- Confirm injection using bounded, non-destructive time-based or out-of-band signals
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for command injection weaknesses
- Remain tool independent

---

# Non-Goals

The Command Injection Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test other injection classes such as SQL or template injection (those are
  dedicated skills)
- Execute destructive commands or run a payload that alters the system
- Perform disruptive exploitation or establish persistence
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; other injection classes belong to dedicated skills; destructive command
execution is prohibited.

---

# Design Principles

The Command Injection Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms injectability with benign, bounded signals only
- Non-destructive — its probes run no harmful commands and bound induced delays
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Command Injection Skill

├── Policy Gate            → Policy Engine
├── Injection Prober      → HTTP Client
├── Time Signal Analyzer
├── Out-Of-Band Analyzer
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

The Command Injection Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Injecting bounded probes and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing bounded time-based and out-of-band interaction signals
- Confirming injectability without running harmful commands
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

Observe Time-Based And Out-Of-Band Signals

↓

Record Observations → Evidence

↓

Analyze For Command Injection Weaknesses

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

`target` SHALL be an in-scope web application or API base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test, including candidate parameters.

`payload_set_ref` MAY reference a managed set of bounded, non-destructive probes. It
SHALL be a reference, never inline destructive commands.

`collector_ref` MAY reference a controlled out-of-band collector used to confirm
interaction.

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

- Command injection confirmed by a bounded, induced execution delay (CWE-78)
- Command injection confirmed by an out-of-band interaction to a controlled
  collector
- Injection points that pass input to a command interpreter without safe handling

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with the confirming signal recorded and sensitive content redacted.

---

# Policy Enforcement

The Command Injection Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Injection probing is an `active`, high-impact action; it SHALL proceed only
on an `allow` decision and within the attached rate ceiling, and SHALL commonly
require approval under the Rules of Engagement. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Time-based probes SHALL bound induced delays, and the skill SHALL NOT run harmful
commands. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The Command Injection Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Timing Schema](../../../schemas/http-timing.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Command Injection Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for command injection weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Command Injection Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm injectability with benign, bounded signals only
- Never run harmful commands, alter the system, or establish persistence
- Bound time-based probe delays to avoid disruption
- Reference managed probe sets, never inline destructive commands
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-78
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and candidate parameters
- Provide a managed bounded probe set and a controlled collector where permitted
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide destructive command payloads
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
- adr/ADR-001-command-injection-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [SQL Injection](../sqli/README.md)
- Path Traversal (Web Security tier, planned)

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

- [ADR-001 — Command Injection Skill](adr/ADR-001-command-injection-skill.md)

---

# Future Extensions

Future versions MAY support

- Argument-injection and wildcard-injection classification
- Operating-system-aware signal modeling
- Blind confirmation via richer out-of-band channels
- Correlation of command sinks with deserialization and file-upload vectors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Command Injection Skill produces evidence-backed Findings for
operating-system command injection weaknesses while acting strictly within scope and
Rules of Engagement through the Policy Engine, confirming injectability with benign
bounded signals, and never running harmful commands or invoking tools directly.
