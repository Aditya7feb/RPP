# Unrestricted File Upload Skill

**File:** `skills/web-security/file-upload/README.md`

**Version:** 1.0.0

---

# Purpose

The Unrestricted File Upload Skill is a Web-Security-tier domain skill that evaluates
whether an in-scope web application safely restricts uploaded files within the Robust
PenTest Platform (RPP).

It examines whether file type, content, and storage are validated, reporting
weaknesses where an application accepts dangerous file types or serves uploaded
content unsafely (CWE-434).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Unrestricted File Upload Skill SHALL

- Evaluate upload endpoints for unsafe type, content, and storage handling
- Confirm acceptance using bounded, non-executable marker files
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for file upload weaknesses
- Remain tool independent

---

# Non-Goals

The Unrestricted File Upload Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test path traversal in upload paths (that is the Path Traversal skill)
- Upload or execute a functional web shell or malicious payload
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; path traversal belongs to a dedicated skill; uploading functional malicious
payloads is prohibited.

---

# Design Principles

The Unrestricted File Upload Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms weak validation with inert marker files, not web shells
- Non-destructive — its markers are inert and non-executable
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Unrestricted File Upload Skill

├── Policy Gate            → Policy Engine
├── Upload Prober         → HTTP Client
├── Type Validation Analyzer
├── Content Validation Analyzer
├── Storage Exposure Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe upload validation. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Unrestricted File Upload Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting inert marker files and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing type, content, and storage validation
- Confirming weak validation without uploading functional malicious payloads
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

Submit Inert Marker Files (HTTP Client)

↓

Analyze Type, Content, And Storage Validation

↓

Record Observations → Evidence

↓

Analyze For File Upload Weaknesses

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

marker_set_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL with upload
functionality.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test, including upload endpoints.

`marker_set_ref` MAY reference a managed set of inert, non-executable marker files. It
SHALL be a reference, never functional malicious payloads.

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

- Dangerous file types accepted without adequate validation (CWE-434)
- Type validation based only on extension or client-supplied content type
- Uploaded content served with an executable or unsafe content type
- Uploaded files stored in a web-accessible location without safeguards

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only inert marker uploads recorded and sensitive content redacted.

---

# Policy Enforcement

The Unrestricted File Upload Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Upload probing is an `active`, higher-impact action; it SHALL proceed only on
an `allow` decision and within the attached rate ceiling, and SHALL commonly require
approval under the Rules of Engagement. Where a decision is `requires_approval`, the
skill SHALL defer the action until approval is granted. The skill SHALL upload only
inert marker files and SHALL NOT upload or execute functional malicious payloads.
Out-of-scope targets SHALL never be tested.

---

# Dependencies

The Unrestricted File Upload Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Unrestricted File Upload Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for file upload weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Unrestricted File Upload Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weak validation with inert, non-executable marker files only
- Never upload or execute functional malicious payloads or web shells
- Reference managed marker sets, never functional malicious payloads
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-434
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and upload endpoints
- Provide a managed inert marker-file set
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Upload functional web shells or malicious payloads
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
- adr/ADR-001-file-upload-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Path Traversal](../path-traversal/README.md)
- [Command Injection](../command-injection/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Unrestricted File Upload Skill](adr/ADR-001-file-upload-skill.md)

---

# Future Extensions

Future versions MAY support

- Content-type and magic-byte validation modeling
- Image and document parser-exposure evaluation
- Correlation of upload sinks with path-traversal and command-injection vectors
- Storage-location exposure classification

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Unrestricted File Upload Skill produces evidence-backed Findings for file
upload weaknesses while acting strictly within scope and Rules of Engagement through
the Policy Engine, confirming weak validation with inert markers, and never uploading
functional malicious payloads or invoking tools directly.
