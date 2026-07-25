# ADR-001 — TCP Transport Abstraction

**File:** `skills/shared/tcp-client/adr/ADR-001-tcp-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform requires raw TCP transport beneath several
higher-level clients, including TLS, SMTP, FTP, SSH, and database clients, and
for port-level checks. TCP can be performed through many socket implementations
and tool adapters.

If each client opened sockets directly, the platform would suffer

- Inconsistent timeout and bound handling
- Divergent proxy routing and rate governance
- Duplicated connection logic
- Tight coupling to specific socket implementations
- Risk of unbounded reads and resource exhaustion

The platform requires a single, canonical, implementation-independent TCP
transport.

---

# Decision

The platform SHALL provide a dedicated TCP Client shared skill that centralizes
TCP transport behind a stable interface.

The TCP Client shared skill SHALL

- Establish bounded connections to a host and port
- Resolve hostnames through the [DNS Client](../../dns-client/README.md)
- Route through the [Proxy](../../proxy/README.md) shared skill
- Apply rate and retry governance through the
  [Rate Limiter](../../rate-limiter/README.md) and
  [Retry](../../retry/README.md) shared skills
- Exchange bytes with bounded read and write operations
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform raw TCP transport exclusively through the
[TCP Client Interface](../interface.md). The TCP Client SHALL NOT interpret
application-layer protocols; higher-level clients layer their protocols atop the
byte stream.

---

# Alternatives Considered

## Per-Client Sockets

Each higher-level client could open sockets directly.

Rejected because it duplicates transport logic and produces inconsistent bounds
and governance.

## Folding TCP Into The TLS Client

TCP could be private to the TLS Client.

Rejected because non-TLS clients such as SMTP, FTP, and SSH also require TCP.
Transport is a distinct, reusable capability beneath TLS.

## Unbounded Transport

TCP could allow unbounded reads and connections.

Rejected because unbounded transport risks resource exhaustion and can harm
targets. Bounds are mandatory.

---

# Consequences

## Positive

- Uniform, bounded TCP transport across clients
- Consistent proxy routing and rate governance
- Reusable, testable abstraction independent of sockets
- Correlated connection evidence

## Negative

- Higher-level clients MUST layer atop the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by consistency and safety.

---

# Compliance

Consumers SHALL

- Perform TCP through the TCP Client Interface
- Supply explicit bounds
- Reference shared rate, retry, and proxy policies
- Delegate application semantics to higher-level clients

Higher-level clients SHALL depend on the TCP Client and SHALL NOT open sockets
directly.

---

# Future Compatibility

Future versions MAY add connection pooling, dual-stack connection racing, and
socket-option descriptors. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [TCP Client README](../README.md)
- [TCP Client Interface](../interface.md)
- [TCP Client Execution Model](../execution.md)
- [TCP Client Error Model](../error-model.md)
- [Proxy](../../proxy/README.md)
- [DNS Client](../../dns-client/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
