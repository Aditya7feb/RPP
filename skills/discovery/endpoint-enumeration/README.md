# Endpoint Enumeration Skill

**File:** `skills/discovery/endpoint-enumeration/README.md`

**Version:** 1.0.0

---

# Purpose

The Endpoint Enumeration Skill is a Discovery-tier domain skill that enumerates the
endpoints and parameters of an in-scope web application within the Robust PenTest
Platform (RPP).

It extracts endpoints and parameters from rendered pages, client-side scripts, and
observed traffic, and mines additional parameters, producing canonical `endpoint`
[Assets](../../../schemas/asset.md), [Observations](../../../schemas/observation.md),
and, where a weakness is identified, [Findings](../../../schemas/finding.md) with
associated [Risk](../../../schemas/risk.md).

Unlike the [HTTP Client](../../shared/http-client/README.md) and
[Browser](../../shared/browser/README.md) shared skills, which perform requests
and rendering, this skill *interprets* application behavior to reveal its endpoint
and parameter surface. It consumes shared infrastructure and SHALL NOT invoke
enumeration tools directly.

---

# Goals

The Endpoint Enumeration Skill SHALL

- Extract endpoints and parameters from rendered pages and client-side scripts
- Mine additional parameters within bounds
- Produce canonical `endpoint` Assets enriched with parameter facts
- Emit Observations and Evidence for every enumeration
- Identify hidden-parameter and undocumented-endpoint exposure as Findings with
  Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  action
- Remain tool independent

---

# Non-Goals

The Endpoint Enumeration Skill SHALL NOT

- Perform HTTP or browser input or output directly
- Enumerate content by wordlist alone (that is Content Discovery)
- Locate API specifications (that is API Discovery)
- Test parameters for vulnerabilities
- Act on out-of-scope applications
- Invoke enumeration command-line tools or parse their output

Transport and rendering belong to the shared clients; wordlist content discovery
and API specification location belong to dedicated skills; vulnerability testing
belongs to the Web Security tier; exploitation is out of scope for Discovery.

---

# Design Principles

The Endpoint Enumeration Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and application behavior
- Confidence-graded, distinguishing observed from mined parameters
- Bounded in request volume and rate
- Tool independent

---

# Architecture

```
Recon Agent

↓

Endpoint Enumeration Skill

├── Policy Gate            → Policy Engine
├── Page Renderer          → Browser
├── Script Extractor       → HTTP Client
├── Parameter Miner        → HTTP Client
├── Asset Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client and Browser to interpret application
behavior. It SHALL remain unaware of any transport or rendering implementation.

---

# Responsibilities

The Endpoint Enumeration Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  action
- Rendering pages through the [Browser](../../shared/browser/README.md) and
  retrieving scripts through the [HTTP Client](../../shared/http-client/README.md)
- Extracting endpoints and parameters from rendered content and scripts
- Mining additional parameters within bounds
- Building `endpoint` [Assets](../../../schemas/asset.md) enriched with parameter
  facts
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for hidden-parameter exposure

---

# Discovery Lifecycle

```
Receive Application Target

↓

Consult Policy Engine (per action)

↓

Render Pages And Retrieve Scripts (Browser / HTTP Client)

↓

Extract Endpoints And Parameters

↓

Mine Additional Parameters (bounded)

↓

Record Observations → Evidence

↓

Build Endpoint Assets

↓

Analyze For Hidden-Parameter Exposure

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

seed_endpoints:

mine_parameters:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application base URL.

`seed_endpoints` MAY reference endpoints discovered by other skills to enrich.

`mine_parameters` SHALL declare whether parameter mining is performed.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce or enrich canonical `endpoint`
[Assets](../../../schemas/asset.md) with parameter facts, and
[Asset Relationships](../../../schemas/asset-relationship.md) such as `references`
linking endpoints to their application.

Observed parameters SHALL carry higher confidence than mined parameters.

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
[Risk](../../../schemas/risk.md), for exposure such as

- Hidden parameters that alter application behavior
- Undocumented or debug endpoints reachable
- Client-side secrets or endpoints disclosed in scripts

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Endpoint Enumeration Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every action.
Rendering, script retrieval, and parameter mining are `active` actions; they SHALL
proceed only on an `allow` decision and within the attached rate ceiling.
Out-of-scope applications SHALL never be enumerated.

---

# Dependencies

The Endpoint Enumeration Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Browser](../../shared/browser/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Endpoint Enumeration Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- Web Security skills that test discovered endpoints and parameters
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Endpoint Assets enriched with parameter facts
- Asset Relationships forming the endpoint portion of the asset graph
- Observations and Evidence references
- Findings with Risk for hidden-parameter exposure

Outputs SHALL remain implementation independent.

---

# Security Principles

The Endpoint Enumeration Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound request volume and rate
- Produce no Finding without supporting Evidence
- Grade parameter confidence honestly
- Report exposure as data; parameter testing is out of scope
- Redact client-side secrets in evidence per Rules of Engagement
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope application and seed endpoints from other skills
- Rely on the skill for endpoint and parameter enrichment
- Treat enriched endpoints as inputs to Web Security testing
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests or drive the browser directly
- Bypass the Policy Engine
- Test parameters for vulnerabilities during discovery
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
- adr/ADR-001-endpoint-enumeration-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Browser](../../shared/browser/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Content Discovery](../content-discovery/README.md)

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

- [ADR-001 — Endpoint Enumeration Skill](adr/ADR-001-endpoint-enumeration-skill.md)

---

# Future Extensions

Future versions MAY support

- Source-map correlation for richer endpoint extraction
- Traffic-replay-driven endpoint discovery
- Parameter-type inference
- Handoff of enriched endpoints to Web Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Endpoint Enumeration Skill produces a canonical, evidence-backed set of
`endpoint` Assets enriched with parameter facts, and hidden-parameter Findings,
while acting strictly within scope and Rules of Engagement through the Policy
Engine, without invoking enumeration tools directly.
