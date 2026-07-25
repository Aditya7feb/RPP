# ADR-001 — Retry Policy Abstraction

**File:** `skills/shared/retry/adr/ADR-001-retry-policy-abstraction.md`

**Version:** 1.0.0

**Status:** Accepted

**Date:** 2026-07-25

---

# Context

Nearly every operation performed by the Robust PenTest Platform (RPP) crosses an
unreliable boundary. HTTP requests, TLS handshakes, DNS queries, and future
network, database, and cloud operations all experience transient failures:
connect timeouts, resets, temporary name-resolution failures, and rate-limit
responses.

If each shared package and domain skill implements its own retry loop, the
platform accumulates the following problems.

- Divergent backoff and jitter behavior across packages
- Inconsistent classification of which failures are retryable
- Unbounded or aggressive retries that can constitute a denial-of-service
  condition against a target
- Retries of non-idempotent operations that compound side effects
- Retry logic that ignores execution deadlines
- Fragmented, non-correlatable retry evidence
- Duplicated code and inconsistent observability

The [HTTP Client](../../http-client/README.md) already delegates retry decisions
to a shared Retry package in its execution and error models, but that package
did not yet exist. This created a broken reference and blocked consistent retry
behavior across the platform.

The platform requires a single, canonical retry capability that every package
consumes, and a declarative policy object that describes retry behavior
independently of any implementation.

---

# Decision

The RPP SHALL expose a single shared Retry package located at
`skills/shared/retry/`.

All recoverable operations performed by shared packages and domain skills SHALL
delegate retry decisioning to the Retry Interface defined in
[interface.md](../interface.md).

Retry behavior SHALL be described declaratively by the
[Retry Policy schema](../../../../schemas/retry-policy.md) and resolved at
runtime through the Retry configuration.

The following rules SHALL apply.

- Consumers SHALL supply the operation as an execution callback and SHALL NOT
  implement their own retry loop.
- The Retry package SHALL decide *whether* and *when* to retry; the consumer
  owns *how* to execute the operation.
- The Retry package SHALL NOT perform input or output, detect vulnerabilities,
  or produce findings.
- Every resolved policy SHALL be clamped to platform-wide global bounds.
- Retries SHALL be bounded by attempt count, elapsed time, and execution
  deadline.
- Non-idempotent operations SHALL NOT be retried unless the consumer explicitly
  declares idempotency.

---

# Rationale

## Why retry is abstracted behind a shared package

A shared Retry package provides one place to enforce consistency and safety.

- **Uniform behavior.** Every package applies the same backoff, jitter, and
  classification semantics.
- **Safety by construction.** Global bounds guarantee that no policy can trigger
  unbounded retries, protecting both the platform and the target from
  amplification and denial-of-service conditions.
- **Correlated evidence.** All retries emit evidence conforming to the canonical
  [Evidence schema](../../../../schemas/evidence.md), enabling cross-package
  correlation.
- **Deadline integrity.** Retry decisions honor execution deadlines centrally
  rather than per package.
- **Separation of concerns.** Packages reason about *what* to execute; the Retry
  package reasons about *whether to try again*.

## Why retry policy is declarative and schema-driven

Encoding retry behavior as a canonical
[Retry Policy](../../../../schemas/retry-policy.md) object rather than as code
inside each package yields several benefits.

- Policies can be reviewed, versioned, and reused across packages.
- Policies remain implementation independent and portable across execution
  backends.
- Global bounds can be validated against every policy at load time.
- New strategies can be introduced through schema extension points without
  changing consumers.

## Why consumers MUST never implement their own retry loops

Ad hoc retry loops defeat every benefit above.

- They bypass global safety bounds and risk denial-of-service behavior.
- They fragment classification, producing inconsistent decisions for identical
  failures.
- They bypass canonical evidence and observability.
- They frequently ignore idempotency and deadlines.

Therefore consumers SHALL delegate all retry decisioning to the Retry Interface.

---

# Consequences

## Positive

- Consistent, bounded, observable retry behavior platform-wide.
- Reusable, versioned retry policies.
- Central enforcement of safety bounds and deadlines.
- Uniform, correlatable retry evidence.
- The existing HTTP Client reference is resolved.

## Negative

- A stable interface and policy schema SHALL be maintained.
- Consumers SHALL express operations as callbacks and declare idempotency.
- Advanced package-specific recovery remains the consumer's responsibility above
  the retry boundary.

## Neutral

- The Retry package becomes a widely shared dependency and SHALL follow semantic
  versioning to protect consumers.

---

# Alternatives Considered

## Allow each package to implement retries directly

Rejected. This is the status quo the platform eliminates. It produces divergent
behavior, unsafe unbounded retries, fragmented evidence, and duplicated logic.

## Provide a retry utility library without a policy schema

Rejected. A code-only utility cannot be reviewed, versioned, or validated as a
canonical artifact, and would couple behavior to a specific implementation.

## Embed retry behavior inside the HTTP Client only

Rejected. Retry is a cross-cutting concern needed by TLS, DNS, and future
network, database, and cloud clients. Placing it in a single client would force
duplication or improper upward dependencies.

---

# Compliance

A component is compliant with this decision when

- It performs all retry decisioning through the Retry Interface.
- It references a canonical Retry Policy rather than inlining retry logic.
- It supplies operations as callbacks and declares idempotency.
- It does not implement its own retry loop or unbounded retries.

---

# References

- [Retry README](../README.md)
- [Retry Interface](../interface.md)
- [Retry Execution Model](../execution.md)
- [Retry Error Model](../error-model.md)
- [Retry Configuration](../configuration.md)
- [Retry Policy Schema](../../../../schemas/retry-policy.md)
- [Evidence Schema](../../../../schemas/evidence.md)
- [HTTP Client](../../http-client/README.md)
- [TLS Client](../../tls-client/README.md)
- [DNS Client](../../dns-client/README.md)
