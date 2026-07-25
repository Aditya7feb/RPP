# ADR-001 — API Discovery Skill

**File:** `skills/discovery/api-discovery/adr/ADR-001-api-discovery-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that maps the API surface of an
in-scope target. Modern applications expose substantial functionality through
APIs described by machine-readable specifications such as OpenAPI and Swagger, or
through GraphQL endpoints. Discovering these surfaces seeds targeted API security
testing.

API discovery locates specifications, detects GraphQL endpoints and their
introspection exposure, and probes common API base paths. These are active actions
subject to scope and Rules of Engagement.

This skill follows the Discovery-skill pattern: consume shared infrastructure,
consult the Policy Engine before every action, and produce canonical domain
objects along the Observation → Evidence → Analysis → Finding → Risk pipeline. It
is distinct from the [Content Discovery](../../content-discovery/README.md) skill,
which enumerates general web content, and from the API Security tier, which tests
API operations.

---

# Decision

The platform SHALL provide an API Discovery Skill in the Discovery tier that

- Locates API definitions and probes common API base paths through the
  [HTTP Client](../../../shared/http-client/README.md)
- Detects GraphQL endpoints and, subject to policy, introspection exposure
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every request and proceeds only on `allow`, within the attached rate ceiling
- Produces canonical `api` and `endpoint`
  [Assets](../../../../schemas/asset.md) and their relationships
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for API-exposure weaknesses, never without
  Evidence

The skill SHALL be tool independent, SHALL NOT test API operations for
vulnerabilities, and SHALL NOT perform HTTP input or output directly.

---

# Alternatives Considered

## Folding Into Content Discovery

API discovery could be part of Content Discovery.

Rejected because API surfaces have distinct signals — specifications, GraphQL
introspection, and versioned base paths — and feed a distinct API Security tier.
Separating them keeps each skill focused.

## Testing API Operations During Discovery

The skill could invoke discovered operations to test them.

Rejected because operation testing is intrusive and belongs to the API Security
tier. Discovery locates and records the surface; it does not exercise operations
beyond what is required to confirm existence, and that is policy-gated.

## Parsing Specifications Into Full Operation Models Now

The skill could build a complete structured operation model.

Deferred. The skill records declared operations as `endpoint` Assets with
provenance to the specification; richer structured operation Assets are a
documented future extension.

---

# Consequences

## Positive

- Produces an evidence-backed map of the API surface
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Seeds API Security testing with canonical API and endpoint Assets
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Introspection detection requires careful policy gating

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every request
- Gate GraphQL introspection as an active action
- Produce only canonical domain objects
- Back every Finding with Evidence
- Redact sensitive specification content in evidence per Rules of Engagement
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add gRPC and AsyncAPI definition discovery, structured
operation Assets from parsed specifications, and API version-diffing. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [API Discovery README](../README.md)
- [API Discovery Interface](../interface.md)
- [API Discovery Execution Model](../execution.md)
- [API Discovery Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Content Discovery](../../content-discovery/README.md)
- [Asset Schema](../../../../schemas/asset.md)
