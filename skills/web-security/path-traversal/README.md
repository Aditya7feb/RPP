# Path Traversal Skill

**File:** `skills/web-security/path-traversal/README.md`

**Version:** 1.0.0

---

# Purpose

The Path Traversal Skill is a Web-Security-tier domain skill that evaluates whether an
in-scope web application allows access to files outside the intended directory within
the Robust PenTest Platform (RPP).

It examines whether user-controllable path input escapes an intended base directory,
reporting weaknesses where traversal sequences reach files outside the intended
location without safe canonicalization (CWE-22).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Path Traversal Skill SHALL

- Evaluate path parameters for directory traversal outside the intended base
- Confirm traversal using bounded, non-sensitive marker reads
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for path traversal weaknesses
- Remain tool independent

---

# Non-Goals

The Path Traversal Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test server-side request forgery or file upload (those are dedicated skills)
- Read, exfiltrate, or modify sensitive files
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; request-forgery and upload testing belong to dedicated skills; reading
sensitive files is prohibited.

---

# Design Principles

The Path Traversal Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms traversal without reading sensitive files
- Non-destructive — its probes read only bounded, non-sensitive markers
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Path Traversal Skill

├── Policy Gate            → Policy Engine
├── Traversal Prober      → HTTP Client
├── Canonicalization Analyzer
├── Marker Read Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe traversal behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Path Traversal Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Injecting bounded traversal probes and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing canonicalization and encoding-bypass handling
- Confirming traversal using non-sensitive marker reads only
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

Inject Bounded Traversal Probes (HTTP Client)

↓

Observe Marker Reads And Canonicalization

↓

Record Observations → Evidence

↓

Analyze For Path Traversal Weaknesses

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

marker_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test, including candidate path parameters.

`marker_ref` MAY reference a non-sensitive marker resource used to confirm traversal
without reading sensitive files.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with OWASP Top 10 (2021) category A01:2021 – Broken Access
Control. This category reference is informational and does not change capability
scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Directory traversal reaching files outside the intended base directory (CWE-22)
- Insufficient canonicalization allowing traversal sequences
- Encoded or double-encoded traversal that bypasses filtering
- Path parameters that resolve outside an allowed root

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with sensitive content redacted and only non-sensitive marker reads recorded.

---

# Policy Enforcement

The Path Traversal Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Traversal probing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted. The
skill SHALL confirm traversal using non-sensitive markers and SHALL NOT read or
exfiltrate sensitive files. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The Path Traversal Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Path Traversal Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for path traversal weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Path Traversal Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm traversal using non-sensitive marker reads only
- Never read, exfiltrate, or modify sensitive files
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-22
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and candidate path parameters
- Provide a non-sensitive marker resource for confirmation
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Read or exfiltrate sensitive files
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
- adr/ADR-001-path-traversal-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Command Injection](../command-injection/README.md)
- File Upload (Web Security tier, planned)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Path Traversal Skill](adr/ADR-001-path-traversal-skill.md)

---

# Future Extensions

Future versions MAY support

- Absolute-path and null-byte injection classification
- Archive-extraction traversal evaluation
- Operating-system-aware path modeling
- Correlation of traversal sinks with file-upload and inclusion vectors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Path Traversal Skill produces evidence-backed Findings for directory
traversal weaknesses while acting strictly within scope and Rules of Engagement
through the Policy Engine, confirming traversal with non-sensitive markers, and never
reading sensitive files or invoking tools directly.
