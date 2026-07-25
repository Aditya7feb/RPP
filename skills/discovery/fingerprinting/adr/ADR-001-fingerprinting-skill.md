# ADR-001 — Fingerprinting Skill

**File:** `skills/discovery/fingerprinting/adr/ADR-001-fingerprinting-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that identifies the technologies
behind in-scope Assets. Technology identification converts services, web
applications, and endpoints into canonical
[Technology](../../../../schemas/technology.md) records that drive targeted web
and API security testing and inform risk.

Fingerprinting correlates signals from multiple shared clients — HTTP behavior and
headers, response bodies, cookies, and TLS facts. It follows the Discovery-skill
pattern: consume shared infrastructure, consult the Policy Engine before every
action, and produce canonical domain objects along the
Observation → Evidence → Analysis → Finding → Risk pipeline.

Deterministic mapping of a technology version to known vulnerabilities requires a
knowledge-retrieval capability, which was deferred by the approved Phase 3
architecture decision. Fingerprinting therefore references vulnerability
identifiers informally where a version is known and defers deterministic mapping.

---

# Decision

The platform SHALL provide a Fingerprinting Skill in the Discovery tier that

- Collects signals through the [HTTP Client](../../../shared/http-client/README.md)
  and [TLS Client](../../../shared/tls-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every action and proceeds only on `allow`
- Produces canonical [Technology](../../../../schemas/technology.md) records with
  confidence grades, linked to their [Assets](../../../../schemas/asset.md)
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for technology-exposure weaknesses, never
  without Evidence

The skill SHALL prefer passive signals, SHALL grade confidence honestly, and
SHALL be tool independent.

---

# Alternatives Considered

## Fingerprinting Inside The HTTP Client

Technology matching could live in the HTTP Client.

Rejected because the HTTP Client is implementation infrastructure that performs
transport. Technology identification is a domain concern belonging to a Discovery
skill.

## Deterministic Vulnerability Mapping Now

The skill could map technologies to vulnerabilities deterministically.

Rejected because deterministic mapping requires a knowledge-retrieval capability
deferred by the approved Phase 3 architecture decision. The skill references
identifiers informally and defers deterministic mapping to a future capability.

## Recording Low-Confidence Guesses As Facts

The skill could record inferred technologies as confirmed.

Rejected because it would produce unreliable identifications. The skill grades
confidence and does not record technologies below a configured minimum.

---

# Consequences

## Positive

- Produces evidence-backed, confidence-graded Technology identifications
- Enforces scope and Rules of Engagement through the Policy Engine
- Seeds targeted web and API security testing
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and shared clients
- Vulnerability mapping remains informal pending a knowledge capability

The negative consequences are acceptable and consistent with the approved
architecture.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every action
- Prefer passive signals and gate active probing
- Produce only canonical Technology and domain objects
- Grade confidence honestly
- Back every Finding with Evidence
- Never act on out-of-scope Assets
- Never perform HTTP or TLS requests directly

---

# Future Compatibility

Future versions MAY add deterministic technology-to-vulnerability mapping via a
knowledge capability, favicon and asset-hash correlation, and behavioral
fingerprinting. These extensions SHALL preserve the existing interface and SHALL
maintain backward compatibility.

---

# Related Documents

- [Fingerprinting README](../README.md)
- [Fingerprinting Interface](../interface.md)
- [Fingerprinting Execution Model](../execution.md)
- [Fingerprinting Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [TLS Client](../../../shared/tls-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Technology Schema](../../../../schemas/technology.md)
