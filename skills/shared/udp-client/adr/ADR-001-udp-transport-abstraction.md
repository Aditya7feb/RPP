# ADR-001 — UDP Transport Abstraction

**File:** `skills/shared/udp-client/adr/ADR-001-udp-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform requires UDP transport for probing datagram
services and for datagram-oriented protocols. UDP is connectionless and
unreliable, and it can be abused for amplification attacks.

If each skill sent datagrams directly, the platform would suffer

- Inconsistent handling of the connectionless, unreliable nature of UDP
- Divergent response correlation and timeout handling
- Risk of amplification abuse
- Duplicated datagram logic
- Tight coupling to specific socket implementations

The platform requires a single, canonical, implementation-independent UDP
transport that makes unreliability explicit and prevents amplification abuse.

---

# Decision

The platform SHALL provide a dedicated UDP Client shared skill that centralizes
UDP transport behind a stable interface.

The UDP Client shared skill SHALL

- Send bounded datagrams and correlate responses within bounded windows
- Treat the absence of a response as a normal outcome
- Enforce amplification protection as a hard boundary
- Resolve hostnames through the [DNS Client](../../dns-client/README.md)
- Apply rate governance through the
  [Rate Limiter](../../rate-limiter/README.md) and retry only idempotent
  exchanges through the [Retry](../../retry/README.md) shared skill
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform UDP transport exclusively through the
[UDP Client Interface](../interface.md). The UDP Client SHALL NOT guarantee
delivery or interpret application-layer protocols.

---

# Alternatives Considered

## Per-Skill Datagrams

Each skill could send datagrams directly.

Rejected because it duplicates logic and risks inconsistent unreliability
handling and amplification abuse.

## Treating No-Response As An Error

The absence of a response could be modeled as an error.

Rejected because for an unreliable protocol the absence of a response is a normal
outcome whose significance is domain specific. Modeling it as an error would
distort control flow.

## Unbounded Datagrams

UDP could allow arbitrary payload and response sizes.

Rejected because unbounded datagrams enable amplification abuse and resource
exhaustion. Bounds and ratio limits are mandatory.

---

# Consequences

## Positive

- Uniform, bounded UDP transport across skills
- Explicit, correct handling of unreliability
- Amplification protection enforced centrally
- Reusable, testable abstraction independent of sockets

## Negative

- Consumers MUST perform UDP through the interface
- An additional shared dependency is introduced
- Idempotency must be declared to enable retries

The negative consequences are outweighed by safety and correctness.

---

# Compliance

Consumers SHALL

- Perform UDP through the UDP Client Interface
- Declare idempotency before enabling retries
- Treat `no_response` as a normal outcome
- Respect amplification bounds

---

# Future Compatibility

Future versions MAY add multi-response collection, multicast descriptors, and
fragmentation awareness. These extensions SHALL preserve the existing interface
and SHALL maintain backward compatibility.

---

# Related Documents

- [UDP Client README](../README.md)
- [UDP Client Interface](../interface.md)
- [UDP Client Execution Model](../execution.md)
- [UDP Client Error Model](../error-model.md)
- [DNS Client](../../dns-client/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
