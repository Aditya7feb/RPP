# Cache Capabilities

**File:** `skills/shared/cache/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Cache Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Cache Interface](interface.md).

---

# Capability Model

```
Key Derivation

Lookup

Freshness

Revalidation

Storage

Scope Enforcement

Eviction

Observability
```

---

# Key Derivation Capabilities

## Deterministic Keying

The Cache Shared Skill SHALL derive deterministic keys from normalized operation
parameters as defined in the
[Cache Entry schema](../../../schemas/cache-entry.md).

---

## Parameter Normalization

The Cache Shared Skill SHALL normalize parameters so that equivalent operations
produce equal keys.

---

# Lookup Capabilities

## Scoped Lookup

The Cache Shared Skill SHALL look up entries by key within the requested scope.

---

## Hit And Miss Classification

The Cache Shared Skill SHALL classify a lookup as a fresh hit, a stale hit, or a
miss.

---

# Freshness Capabilities

## Freshness Evaluation

The Cache Shared Skill SHALL evaluate freshness against `expires_at`.

---

## Stale-While-Revalidate

The Cache Shared Skill SHALL serve a stale entry within
`stale_while_revalidate` while obtaining a fresh value.

---

# Revalidation Capabilities

## Conditional Revalidation

The Cache Shared Skill SHALL support revalidation using entry validators.

---

## Freshness Refresh

The Cache Shared Skill SHALL refresh freshness on a confirmed entry without
re-storing the value.

---

# Storage Capabilities

## Entry Storage

The Cache Shared Skill SHALL store a caller-produced value as a
[Cache Entry](../../../schemas/cache-entry.md) when the result is cacheable.

---

## Cacheability Enforcement

The Cache Shared Skill SHALL NOT store non-deterministic results or results
containing secrets.

---

# Scope Enforcement Capabilities

## Scope Isolation

The Cache Shared Skill SHALL serve entries only within their declared scope.

---

# Eviction Capabilities

## Expiry Eviction

The Cache Shared Skill SHALL evict expired entries beyond any revalidation
window.

---

## Budget Eviction

The Cache Shared Skill SHALL evict entries exceeding configured size or count
budgets according to the eviction policy.

---

# Observability Capabilities

## Evidence Capture

The Cache Shared Skill SHOULD capture lookup evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Cache Shared Skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Cache Shared Skill SHOULD expose metrics including hits, misses, stale
serves, revalidations, stores, and evictions.

---

# Capability Boundaries

The Cache Shared Skill SHALL NOT

- Execute operations directly
- Perform input or output
- Interpret cached content as findings
- Cache secrets or credentials
- Serve entries out of scope

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Deterministic Keying | Key Derivation | SHALL |
| Parameter Normalization | Key Derivation | SHALL |
| Scoped Lookup | Lookup | SHALL |
| Hit And Miss Classification | Lookup | SHALL |
| Freshness Evaluation | Freshness | SHALL |
| Stale-While-Revalidate | Freshness | SHALL |
| Conditional Revalidation | Revalidation | SHALL |
| Freshness Refresh | Revalidation | SHALL |
| Entry Storage | Storage | SHALL |
| Cacheability Enforcement | Storage | SHALL |
| Scope Isolation | Scope | SHALL |
| Expiry Eviction | Eviction | SHALL |
| Budget Eviction | Eviction | SHALL |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Cache Entry Schema](../../../schemas/cache-entry.md)
