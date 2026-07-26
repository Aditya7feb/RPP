# Payload Generation Capabilities

**File:** `skills/active-testing/payload-generation/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Payload Generation Capability. Each
capability is deterministic, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| PG-1 | Template composition | template_ref | Composed Payloads |
| PG-2 | Seed composition | seeds | Seeded Payloads |
| PG-3 | Variant composition | mutation | Variant Payloads |
| PG-4 | Encoding | encoding | Encoded Payloads |
| PG-5 | Safety marking | payloads | Safety markers |
| PG-6 | Metrics emission | run | Metrics |

---

# PG-1 — Template Composition

The capability SHALL compose [Payloads](../../../schemas/payload.md) from a resolved template
and variable bindings.

---

# PG-2 — Seed Composition

The capability SHALL draw candidate values from [Wordlists](../wordlists/README.md) and bind
them into Payloads.

---

# PG-3 — Variant Composition

The capability SHALL derive variants through the
[Mutation Engine](../mutation-engine/README.md), preserving lineage.

---

# PG-4 — Encoding

The capability SHALL apply the requested `encoding` and record it in
`classification.encoding`.

---

# PG-5 — Safety Marking

The capability SHALL set `safety.non_destructive` and `safety.requires_approval`
appropriately, referencing markers and out-of-band values rather than inlining them.

---

# PG-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing generation counts.

---

# Capability Boundaries

The capability SHALL NOT contact targets, deliver payloads, interpret results, or produce
Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
