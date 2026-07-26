# GCP Client Examples

**File:** `skills/shared/gcp-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the GCP Client Shared
Skill. Examples illustrate the interface and outputs; they contain no implementation code
and report provider-native metadata as data.

---

# Example 1 — Get IAM Policy (Read)

## Request

```yaml
service_target:
  organization: "1234567890"
  project: app-prod
  region: us-central1
  service: iam
scope_ref:
  organizations: ["1234567890"]
  projects: [app-prod]
  regions: [us-central1]
  services: [iam]
operation:
  kind: get
  resource_type: iam-policy
  selectors:
    resource: projects/app-prod
```

## Result

```yaml
operation_result:
  service: iam
  resource_type: iam-policy
  item_count: 1
  iam_observations:
    - member: serviceAccount:app-runtime@app-prod.iam.gserviceaccount.com
      role: roles/editor
  outcome: completed
evidence_ref: evidence-gcp-9001
```

The client gets the project IAM policy and reports bindings as data. Whether the editor
role is over-permissive is left to the domain skill.

---

# Example 2 — Observe Metadata Server (Read)

## Request

```yaml
service_target:
  organization: "1234567890"
  project: app-prod
  region: us-central1
  service: metadata-server
operation:
  kind: get
  resource_type: instance-metadata
```

## Result

```yaml
operation_result:
  service: metadata-server
  resource_type: instance-metadata
  metadata_observations:
    - endpoint_reachable: true
      default_service_account_present: true
  outcome: completed
evidence_ref: evidence-gcp-9002
```

The client reports metadata server reachability and default-service-account presence as
data.

---

# Example 3 — Mutation Requires Approval

## Request

```yaml
service_target:
  organization: "1234567890"
  project: app-prod
  region: us-central1
  service: compute
operation:
  kind: update
  resource_type: firewall
  selectors:
    name: allow-app
```

## Result

```yaml
operation_result:
  service: compute
  resource_type: firewall
  outcome: awaiting_approval
evidence_ref: evidence-gcp-9003
```

The mutation is gated by the Policy Engine and deferred until approval is granted.

---

# Example 4 — Out Of Scope Rejected

## Request

```yaml
service_target:
  organization: "1234567890"
  project: other-project
  region: europe-west1
  service: storage
scope_ref:
  organizations: ["1234567890"]
  projects: [app-prod]
  regions: [us-central1]
  services: [iam, compute]
operation:
  kind: list
  resource_type: bucket
```

## Result

```yaml
operation_result:
  service: storage
  resource_type: bucket
  outcome: rejected
evidence_ref: evidence-gcp-9004
```

The target project, region, and service are outside authorized scope, so the operation is
rejected before any request.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
