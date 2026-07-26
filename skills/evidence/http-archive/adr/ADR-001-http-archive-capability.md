# ADR-001 — HTTP Archive Capability

**File:** `skills/evidence/http-archive/adr/ADR-001-http-archive-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments require durable HTTP evidence — request and response detail — for confirmation,
reporting, and reproducibility. HAR, HTTP archival, and response archival are the same collection
concern expressed in different serializations; modeling them as separate packages would create
format-only packages. Collecting HTTP evidence is an Evidence-tier collection capability distinct
from Active Testing's transient traffic recording, and it must not own the durable evidence
lifecycle.

---

# Decision

We SHALL provide an HTTP Archive Capability in the Evidence tier that consolidates HAR, HTTP
archival, and response archival. It collects transactions through the
[HTTP Client](../../../shared/http-client/README.md) and, where configured, the
[Proxy](../../../shared/proxy/README.md); gates every request through the
[Policy Engine](../../../shared/policy-engine/README.md); records transactions as
[Artifacts](../../../../schemas/artifact.md) referencing the
[HTTP Transaction](../../../../schemas/http-transaction.md) schema; invokes the shared
[Evidence](../../../shared/evidence/README.md) lifecycle to promote archives into durable Evidence;
and emits [Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and does not
own durable persistence, integrity, or retention.

---

# Consequences

## Positive

- One HTTP evidence capability rather than three format packages.
- Policy-gated, redacted, durable HTTP evidence referencing canonical schemas.

## Negative

- Archive fidelity depends on the shared HTTP Client and Proxy.

## Neutral

- Session-grouped and streaming archives are deferred to future extensions.

---

# Alternatives Considered

- Separate HAR, HTTP Archive, and Response Archive packages. Rejected as format-only packages.
- Reusing Active Testing's traffic-recording. Rejected because that capability is a transient
  producer, while HTTP Archive owns durable HTTP evidence collection.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Evidence](../../../shared/evidence/README.md)
