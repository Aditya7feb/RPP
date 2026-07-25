# ADR-001 — Queue Transport Abstraction

**File:** `skills/shared/queue-client/adr/ADR-001-queue-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform uses message brokers for asynchronous workflow
coordination and to assess broker endpoints. Message queues involve delivery
semantics, visibility timeouts, acknowledgment, and poison-message handling,
which vary across brokers and are easy to implement inconsistently.

If each skill interacted with brokers directly, the platform would suffer

- Duplicated publish and consume logic
- Inconsistent or dishonest delivery-semantic handling
- Poison messages looping indefinitely
- Unbounded production overwhelming brokers
- Divergent evidence and governance

The platform requires a single, canonical, implementation-independent
message-queue abstraction with explicit semantics and poison handling.

---

# Decision

The platform SHALL provide a dedicated Queue Client shared skill that centralizes
message-queue access behind a stable interface.

The Queue Client shared skill SHALL

- Connect to brokers and authenticate through the
  [Authentication](../../authentication/README.md) package
- Publish and consume messages with explicit, honestly reported delivery
  semantics
- Manage acknowledgment and visibility timeouts
- Bound redelivery and dead-letter poison messages
- Gate publishing to target-owned queues as intrusive
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform message-queue access exclusively through the
[Queue Client Interface](../interface.md). The Queue Client SHALL NOT detect
broker vulnerabilities; that interpretation belongs to domain skills.

---

# Alternatives Considered

## Per-Skill Broker Access

Each skill could interact with brokers directly.

Rejected because it duplicates logic and risks inconsistent semantics and poison
loops.

## Silently Degrading Semantics

The client could accept a requested semantic and provide a weaker one silently.

Rejected because silent degradation misleads consumers. The effective semantic is
reported honestly so consumers can process idempotently.

## Unbounded Redelivery

Poison messages could be redelivered indefinitely.

Rejected because unbounded redelivery wastes resources and can overwhelm a
broker. Redelivery is bounded and poison messages are dead-lettered.

---

# Consequences

## Positive

- Uniform publish and consume behavior across brokers
- Honest delivery-semantic reporting
- Bounded redelivery with dead-lettering
- Message preservation on failure
- Consistent evidence and governance

## Negative

- Consumers MUST use the interface and handle at-least-once idempotently
- An additional shared dependency is introduced

The negative consequences are outweighed by correctness and consistency.

---

# Compliance

Consumers SHALL

- Perform message-queue access through the Queue Client Interface
- Process idempotently under at-least-once semantics
- Bound consumption volume and message size
- Publish to target queues only when authorized
- Interpret broker posture at the domain layer

---

# Future Compatibility

Future versions MAY add streaming consumption, ordered partitions, and
transactional publish batches. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Queue Client README](../README.md)
- [Queue Client Interface](../interface.md)
- [Queue Client Execution Model](../execution.md)
- [Queue Client Error Model](../error-model.md)
- [Authentication](../../authentication/README.md)
- [Workflow Runtime](../../workflow-runtime/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
