# Parameter Mining Capabilities

**File:** `skills/active-testing/parameter-mining/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Parameter Mining Capability. Each capability
is scope-confined, policy-gated, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| PM-1 | Policy consultation | request | Decision |
| PM-2 | Candidate sourcing | candidate_source | Candidate names |
| PM-3 | Location probing | locations | Probe interactions |
| PM-4 | Acceptance detection | responses | Observations |
| PM-5 | Artifact emission | interactions | Artifacts |
| PM-6 | Metrics emission | run | Metrics |

---

# PM-1 — Policy Consultation

The capability SHALL consult the [Policy Engine](../../shared/policy-engine/README.md) before
every request.

---

# PM-2 — Candidate Sourcing

The capability SHALL draw bounded candidate parameter names from
[Wordlists](../wordlists/README.md).

---

# PM-3 — Location Probing

The capability SHALL probe candidates across query, body, header, and cookie locations through
the [HTTP Client](../../shared/http-client/README.md), non-destructively and within bounds.

---

# PM-4 — Acceptance Detection

The capability SHALL detect accepted, reflected, or behavior-changing parameters and record
them as [Observations](../../../schemas/observation.md).

---

# PM-5 — Artifact Emission

The capability SHALL capture probe interactions as [Artifacts](../../../schemas/artifact.md).

---

# PM-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing coverage and
request counts.

---

# Capability Boundaries

The capability SHALL NOT interpret parameters as vulnerabilities, test weaknesses, perform
destructive probing, or produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
