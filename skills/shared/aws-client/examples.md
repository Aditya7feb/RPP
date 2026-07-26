# AWS Client Examples

**File:** `skills/shared/aws-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the AWS Client Shared
Skill. Examples illustrate the interface and outputs; they contain no implementation
code and report provider-native metadata as data.

---

# Example 1 — Describe IAM Policies (Read)

## Request

```yaml
service_target:
  account: "111122223333"
  region: us-east-1
  service: iam
scope_ref:
  accounts: ["111122223333"]
  regions: [us-east-1]
  services: [iam]
operation:
  kind: list
  resource_type: policy
  pagination:
    max_items: 200
    max_pages: 5
```

## Result

```yaml
operation_result:
  service: iam
  resource_type: policy
  item_count: 42
  iam_observations:
    - principal: role/app-runtime
      attached_policies: 3
  outcome: completed
evidence_ref: evidence-aws-9001
```

The client lists IAM policies within bounds and reports attachment metadata as data.
Whether any policy is over-permissive is left to the domain skill.

---

# Example 2 — Observe Instance Metadata Service (Read)

## Request

```yaml
service_target:
  account: "111122223333"
  region: us-east-1
  service: ec2-imds
operation:
  kind: get
  resource_type: instance-metadata
```

## Result

```yaml
operation_result:
  service: ec2-imds
  resource_type: instance-metadata
  metadata_observations:
    - endpoint_reachable: true
      imds_version_observed: v2
  outcome: completed
evidence_ref: evidence-aws-9002
```

The client reports IMDS reachability and observed version as data.

---

# Example 3 — Mutation Requires Approval

## Request

```yaml
service_target:
  account: "111122223333"
  region: us-east-1
  service: ec2
operation:
  kind: update
  resource_type: security-group
  selectors:
    group_id: sg-0abc123
```

## Result

```yaml
operation_result:
  service: ec2
  resource_type: security-group
  outcome: awaiting_approval
evidence_ref: evidence-aws-9003
```

The mutation is gated by the Policy Engine and deferred until approval is granted.

---

# Example 4 — Out Of Scope Rejected

## Request

```yaml
service_target:
  account: "999988887777"
  region: eu-west-1
  service: s3
scope_ref:
  accounts: ["111122223333"]
  regions: [us-east-1]
  services: [iam, ec2]
operation:
  kind: list
  resource_type: bucket
```

## Result

```yaml
operation_result:
  service: s3
  resource_type: bucket
  outcome: rejected
evidence_ref: evidence-aws-9004
```

The target account, region, and service are outside authorized scope, so the operation
is rejected before any request.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
