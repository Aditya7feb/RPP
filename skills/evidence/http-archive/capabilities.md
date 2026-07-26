# HTTP Archive Capabilities

**File:** `skills/evidence/http-archive/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the HTTP Archive Capability. Each capability is
scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| HA-1 | Policy consultation | request | Decision |
| HA-2 | Transaction collection | selection | HTTP transactions |
| HA-3 | Redaction | transactions | Redacted transactions |
| HA-4 | Archive writing | transactions | Artifact |
| HA-5 | Evidence promotion | artifact | Evidence reference |
| HA-6 | Metrics emission | run | Metrics |

---

# HA-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) before every
request.

---

# HA-2 — Transaction Collection

The capability SHALL collect HTTP transactions through the
[HTTP Client](../../shared/http-client/README.md) and, where configured, the
[Proxy](../../shared/proxy/README.md), bounded by volume.

---

# HA-3 — Redaction

The capability SHALL redact sensitive request and response content before storage.

---

# HA-4 — Archive Writing

The capability SHALL record transactions as [Artifacts](../../../schemas/artifact.md) of type
`http-archive` referencing the [HTTP Transaction](../../../schemas/http-transaction.md) schema.

---

# HA-5 — Evidence Promotion

The capability SHALL invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to
promote archives into durable Evidence. The capability invokes promotion but does not own its
implementation.

---

# HA-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing archived transaction
counts.

---

# Capability Boundaries

The capability SHALL NOT issue requests directly, interpret transactions, own durable persistence,
or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
