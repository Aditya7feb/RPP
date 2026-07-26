# ADR-001 — Screenshot Capture Capability

**File:** `skills/evidence/screenshot-capture/adr/ADR-001-screenshot-capture-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments require faithful visual evidence of rendered pages — for confirmation, reporting, and
reproducibility. Capturing rendered screenshots is a distinct collection capability that depends on
browser rendering and differs from HTTP or network capture. It is an Evidence-tier collection
capability, not a domain skill and not shared infrastructure, and it must not own the durable
evidence lifecycle.

---

# Decision

We SHALL provide a Screenshot Capture Capability in the Evidence tier that renders in-scope pages
through the [Browser](../../../shared/browser/README.md); gates every capture through the
[Policy Engine](../../../shared/policy-engine/README.md); records captures as
[Artifacts](../../../../schemas/artifact.md) of type `screenshot`; invokes the shared
[Evidence](../../../shared/evidence/README.md) lifecycle to promote captures into durable Evidence;
and emits [Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and does not
own durable persistence, integrity, or retention.

---

# Consequences

## Positive

- Faithful, policy-gated, redacted visual evidence with durability via the shared lifecycle.
- Clear separation of capture from interpretation and from the durable evidence lifecycle.

## Negative

- Capture fidelity depends on the shared Browser.

## Neutral

- Element-scoped and multi-viewport captures are deferred to future extensions.

---

# Alternatives Considered

- Rendering pages directly in the capability. Rejected because rendering belongs to the shared
  Browser.
- Owning durable persistence within the capability. Rejected because packaging, integrity, and
  retention are shared Evidence lifecycle mechanics.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Browser](../../../shared/browser/README.md)
- [Evidence](../../../shared/evidence/README.md)
