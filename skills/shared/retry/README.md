# Retry Shared Skill

**File:** `skills/shared/retry/README.md`

**Version:** 1.0.0

---

# Purpose

The Retry Shared Skill provides the canonical, implementation-independent
mechanism for recovering from transient failures within the Robust PenTest
Platform (RPP).

Rather than allowing individual skills and shared packages to implement their
own retry loops, this shared skill centralizes retry decisioning, backoff
computation, attempt budgeting, deadline awareness, and retry observability.

All packages that perform recoverable operations SHALL delegate retry decisions
to this shared skill.

---

# Goals

The Retry Shared Skill SHALL

- Abstract retry logic behind a stable interface
- Evaluate whether a failed operation is retryable
- Compute backoff delays deterministically
- Enforce attempt and time budgets
- Respect execution deadlines
- Honor transport-provided retry signals
- Generate retry evidence
- Integrate with platform observability

---

# Non-Goals

The Retry Shared Skill SHALL NOT

- Execute the underlying operation itself
- Perform network, DNS, or TLS input or output
- Detect vulnerabilities
- Produce security findings
- Interpret response content
- Own connection or session state

The Retry Shared Skill decides *whether* and *when* to retry. The caller owns
*how* to execute the operation.

---

# Design Principles

The Retry Shared Skill SHALL be

- Deterministic given the same policy and inputs
- Stateless between invocations except for the supplied attempt context
- Policy driven
- Transport independent
- Observable
- Bounded
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill or Shared Package

↓

Retry Shared Skill

├── Policy Resolver
├── Retryable Classifier
├── Backoff Calculator
├── Budget Manager
├── Deadline Guard
├── Evidence Manager
├── Event Manager

↓

Caller-Provided Operation
```

The Retry Shared Skill drives the retry loop but SHALL invoke the operation only
through a caller-supplied execution callback. It SHALL remain unaware of the
operation implementation.

---

# Responsibilities

The Retry Shared Skill is responsible for

- Resolving the applicable [Retry Policy](../../../schemas/retry-policy.md)
- Classifying failures as retryable or non-retryable
- Computing backoff and jitter
- Tracking attempt count and elapsed time
- Enforcing deadlines
- Honoring `Retry-After` and retryable status codes
- Emitting retry lifecycle events
- Capturing per-attempt evidence

---

# Retry Lifecycle

```
Receive Operation

↓

Resolve Policy

↓

Execute Attempt

↓

Evaluate Outcome

↓

Retryable?

├── No → Return Result or Error

└── Yes → Check Budget and Deadline

          ↓

          Compute Backoff

          ↓

          Wait

          ↓

          Next Attempt
```

The complete attempt history SHOULD be preserved as evidence.

---

# Retryable Classification

An outcome SHALL be classified using the resolved policy.

Classification SHALL consider

- Canonical error category
- Idempotency of the operation
- Explicit non-retryable categories
- Explicit abort categories
- Retryable protocol status codes

Ambiguous outcomes SHALL default to non-retryable to preserve safety.

---

# Backoff Strategies

The Retry Shared Skill SHALL support the strategies defined in the
[Retry Policy schema](../../../schemas/retry-policy.md)

- none
- fixed
- linear
- exponential
- exponential_jitter

Computed delays SHALL never exceed `backoff.max_delay`.

---

# Jitter

Where a policy requests jitter, the shared skill SHALL support

- full
- equal
- decorrelated

Jitter SHALL reduce synchronized retries across concurrent callers.

---

# Budgets and Deadlines

The Retry Shared Skill SHALL enforce

- `max_attempts`
- `max_elapsed_time` where configured
- Caller execution deadlines where `deadline_aware` is enabled

A retry SHALL NOT be scheduled when it would exceed any active bound.

---

# Retry Signals

Where a policy enables it, the shared skill SHALL honor

- Transport-provided `Retry-After` durations
- Retryable protocol status codes such as `429`, `502`, `503`, and `504`

Signal handling SHALL remain policy driven.

---

# Idempotency

Retries of non-idempotent operations carry risk.

When a policy sets `idempotent_only`, the shared skill SHALL retry only
operations the caller has declared idempotent.

Callers SHALL declare idempotency explicitly.

---

# Evidence

The Retry Shared Skill SHOULD capture

- Policy reference
- Attempt number
- Outcome category
- Computed delay
- Elapsed time
- Terminal decision

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Events

The Retry Shared Skill SHOULD publish

- RetryStarted
- AttemptStarted
- AttemptFailed
- RetryScheduled
- RetrySucceeded
- RetryExhausted
- RetryAborted

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Retry Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Retry Policy Schema](../../../schemas/retry-policy.md)

The Retry Shared Skill SHALL NOT depend on domain skills or on any package that
performs input or output.

---

# Consumers

Typical consumers include

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [DNS Client](../dns-client/README.md)
- Future network clients
- Discovery skills

---

# Outputs

Typical outputs MAY include

- Final operation result
- Terminal error
- Attempt history
- Retry metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Retry Shared Skill SHALL

- Enforce bounded attempts to prevent amplification
- Respect Rules of Engagement and rate constraints
- Avoid retrying operations that could compound side effects
- Protect secrets present in operation context
- Preserve auditability

Unbounded or aggressive retries can constitute a denial-of-service condition.
The shared skill SHALL always enforce a finite budget.

---

# Best Practices

Consumers SHOULD

- Reference shared retry policies rather than inlining values
- Declare operation idempotency explicitly
- Combine retry with the Rate Limiter for outbound safety
- Capture retry evidence
- Propagate execution deadlines

---

# Anti-Patterns

Consumers SHOULD NOT

- Implement manual retry loops
- Retry without a bounded budget
- Retry non-idempotent operations silently
- Hardcode backoff values
- Retry validation or authorization failures

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
- adr/ADR-001-retry-policy-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [DNS Client](../dns-client/README.md)

---

# Canonical Schemas

- [Retry Policy](../../../schemas/retry-policy.md)
- [Evidence](../../../schemas/evidence.md)
- [Execution State](../../../schemas/execution-state.md)

---

# Architecture Decisions

- [ADR-001 — Retry Policy Abstraction](adr/ADR-001-retry-policy-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Circuit breaking
- Adaptive backoff informed by observed latency
- Shared budgets across request batches
- Retry storms detection
- Distributed retry coordination

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Retry Shared Skill provides a bounded, deterministic, and
implementation-independent retry abstraction for the Robust PenTest Platform.

It enables consistent recovery from transient failures across every shared
package while preserving safety, evidence, and observability, and without
embedding retry logic in consumers.
