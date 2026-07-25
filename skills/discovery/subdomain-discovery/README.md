# Subdomain Discovery Skill

**File:** `skills/discovery/subdomain-discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The Subdomain Discovery Skill is a Discovery-tier domain skill that identifies the
subdomains of an in-scope apex domain within the Robust PenTest Platform (RPP).

It combines passive enumeration and bounded active resolution to discover
subdomains, producing canonical `subdomain`
[Assets](../../../schemas/asset.md), `resolves-to`
[Asset Relationships](../../../schemas/asset-relationship.md),
[Observations](../../../schemas/observation.md), and, where a weakness is
identified, [Findings](../../../schemas/finding.md) with associated
[Risk](../../../schemas/risk.md).

Unlike the [DNS Enumeration](../dns-enumeration/README.md) skill, which enumerates
records for known names, this skill *discovers previously unknown names*. It
consumes shared infrastructure and SHALL NOT invoke subdomain tools directly.

---

# Goals

The Subdomain Discovery Skill SHALL

- Discover subdomains of an in-scope apex domain
- Combine passive sources with bounded active resolution
- Produce canonical `subdomain` Assets and `resolves-to` relationships
- Emit Observations and Evidence for every candidate
- Identify subdomain-takeover exposure as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  active resolution
- Remain tool independent

---

# Non-Goals

The Subdomain Discovery Skill SHALL NOT

- Perform DNS input or output directly
- Enumerate all records for each name (that is DNS Enumeration)
- Exploit takeover opportunities
- Act on out-of-scope domains
- Invoke subdomain-enumeration command-line tools or parse their output

Record enumeration belongs to the
[DNS Enumeration](../dns-enumeration/README.md) skill; exploitation is out of
scope for Discovery.

---

# Design Principles

The Subdomain Discovery Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and sources
- Confidence-graded, distinguishing passive candidates from resolved subdomains
- Bounded in candidate volume and resolution rate
- Tool independent

---

# Architecture

```
Recon Agent

↓

Subdomain Discovery Skill

├── Policy Gate            → Policy Engine
├── Passive Collector
├── Candidate Generator
├── Resolver               → DNS Client
├── Asset Builder
├── Takeover Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates the DNS Client and passive sources to discover names. It
SHALL remain unaware of any DNS implementation.

---

# Responsibilities

The Subdomain Discovery Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  active resolution
- Collecting passive subdomain candidates
- Generating bounded active candidates within scope
- Resolving candidates through the [DNS Client](../../shared/dns-client/README.md)
- Building `subdomain` [Assets](../../../schemas/asset.md) and `resolves-to`
  relationships
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for subdomain-takeover exposure

---

# Discovery Lifecycle

```
Receive Apex Domain

↓

Collect Passive Candidates

↓

Generate Bounded Active Candidates

↓

For Each Candidate:

  ├── Consult Policy Engine (active resolution)
  └── Resolve (DNS Client)

↓

Record Observations → Evidence

↓

Build Subdomain Assets and Relationships

↓

Analyze For Takeover Exposure

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
apex_domain:

sources:

wordlist_ref:

scope_id:

roe_id:
```

`apex_domain` SHALL be an in-scope apex domain.

`sources` SHALL declare the passive sources and whether active resolution is
enabled.

`wordlist_ref` SHALL reference a candidate list for active generation.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical `subdomain`
[Assets](../../../schemas/asset.md) and `resolves-to`
[Asset Relationships](../../../schemas/asset-relationship.md) linking each
subdomain to the host or address it resolves to.

Passive-only candidates that are not resolved SHALL be recorded as `subdomain`
Assets in the `suspected` state; resolved subdomains SHALL be `confirmed`.

Each Asset SHALL carry provenance and a `scope_status` set from the assessment
Scope.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for exposure such as

- Subdomain takeover potential from a dangling delegation or CNAME to an
  unclaimed resource
- Internal or staging subdomains exposed publicly

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Subdomain Discovery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every active
resolution. Passive collection uses no direct target interaction, but every
resolved candidate SHALL be confirmed in-scope, and out-of-scope subdomains SHALL
be recorded without further active probing.

---

# Dependencies

The Subdomain Discovery Skill depends on

- [DNS Client](../../shared/dns-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Subdomain Discovery Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- The DNS Enumeration, Port Discovery, and Content Discovery skills
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Subdomain Assets and `resolves-to` relationships
- Observations and Evidence references
- Findings with Risk for takeover exposure

Outputs SHALL remain implementation independent.

---

# Security Principles

The Subdomain Discovery Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound candidate volume and resolution rate
- Produce no Finding without supporting Evidence
- Grade candidate confidence honestly
- Report takeover potential as data; exploitation is out of scope
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope apex domain and curated passive sources
- Rely on the skill for subdomain Asset construction
- Treat resolved subdomains as inputs to DNS Enumeration and Port Discovery
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Resolve names directly
- Bypass the Policy Engine for active resolution
- Generate unbounded candidate lists
- Act on out-of-scope domains

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
- adr/ADR-001-subdomain-discovery-skill.md

---

# Related Packages

- [DNS Client](../../shared/dns-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [DNS Enumeration](../dns-enumeration/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Asset Relationship](../../../schemas/asset-relationship.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Subdomain Discovery Skill](adr/ADR-001-subdomain-discovery-skill.md)

---

# Future Extensions

Future versions MAY support

- Certificate-transparency source integration
- Permutation and alteration candidate generation
- Passive DNS correlation
- Wildcard-aware resolution filtering

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Subdomain Discovery Skill produces a canonical, evidence-backed set of
`subdomain` Assets and takeover-exposure Findings, while acting strictly within
scope and Rules of Engagement through the Policy Engine, without invoking
subdomain tools directly.
