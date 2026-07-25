# ADR-001 — Rate Limit Abstraction

**File:** `skills/shared/rate-limiter/adr/ADR-001-rate-limit-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform performs large volumes of outbound operations
against targets during discovery, authentication testing, and active security
testing. Uncontrolled outbound rates can

- Overwhelm or damage fragile targets
- Violate Rules of Engagement
- Trigger remote throttling that distorts results
- Constitute an unintended denial-of-service condition

Before this decision, pacing could be implemented independently inside each
shared package and domain skill. That approach produced

- Inconsistent throttling behavior across packages
- Duplicated and divergent logic
- Rate ceilings that were difficult to audit or enforce centrally
- No shared mechanism to adapt to remote throttling signals

The platform requires a single, canonical, implementation-independent mechanism
to pace outbound operations.

---

# Decision

The platform SHALL provide a dedicated Rate Limiter shared skill that centralizes
all outbound pacing decisions behind a stable interface.

The Rate Limiter SHALL

- Resolve a canonical
  [Rate Limit Policy](../../../../schemas/rate-limit-policy.md)
- Enforce rate, burst, and concurrency ceilings per configurable scope
- Apply declarative overflow behavior
- Adapt to remote throttling signals
- Enforce Rules of Engagement ceilings as inviolable bounds
- Emit evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL pace outbound operations exclusively through the
[Rate Limiter Interface](../interface.md) by supplying an execution callback.
The Rate Limiter SHALL remain unaware of the operation implementation.

Rate limiting policy SHALL be expressed as a canonical schema, mirroring the
established pattern of the [Retry](../../retry/README.md) shared skill and its
[Retry Policy](../../../../schemas/retry-policy.md) schema.

---

# Alternatives Considered

## Per-Package Rate Limiting

Each shared package could implement its own pacing.

Rejected because it duplicates logic, diverges over time, and makes Rules of
Engagement ceilings impossible to enforce or audit centrally.

## Combining Rate Limiting With Retry

Pacing could be folded into the Retry shared skill.

Rejected because pacing and recovery are orthogonal concerns. Pacing decides
whether an operation MAY proceed now; retry decides whether a failed operation
SHOULD be attempted again. Conflating them would produce a less cohesive
abstraction and complicate reuse. The two skills remain complementary and
independent.

## Transport-Level Throttling Only

Pacing could be delegated to individual transport adapters.

Rejected because it would tie rate policy to specific implementations, prevent
cross-transport consistency, and expose implementation detail to consumers.

---

# Consequences

## Positive

- Uniform outbound pacing across every package
- Central, auditable enforcement of Rules of Engagement ceilings
- Consistent adaptive throttling behavior
- Reusable, testable abstraction independent of transport
- Correlated rate-limit evidence for reporting

## Negative

- Consumers MUST route outbound operations through the interface
- An additional shared dependency is introduced
- Distributed coordination, if later required, adds complexity

The negative consequences are outweighed by the safety and consistency benefits.

---

# Compliance

Consumers SHALL

- Acquire a permit for every outbound operation, including retries
- Reference shared rate-limit policies rather than inlining values
- Never exceed Rules of Engagement ceilings through overrides

Shared packages that perform input or output SHALL depend on the Rate Limiter
and SHALL NOT implement independent throttling.

---

# Future Compatibility

Future versions MAY introduce distributed coordination, cost-weighted permits,
and priority-aware fair queuing. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Rate Limiter README](../README.md)
- [Rate Limiter Interface](../interface.md)
- [Rate Limiter Execution Model](../execution.md)
- [Rate Limiter Error Model](../error-model.md)
- [Retry](../../retry/README.md)
- [Rate Limit Policy Schema](../../../../schemas/rate-limit-policy.md)
- [Evidence Schema](../../../../schemas/evidence.md)
