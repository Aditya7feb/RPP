# Unrestricted File Upload Examples

**File:** `skills/web-security/file-upload/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Unrestricted
File Upload Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Dangerous Type Accepted

## Request

```yaml
target: https://app.example.com
marker_set_ref: upload-inert-markers
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-fu-5001
    title: Dangerous file type accepted with extension-only validation
    weakness: CWE-434
    risk_ref: risk-fu-3001
    evidence_refs:
      - evidence-fu-7001
observations:
  - id: obs-fu-4001
    kind: type-validation-analysis
evidence:
  - id: evidence-fu-7001
    observation_ref: obs-fu-4001
status: completed
metrics:
  upload_endpoints_tested: 2
  findings: 1
```

The upload endpoint accepts an inert marker with a dangerous extension, validating
only the extension. No functional payload is uploaded.

---

# Example 2 — Web-Accessible Storage

## Request

```yaml
target: https://app.example.com
marker_set_ref: upload-inert-markers
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-fu-5002
    title: Uploaded content stored in a web-accessible location
    weakness: CWE-434
    risk_ref: risk-fu-3002
    evidence_refs:
      - evidence-fu-7002
status: completed
metrics:
  upload_endpoints_tested: 2
  findings: 1
```

An inert marker is retrievable from a predictable web-accessible path, indicating
unsafe storage. No executable content is uploaded.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
marker_set_ref: upload-inert-markers
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

Upload testing is higher impact; the Rules of Engagement require approval, so the
skill defers until approval is granted.

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
