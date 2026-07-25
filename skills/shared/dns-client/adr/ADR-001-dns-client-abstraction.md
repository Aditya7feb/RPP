# ADR-001 — DNS Client Abstraction

**File:** `skills/shared/dns-client/adr/ADR-001-dns-client-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform requires DNS resolution and enumeration across many
domain skills, including recon, subdomain discovery, and fingerprinting. DNS can
be performed through many implementations: system resolvers, custom resolver
libraries, DNS-over-HTTPS services, and tool adapters such as Kali MCP.

If each skill performed DNS directly, the platform would suffer

- Divergent resolver behavior and record handling
- Inconsistent evidence and observability
- Duplicated caching, retry, and rate-limit logic
- Tight coupling to specific DNS implementations

The platform requires a single, canonical, implementation-independent mechanism
for DNS operations.

---

# Decision

The platform SHALL provide a dedicated DNS Client shared skill that centralizes
all DNS operations behind a stable interface.

The DNS Client shared skill SHALL

- Abstract DNS implementations behind adapters
- Support standard record resolution and validation
- Produce canonical results and evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)
- Integrate with the [Retry](../../retry/README.md),
  [Rate Limiter](../../rate-limiter/README.md), and
  [Cache](../../cache/README.md) shared skills
- Remain free of vulnerability detection and finding generation

Consumers SHALL perform DNS operations exclusively through the
[DNS Client Interface](../interface.md). Adapter implementations SHALL remain
hidden from consumers.

---

# Alternatives Considered

## Per-Skill DNS

Each skill could resolve DNS directly.

Rejected because it duplicates logic, diverges over time, and couples skills to
DNS implementations.

## Embedding DNS In The HTTP Client

DNS could be a private concern of the HTTP Client.

Rejected because DNS is required independently by discovery skills that do not
issue HTTP requests. DNS is a distinct, reusable capability.

---

# Consequences

## Positive

- Uniform DNS behavior across skills
- Consistent evidence and observability
- Centralized caching, retry, and rate limiting
- Implementation independence through adapters

## Negative

- Consumers MUST route DNS through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by consistency and reuse.

---

# Compliance

Consumers SHALL perform DNS through the DNS Client Interface and SHALL NOT invoke
DNS utilities directly or parse tool output.

---

# Future Compatibility

Future versions MAY add DNSSEC validation detail, encrypted transport options,
and passive DNS integration. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [DNS Client README](../README.md)
- [DNS Client Interface](../interface.md)
- [DNS Client Execution Model](../execution.md)
- [DNS Client Error Model](../error-model.md)
- [Evidence Schema](../../../../schemas/evidence.md)
