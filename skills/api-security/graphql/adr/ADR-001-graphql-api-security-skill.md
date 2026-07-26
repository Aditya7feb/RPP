# ADR-001 — GraphQL API Security Skill

**File:** `skills/api-security/graphql/adr/ADR-001-graphql-api-security-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The API Security phase requires a domain skill that evaluates the security of an
in-scope GraphQL API. GraphQL introduces weaknesses distinct from REST: introspection
exposure, unbounded query depth and complexity (a resource-consumption denial-of-
service vector), field- and object-level authorization gaps, and batching or
alias-based amplification.

The skill follows the API Security-tier pattern established by the REST skill: consume
the `api` and `endpoint` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classified with canonical
identifiers and OWASP API Security Top 10 (2023) references.

Because depth and complexity testing can deny service, the skill confirms missing
limits using bounded, incrementally deeper probes and SHALL NOT execute unbounded
queries. Generic injection and client-side weaknesses are delegated to the Web
Security tier.

---

# Decision

The platform SHALL provide a GraphQL API Security Skill in the API Security tier that

- Submits bounded GraphQL queries across two authorized controlled identities through
  the HTTP Client
- Analyzes introspection exposure, depth and complexity limits, field- and
  object-level authorization, and batching amplification
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only bounded, minimal confirmation
  recorded
- Emits Findings with Risk for GraphQL security weaknesses, never without Evidence,
  classified with canonical identifiers and OWASP API Security Top 10 (2023)
  references

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output directly,
SHALL bound depth and complexity probes to avoid denial of service, and SHALL NOT
enumerate or exfiltrate other principals' data.

---

# Alternatives Considered

## Folding GraphQL Into The REST Skill

GraphQL could be tested by the REST API Security skill.

Rejected because GraphQL has a distinct query model with introspection, depth and
complexity, and batching concerns absent from REST. A dedicated skill keeps each
focused while both share the API Security-tier pattern.

## Executing Deep Queries To Prove Denial Of Service

The skill could execute an expensive query to demonstrate exhaustion.

Rejected because unbounded queries deny service. Bounded, incrementally deeper probes
confirm missing limits safely.

## Testing Generic Injection Here

The skill could test SQL, command, and template injection against resolvers.

Rejected because those injection classes are owned by dedicated Web Security skills.
The GraphQL skill references them rather than duplicating them.

---

# Consequences

## Positive

- Produces evidence-backed GraphQL-specific Findings aligned to OWASP API Security
- Reuses the API Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms resource-consumption gaps without denying service

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Bounded depth and complexity probing requires careful configuration

The negative consequences are outweighed by safety and clarity.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Bound depth and complexity probes to avoid denial of service
- Use only authorized controlled identities for authorization testing
- Confirm authorization gaps with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers and OWASP API Security references
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add schema-driven authorization modeling, subscription and
mutation-specific evaluation, and cost-analysis evaluation. These extensions SHALL
preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [GraphQL API Security README](../README.md)
- [GraphQL API Security Interface](../interface.md)
- [GraphQL API Security Execution Model](../execution.md)
- [GraphQL API Security Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [REST API Security](../../rest/README.md)
