# Queue Client Shared Skill

**File:** `skills/shared/queue-client/README.md`

**Version:** 1.0.0

---

# Purpose

The Queue Client Shared Skill provides the canonical, implementation-independent
mechanism for publishing and consuming messages through message brokers within
the Robust PenTest Platform (RPP).

Rather than allowing individual skills to interact with brokers directly, this
shared skill centralizes publishing, consuming, acknowledgment, visibility
management, poison-message handling, and observability behind a stable interface.

All packages that require message-queue access SHALL delegate to this shared
skill.

---

# Goals

The Queue Client Shared Skill SHALL

- Abstract message brokers behind a stable interface
- Publish and consume messages with explicit delivery semantics
- Manage acknowledgment and visibility timeouts
- Handle poison messages through bounded redelivery and dead-lettering
- Authenticate to brokers through the
  [Authentication](../authentication/README.md) package
- Produce queue evidence
- Integrate with platform observability

---

# Non-Goals

The Queue Client Shared Skill SHALL NOT

- Detect vulnerabilities such as unauthenticated brokers
- Produce security findings
- Interpret message contents as findings
- Perform unbounded message production
- Guarantee semantics the broker cannot provide

The Queue Client moves messages with explicit semantics and reports outcomes as
data. Interpretation belongs to domain skills.

---

# Design Principles

The Queue Client Shared Skill SHALL be

- Explicit about delivery semantics
- Deterministic in bounds given the same configuration and inputs
- Bounded in message size and consumption volume
- Governed
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

Queue Client Shared Skill

├── Broker Connector
├── Publisher
├── Consumer
├── Acknowledgment Manager
├── Visibility Manager
├── Poison Handler
├── Evidence Manager
├── Event Manager

↓

Broker Adapter
```

The Queue Client publishes and consumes messages but SHALL remain unaware of the
broker adapter implementation.

---

# Responsibilities

The Queue Client Shared Skill is responsible for

- Connecting to a broker and authenticating via the
  [Authentication](../authentication/README.md) package
- Publishing messages with declared delivery semantics
- Consuming messages with visibility timeouts and acknowledgment
- Enforcing bounded redelivery and dead-lettering poison messages
- Applying rate and retry governance
- Emitting queue lifecycle events and capturing evidence

---

# Delivery Semantics

The Queue Client SHALL support the semantics offered by the broker

```
at_most_once

at_least_once

exactly_once
```

Where a broker cannot provide a requested semantic, the Queue Client SHALL report
the strongest available semantic rather than silently degrade.

Consumers relying on `at_least_once` SHALL implement idempotent processing.

---

# Publishing

The Queue Client SHALL publish messages bounded by message size and publish rate.

Publishing SHALL be treated as an operation with side effects; publishing to
target-owned queues SHALL be gated as intrusive.

---

# Consuming And Acknowledgment

The Queue Client SHALL consume messages with a visibility timeout during which a
message is invisible to other consumers.

A successfully processed message SHALL be acknowledged; an unprocessed message
SHALL be negatively acknowledged or allowed to time out for redelivery.

Consumption SHALL be bounded by a maximum message count and total duration.

---

# Poison-Message Handling

The Queue Client SHALL bound redelivery attempts.

A message exceeding its redelivery bound SHALL be dead-lettered where the broker
supports it, or reported as a poison message otherwise, rather than looped
indefinitely.

---

# Governance

The Queue Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per publish
  and per consume batch
- Recover transient broker failures through the [Retry](../retry/README.md)
  shared skill

Publishing to queues not owned by the platform SHALL be gated as intrusive.

---

# Evidence

The Queue Client Shared Skill SHOULD capture

- Broker and queue identifiers
- Operation kind and delivery semantic
- Message counts and sizes
- Acknowledgment and dead-letter outcomes
- Operation duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain sensitive
message contents unless explicitly authorized and redacted.

---

# Events

The Queue Client Shared Skill SHOULD publish

- BrokerConnected
- MessagePublished
- MessageConsumed
- MessageAcknowledged
- MessageRedelivered
- MessageDeadLettered
- OperationFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Queue Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Queue Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Asynchronous workflow coordination within the platform
- Message-broker assessment skills
- Service enumeration skills probing broker endpoints

---

# Outputs

Typical outputs MAY include

- Publish confirmations
- Consumed messages by reference
- Acknowledgment and dead-letter outcomes
- Queue evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Queue Client Shared Skill SHALL

- Report delivery semantics honestly rather than silently degrade
- Bound message size, redelivery, and consumption volume
- Treat publishing to target queues as intrusive
- Protect sensitive message contents from evidence and logs
- Preserve auditability

Unbounded production or redelivery can overwhelm a broker. The shared skill SHALL
enforce bounds.

---

# Best Practices

Consumers SHOULD

- Implement idempotent processing under at-least-once semantics
- Bound consumption volume and message size
- Rely on dead-lettering for poison messages
- Authorize publishing to target queues explicitly
- Capture queue evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Interact with brokers directly
- Assume exactly-once where unavailable
- Loop poison messages indefinitely
- Publish to target queues without authorization
- Persist sensitive message contents in evidence

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
- adr/ADR-001-queue-transport-abstraction.md

---

# Related Shared Packages

- [Authentication](../authentication/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Workflow Runtime](../workflow-runtime/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — Queue Transport Abstraction](adr/ADR-001-queue-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Streaming consumption descriptors
- Ordered partition consumption
- Transactional publish batches
- Schema-registry integration expressed canonically

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Queue Client Shared Skill provides a bounded, semantics-explicit, and
implementation-independent message-queue abstraction for the Robust PenTest
Platform.

It enables consistent, auditable publishing and consumption across brokers while
handling poison messages and honoring delivery semantics, without embedding
security interpretation or broker implementations in consumers.
