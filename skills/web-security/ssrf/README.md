# Server-Side Request Forgery Skill

**File:** `skills/web-security/ssrf/README.md`

**Version:** 1.0.0

---

# Purpose

The Server-Side Request Forgery Skill is a Web-Security-tier domain skill that
evaluates whether an in-scope web application can be induced to make server-side
requests to attacker-influenced destinations within the Robust PenTest Platform
(RPP).

It examines whether user-controllable input causes the server to fetch a destination,
reporting weaknesses confirmed through out-of-band interaction and bounded response
differential signals where forgery is possible (CWE-918).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Server-Side Request Forgery Skill SHALL

- Evaluate request-issuing parameters for server-side request forgery
- Confirm forgery using a controlled out-of-band collector and bounded differentials
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for SSRF weaknesses
- Remain tool independent

---

# Non-Goals

The Server-Side Request Forgery Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test client-side open redirection (that is the Open Redirect skill)
- Access internal services, cloud metadata, or sensitive endpoints to demonstrate
  impact
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; client-side redirection belongs to the Open Redirect skill; reaching internal
or sensitive services is prohibited.

---

# Design Principles

The Server-Side Request Forgery Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms forgery to a controlled destination, not internal
  services
- Non-destructive — it targets only authorized controlled or benign destinations
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Server-Side Request Forgery Skill

├── Policy Gate            → Policy Engine
├── Request Prober        → HTTP Client
├── Out-Of-Band Analyzer
├── Differential Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe forgery behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Server-Side Request Forgery Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting bounded probes toward a controlled destination and observing responses
  through the [HTTP Client](../../shared/http-client/README.md)
- Analyzing out-of-band interaction and response-differential signals
- Confirming forgery to a controlled destination without reaching internal services
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

Submit Bounded Probes Toward Controlled Destination (HTTP Client)

↓

Observe Out-Of-Band And Differential Signals

↓

Record Observations → Evidence

↓

Analyze For SSRF Weaknesses

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

collector_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test, including request-issuing parameters.

`collector_ref` MAY reference a controlled out-of-band collector used to confirm
forgery.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with OWASP Top 10 (2021) category A10:2021 – Server-Side
Request Forgery (SSRF). This category reference is informational and does not change
capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Server-side request forgery confirmed by an out-of-band interaction to a controlled
  collector (CWE-918)
- Request-issuing parameters that fetch attacker-influenced destinations
- Insufficient destination validation permitting internal-address targeting

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only controlled-destination interaction recorded and sensitive content redacted.

---

# Policy Enforcement

The Server-Side Request Forgery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Forgery probing is an `active`, high-impact action; it SHALL proceed only on
an `allow` decision and within the attached rate ceiling, and SHALL commonly require
approval under the Rules of Engagement. Where a decision is `requires_approval`, the
skill SHALL defer the action until approval is granted. The skill SHALL confirm
forgery using a controlled destination and SHALL NOT reach internal services, cloud
metadata, or sensitive endpoints. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The Server-Side Request Forgery Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [HTTP Timing Schema](../../../schemas/http-timing.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Server-Side Request Forgery Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- Cloud Security skills that assess metadata-service exposure
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for SSRF weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Server-Side Request Forgery Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm forgery to a controlled destination only
- Never reach internal services, cloud metadata, or sensitive endpoints
- Reference authorized collectors only
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-918
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and request-issuing parameters
- Provide a controlled out-of-band collector
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Target internal services or cloud metadata to prove impact
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
- adr/ADR-001-ssrf-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Open Redirect](../open-redirect/README.md)
- [XML External Entity](../xxe/README.md)

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

- [ADR-001 — Server-Side Request Forgery Skill](adr/ADR-001-ssrf-skill.md)

---

# Future Extensions

Future versions MAY support

- Blind SSRF confirmation via richer out-of-band channels
- Protocol-smuggling and redirect-based SSRF classification
- Correlation of SSRF with cloud metadata-service exposure under stricter approval
- Destination-allow-list bypass classification

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Server-Side Request Forgery Skill produces evidence-backed Findings for
SSRF weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming forgery to a controlled destination, and never reaching
internal services or invoking tools directly.
