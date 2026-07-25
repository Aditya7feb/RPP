# ADR-001 — Port Discovery Skill

**File:** `skills/discovery/port-discovery/adr/ADR-001-port-discovery-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that maps the reachable network
services of an assessment target. Port discovery converts hosts into a set of
`port` and `service` Assets that seed service fingerprinting, TLS analysis, and
web discovery.

Port probing is an active action with the potential to disrupt fragile targets
and to stray outside scope. It therefore requires strict authorization and
pacing.

This skill follows the Discovery-skill pattern established by the DNS Enumeration
skill: consume shared infrastructure, consult the Policy Engine before every
action, and produce canonical domain objects along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

---

# Decision

The platform SHALL provide a Port Discovery Skill in the Discovery tier that

- Probes TCP and UDP ports through the
  [TCP Client](../../../shared/tcp-client/README.md) and
  [UDP Client](../../../shared/udp-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every probe and proceeds only on `allow`, within the attached rate ceiling
- Classifies port state and produces canonical
  [Assets](../../../../schemas/asset.md) and
  [Asset Relationships](../../../../schemas/asset-relationship.md)
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for exposure weaknesses, never without
  Evidence

The skill SHALL be tool independent and SHALL NOT perform socket input or output
directly.

---

# Alternatives Considered

## Scanning Inside The TCP Client

Port interpretation could live in the TCP Client shared package.

Rejected because the TCP Client is implementation infrastructure that performs
transport without producing findings or assets. Interpretation is a domain
concern belonging to a Discovery skill.

## Skipping The Policy Engine For Probing

Probing could proceed without authorization.

Rejected because probing is active and can disrupt targets. Every probe SHALL be
authorized and paced through the Policy Engine and Rate Limiter.

## Deep Fingerprinting Within Port Discovery

Port Discovery could identify service software in depth.

Rejected because deep fingerprinting is a distinct concern belonging to the
Fingerprinting skill. Port Discovery establishes service Assets and hands them
onward.

---

# Consequences

## Positive

- Produces an evidence-backed map of reachable services
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Seeds Fingerprinting and TLS Analysis with canonical service Assets
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and transport clients
- Requires careful bounds to avoid target disruption

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every probe
- Bound port ranges, concurrency, and rate
- Produce only canonical domain objects
- Back every Finding with Evidence
- Never act on out-of-scope hosts
- Never open sockets directly

---

# Future Compatibility

Future versions MAY add adaptive timing, service-version hints for Fingerprinting,
and IPv6 sweeps. These extensions SHALL preserve the existing interface and SHALL
maintain backward compatibility.

---

# Related Documents

- [Port Discovery README](../README.md)
- [Port Discovery Interface](../interface.md)
- [Port Discovery Execution Model](../execution.md)
- [Port Discovery Error Model](../error-model.md)
- [TCP Client](../../../shared/tcp-client/README.md)
- [UDP Client](../../../shared/udp-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
- [Finding Schema](../../../../schemas/finding.md)
