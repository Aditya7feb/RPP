# Container Client Examples

**File:** `skills/shared/container-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Container Client Shared
Skill. Examples illustrate the interface and outputs; they contain no implementation code and
report provider-native metadata as data.

---

# Example 1 — Inspect A Container (Read)

## Request

```yaml
engine_target:
  engine: local-engine
scope_ref:
  engines: [local-engine]
  containers: [app-web]
operation:
  kind: inspect
  resource_type: container
  selectors:
    name: app-web
  bounds:
    max_depth: 3
```

## Result

```yaml
operation_result:
  engine: local-engine
  resource_type: container
  item_count: 1
  config_observations:
    - privileged: true
      mounts:
        - source: /var/run/engine.sock
          target: /var/run/engine.sock
  outcome: completed
evidence_ref: evidence-container-9001
```

The client inspects the container and reports its privileged flag and mount configuration as
data. Whether these represent a weakness is left to the domain skill.

---

# Example 2 — List Images (Read)

## Request

```yaml
engine_target:
  engine: local-engine
scope_ref:
  engines: [local-engine]
operation:
  kind: list
  resource_type: image
  bounds:
    max_items: 100
```

## Result

```yaml
operation_result:
  engine: local-engine
  resource_type: image
  item_count: 27
  outcome: completed
evidence_ref: evidence-container-9002
```

The client lists images within bounds and reports them by reference.

---

# Example 3 — Exec Requires Elevated Authorization

## Request

```yaml
engine_target:
  engine: local-engine
scope_ref:
  engines: [local-engine]
  containers: [app-web]
operation:
  kind: exec
  resource_type: container
  selectors:
    name: app-web
```

## Result

```yaml
operation_result:
  engine: local-engine
  resource_type: container
  outcome: awaiting_approval
evidence_ref: evidence-container-9003
```

The exec operation executes a workload and is deferred pending elevated authorization from
the Policy Engine.

---

# Example 4 — Out Of Scope Rejected

## Request

```yaml
engine_target:
  engine: remote-engine
scope_ref:
  engines: [local-engine]
operation:
  kind: list
  resource_type: container
```

## Result

```yaml
operation_result:
  engine: remote-engine
  resource_type: container
  outcome: rejected
evidence_ref: evidence-container-9004
```

The target engine is outside authorized scope, so the operation is rejected before any
request.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
