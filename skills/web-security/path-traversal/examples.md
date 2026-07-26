# Path Traversal Examples

**File:** `skills/web-security/path-traversal/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Path Traversal
Skill. Examples illustrate the interface and outputs; they contain no implementation
code.

---

# Example 1 — Traversal Confirmed With Non-Sensitive Marker

## Request

```yaml
target: https://app.example.com
marker_ref: benign-marker-resource
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-pt-5001
    title: Directory traversal in file parameter
    weakness: CWE-22
    risk_ref: risk-pt-3001
    evidence_refs:
      - evidence-pt-7001
observations:
  - id: obs-pt-4001
    kind: marker-read-analysis
evidence:
  - id: evidence-pt-7001
    observation_ref: obs-pt-4001
status: completed
metrics:
  path_parameters_tested: 4
  findings: 1
```

The `file` parameter permits traversal outside the intended base directory,
confirmed by reading a non-sensitive marker resource. No sensitive file is read.

---

# Example 2 — Encoded Traversal Bypass

## Request

```yaml
target: https://app.example.com
marker_ref: benign-marker-resource
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-pt-5002
    title: Encoded traversal bypasses input filtering
    weakness: CWE-22
    risk_ref: risk-pt-3002
    evidence_refs:
      - evidence-pt-7002
status: completed
metrics:
  path_parameters_tested: 4
  findings: 1
```

A double-encoded traversal sequence bypasses filtering and reaches the non-sensitive
marker, confirming insufficient canonicalization.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
marker_ref: benign-marker-resource
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: awaiting_approval
metrics:
  approvals_requested: 1
```

The Rules of Engagement require approval before active traversal probing; the skill
defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: denied
metrics:
  policy_denials: 1
```

The target is out of scope. The Policy Engine denies the action and no testing is
performed.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Asset Schema](../../../schemas/asset.md)
