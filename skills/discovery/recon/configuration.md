# Recon Configuration

**File:** `skills/discovery/recon/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Recon Skill and the
precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
recon:

  profile:
    name:
    include_skills:
    exclude_skills:

  phases:
    passive:
      skills:
    active:
      skills:
      require_approval:

  execution:
    stop_on_denied_phase:
    continue_on_step_error:

  consolidation:
    run_asset_discovery:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Profile

- `name` — the reconnaissance profile identifier.
- `include_skills` — Discovery skills to compose. Each SHALL be an existing
  Discovery skill.
- `exclude_skills` — Discovery skills to omit from the selected profile.

---

## Phases

- `passive.skills` — the ordered passive Discovery skills (for example, DNS
  Enumeration, Subdomain Discovery, passive Fingerprinting).
- `active.skills` — the ordered active Discovery skills (for example, Port
  Discovery, TLS Analysis, Content Discovery, Virtual Host Discovery, API
  Discovery, Endpoint Enumeration).
- `active.require_approval` — whether active phases require an approval gate.
  Default `true` and SHALL NOT be disabled in enforcing environments.

---

## Execution

- `stop_on_denied_phase` — whether a denied phase halts the workflow. Default
  `true`.
- `continue_on_step_error` — whether a failed skill step allows the workflow to
  continue with remaining steps. Default `true`.

---

## Consolidation

- `run_asset_discovery` — whether [Asset Discovery](../asset-discovery/README.md)
  is invoked to consolidate the graph. Default `true` and SHALL NOT be disabled.

---

## Policy

- `scope_id` — the [Scope](../../../schemas/scope.md) reference.
- `roe_id` — the [Rules of Engagement](../../../schemas/rules-of-engagement.md)
  reference.

---

# Precedence

Configuration resolves in the following order, later overriding earlier, except
that policy and approval constraints SHALL NOT be weakened:

```
Skill Defaults

↓

Profile

↓

Assessment Configuration

↓

Request Parameters

↓

Policy Engine Decisions (highest; approvals may only tighten)
```

The [Policy Engine](../../shared/policy-engine/README.md) phase decisions and the
active-phase approval gate SHALL always take precedence.

---

# Validation Rules

- `scope_id` and `roe_id` SHALL be present.
- Every referenced skill SHALL be an existing Discovery skill.
- `active.require_approval` SHALL NOT be disabled in enforcing environments.
- `run_asset_discovery` SHALL NOT be disabled.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
- [Scope Schema](../../../schemas/scope.md)
