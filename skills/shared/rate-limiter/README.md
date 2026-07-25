# Rate Limiter Shared Skill

**File:** `skills/shared/rate-limiter/README.md`

**Version:** 1.0.0

---

# Purpose

The Rate Limiter Shared Skill provides the canonical, implementation-independent
mechanism for pacing outbound operations within the Robust PenTest Platform
(RPP).

Rather than allowing individual skills and shared packages to implement their
own throttling, this shared skill centralizes rate decisioning, burst control,
concurrency limiting, adaptive throttling, and rate observability.

All packages that perform outbound operations SHALL delegate pacing decisions to
this shared skill.

---

# Goals

The Rate Limiter Shared Skill SHALL

- Abstract rate limiting behind a stable interface
- Enforce a configured request rate per scope
- Enforce burst and concurrency ceilings
- Adapt to remote throttling signals
- Honor Rules of Engagement rate ceilings
- Generate rate-limit evidence
- Integrate with platform observability

---

# Non-Goals

The Rate Limiter Shared Skill SHALL NOT

- Execute the underlying operation itself
- Perform network, DNS, or TLS input or output
- Detect vulnerabilities
- Produce security findings
- Interpret response content
- Own connection or session state
- Decide whether an operation is retryable

The Rate Limiter decides *whether* and *when* an operation MAY proceed. The
caller owns *how* to execute the operation. Recovery from transient failure
remains the responsibility of the [Retry](../retry/README.md) shared skill.

---

# Design Principles

The Rate Limiter Shared Skill SHALL be

- Deterministic given the same policy and inputs
- Policy driven
- Transport independent
- Observable
- Bounded
- Fair across concurrent callers
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill or Shared Package

↓

Rate Limiter Shared Skill

├── Policy Resolver
├── Scope Keyer
├── Permit Allocator
├── Concurrency Guard
├── Adaptive Controller
├── Queue Manager
├── Evidence Manager
├── Event Manager

↓

Caller-Provided Operation
```

The Rate Limiter grants or defers permits but SHALL invoke the operation only
through a caller-supplied execution callback. It SHALL remain unaware of the
operation implementation.

---

# Responsibilities

The Rate Limiter Shared Skill is responsible for

- Resolving the applicable
  [Rate Limit Policy](../../../schemas/rate-limit-policy.md)
- Computing the enforcement key from the policy `scope`
- Allocating permits according to the configured algorithm
- Enforcing burst and concurrency ceilings
- Applying overflow behavior when a limit is reached
- Adapting the effective rate to remote throttling signals
- Emitting rate-limit lifecycle events
- Capturing per-decision evidence

---

# Rate Limiting Lifecycle

```
Receive Operation

↓

Resolve Policy

↓

Compute Scope Key

↓

Request Permit

↓

Permit Available?

├── Yes → Acquire Concurrency Slot → Execute → Release

└── No  → Apply Overflow Action

          ├── wait   → Queue Until Permit or max_wait
          ├── reject → Return Rate-Limit Error
          └── shed   → Drop Lowest Priority
```

The complete decision history SHOULD be preserved as evidence.

---

# Enforcement Scope

The scope key SHALL be derived from the policy `scope` field as defined in the
[Rate Limit Policy schema](../../../schemas/rate-limit-policy.md).

- `global` maintains a single limit across all operations
- `per_host` maintains an independent limit per resolved host
- `per_target` keys on the assessment target
- `per_assessment` keys on the assessment identifier
- `per_credential` keys on the authenticating principal

Independent scope keys SHALL be limited independently.

---

# Algorithms

The Rate Limiter Shared Skill SHALL support the algorithms defined in the
[Rate Limit Policy schema](../../../schemas/rate-limit-policy.md)

- token_bucket
- leaky_bucket
- fixed_window
- sliding_window

Burst allowance SHALL apply only to `token_bucket` and `leaky_bucket`.

---

# Concurrency Limiting

Where a policy defines `concurrency.max_in_flight`, the Rate Limiter SHALL bound
the number of simultaneously outstanding operations within the resolved scope.

A concurrency slot SHALL be acquired before execution and released on
completion, including on error.

---

# Overflow Behavior

When no permit is available, the Rate Limiter SHALL apply the policy
`on_limit.action`

- `wait` queues the caller until a permit is available or `max_wait` elapses
- `reject` returns a canonical rate-limit error immediately
- `shed` discards the lowest-priority queued operations

Queue depth SHALL never exceed `on_limit.max_queue_depth` where configured.

---

# Adaptive Throttling

Where a policy enables `adaptive`, the Rate Limiter SHALL reduce the effective
rate in response to caller-reported throttling signals such as `Retry-After`
durations and configured `throttle_status_codes`.

The effective rate SHALL recover toward the configured rate according to the
policy `recovery` mode once throttling subsides.

Adaptation SHALL never raise the rate above the configured or Rules of
Engagement ceiling.

---

# Rules of Engagement

Where a policy sets `roe_binding.enforced`, the configured bounds SHALL be
treated as an inviolable ceiling.

No override, adaptive adjustment, or caller request SHALL cause outbound
operations to exceed a Rules of Engagement rate ceiling.

---

# Evidence

The Rate Limiter Shared Skill SHOULD capture

- Policy reference
- Scope key
- Decision outcome
- Wait duration
- Effective rate at decision time
- Queue depth at decision time

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Events

The Rate Limiter Shared Skill SHOULD publish

- PermitRequested
- PermitGranted
- PermitDeferred
- OperationQueued
- OperationRejected
- OperationShed
- RateThrottled
- RateRecovered

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Rate Limiter Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)

The Rate Limiter Shared Skill SHALL NOT depend on domain skills or on any
package that performs input or output.

---

# Consumers

Typical consumers include

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [DNS Client](../dns-client/README.md)
- Future network clients
- Discovery skills

---

# Relationship to Retry

The Rate Limiter and [Retry](../retry/README.md) shared skills are
complementary and independent.

- The Rate Limiter decides whether an operation MAY proceed now.
- Retry decides whether a failed operation SHOULD be attempted again.

Consumers SHOULD acquire a rate permit for every attempt, including retries, so
that retry traffic remains within the configured rate.

---

# Outputs

Typical outputs MAY include

- Final operation result
- Rate-limit error
- Decision history
- Rate metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Rate Limiter Shared Skill SHALL

- Enforce bounded outbound rates to prevent denial-of-service conditions
- Respect Rules of Engagement rate ceilings
- Prevent burst amplification beyond configured allowances
- Protect secrets present in operation context
- Preserve auditability

Uncontrolled outbound rates can harm targets and violate engagement scope. The
shared skill SHALL always enforce a finite, configured rate.

---

# Best Practices

Consumers SHOULD

- Reference shared rate-limit policies rather than inlining values
- Acquire a permit for every attempt, including retries
- Choose `per_host` scope for target-facing operations
- Enable adaptive throttling for authenticated APIs
- Capture rate-limit evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Implement manual throttling loops
- Bypass the limiter for "small" bursts
- Hardcode rate values
- Exceed Rules of Engagement ceilings through overrides
- Share a single scope key across unrelated targets

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
- adr/ADR-001-rate-limit-abstraction.md

---

# Related Shared Packages

- [Retry](../retry/README.md)
- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [DNS Client](../dns-client/README.md)

---

# Canonical Schemas

- [Rate Limit Policy](../../../schemas/rate-limit-policy.md)
- [Evidence](../../../schemas/evidence.md)
- [Execution State](../../../schemas/execution-state.md)

---

# Architecture Decisions

- [ADR-001 — Rate Limit Abstraction](adr/ADR-001-rate-limit-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Distributed rate coordination across workers
- Priority-aware fair queuing
- Cost-weighted permits for heterogeneous operations
- Predictive throttling from observed latency
- Shared budgets across assessment phases

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Rate Limiter Shared Skill provides a bounded, deterministic, and
implementation-independent pacing abstraction for the Robust PenTest Platform.

It enables consistent outbound safety across every shared package while
preserving Rules of Engagement, evidence, and observability, and without
embedding throttling logic in consumers.
