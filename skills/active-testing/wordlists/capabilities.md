# Wordlists Capabilities

**File:** `skills/active-testing/wordlists/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Wordlists Capability. Each capability is
data-serving, bounded, and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| WL-1 | List registry | list_name | Registered list reference |
| WL-2 | Selection and filtering | filter | Filtered entries |
| WL-3 | Bounded sampling | max_entries | Bounded entry set |
| WL-4 | Artifact emission | selection | Artifact reference |
| WL-5 | Seed emission | selection | Payload seeds |
| WL-6 | Metrics emission | selection | Metrics |

---

# WL-1 — List Registry

The capability SHALL register named, versioned lists and resolve a `list_name` to a
specific list version.

---

# WL-2 — Selection And Filtering

The capability SHALL select entries by filter criteria such as prefix, length, or category.

---

# WL-3 — Bounded Sampling

The capability SHALL return at most `max_entries` entries, sampling deterministically given
the same inputs.

---

# WL-4 — Artifact Emission

The capability SHALL emit selected content by reference as an
[Artifact](../../../schemas/artifact.md).

---

# WL-5 — Seed Emission

The capability SHALL emit candidate values as [Payload](../../../schemas/payload.md) seeds
where requested, with `lineage.source` set to `wordlist`.

---

# WL-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing selection counts
and sampling ratios.

---

# Capability Boundaries

The capability SHALL NOT contact targets, shape or mutate payloads, interpret results, or
produce Findings or Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface
operations in [interface.md](interface.md).
