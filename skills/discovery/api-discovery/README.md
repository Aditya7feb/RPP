# API Discovery Skill

**File:** `skills/discovery/api-discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The API Discovery Skill is a Discovery-tier domain skill that identifies the
application programming interfaces (APIs) exposed by an in-scope target within the
Robust PenTest Platform (RPP).

It locates API definitions such as OpenAPI and Swagger documents, detects GraphQL
endpoints and their introspection exposure, and identifies common API base paths,
producing canonical `api` and `endpoint`
[Assets](../../../schemas/asset.md), [Observations](../../../schemas/observation.md),
and, where a weakness is identified, [Findings](../../../schemas/finding.md) with
associated [Risk](../../../schemas/risk.md).

Unlike the [HTTP Client](../../shared/http-client/README.md) shared skill, which
performs requests, this skill *interprets* responses to map the API surface. It
consumes shared infrastructure and SHALL NOT invoke API-discovery tools directly.

---

# Goals

The API Discovery Skill SHALL

- Locate API definitions and specifications for in-scope targets
- Detect GraphQL endpoints and introspection exposure
- Identify common API base paths and versions
- Produce canonical `api` and `endpoint` Assets
- Emit Observations and Evidence for every probe
- Identify API-exposure weaknesses as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  request
- Remain tool independent

---

# Non-Goals

The API Discovery Skill SHALL NOT

- Perform HTTP input or output directly
- Test API operations for vulnerabilities (that is API Security testing)
- Enumerate arbitrary web content (that is Content Discovery)
- Exploit discovered APIs
- Act on out-of-scope targets
- Invoke API-discovery command-line tools or parse their output

HTTP transport belongs to the [HTTP Client](../../shared/http-client/README.md);
vulnerability testing belongs to the API Security tier; general content
enumeration belongs to the [Content Discovery](../content-discovery/README.md)
skill; exploitation is out of scope for Discovery.

---

# Design Principles

The API Discovery Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and responses
- Confidence-graded
- Bounded in request volume and rate
- Tool independent

---

# Architecture

```
Recon Agent

↓

API Discovery Skill

├── Policy Gate            → Policy Engine
├── Definition Locator      → HTTP Client
├── GraphQL Detector        → HTTP Client
├── Base-Path Prober        → HTTP Client
├── Asset Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to interpret API surfaces. It SHALL remain
unaware of any HTTP implementation.

---

# Responsibilities

The API Discovery Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  request
- Locating API definitions through the
  [HTTP Client](../../shared/http-client/README.md)
- Detecting GraphQL endpoints and introspection exposure
- Building `api` and `endpoint`
  [Assets](../../../schemas/asset.md) and their relationships
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for API-exposure weaknesses

---

# Discovery Lifecycle

```
Receive Application Target

↓

Consult Policy Engine (per request)

↓

Locate API Definitions (HTTP Client)

↓

Detect GraphQL And Introspection

↓

Probe Common API Base Paths

↓

Record Observations → Evidence

↓

Build API and Endpoint Assets

↓

Analyze For API-Exposure Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

definition_hints:

detect_graphql:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL.

`definition_hints` SHALL reference candidate specification paths, such as
`/openapi.json` and `/swagger.json`.

`detect_graphql` SHALL declare whether GraphQL detection is performed.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical [Assets](../../../schemas/asset.md) of types

- `api`
- `endpoint`

and [Asset Relationships](../../../schemas/asset-relationship.md) such as `serves`
and `references` linking API endpoints to their API and application.

Where a specification is located, the operations it declares MAY be recorded as
`endpoint` Assets with provenance to the specification.

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
[Risk](../../../schemas/risk.md), for API-exposure weaknesses such as

- API specification or documentation publicly exposed without authentication
- GraphQL introspection enabled in production
- Unversioned or deprecated API surfaces reachable
- Debug or internal API endpoints exposed

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The API Discovery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every request.
Definition retrieval and probing are `active` actions; they SHALL proceed only on
an `allow` decision and within the attached rate ceiling. Out-of-scope targets
SHALL never be probed.

---

# Dependencies

The API Discovery Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The API Discovery Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- API Security skills that test discovered API operations
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- API and endpoint Assets
- Asset Relationships forming the API portion of the asset graph
- Observations and Evidence references
- Findings with Risk for API-exposure weaknesses

Outputs SHALL remain implementation independent.

---

# Security Principles

The API Discovery Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound request volume and rate
- Produce no Finding without supporting Evidence
- Report exposure as data; exploitation and operation testing are out of scope
- Redact sensitive specification content in evidence per Rules of Engagement
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope application or API base URL
- Rely on the skill for API and endpoint Asset construction
- Treat discovered API operations as inputs to API Security testing
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Invoke API operations for testing during discovery
- Act on out-of-scope targets

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
- adr/ADR-001-api-discovery-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
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

- [ADR-001 — API Discovery Skill](adr/ADR-001-api-discovery-skill.md)

---

# Future Extensions

Future versions MAY support

- gRPC and AsyncAPI definition discovery
- Specification parsing into structured operation Assets
- API version-diffing across environments
- Handoff of discovered operations to API Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant API Discovery Skill produces a canonical, evidence-backed map of the
API surface — `api` and `endpoint` Assets and API-exposure Findings — while
acting strictly within scope and Rules of Engagement through the Policy Engine,
without invoking API-discovery tools directly.
