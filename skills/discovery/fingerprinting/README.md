# Fingerprinting Skill

**File:** `skills/discovery/fingerprinting/README.md`

**Version:** 1.0.0

---

# Purpose

The Fingerprinting Skill is a Discovery-tier domain skill that identifies the
technologies operating behind in-scope services, web applications, and endpoints
within the Robust PenTest Platform (RPP).

It correlates HTTP behavior, headers, response bodies, and TLS facts to identify
software, frameworks, and versions, producing canonical
[Technology](../../../schemas/technology.md) records associated with
[Assets](../../../schemas/asset.md), along with
[Observations](../../../schemas/observation.md) and, where a weakness is
identified, [Findings](../../../schemas/finding.md) with associated
[Risk](../../../schemas/risk.md).

Unlike the [HTTP Client](../../shared/http-client/README.md) and
[TLS Client](../../shared/tls-client/README.md) shared skills, which perform
transport, this skill *interprets* signals to identify technologies. It consumes
shared infrastructure and SHALL NOT invoke fingerprinting tools directly.

---

# Goals

The Fingerprinting Skill SHALL

- Identify technologies and versions behind in-scope Assets
- Correlate HTTP and TLS signals into technology identifications
- Produce canonical [Technology](../../../schemas/technology.md) records
- Emit Observations and Evidence for every identification
- Identify technology-exposure weaknesses as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  action
- Remain tool independent

---

# Non-Goals

The Fingerprinting Skill SHALL NOT

- Perform HTTP or TLS input or output directly
- Enumerate content or ports (those are dedicated skills)
- Exploit identified technologies
- Retrieve vulnerability intelligence directly from external sources
- Act on out-of-scope Assets
- Invoke fingerprinting command-line tools or parse their output

Transport belongs to the shared clients; content and port discovery belong to
dedicated skills; exploitation is out of scope for Discovery. Vulnerability
intelligence mapping is deferred to a future knowledge capability and referenced
informally where a version is known.

---

# Design Principles

The Fingerprinting Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every identification and Finding
- Deterministic given the same signals
- Confidence-graded, distinguishing certain from inferred identifications
- Passive-preferring
- Tool independent

---

# Architecture

```
Recon Agent

↓

Fingerprinting Skill

├── Policy Gate            → Policy Engine
├── Signal Collector       → HTTP Client / TLS Client
├── Technology Matcher
├── Technology Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Technologies · Assets · Observations · Evidence · Findings · Risk
```

The skill orchestrates shared clients to interpret signals. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The Fingerprinting Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  action
- Collecting signals through the [HTTP Client](../../shared/http-client/README.md)
  and [TLS Client](../../shared/tls-client/README.md)
- Matching signals to technologies and versions
- Producing canonical [Technology](../../../schemas/technology.md) records and
  linking them to [Assets](../../../schemas/asset.md)
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for technology-exposure weaknesses

---

# Discovery Lifecycle

```
Receive Asset Target

↓

Consult Policy Engine (per action)

↓

Collect Signals (HTTP / TLS Client)

↓

Match Technologies And Versions

↓

Record Observations → Evidence

↓

Produce Technology Records

↓

Analyze For Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

asset_id:

signals:

scope_id:

roe_id:
```

`target` SHALL be an in-scope service, web application, or endpoint.

`asset_id` MAY reference the Asset being fingerprinted.

`signals` SHALL declare the signal sources to consult, such as `headers`, `body`,
`cookies`, `favicon`, and `tls`.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Objects

The skill SHALL produce canonical
[Technology](../../../schemas/technology.md) records identifying software,
frameworks, and versions, and SHALL link each to the fingerprinted
[Asset](../../../schemas/asset.md) through an
[Asset Relationship](../../../schemas/asset-relationship.md) such as `references`.

Where a web application is confirmed, the skill MAY produce or enrich a
`web-application` Asset.

Each produced object SHALL carry provenance and a `scope_status` set from the
assessment Scope.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for technology-exposure weaknesses such as

- Outdated or end-of-life software versions observed
- Verbose version disclosure in headers or errors
- Default or sample components exposed

Where a version is identified, the Finding MAY reference known-vulnerability
identifiers informally; deterministic vulnerability mapping is deferred to a
future knowledge capability.

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Fingerprinting Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every action and
SHALL proceed only on an `allow` decision. Fingerprinting SHOULD prefer passive
signals; active probing SHALL be gated accordingly. Out-of-scope Assets SHALL
never be fingerprinted.

---

# Dependencies

The Fingerprinting Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [TLS Client](../../shared/tls-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Technology Schema](../../../schemas/technology.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Fingerprinting Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- Web Security and API Security skills that target identified technologies
- Reporting, through the produced Technologies, Findings, and Risk

---

# Outputs

Typical outputs MAY include

- Technology records linked to Assets
- Observations and Evidence references
- Findings with Risk for technology-exposure weaknesses

Outputs SHALL remain implementation independent.

---

# Security Principles

The Fingerprinting Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Prefer passive signals to minimize target interaction
- Produce no Finding without supporting Evidence
- Grade identification confidence honestly
- Report weaknesses as data; exploitation is out of scope
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope Asset and available signals
- Rely on the skill for canonical Technology production
- Treat identified Technologies as inputs to security testing
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Perform HTTP or TLS requests directly
- Bypass the Policy Engine
- Assert technologies without evidence or confidence grading
- Act on out-of-scope Assets

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
- adr/ADR-001-fingerprinting-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [TLS Client](../../shared/tls-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)

---

# Canonical Schemas

- [Technology](../../../schemas/technology.md)
- [Asset](../../../schemas/asset.md)
- [Asset Relationship](../../../schemas/asset-relationship.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Fingerprinting Skill](adr/ADR-001-fingerprinting-skill.md)

---

# Future Extensions

Future versions MAY support

- Deterministic technology-to-vulnerability mapping via a knowledge capability
- Favicon and asset-hash correlation
- Behavioral fingerprinting of frameworks
- Version-inference confidence refinement

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Fingerprinting Skill produces canonical, evidence-backed
[Technology](../../../schemas/technology.md) identifications linked to Assets, and
technology-exposure Findings, while acting strictly within scope and Rules of
Engagement through the Policy Engine, without invoking fingerprinting tools
directly.
