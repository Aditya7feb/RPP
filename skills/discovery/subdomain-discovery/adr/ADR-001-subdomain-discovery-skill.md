# ADR-001 — Subdomain Discovery Skill

**File:** `skills/discovery/subdomain-discovery/adr/ADR-001-subdomain-discovery-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that expands an apex domain into its
subdomains. Subdomain discovery broadens the assessment attack surface by finding
previously unknown names, which seed DNS enumeration, port discovery, and content
discovery.

Subdomain discovery combines passive collection, which does not interact with the
target directly, with bounded active resolution, which does. Active resolution is
subject to scope and Rules of Engagement.

This skill follows the Discovery-skill pattern: consume shared infrastructure,
consult the Policy Engine before every active action, and produce canonical domain
objects along the Observation → Evidence → Analysis → Finding → Risk pipeline. It
is distinct from the [DNS Enumeration](../../dns-enumeration/README.md) skill,
which enumerates records for already-known names.

---

# Decision

The platform SHALL provide a Subdomain Discovery Skill in the Discovery tier that

- Collects passive subdomain candidates and generates bounded active candidates
- Resolves candidates through the [DNS Client](../../../shared/dns-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every active resolution and proceeds only on `allow`
- Produces canonical `subdomain` [Assets](../../../../schemas/asset.md), suspected
  for passive-only and confirmed for resolved candidates, with `resolves-to`
  relationships
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for subdomain-takeover exposure, never
  without Evidence

The skill SHALL be tool independent and SHALL NOT perform DNS input or output
directly.

---

# Alternatives Considered

## Merging With DNS Enumeration

Subdomain discovery could be folded into DNS Enumeration.

Rejected because the two have different purposes: DNS Enumeration enumerates
records for known names, while Subdomain Discovery finds previously unknown names
through passive sources and active candidate generation. Separating them keeps
each skill focused.

## Passive-Only Discovery

The skill could rely on passive sources only.

Rejected because active resolution confirms candidates and enables takeover
analysis. Active resolution is bounded and policy-gated.

## Recording Unresolved Candidates As Confirmed

Passive-only candidates could be recorded as confirmed.

Rejected because unresolved candidates are uncertain. They are recorded as
`suspected` Assets with lower confidence until resolved.

---

# Consequences

## Positive

- Broadens the attack surface with evidence-backed subdomains
- Enforces scope and Rules of Engagement for active resolution
- Distinguishes suspected from confirmed subdomains honestly
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and DNS Client
- Passive sources vary in reliability, reflected in confidence

The negative consequences are outweighed by consistency and coverage.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every active resolution
- Bound candidate volume and resolution rate
- Produce only canonical domain objects
- Record passive-only candidates as suspected
- Back every Finding with Evidence
- Never act on out-of-scope domains
- Never resolve names directly

---

# Future Compatibility

Future versions MAY add certificate-transparency and passive DNS source
integration, permutation generation, and wildcard-aware filtering. These
extensions SHALL preserve the existing interface and SHALL maintain backward
compatibility.

---

# Related Documents

- [Subdomain Discovery README](../README.md)
- [Subdomain Discovery Interface](../interface.md)
- [Subdomain Discovery Execution Model](../execution.md)
- [Subdomain Discovery Error Model](../error-model.md)
- [DNS Client](../../../shared/dns-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [DNS Enumeration](../../dns-enumeration/README.md)
- [Asset Schema](../../../../schemas/asset.md)
