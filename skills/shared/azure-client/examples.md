# Azure Client Examples

**File:** `skills/shared/azure-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Azure Client Shared
Skill. Examples illustrate the interface and outputs; they contain no implementation code
and report provider-native metadata as data.

---

# Example 1 — List Role Assignments (Read)

## Request

```yaml
service_target:
  subscription: 00000000-0000-0000-0000-000000000000
  resource_group: rg-app
  region: eastus
  service: authorization
scope_ref:
  subscriptions: ["00000000-0000-0000-0000-000000000000"]
  resource_groups: [rg-app]
  regions: [eastus]
  services: [authorization]
operation:
  kind: list
  resource_type: role-assignment
  pagination:
    max_items: 200
    max_pages: 5
```

## Result

```yaml
operation_result:
  service: authorization
  resource_type: role-assignment
  item_count: 18
  role_observations:
    - principal: sp/app-runtime
      role: Contributor
      scope: /subscriptions/.../resourceGroups/rg-app
  outcome: completed
evidence_ref: evidence-azure-9001
```

The client lists role assignments within bounds and reports them as data. Whether the
Contributor assignment is over-permissive is left to the domain skill.

---

# Example 2 — Observe Instance Metadata Service (Read)

## Request

```yaml
service_target:
  subscription: 00000000-0000-0000-0000-000000000000
  resource_group: rg-app
  region: eastus
  service: imds
operation:
  kind: get
  resource_type: instance-metadata
```

## Result

```yaml
operation_result:
  service: imds
  resource_type: instance-metadata
  metadata_observations:
    - endpoint_reachable: true
      identity_endpoint_present: true
  outcome: completed
evidence_ref: evidence-azure-9002
```

The client reports IMDS reachability and identity-endpoint presence as data.

---

# Example 3 — Mutation Requires Approval

## Request

```yaml
service_target:
  subscription: 00000000-0000-0000-0000-000000000000
  resource_group: rg-app
  region: eastus
  service: network
operation:
  kind: update
  resource_type: network-security-group
  selectors:
    name: nsg-app
```

## Result

```yaml
operation_result:
  service: network
  resource_type: network-security-group
  outcome: awaiting_approval
evidence_ref: evidence-azure-9003
```

The mutation is gated by the Policy Engine and deferred until approval is granted.

---

# Example 4 — Out Of Scope Rejected

## Request

```yaml
service_target:
  subscription: ffffffff-ffff-ffff-ffff-ffffffffffff
  resource_group: rg-other
  region: westus
  service: storage
scope_ref:
  subscriptions: ["00000000-0000-0000-0000-000000000000"]
  resource_groups: [rg-app]
  regions: [eastus]
  services: [authorization, network]
operation:
  kind: list
  resource_type: storage-account
```

## Result

```yaml
operation_result:
  service: storage
  resource_type: storage-account
  outcome: rejected
evidence_ref: evidence-azure-9004
```

The target subscription, resource group, region, and service are outside authorized scope,
so the operation is rejected before any request.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
