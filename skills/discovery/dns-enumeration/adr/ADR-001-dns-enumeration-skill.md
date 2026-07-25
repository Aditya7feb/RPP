# ADR-001 — DNS Enumeration Skill

**File:** `skills/discovery/dns-enumeration/adr/ADR-001-dns-enumeration-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that establishes the DNS footprint of
an assessment target. DNS enumeration is the earliest and most foundational
discovery activity: its outputs — domains, subdomains, hosts, addresses, and
services — seed the entire assessment attack surface.

This is the first Discovery-tier domain skill. It sets the pattern that every
Discovery skill follows:

- It consumes shared infrastructure rather than invoking tools.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every target-facing action.
- It produces canonical domain objects along the pipeline
  Observation → Evidence → Analysis → Finding → Risk.

Without a canonical DNS enumeration skill, discovery would improvise DNS handling,
produce free-form results, and risk acting outside scope.

---

# Decision

The platform SHALL provide a DNS Enumeration Skill in the Discovery tier that

- Enumerates DNS records through the
  [DNS Client](../../../shared/dns-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every action and proceeds only on `allow`
- Produces canonical [Assets](../../../../schemas/asset.md) and
  [Asset Relationships](../../../../schemas/asset-relationship.md)
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for DNS weaknesses, never without Evidence

The skill SHALL be tool independent and SHALL NOT perform DNS input or output
directly.

---

# Alternatives Considered

## Enumerating DNS Inside The DNS Client

DNS interpretation could live in the DNS Client shared package.

Rejected because the DNS Client is implementation infrastructure that performs
DNS operations without producing findings or assets. Interpretation is a domain
concern belonging to a Discovery skill.

## Skipping The Policy Engine For Passive Queries

Passive queries could bypass authorization.

Rejected because scope enforcement applies to all target-facing actions. Even
passive queries SHALL be confirmed in-scope. The Policy Engine is consulted for
every action.

## Producing Free-Form Results

The skill could emit ad hoc result objects.

Rejected because the platform is schema-first. The skill produces canonical
Assets, Observations, and Findings so that later skills and reports share one
vocabulary.

---

# Consequences

## Positive

- Establishes the canonical Discovery-skill pattern
- Produces an evidence-backed DNS asset graph
- Enforces scope and Rules of Engagement through the Policy Engine
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces a dependency on the Policy Engine and DNS Client
- Requires canonical domain schemas to be present (they are)

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every action
- Produce only canonical domain objects
- Back every Finding with Evidence
- Never act on out-of-scope targets
- Never invoke DNS tools directly

---

# Future Compatibility

Future versions MAY add passive DNS integration, DNSSEC validation-state
reporting, and reverse-DNS sweeps. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [DNS Enumeration README](../README.md)
- [DNS Enumeration Interface](../interface.md)
- [DNS Enumeration Execution Model](../execution.md)
- [DNS Enumeration Error Model](../error-model.md)
- [DNS Client](../../../shared/dns-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
- [Finding Schema](../../../../schemas/finding.md)
