# ADR-001 — Cache Abstraction

**File:** `skills/shared/cache/adr/ADR-001-cache-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform repeatedly performs deterministic, expensive
operations during an assessment: DNS resolutions, TLS metadata retrieval,
content fetches, and enumeration lookups. Re-performing identical operations
wastes time, increases outbound load against targets, and can distort rate
budgets.

Before this decision, caching could be implemented independently inside each
shared package. That approach produced

- Inconsistent freshness and eviction behavior
- Duplicated and divergent caching logic
- Risk of caching sensitive data or serving it out of scope
- No central place to audit what was cached and reused

The platform requires a single, canonical, implementation-independent mechanism
to store and reuse deterministic results safely.

---

# Decision

The platform SHALL provide a dedicated Cache shared skill that centralizes all
result reuse behind a stable interface.

The Cache shared skill SHALL

- Derive deterministic keys from normalized parameters
- Store and retrieve canonical
  [Cache Entry](../../../../schemas/cache-entry.md) objects
- Evaluate freshness and support revalidation
- Enforce cache scope to prevent leakage
- Refuse to cache secrets or non-deterministic results
- Degrade to a miss when the backend is unavailable
- Emit evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL cache results exclusively through the
[Cache Interface](../interface.md) by supplying a producer callback. The Cache
shared skill SHALL remain unaware of the producer implementation.

Caching SHALL be expressed through a canonical schema, consistent with the
platform's schema-first architecture.

---

# Alternatives Considered

## Per-Package Caching

Each shared package could implement its own cache.

Rejected because it duplicates logic, diverges over time, and makes scope and
secret-safety impossible to enforce or audit centrally.

## No Caching

Operations could always be re-performed.

Rejected because it wastes time, increases outbound load, and consumes rate
budget unnecessarily. Deterministic results are safe to reuse within bounds.

## Transparent Transport-Level Caching

Caching could be embedded in transport adapters.

Rejected because it ties caching to specific implementations, hides scope and
freshness decisions from consumers, and risks caching sensitive data invisibly.

---

# Consequences

## Positive

- Uniform freshness, scope, and eviction behavior across packages
- Central, auditable control over what is cached and reused
- Reduced outbound load and rate-budget consumption
- Safe by default: secrets and non-deterministic results are never cached
- Correctness preserved through graceful degradation to a miss

## Negative

- Consumers MUST declare cacheability and scope
- An additional shared dependency is introduced
- Distributed caching, if later required, adds complexity

The negative consequences are outweighed by the safety, efficiency, and
consistency benefits.

---

# Compliance

Consumers SHALL

- Cache results through the Cache Interface
- Declare cacheability and the narrowest sufficient scope
- Never place secret material in cache parameters or values
- Treat cache misses as normal

Shared packages that reuse deterministic results SHOULD depend on the Cache
shared skill and SHALL NOT implement independent caches.

---

# Future Compatibility

Future versions MAY introduce distributed caches, negative caching, and
content-addressed deduplication. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Cache README](../README.md)
- [Cache Interface](../interface.md)
- [Cache Execution Model](../execution.md)
- [Cache Error Model](../error-model.md)
- [Cache Entry Schema](../../../../schemas/cache-entry.md)
- [Evidence Schema](../../../../schemas/evidence.md)
