# ADR-001 — Content Discovery Skill

**File:** `skills/discovery/content-discovery/adr/ADR-001-content-discovery-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase requires a domain skill that maps the reachable content of an
in-scope web application. Content discovery converts a web application into a set
of `endpoint` Assets that seed fingerprinting, API discovery, and later web
security testing.

Content probing is an active action that issues many requests and can disrupt
fragile applications or stray outside scope. It therefore requires strict
authorization and pacing.

This skill follows the Discovery-skill pattern established by the DNS Enumeration,
Port Discovery, and TLS Analysis skills: consume shared infrastructure, consult
the Policy Engine before every action, and produce canonical domain objects along
the Observation → Evidence → Analysis → Finding → Risk pipeline.

---

# Decision

The platform SHALL provide a Content Discovery Skill in the Discovery tier that

- Probes candidate paths and follows in-scope links through the
  [HTTP Client](../../../shared/http-client/README.md)
- Consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every request and proceeds only on `allow`, within the attached rate ceiling
- Produces canonical `endpoint` and `web-application`
  [Assets](../../../../schemas/asset.md) and their relationships
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md)
- Emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) for content-exposure weaknesses, never
  without Evidence

The skill SHALL be tool independent and SHALL NOT perform HTTP input or output
directly.

---

# Alternatives Considered

## Crawling Inside The HTTP Client

Content crawling could live in the HTTP Client shared package.

Rejected because the HTTP Client is implementation infrastructure that performs
transport without producing findings or assets. Crawling and interpretation are
domain concerns belonging to a Discovery skill.

## Following Out-Of-Scope Links

The skill could follow all discovered links.

Rejected because following out-of-scope links violates scope. Only links whose
scope evaluates to `in_scope` are followed; out-of-scope links are recorded but
not probed.

## Unbounded Crawling

The skill could crawl without depth or volume limits.

Rejected because unbounded crawling can disrupt targets and overwhelm rate
budgets. Crawling is bounded and paced through the Policy Engine and Rate
Limiter.

---

# Consequences

## Positive

- Produces an evidence-backed map of reachable content
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Seeds Fingerprinting and API Discovery with canonical endpoints
- Reuses shared infrastructure; remains tool independent

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Requires careful bounds to avoid target disruption

The negative consequences are outweighed by consistency and safety.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every request
- Follow only in-scope links and bound crawl depth and volume
- Produce only canonical domain objects
- Back every Finding with Evidence
- Redact sensitive content in evidence per Rules of Engagement
- Never act on out-of-scope applications
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add rendered-content discovery via the Browser shared skill,
response-similarity clustering, and parameter-discovery handoff to API Discovery.
These extensions SHALL preserve the existing interface and SHALL maintain
backward compatibility.

---

# Related Documents

- [Content Discovery README](../README.md)
- [Content Discovery Interface](../interface.md)
- [Content Discovery Execution Model](../execution.md)
- [Content Discovery Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
- [Finding Schema](../../../../schemas/finding.md)
