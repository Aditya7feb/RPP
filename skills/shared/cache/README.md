# Cache Shared Skill

**File:** `skills/shared/cache/README.md`

**Version:** 1.0.0

---

# Purpose

The Cache Shared Skill provides the canonical, implementation-independent
mechanism for storing and reusing the results of expensive or repeated
operations within the Robust PenTest Platform (RPP).

Rather than allowing individual skills and shared packages to implement their
own caching, this shared skill centralizes key derivation, freshness
evaluation, revalidation, scoping, and cache observability.

All packages that reuse deterministic operation results SHOULD delegate caching
to this shared skill.

---

# Goals

The Cache Shared Skill SHALL

- Abstract caching behind a stable interface
- Derive deterministic cache keys
- Evaluate freshness and staleness
- Support conditional revalidation
- Enforce cache scope
- Prevent caching of non-deterministic or sensitive results
- Generate cache evidence
- Integrate with platform observability

---

# Non-Goals

The Cache Shared Skill SHALL NOT

- Execute the underlying operation itself
- Perform network, DNS, or TLS input or output
- Detect vulnerabilities
- Produce security findings
- Interpret cached content
- Cache secrets or credentials

The Cache Shared Skill decides *whether* a fresh result exists and *how* to
store one. The caller owns *how* to produce the result on a miss.

---

# Design Principles

The Cache Shared Skill SHALL be

- Deterministic in key derivation
- Freshness driven
- Scope aware
- Transport independent
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill or Shared Package

↓

Cache Shared Skill

├── Key Deriver
├── Freshness Evaluator
├── Revalidation Coordinator
├── Scope Guard
├── Eviction Manager
├── Evidence Manager
├── Event Manager

↓

Caller-Provided Producer
```

On a miss, the Cache Shared Skill SHALL obtain a value only through a
caller-supplied producer callback. It SHALL remain unaware of the producer
implementation.

---

# Responsibilities

The Cache Shared Skill is responsible for

- Deriving a deterministic key from normalized operation parameters
- Looking up a [Cache Entry](../../../schemas/cache-entry.md) by key and scope
- Evaluating freshness and staleness
- Coordinating revalidation using entry validators
- Storing new entries produced by the caller
- Enforcing scope boundaries
- Evicting expired or over-budget entries
- Emitting cache lifecycle events
- Capturing cache evidence

---

# Cache Lifecycle

```
Receive Lookup

↓

Derive Key

↓

Lookup Entry In Scope

├── Fresh Hit → Return Cached Value

├── Stale Hit
│     ├── stale_while_revalidate → Return Stale + Revalidate
│     └── else → Revalidate Or Miss

└── Miss → Invoke Producer

           ↓

           Cacheable?

           ├── Yes → Store Entry → Return Value
           └── No  → Return Value (uncached)
```

The lookup decision SHOULD be preserved as evidence.

---

# Key Derivation

The Cache Shared Skill SHALL derive keys deterministically from the
`key_components` defined in the
[Cache Entry schema](../../../schemas/cache-entry.md).

Equivalent operations SHALL produce equal keys through parameter normalization.

Keys SHALL NOT incorporate secret material.

---

# Freshness Evaluation

The Cache Shared Skill SHALL classify an entry as

- Fresh when the current time is before `expires_at`
- Stale when the current time is at or after `expires_at`

A stale entry MAY be served within `stale_while_revalidate` while a fresh value
is obtained.

---

# Revalidation

Where an entry carries validators, the Cache Shared Skill SHALL support
conditional revalidation.

The caller-provided producer MAY use validators to obtain either a confirmation
that the entry is still valid or a fresh value.

A confirmed entry SHALL have its freshness refreshed without re-storing the full
value.

---

# Scope Enforcement

The Cache Shared Skill SHALL enforce the entry `scope`.

- `assessment` entries SHALL be visible only within the originating assessment
- `session` entries SHALL be visible only within the originating session
- `global` entries MAY be reused across assessments where policy permits

An entry SHALL NOT be served outside its scope.

---

# Cacheability

The Cache Shared Skill SHALL NOT store

- Results marked non-deterministic by the caller
- Values containing secrets or credentials
- Results of operations with side effects intended to be repeated

The caller SHALL declare whether a result is cacheable.

---

# Eviction

The Cache Shared Skill SHALL evict

- Expired entries beyond any revalidation window
- Entries exceeding configured size or count budgets

Eviction SHALL follow the configured policy and SHALL be observable.

---

# Evidence

The Cache Shared Skill SHOULD capture

- Key reference
- Hit, miss, or revalidation decision
- Entry provenance
- Freshness at decision time

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

Evidence SHALL NOT contain cached secrets.

---

# Events

The Cache Shared Skill SHOULD publish

- CacheLookup
- CacheHit
- CacheMiss
- CacheStaleServed
- CacheRevalidated
- CacheStored
- CacheEvicted

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Cache Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Cache Entry Schema](../../../schemas/cache-entry.md)

The Cache Shared Skill SHALL NOT depend on domain skills or on any package that
performs input or output.

---

# Consumers

Typical consumers include

- [DNS Client](../dns-client/README.md)
- [TLS Client](../tls-client/README.md)
- [HTTP Client](../http-client/README.md)
- Discovery skills reusing enumeration results

---

# Outputs

Typical outputs MAY include

- Cached or freshly produced value
- Lookup decision
- Cache metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Cache Shared Skill SHALL

- Never cache secrets or credentials
- Enforce scope to prevent cross-assessment leakage
- Exclude secret material from keys and evidence
- Preserve provenance for auditing
- Bound cache size to prevent resource exhaustion

Caching sensitive results or serving them out of scope can leak data. The shared
skill SHALL make caching decisions explicit and auditable.

---

# Best Practices

Consumers SHOULD

- Declare cacheability and scope explicitly
- Provide validators where revalidation is possible
- Choose the narrowest sufficient scope
- Capture cache evidence
- Treat cache misses as normal

---

# Anti-Patterns

Consumers SHOULD NOT

- Cache authenticated responses containing secrets
- Reuse entries across scopes
- Derive keys from secret material
- Cache non-deterministic results
- Implement ad hoc caches

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-cache-abstraction.md

---

# Related Shared Packages

- [DNS Client](../dns-client/README.md)
- [TLS Client](../tls-client/README.md)
- [HTTP Client](../http-client/README.md)

---

# Canonical Schemas

- [Cache Entry](../../../schemas/cache-entry.md)
- [Evidence](../../../schemas/evidence.md)
- [Execution State](../../../schemas/execution-state.md)

---

# Architecture Decisions

- [ADR-001 — Cache Abstraction](adr/ADR-001-cache-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Distributed shared caches
- Negative caching with bounded lifetimes
- Content-addressed deduplication
- Tiered storage backends expressed behind the same interface

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Cache Shared Skill provides a deterministic, scope-aware, and
implementation-independent caching abstraction for the Robust PenTest Platform.

It enables consistent reuse of expensive results across every shared package
while preventing leakage of sensitive data and preserving evidence, without
embedding caching logic in consumers.
