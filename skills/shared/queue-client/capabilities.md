# Queue Client Capabilities

**File:** `skills/shared/queue-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Queue Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Queue Client Interface](interface.md).

---

# Capability Model

```
Connection

Publishing

Consumption

Acknowledgment

Poison Handling

Governance

Observability
```

---

# Connection Capabilities

## Broker Connection

The Queue Client SHALL connect to brokers behind a uniform interface.

---

## Authentication

The Queue Client SHALL authenticate to brokers through the
[Authentication](../authentication/README.md) package.

---

# Publishing Capabilities

## Message Publishing

The Queue Client SHALL publish messages with declared delivery semantics.

---

## Publish Bounding

The Queue Client SHALL bound message size and publish rate.

---

## Intrusive Gating

The Queue Client SHALL gate publishing to target-owned queues as intrusive.

---

# Consumption Capabilities

## Message Consumption

The Queue Client SHALL consume messages with visibility timeouts.

---

## Consumption Bounding

The Queue Client SHALL bound consumption by message count and duration.

---

# Acknowledgment Capabilities

## Acknowledgment

The Queue Client SHALL acknowledge processed messages.

---

## Negative Acknowledgment

The Queue Client SHALL negatively acknowledge or time out unprocessed messages.

---

# Poison Handling Capabilities

## Redelivery Bounding

The Queue Client SHALL bound redelivery attempts.

---

## Dead-Lettering

The Queue Client SHALL dead-letter or report poison messages rather than loop.

---

# Governance Capabilities

## Rate Governance

The Queue Client SHALL acquire a rate permit per publish and consume batch
through the [Rate Limiter](../rate-limiter/README.md).

---

## Retry Governance

The Queue Client MAY retry transient broker failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The Queue Client SHOULD capture operation evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Queue Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Queue Client SHOULD expose metrics including published, consumed,
acknowledged, redelivered, and dead-lettered counts.

---

# Capability Boundaries

The Queue Client SHALL NOT

- Detect broker vulnerabilities
- Produce findings
- Guarantee unavailable semantics
- Loop poison messages indefinitely
- Persist sensitive contents without authorization

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Broker Connection | Connection | SHALL |
| Authentication | Connection | SHALL |
| Message Publishing | Publishing | SHALL |
| Publish Bounding | Publishing | SHALL |
| Intrusive Gating | Publishing | SHALL |
| Message Consumption | Consumption | SHALL |
| Consumption Bounding | Consumption | SHALL |
| Acknowledgment | Acknowledgment | SHALL |
| Negative Acknowledgment | Acknowledgment | SHALL |
| Redelivery Bounding | Poison Handling | SHALL |
| Dead-Lettering | Poison Handling | SHALL |
| Rate Governance | Governance | SHALL |
| Retry Governance | Governance | MAY |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Authentication](../authentication/README.md)
