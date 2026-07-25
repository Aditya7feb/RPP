# Content Discovery Skill

**File:** `skills/discovery/content-discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The Content Discovery Skill is a Discovery-tier domain skill that enumerates the
reachable paths, directories, and files of an in-scope web application within the
Robust PenTest Platform (RPP).

It probes candidate paths, follows discovered links within scope, and produces
canonical `endpoint` and `web-application`
[Assets](../../../schemas/asset.md), [Observations](../../../schemas/observation.md),
and, where a weakness is identified, [Findings](../../../schemas/finding.md) with
associated [Risk](../../../schemas/risk.md).

Unlike the [HTTP Client](../../shared/http-client/README.md) shared skill, which
performs requests, this skill *interprets* responses to map the web content
surface. It consumes shared infrastructure and SHALL NOT invoke content-discovery
tools directly.

---

# Goals

The Content Discovery Skill SHALL

- Enumerate candidate paths and directories on in-scope web applications
- Discover linked content within scope and bounds
- Produce canonical `endpoint` and `web-application` Assets
- Emit Observations and Evidence for every probe
- Identify content-exposure weaknesses as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  request
- Remain tool independent

---

# Non-Goals

The Content Discovery Skill SHALL NOT

- Perform HTTP input or output directly
- Fingerprint technologies in depth (that is the Fingerprinting skill)
- Enumerate API operations in depth (that is the API Discovery skill)
- Exploit discovered content
- Act on out-of-scope applications
- Invoke content-discovery command-line tools or parse their output

HTTP transport belongs to the [HTTP Client](../../shared/http-client/README.md);
deep technology and API analysis belong to dedicated skills; exploitation is out
of scope for Discovery.

---

# Design Principles

The Content Discovery Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and responses
- Confidence-graded
- Bounded in request volume and crawl depth
- Tool independent

---

# Architecture

```
Recon Agent

↓

Content Discovery Skill

├── Policy Gate            → Policy Engine
├── Path Prober            → HTTP Client
├── Link Extractor
├── Asset Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to interpret web content. It SHALL remain
unaware of any HTTP implementation.

---

# Responsibilities

The Content Discovery Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  request
- Probing paths through the [HTTP Client](../../shared/http-client/README.md)
- Extracting in-scope links from responses
- Building `endpoint` and `web-application`
  [Assets](../../../schemas/asset.md) and their relationships
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for content-exposure weaknesses

---

# Discovery Lifecycle

```
Receive Application Target

↓

Consult Policy Engine (per request)

↓

Probe Candidate Paths (HTTP Client)

↓

Extract In-Scope Links

↓

Record Observations → Evidence

↓

Build Endpoint Assets

↓

Analyze For Exposure Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

wordlist_ref:

follow_links:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application base URL.

`wordlist_ref` SHALL reference a curated candidate-path list.

`follow_links` SHALL declare whether discovered in-scope links are enumerated
within bounds.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical [Assets](../../../schemas/asset.md) of types

- `endpoint`
- `web-application`

and [Asset Relationships](../../../schemas/asset-relationship.md) such as
`serves` and `references` linking endpoints to their application.

Each Asset SHALL carry provenance and a `scope_status` set from the assessment
Scope.

---

# Endpoint Asset Ownership

The `endpoint` Asset type is produced by several Discovery skills, each from a
distinct discovery vector. Responsibilities are delineated as follows:

- [Content Discovery](../content-discovery/README.md) produces `endpoint` Assets
  discovered through path and directory enumeration and same-scope link crawling.
- [API Discovery](../api-discovery/README.md) produces `endpoint` Assets declared
  by located API specifications and detected GraphQL schemas.
- [Endpoint Enumeration](../endpoint-enumeration/README.md) produces or enriches
  `endpoint` Assets from rendered pages, client-side scripts, and bounded
  parameter mining.
- [Asset Discovery](../asset-discovery/README.md) is the canonical authority for
  consolidating and deduplicating `endpoint` Assets across all sources and
  introduces no new `endpoint` Assets of its own.

Each producing skill SHALL attach provenance to every `endpoint` Asset it emits.
Asset Discovery SHALL be the single point at which duplicate `endpoint` Assets are
merged.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for content-exposure weaknesses such as

- Directory listing enabled
- Backup, temporary, or source files exposed
- Administrative or debug interfaces reachable
- Sensitive files reachable without authentication

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Content Discovery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every request. Path
probing is an `active` action; it SHALL proceed only on an `allow` decision and
within the attached rate ceiling. Out-of-scope applications SHALL never be
probed.

---

# Dependencies

The Content Discovery Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Content Discovery Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- The Fingerprinting, API Discovery, and Endpoint Enumeration skills
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Endpoint and web-application Assets
- Asset Relationships forming the content portion of the asset graph
- Observations and Evidence references
- Findings with Risk for content-exposure weaknesses

Outputs SHALL remain implementation independent.

---

# Security Principles

The Content Discovery Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound request volume and crawl depth to avoid target disruption
- Produce no Finding without supporting Evidence
- Report exposure as data; exploitation is out of scope
- Redact sensitive content in evidence per Rules of Engagement
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope application base URL and a curated wordlist
- Rely on the skill for endpoint Asset construction
- Treat produced endpoints as inputs to Fingerprinting and API Discovery
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Crawl without depth or volume bounds
- Act on out-of-scope applications

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
- adr/ADR-001-content-discovery-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
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

- [ADR-001 — Content Discovery Skill](adr/ADR-001-content-discovery-skill.md)

---

# Future Extensions

Future versions MAY support

- Recursive discovery with adaptive wordlists
- Response-similarity clustering to reduce noise
- Rendered-content discovery via the Browser shared skill
- Parameter discovery handed to API Discovery

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Content Discovery Skill produces a canonical, evidence-backed map of
reachable web content — `endpoint` and `web-application` Assets and
content-exposure Findings — while acting strictly within scope and Rules of
Engagement through the Policy Engine, without invoking content-discovery tools
directly.
