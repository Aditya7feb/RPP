# ADR-001 — Virtual Host Discovery Skill

**File:** `skills/discovery/virtual-host-discovery/adr/ADR-001-virtual-host-discovery-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that reveals name-based virtual hosts
served from a shared address. Many applications are reachable only when the
correct host name is supplied, so address-based discovery alone misses them.
Virtual host discovery expands the web attack surface by finding these hidden
applications.

Virtual host discovery is inherently differential: it compares candidate responses
to a baseline to distinguish real virtual hosts from a default response, and it
must handle wildcard responses to avoid false positives.

This skill follows the Discovery-skill pattern: consume shared infrastructure,
consult the Policy Engine before every action, and produce canonical domain
objects along the Observation → Evidence → Analysis → Finding → Risk pipeline.

---

# Decision

The platform SHALL provide a Virtual Host Discovery Skill in the Discovery tier
that

- Establishes a baseline and probes candidate host names through the
  [HTTP Client](../../../shared/http-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every probe and proceeds only on `allow`, within the attached rate ceiling
- Analyzes responses differentially and discounts wildcard responses
- Produces canonical `web-application` [Assets](../../../../schemas/asset.md) for
  distinct virtual hosts and `serves` relationships
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for hidden-host exposure, never without
  Evidence

The skill SHALL be tool independent and SHALL NOT perform HTTP input or output
directly.

---

# Alternatives Considered

## Folding Into Content Discovery

Virtual host discovery could be part of Content Discovery.

Rejected because the two differ: Content Discovery enumerates paths within a known
application, while Virtual Host Discovery finds distinct applications by host name.
Separating them keeps each focused, and virtual hosts feed content discovery.

## Ignoring Wildcard Responses

The skill could treat every differing response as a virtual host.

Rejected because wildcard responses would produce many false positives. The skill
detects and discounts wildcard responses.

## Address-Only Discovery

Discovery could rely on addresses alone.

Rejected because name-based virtual hosts are invisible without host-name probing.
Differential host-name probing is required.

---

# Consequences

## Positive

- Reveals hidden web applications behind shared addresses
- Enforces scope and Rules of Engagement through the Policy Engine
- Reduces false positives through wildcard handling
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Differential analysis requires careful thresholds

The negative consequences are outweighed by coverage and accuracy.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every probe
- Establish a baseline and analyze differentially
- Discount wildcard responses
- Produce only canonical domain objects
- Back every Finding with Evidence
- Never act on out-of-scope addresses or host names
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add response-similarity clustering, TLS SNI correlation, and
refined wildcard filtering. These extensions SHALL preserve the existing interface
and SHALL maintain backward compatibility.

---

# Related Documents

- [Virtual Host Discovery README](../README.md)
- [Virtual Host Discovery Interface](../interface.md)
- [Virtual Host Discovery Execution Model](../execution.md)
- [Virtual Host Discovery Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Content Discovery](../../content-discovery/README.md)
- [Asset Schema](../../../../schemas/asset.md)
