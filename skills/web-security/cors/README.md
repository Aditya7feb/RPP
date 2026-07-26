# CORS Skill

**File:** `skills/web-security/cors/README.md`

**Version:** 1.0.0

---

# Purpose

The CORS Skill is a Web-Security-tier domain skill that evaluates whether an in-scope
web application's Cross-Origin Resource Sharing (CORS) configuration is safe within
the Robust PenTest Platform (RPP).

It examines how the application responds to cross-origin requests, reporting
weaknesses such as reflecting an arbitrary `Origin` into
`Access-Control-Allow-Origin`, allowing credentialed access from untrusted origins,
accepting the `null` origin, and overly permissive allowed methods or headers
(CWE-942).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The CORS Skill SHALL

- Evaluate cross-origin response headers and origin-reflection behavior
- Identify credentialed access permitted from untrusted origins
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for CORS weaknesses
- Remain tool independent

---

# Non-Goals

The CORS Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Evaluate the full Content Security Policy (that is the CSP skill)
- Test cross-site request forgery defenses (that is the CSRF skill)
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; CSP and CSRF testing belong to dedicated skills.

---

# Design Principles

The CORS Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same response behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Non-destructive — it probes origin handling without harming the target
- Tool independent

---

# Architecture

```
Web Security Agent

↓

CORS Skill

├── Policy Gate            → Policy Engine
├── Origin Prober         → HTTP Client
├── Reflection Analyzer
├── Credential Analyzer
├── Method Header Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe cross-origin behavior. It SHALL
remain unaware of any transport implementation.

---

# Responsibilities

The CORS Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing cross-origin response headers through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing origin reflection, credentialed access, and permitted methods and
  headers
- Detecting arbitrary-origin reflection, `null` origin acceptance, and wildcard with
  credentials
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

Observe Cross-Origin Responses (HTTP Client)

↓

Analyze Reflection, Credentials, And Permissions

↓

Record Observations → Evidence

↓

Analyze For CORS Weaknesses

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

test_origins:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test.

`test_origins` MAY reference the untrusted origins used to probe reflection
behavior.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with OWASP Top 10 (2021) category A05:2021 – Security
Misconfiguration. This category reference is informational and does not change
capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Arbitrary `Origin` reflected into `Access-Control-Allow-Origin` (CWE-942)
- Credentialed cross-origin access allowed from untrusted origins
- Wildcard `Access-Control-Allow-Origin` combined with credentials
- The `null` origin accepted as trusted
- Overly permissive allowed methods or headers
- Weak origin validation based on substring or suffix matching

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The CORS Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Cross-origin probing is an `active` action; it SHALL proceed only on an
`allow` decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope targets SHALL never be tested.

---

# Dependencies

The CORS Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Header Schema](../../../schemas/http-header.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The CORS Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- API Security skills that rely on cross-origin context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for CORS weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The CORS Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-942
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets
- Rely on the skill for CORS evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Attempt destructive exploitation
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
- adr/ADR-001-cors-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Content Security Policy](../csp/README.md)
- [Clickjacking](../clickjacking/README.md)

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

- [ADR-001 — CORS Skill](adr/ADR-001-cors-skill.md)

---

# Future Extensions

Future versions MAY support

- Preflight-request behavior evaluation
- Origin-validation logic-flaw classification
- Correlation with authentication context for credentialed-access impact
- Handoff of cross-origin context to API Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant CORS Skill produces evidence-backed Findings for cross-origin
resource-sharing weaknesses while acting strictly within scope and Rules of
Engagement through the Policy Engine, confirming weaknesses without disruptive
exploitation, and never invoking tools directly.
