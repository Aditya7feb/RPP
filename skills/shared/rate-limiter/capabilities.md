# Rate Limiter Capabilities

**File:** `skills/shared/rate-limiter/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Rate Limiter Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Rate Limiter Interface](interface.md).

---

# Capability Model

Capabilities are grouped as follows.

```
Pacing

Concurrency

Overflow Handling

Adaptive Control

Governance

Observability
```

---

# Pacing Capabilities

## Permit Acquisition

The Rate Limiter SHALL grant a permit when the resolved scope is within its
configured rate.

Inputs

- Policy reference
- Scope key inputs
- Operation priority

Outputs

- Permit grant or deferral decision

---

## Rate Enforcement

The Rate Limiter SHALL enforce the configured `permits` per `interval` using the
selected algorithm.

Supported algorithms

- token_bucket
- leaky_bucket
- fixed_window
- sliding_window

---

## Burst Control

The Rate Limiter SHALL allow instantaneous bursts up to the configured `burst`
allowance for bucket algorithms and SHALL never exceed it.

---

# Concurrency Capabilities

## Concurrency Limiting

The Rate Limiter SHALL bound the number of simultaneously outstanding operations
within a scope to `concurrency.max_in_flight`.

---

## Slot Lifecycle Management

The Rate Limiter SHALL acquire a concurrency slot before execution and release
it on completion, including on error.

---

# Overflow Handling Capabilities

## Wait

The Rate Limiter SHALL block a caller until a permit is available or `max_wait`
elapses.

---

## Reject

The Rate Limiter SHALL return a canonical rate-limit error immediately when the
policy action is `reject`.

---

## Shed

The Rate Limiter SHALL discard the lowest-priority queued operations when the
policy action is `shed`.

---

## Queue Bounding

The Rate Limiter SHALL enforce `max_queue_depth` and SHALL reject operations
that would exceed it.

---

# Adaptive Control Capabilities

## Throttle Signal Handling

The Rate Limiter SHALL reduce the effective rate in response to caller-reported
throttling signals when `adaptive.enabled` is `true`.

---

## Retry-After Suppression

The Rate Limiter SHALL suppress outbound operations within a scope for the
duration of a transport-provided `Retry-After` signal when
`respect_retry_after` is `true`.

---

## Rate Recovery

The Rate Limiter SHALL restore the effective rate toward the configured rate
according to the policy `recovery` mode once throttling subsides.

---

# Governance Capabilities

## Rules of Engagement Enforcement

The Rate Limiter SHALL treat `roe_binding.enforced` bounds as an inviolable
ceiling and SHALL reject any override that would exceed them.

---

## Policy Resolution

The Rate Limiter SHALL resolve the applicable
[Rate Limit Policy](../../../schemas/rate-limit-policy.md) from a policy
reference or a validated inline override.

---

# Observability Capabilities

## Evidence Capture

The Rate Limiter SHOULD capture per-decision evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Rate Limiter SHOULD publish lifecycle events to the platform Execution
State.

---

## Metrics

The Rate Limiter SHOULD expose metrics including granted permits, deferred
permits, rejected operations, shed operations, and average wait time.

---

# Capability Boundaries

The Rate Limiter SHALL NOT

- Execute operations directly
- Perform input or output
- Decide retryability
- Interpret response content as findings
- Own session or connection state

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Permit Acquisition | Pacing | SHALL |
| Rate Enforcement | Pacing | SHALL |
| Burst Control | Pacing | SHALL |
| Concurrency Limiting | Concurrency | SHALL |
| Slot Lifecycle Management | Concurrency | SHALL |
| Wait | Overflow | SHALL |
| Reject | Overflow | SHALL |
| Shed | Overflow | SHALL |
| Queue Bounding | Overflow | SHALL |
| Throttle Signal Handling | Adaptive | SHALL |
| Retry-After Suppression | Adaptive | SHALL |
| Rate Recovery | Adaptive | SHALL |
| Rules of Engagement Enforcement | Governance | SHALL |
| Policy Resolution | Governance | SHALL |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)
