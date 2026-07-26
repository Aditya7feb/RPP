# Web Cache Poisoning Skill

**File:** `skills/web-security/cache-poisoning/README.md`

**Version:** 1.0.0

---

# Purpose

The Web Cache Poisoning Skill is a Web-Security-tier domain skill that evaluates
whether an in-scope web application's caching behavior can be poisoned through
unkeyed input within the Robust PenTest Platform (RPP).

It examines whether unkeyed request inputs influence cached responses, reporting
weaknesses where an attacker can cause a harmful response to be served to other users
from the cache (CWE-444 and related web-cache-poisoning weaknesses).

The skill consumes the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Web Cache Poisoning Skill SHALL

- Evaluate caching behavior for unkeyed inputs that influence cached responses
- Confirm poisoning using bounded, benign markers scoped to a controlled cache key
- Consume `web-application` and `endpoint` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for cache poisoning weaknesses
- Remain tool independent

---

# Non-Goals

The Web Cache Poisoning Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test cross-site scripting payloads in cached responses (that is the XSS skill)
- Poison a shared cache key that serves real users
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; script-execution testing belongs to the XSS skill; poisoning shared user-facing
cache keys is prohibited.

---

# Design Principles

The Web Cache Poisoning Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same caching behavior
- Conservative — it confirms cacheability of unkeyed input using controlled cache keys
- Non-destructive — it never poisons a cache entry that serves real users
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Web Cache Poisoning Skill

├── Policy Gate            → Policy Engine
├── Cache Prober          → HTTP Client
├── Unkeyed Input Analyzer
├── Cache Reflection Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe caching behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Web Cache Poisoning Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting bounded probes with unkeyed inputs against a controlled cache key through
  the [HTTP Client](../../shared/http-client/README.md)
- Analyzing whether unkeyed inputs are reflected into cached responses
- Confirming poisonability without affecting real users
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

Submit Bounded Probes Against Controlled Cache Key (HTTP Client)

↓

Analyze Unkeyed Input Reflection Into Cache

↓

Record Observations → Evidence

↓

Analyze For Cache Poisoning Weaknesses

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

`target` SHALL be an in-scope web application base URL served through a cache.

`assets` reference the `web-application` and `endpoint`
[Assets](../../../schemas/asset.md) under test.

`marker_ref` MAY reference a benign marker used to confirm reflection into a
controlled cache key.

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

- Unkeyed input reflected into a cached response, enabling cache poisoning
- Cache keys that omit security-relevant request inputs
- Response splitting or header-based cache manipulation (CWE-444)
- Cache-deception conditions serving one user's response to another

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only controlled-cache-key confirmation recorded and sensitive content redacted.

---

# Policy Enforcement

The Web Cache Poisoning Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Cache probing is an `active`, higher-impact action; it SHALL proceed only on
an `allow` decision and within the attached rate ceiling, and SHALL commonly require
approval under the Rules of Engagement. Where a decision is `requires_approval`, the
skill SHALL defer the action until approval is granted. The skill SHALL confirm
poisonability using a controlled cache key and SHALL NOT poison a cache entry that
serves real users. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The Web Cache Poisoning Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Header Schema](../../../schemas/http-header.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Web Cache Poisoning Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for cache poisoning weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Web Cache Poisoning Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm poisonability using controlled cache keys only
- Never poison a cache entry that serves real users
- Reference benign markers only
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-444
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets served through a cache
- Provide a benign marker and a controllable cache-key strategy
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Poison shared user-facing cache keys
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
- adr/ADR-001-cache-poisoning-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Content Security Policy](../csp/README.md)
- [Cross-Site Scripting](../xss/README.md)

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

- [ADR-001 — Web Cache Poisoning Skill](adr/ADR-001-cache-poisoning-skill.md)

---

# Future Extensions

Future versions MAY support

- Cache-deception condition modeling
- Header-and-parameter cloaking classification
- Fat-GET and parameter-pollution cache evaluation
- Correlation of cache poisoning with XSS delivery under stricter approval

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Web Cache Poisoning Skill produces evidence-backed Findings for web cache
poisoning weaknesses while acting strictly within scope and Rules of Engagement
through the Policy Engine, confirming poisonability using controlled cache keys, and
never affecting real users or invoking tools directly.
