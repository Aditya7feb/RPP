# Mutation Engine Capabilities

**File:** `skills/active-testing/mutation-engine/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Mutation Engine Capability. Each capability
is deterministic, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| ME-1 | Strategy registry | strategies | Resolved strategies |
| ME-2 | Mutation application | base_payload_ref | Derived Payloads |
| ME-3 | Lineage recording | derived payloads | Lineage metadata |
| ME-4 | Safety preservation | derived payloads | Safety markers |
| ME-5 | Metrics emission | run | Metrics |

---

# ME-1 — Strategy Registry

The capability SHALL register named, deterministic mutation strategies such as encoding,
case, boundary, structural, and marker insertion.

---

# ME-2 — Mutation Application

The capability SHALL apply the requested strategies to the base input, producing at most
`max_variants` derived [Payloads](../../../schemas/payload.md).

---

# ME-3 — Lineage Recording

The capability SHALL set `lineage.source` to `mutated`, `lineage.base_payload_id`, and
`lineage.mutation_ref` on each derived Payload.

---

# ME-4 — Safety Preservation

The capability SHALL preserve `safety.non_destructive` and set `safety.requires_approval`
where a mutation could alter target state.

---

# ME-5 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing variant counts by
strategy.

---

# Capability Boundaries

The capability SHALL NOT contact targets, deliver payloads, interpret results, or produce
Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
