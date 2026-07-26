# ADR-001 — Web Cache Poisoning Skill

**File:** `skills/web-security/cache-poisoning/adr/ADR-001-cache-poisoning-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application's caching behavior can be poisoned through unkeyed input. Web cache
poisoning (CWE-444 and related weaknesses) allows an attacker to cause a harmful
response to be served to other users from a shared cache.

Confirming this weakness safely is delicate: poisoning a shared cache key would affect
real users. The skill therefore confirms poisonability using a controlled cache key
that isolates testing from real users' entries, and SHALL NOT poison a shared
user-facing cache key.

The skill follows the Web Security-tier pattern: consume the `web-application` and
`endpoint` [Assets](../../../../schemas/asset.md) produced by Discovery, consult the
[Policy Engine](../../../shared/policy-engine/README.md) before every target-facing
action, drive the [HTTP Client](../../../shared/http-client/README.md), and produce
[Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-444.

This is the final skill of the Web Security tier.

---

# Decision

The platform SHALL provide a Web Cache Poisoning Skill in the Web Security tier that

- Submits bounded probes with candidate unkeyed inputs against a controlled cache key
  and analyzes reflection into cached responses through the HTTP Client
- Confirms poisonability using controlled cache keys without affecting real users
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with only controlled-cache-key
  confirmation recorded
- Emits Findings with Risk for cache poisoning weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-444

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT poison a cache entry that serves real users.

---

# Alternatives Considered

## Poisoning A Shared Cache Key To Prove Impact

The skill could poison a shared cache key to demonstrate user impact.

Rejected because poisoning a shared key affects real users and is unsafe. A controlled
cache key confirms poisonability without collateral impact.

## Folding Cache Poisoning Into XSS

Cache poisoning is often used to deliver XSS.

Rejected as a merge because cache poisoning is a distinct caching-behavior weakness
independent of script execution. The XSS skill owns script execution; this skill owns
cache-key and unkeyed-input analysis and MAY reference XSS delivery.

## Testing Only Header-Based Poisoning

The skill could test only header-based vectors.

Rejected because parameter-based and cache-deception vectors are also relevant. The
skill evaluates unkeyed inputs broadly while remaining scoped to a controlled cache
key.

---

# Consequences

## Positive

- Produces evidence-backed cache poisoning Findings safely
- Completes the Web Security tier with consistent structure
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms poisonability without affecting real users

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Controlled-cache-key isolation requires careful configuration

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm poisonability using controlled cache keys only
- Never poison a cache entry that serves real users
- Reference benign markers only
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-444
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add cache-deception modeling, cloaking classification, and
fat-GET evaluation. These extensions SHALL preserve the existing interface and SHALL
maintain backward compatibility.

---

# Related Documents

- [Web Cache Poisoning README](../README.md)
- [Web Cache Poisoning Interface](../interface.md)
- [Web Cache Poisoning Execution Model](../execution.md)
- [Web Cache Poisoning Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Header Schema](../../../../schemas/http-header.md)
