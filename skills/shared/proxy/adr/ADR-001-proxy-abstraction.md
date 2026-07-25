# ADR-001 — Proxy Abstraction

**File:** `skills/shared/proxy/adr/ADR-001-proxy-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform frequently operates in environments that require or
benefit from routing outbound traffic through intermediaries, including
corporate forwarding proxies, testing interception proxies, and SOCKS gateways.
Proxy handling intersects with several concerns:

- Correct selection and bypass for each destination
- Secure handling of proxy credentials
- Accurate TLS validation in the presence of interception
- Rules of Engagement constraints on egress

Before this decision, proxy handling could be implemented independently inside
each shared network package. That approach produced

- Inconsistent selection and bypass behavior
- Duplicated and divergent tunnel logic
- Risk of credential leakage in per-package implementations
- Interception boundaries that were invisible to the TLS Client, producing
  spurious certificate findings
- No central place to enforce egress governance

The platform requires a single, canonical, implementation-independent mechanism
to route outbound operations.

---

# Decision

The platform SHALL provide a dedicated Proxy shared skill that centralizes all
outbound routing decisions behind a stable interface.

The Proxy shared skill SHALL

- Resolve a canonical
  [Proxy Configuration](../../../../schemas/proxy-configuration.md)
- Evaluate selection and bypass rules for each destination
- Establish tunnels through supported proxy protocols
- Resolve proxy credentials through the
  [Authentication](../../authentication/README.md) shared package without
  exposing secrets
- Inform the [TLS Client](../../tls-client/README.md) of interception
  boundaries
- Enforce egress governance and Rules of Engagement
- Emit evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL route outbound operations exclusively through the
[Proxy Interface](../interface.md) by supplying an execution callback bound to
the routed channel. The Proxy shared skill SHALL remain unaware of the operation
implementation.

---

# Alternatives Considered

## Per-Package Proxy Handling

Each network package could implement its own proxy support.

Rejected because it duplicates logic, risks credential leakage, and makes
egress governance and interception awareness impossible to enforce centrally.

## Transport-Level Proxy Only

Proxy handling could be delegated to individual transport adapters.

Rejected because it ties proxy policy to specific implementations, prevents
cross-transport consistency, and hides interception boundaries from the TLS
Client.

## Folding Proxy Into The HTTP Client

Proxy logic could live inside the HTTP Client.

Rejected because non-HTTP operations such as TLS handshakes and DNS queries also
require routing. Proxy handling is a cross-cutting concern and belongs in a
dedicated shared skill.

---

# Consequences

## Positive

- Uniform selection and bypass behavior across every network package
- Central, auditable enforcement of egress governance
- Secure, centralized proxy credential handling
- Accurate TLS findings through interception awareness
- Reusable, testable abstraction independent of transport

## Negative

- Consumers MUST route outbound operations through the interface
- An additional shared dependency is introduced
- Proxy chaining, if later required, adds complexity

The negative consequences are outweighed by the safety, accuracy, and
consistency benefits.

---

# Compliance

Consumers SHALL

- Route outbound operations through the Proxy Interface
- Reference shared proxy configurations rather than inlining values
- Never embed proxy credentials in configuration
- Honor interception awareness when validating certificates

Shared network packages SHALL depend on the Proxy shared skill and SHALL NOT
implement independent tunnel logic.

---

# Future Compatibility

Future versions MAY introduce proxy chaining, health-aware proxy pools, and
dynamic selection rule sets. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Proxy README](../README.md)
- [Proxy Interface](../interface.md)
- [Proxy Execution Model](../execution.md)
- [Proxy Error Model](../error-model.md)
- [Authentication](../../authentication/README.md)
- [TLS Client](../../tls-client/README.md)
- [Proxy Configuration Schema](../../../../schemas/proxy-configuration.md)
- [Evidence Schema](../../../../schemas/evidence.md)
