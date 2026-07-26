# ADR-001 — Server-Side Request Forgery Skill

**File:** `skills/web-security/ssrf/adr/ADR-001-ssrf-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application can be induced to make server-side requests to attacker-influenced
destinations. Server-side request forgery (CWE-918) can expose internal services,
cloud metadata, and sensitive endpoints.

Confirming SSRF safely is delicate: naive testing could reach internal services or
cloud metadata. The skill therefore confirms forgery using an out-of-band interaction
to a controlled collector, corroborated by bounded response and timing differentials,
and SHALL NOT reach internal services, cloud metadata, or sensitive endpoints.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-918. It reuses the canonical
[HTTP Timing](../../../../schemas/http-timing.md) representation.

---

# Decision

The platform SHALL provide a Server-Side Request Forgery Skill in the Web Security
tier that

- Submits bounded probes toward a controlled destination and observes out-of-band and
  differential signals through the HTTP Client
- Confirms forgery to a controlled destination without reaching internal services
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the high impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only controlled-destination
  interaction recorded
- Emits Findings with Risk for SSRF weaknesses, never without Evidence, classified
  with canonical weakness identifiers such as CWE-918

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT reach internal services, cloud metadata, or sensitive
endpoints.

---

# Alternatives Considered

## Folding SSRF Into Open Redirect

SSRF and open redirect both involve attacker-influenced destinations.

Rejected because open redirect concerns client-side redirection while SSRF concerns
server-side requests to internal resources. The threat models and impacts differ;
separate skills keep each focused.

## Reaching Internal Services To Prove Impact

The skill could target internal services or cloud metadata to demonstrate impact.

Rejected because reaching internal or sensitive services is intrusive and dangerous.
Confirming forgery to a controlled collector is sufficient and safe; metadata-service
exposure correlation is deferred to a stricter, explicitly approved future capability.

## Relying Solely On Response Differentials

The skill could infer SSRF from response differentials alone.

Rejected as a default because differentials are noisy. Out-of-band confirmation is the
primary signal, corroborated by bounded differentials.

---

# Consequences

## Positive

- Produces evidence-backed SSRF Findings safely
- Reuses the Web Security-tier skill pattern and canonical timing schema
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms forgery without reaching internal services

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Reliable confirmation benefits from an authorized out-of-band collector

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm forgery to a controlled destination only
- Never reach internal services, cloud metadata, or sensitive endpoints
- Reference authorized collectors only
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-918
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add blind-SSRF confirmation via richer out-of-band channels,
protocol-smuggling classification, and cloud metadata-service exposure correlation
under stricter approval. These extensions SHALL preserve the existing interface and
SHALL maintain backward compatibility.

---

# Related Documents

- [Server-Side Request Forgery README](../README.md)
- [Server-Side Request Forgery Interface](../interface.md)
- [Server-Side Request Forgery Execution Model](../execution.md)
- [Server-Side Request Forgery Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Timing Schema](../../../../schemas/http-timing.md)
