# API Security Capability Tier

**File:** `skills/api-security/README.md`

**Version:** 1.0.0

---

# Purpose

The API Security tier provides reusable, implementation-independent capabilities
that analyze the security of API surfaces within the Robust PenTest Platform
(RPP). These capabilities produce Observations, Findings, and Evidence references
across multiple API protocols.

This tier comprises the following capabilities.

- [REST](rest/README.md)
- [GraphQL](graphql/README.md)
- [SOAP](soap/README.md)
- [gRPC](grpc/README.md)
- [WebSocket](websocket/README.md)

---

# Ownership Boundary

API Security capabilities identify weaknesses and produce Findings and Evidence
references. State-changing validation is owned by the Active Testing tier and
requires human approval; it is not performed by this tier unbidden.

---

# Role in the Canonical Pipeline

API Security capabilities contribute Observations, Evidence, and Findings to the
pipeline **Observation → Evidence → Finding → Risk → Recommendation**.

---

# Canonical Schemas

API Security capabilities consume and produce
[observation](../../schemas/observation.md),
[finding](../../schemas/finding.md),
[evidence](../../schemas/evidence.md), and
[http-transaction](../../schemas/http-transaction.md), and reference
[scope](../../schemas/scope.md) and
[rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- Orchestrated by the [API Security Agent](../../agents/api-security/README.md).
- Shared infrastructure under [skills/shared](../shared/README.md).
