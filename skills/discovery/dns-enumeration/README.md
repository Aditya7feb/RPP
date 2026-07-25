# DNS Enumeration Skill

**File:** `skills/discovery/dns-enumeration/README.md`

**Version:** 1.0.0

---

# Purpose

The DNS Enumeration Skill is a Discovery-tier domain skill that identifies the
Domain Name System (DNS) footprint of an assessment target within the Robust
PenTest Platform (RPP).

It enumerates records, resolves names, and maps name-to-address and
name-to-service relationships, producing canonical
[Assets](../../../schemas/asset.md), [Asset Relationships](../../../schemas/asset-relationship.md),
[Observations](../../../schemas/observation.md), and, where a weakness is
identified, [Findings](../../../schemas/finding.md) with associated
[Risk](../../../schemas/risk.md).

Unlike the [DNS Client](../../shared/dns-client/README.md) shared skill, which
performs DNS operations, this skill *interprets* DNS results to build the
assessment attack surface. It consumes shared infrastructure and SHALL NOT invoke
DNS tools directly.

---

# Goals

The DNS Enumeration Skill SHALL

- Enumerate DNS records for in-scope targets
- Resolve names to addresses and services
- Produce canonical Assets and Asset Relationships
- Emit Observations and Evidence for every result
- Identify DNS-related weaknesses as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  action
- Remain tool independent

---

# Non-Goals

The DNS Enumeration Skill SHALL NOT

- Perform raw DNS input or output directly
- Brute-force subdomains (that is the Subdomain Discovery skill)
- Exploit DNS weaknesses
- Act on out-of-scope targets
- Invoke DNS command-line tools or parse their output

Record retrieval belongs to the [DNS Client](../../shared/dns-client/README.md);
subdomain brute-forcing belongs to a dedicated Subdomain Discovery skill;
exploitation is out of scope for Discovery.

---

# Design Principles

The DNS Enumeration Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and DNS responses
- Confidence-graded
- Tool independent
- Observable

---

# Architecture

```
Recon Agent

↓

DNS Enumeration Skill

├── Policy Gate            → Policy Engine
├── Record Enumerator      → DNS Client
├── Asset Builder
├── Relationship Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates shared infrastructure to interpret DNS results. It SHALL
remain unaware of any DNS implementation.

---

# Responsibilities

The DNS Enumeration Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Enumerating records through the [DNS Client](../../shared/dns-client/README.md)
- Building [Assets](../../../schemas/asset.md) for domains, subdomains, hosts, and
  services
- Building [Asset Relationships](../../../schemas/asset-relationship.md) such as
  `resolves-to`
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and [Risk](../../../schemas/risk.md)
  for DNS weaknesses

---

# Discovery Lifecycle

```
Receive Target

↓

Consult Policy Engine (per action)

↓

Enumerate Records (DNS Client)

↓

Record Observations → Evidence

↓

Build Assets and Relationships

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

record_types:

scope_id:

roe_id:
```

`target` SHALL be an in-scope domain or host.

`record_types` SHALL enumerate the record classes to query, such as `A`, `AAAA`,
`CNAME`, `MX`, `NS`, `TXT`, `SOA`, and `SRV`.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical [Assets](../../../schemas/asset.md) of types

- `domain`
- `subdomain`
- `host`
- `ip`
- `service`

and canonical [Asset Relationships](../../../schemas/asset-relationship.md) such
as `resolves-to`, `hosts`, and `serves`.

Each Asset SHALL carry provenance referencing the Observations and Evidence from
which it was derived, and a `scope_status` set from the assessment Scope.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for DNS-related weaknesses such as

- Zone transfer exposure
- Dangling or stale records pointing to unclaimed resources
- Wildcard records that broaden the attack surface
- Missing or weak email-authentication records observed as informational

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
and SHALL NOT exist without it.

---

# Policy Enforcement

The DNS Enumeration Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action and SHALL proceed only on an `allow` decision. Actions requiring approval
SHALL be routed accordingly. Out-of-scope targets SHALL never be queried.

---

# Dependencies

The DNS Enumeration Skill depends on

- [DNS Client](../../shared/dns-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The DNS Enumeration Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- Subdomain Discovery and Asset Discovery skills that build on DNS assets
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Domain, subdomain, host, and service Assets
- Asset Relationships forming the DNS portion of the asset graph
- Observations and Evidence references
- Findings with Risk for DNS weaknesses

Outputs SHALL remain implementation independent.

---

# Security Principles

The DNS Enumeration Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Produce no Finding without supporting Evidence
- Report weaknesses as data; exploitation is out of scope
- Protect any sensitive record data through evidence redaction
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an explicit, in-scope target
- Rely on the skill for Asset and Relationship construction
- Treat produced Assets as canonical inputs to later skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call DNS tools directly
- Bypass the Policy Engine
- Treat enumeration results as findings without evidence
- Act on out-of-scope names

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
- adr/ADR-001-dns-enumeration-skill.md

---

# Related Packages

- [DNS Client](../../shared/dns-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)

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

- [ADR-001 — DNS Enumeration Skill](adr/ADR-001-dns-enumeration-skill.md)

---

# Future Extensions

Future versions MAY support

- Passive DNS integration
- DNSSEC validation-state reporting
- Reverse-DNS sweeps within scope
- Historical record correlation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant DNS Enumeration Skill produces a canonical, evidence-backed DNS view
of the assessment attack surface — Assets, Relationships, Observations, and
DNS-weakness Findings — while acting strictly within scope and Rules of
Engagement through the Policy Engine, without invoking DNS tools directly.
