# Cross-Site Scripting Capabilities

**File:** `skills/web-security/xss/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Cross-Site Scripting Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Cross-Site Scripting Interface](interface.md).

---

# Capability Model

```
Authorization

Injection Probing

Rendering Observation

Context Analysis

Encoding Analysis

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every target-facing action.

---

## Scope Confinement

The skill SHALL test only in-scope applications.

---

# Injection Probing Capabilities

## Bounded Marker Injection

The skill SHALL inject bounded, non-destructive marker payloads through the
[HTTP Client](../../shared/http-client/README.md).

---

## Reflected And Stored Probing

The skill SHALL probe reflected and stored injection points, treating stored
probing as higher impact.

---

# Rendering Observation Capabilities

## Rendered Execution Observation

The skill SHALL observe marker execution in rendered and DOM-based contexts through
the [Browser](../../shared/browser/README.md).

---

# Context Analysis Capabilities

## Output Context Analysis

The skill SHALL determine the output context — HTML, attribute, JavaScript, or URL —
into which input is placed.

---

# Encoding Analysis Capabilities

## Encoding Adequacy Analysis

The skill SHALL determine whether encoding or sanitization is context-appropriate and
adequate.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify reflected, stored, and DOM-based XSS from observed behavior
and classify them using canonical weakness identifiers such as CWE-79.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with the confirming marker recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including injection points tested and findings
emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output or browser rendering directly
- Discover applications or endpoints
- Evaluate CSP in isolation or test server-side template injection
- Deliver weaponized payloads or perform destructive exploitation
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Marker Injection | Injection Probing | SHALL |
| Reflected And Stored Probing | Injection Probing | SHALL |
| Rendered Execution Observation | Rendering Observation | SHALL |
| Output Context Analysis | Context Analysis | SHALL |
| Encoding Adequacy Analysis | Encoding Analysis | SHALL |
| Weakness Identification | Weakness Analysis | SHALL |
| Finding Production | Weakness Analysis | SHALL |
| Observation And Evidence | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Browser](../../shared/browser/README.md)
