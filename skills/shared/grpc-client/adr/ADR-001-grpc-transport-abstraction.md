# ADR-001 — gRPC Transport Abstraction

**File:** `skills/shared/grpc-client/adr/ADR-001-grpc-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with gRPC services, which run over
HTTP/2, commonly secured with TLS, and support unary and streaming methods with
metadata and trailing status codes.

If each skill constructed gRPC calls directly, the platform would suffer

- Duplicated channel and framing logic
- Inconsistent reuse of existing HTTP/2 and TLS handling
- Unbounded streaming and message sizes
- Divergent status mapping, governance, and evidence

The platform requires a single, canonical, implementation-independent gRPC
transport that reuses the existing HTTP and TLS shared skills.

---

# Decision

The platform SHALL provide a dedicated gRPC Client shared skill that centralizes
gRPC transport behind a stable interface.

The gRPC Client shared skill SHALL

- Establish HTTP/2 channels through the
  [HTTP Client](../../http-client/README.md)
- Secure channels through the [TLS Client](../../tls-client/README.md)
- Invoke unary and streaming methods with bounded messages
- Carry metadata and observe trailers
- Map gRPC status codes to canonical outcomes, preserving the status code
- Apply rate, retry, and proxy governance
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform gRPC transport exclusively through the
[gRPC Client Interface](../interface.md). The gRPC Client SHALL NOT interpret
message semantics or classify status codes as findings.

---

# Alternatives Considered

## Per-Skill gRPC Handling

Each skill could construct gRPC calls directly.

Rejected because it duplicates logic and fails to reuse existing HTTP/2 and TLS
handling.

## Reimplementing HTTP/2 And TLS Internally

gRPC could implement its own HTTP/2 and TLS.

Rejected because it would duplicate mature, governed handling already provided by
the HTTP and TLS shared skills.

## Interpreting Status Codes As Findings

The gRPC Client could classify non-`OK` statuses as findings.

Rejected because finding generation belongs to domain skills. The gRPC Client
preserves the status code as data for interpretation.

---

# Consequences

## Positive

- Uniform gRPC transport reusing HTTP/2 and TLS handling
- Bounded streaming and message sizes
- Consistent status mapping, governance, and evidence
- Reusable, testable abstraction independent of adapters

## Negative

- Consumers MUST perform gRPC through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by reuse and consistency.

---

# Compliance

Consumers SHALL

- Perform gRPC through the gRPC Client Interface
- Bound streaming message counts and sizes
- Set explicit deadlines
- Reference credentials rather than inlining metadata secrets
- Interpret status codes at the domain layer, not the transport layer

---

# Future Compatibility

Future versions MAY add reflection-based method discovery, compression
directives, and deadline propagation. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [gRPC Client README](../README.md)
- [gRPC Client Interface](../interface.md)
- [gRPC Client Execution Model](../execution.md)
- [gRPC Client Error Model](../error-model.md)
- [HTTP Client](../../http-client/README.md)
- [TLS Client](../../tls-client/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
