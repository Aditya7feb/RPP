# ADR-001 — TLS Client Abstraction

**File:** `skills/shared/tls-client/adr/ADR-001-tls-client-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform establishes and observes TLS connections for many
skills, including TLS analysis, HTTPS transport, and certificate enumeration.
TLS can be negotiated through many implementations such as OpenSSL, Go TLS,
rustls, Schannel, and tool adapters.

If each skill negotiated TLS directly, the platform would suffer

- Divergent negotiation and validation behavior
- Inconsistent certificate handling and evidence
- Duplicated session-reuse logic
- Tight coupling to specific TLS libraries
- Ambiguity when a proxy intercepts TLS

The platform requires a single, canonical, implementation-independent mechanism
for TLS operations.

---

# Decision

The platform SHALL provide a dedicated TLS Client shared skill that centralizes
TLS negotiation, certificate retrieval, and validation behind a stable
interface.

The TLS Client shared skill SHALL

- Abstract TLS implementations behind adapters
- Support negotiation, certificate-chain retrieval, and validation
- Produce canonical TLS schemas and evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)
- Honor interception boundaries communicated by the
  [Proxy](../../proxy/README.md) shared skill
- Remain free of vulnerability detection and finding generation, reporting
  validation outcomes rather than security verdicts

Consumers SHALL perform TLS operations exclusively through the
[TLS Client Interface](../interface.md). Adapter-specific TLS APIs SHALL NOT be
exposed to consumers.

---

# Alternatives Considered

## Per-Skill TLS

Each skill could negotiate TLS directly.

Rejected because it duplicates logic, diverges over time, and couples skills to
TLS libraries.

## Embedding TLS Solely In The HTTP Client

TLS could be a private concern of the HTTP Client.

Rejected because TLS analysis and certificate enumeration require TLS
independently of HTTP. TLS is a distinct, reusable capability.

## Reporting Validation Failures As Findings

The TLS Client could classify validation failures as findings.

Rejected because finding generation belongs to domain skills. The TLS Client
reports validation outcomes as canonical data; interpretation is a separate
responsibility.

---

# Consequences

## Positive

- Uniform TLS behavior across skills
- Consistent certificate handling and evidence
- Accurate validation in the presence of interception
- Implementation independence through adapters

## Negative

- Consumers MUST route TLS through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by consistency and accuracy.

---

# Compliance

Consumers SHALL perform TLS through the TLS Client Interface and SHALL NOT invoke
TLS libraries directly or interpret validation outcomes as findings within the
shared skill.

---

# Future Compatibility

Future versions MAY add post-quantum negotiation observation, session-ticket
analysis detail, and additional adapters. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [TLS Client README](../README.md)
- [TLS Client Interface](../interface.md)
- [TLS Client Execution Model](../execution.md)
- [TLS Client Error Model](../error-model.md)
- [Proxy](../../proxy/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
