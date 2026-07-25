# ADR-001 — TLS Analysis Skill

**File:** `skills/discovery/tls-analysis/adr/ADR-001-tls-analysis-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that evaluates the TLS posture of
in-scope services. TLS analysis converts service Assets into certificate Assets
and TLS-weakness Findings that inform risk and reporting.

The [TLS Client](../../../shared/tls-client/README.md) shared skill negotiates
TLS and reports validation outcomes and interception boundaries as data, but it
deliberately does not interpret those outcomes as findings. That interpretation is
a domain concern.

This skill follows the Discovery-skill pattern: consume shared infrastructure,
consult the Policy Engine before every action, and produce canonical domain
objects along the Observation → Evidence → Analysis → Finding → Risk pipeline.

---

# Decision

The platform SHALL provide a TLS Analysis Skill in the Discovery tier that

- Analyzes protocols, ciphers, and certificate chains through the
  [TLS Client](../../../shared/tls-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every action and proceeds only on `allow`
- Produces canonical `certificate` [Assets](../../../../schemas/asset.md) and
  relationships to their services
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for TLS weaknesses, never without Evidence
- Honors interception boundaries reported by the TLS Client

The skill SHALL be tool independent and SHALL NOT negotiate TLS directly.

---

# Alternatives Considered

## Interpreting TLS Weaknesses In The TLS Client

The TLS Client could classify weaknesses.

Rejected because the TLS Client is implementation infrastructure that reports
validation outcomes as data. Classifying weaknesses is a domain concern belonging
to a Discovery skill, which keeps the client reusable and neutral.

## Ignoring Interception Boundaries

Analysis could treat every validation failure as a certificate weakness.

Rejected because a legitimate intercepting proxy would generate spurious findings.
The skill honors interception boundaries reported by the TLS Client.

## Producing Free-Form TLS Results

The skill could emit ad hoc TLS result objects.

Rejected because the platform is schema-first. The skill produces canonical
certificate Assets, Observations, and Findings.

---

# Consequences

## Positive

- Produces an evidence-backed view of TLS posture
- Enforces scope and Rules of Engagement through the Policy Engine
- Avoids spurious findings by honoring interception boundaries
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and TLS Client
- Requires accurate interception-boundary handling

The negative consequences are outweighed by consistency and accuracy.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every action
- Honor interception boundaries
- Produce only canonical domain objects
- Back every Finding with Evidence
- Never act on out-of-scope services
- Never negotiate TLS directly

---

# Future Compatibility

Future versions MAY add revocation-state reporting, certificate transparency
correlation, and cipher-preference-order analysis. These extensions SHALL preserve
the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [TLS Analysis README](../README.md)
- [TLS Analysis Interface](../interface.md)
- [TLS Analysis Execution Model](../execution.md)
- [TLS Analysis Error Model](../error-model.md)
- [TLS Client](../../../shared/tls-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
- [Finding Schema](../../../../schemas/finding.md)
