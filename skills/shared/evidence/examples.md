# Evidence Examples

**File:** `skills/shared/evidence/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Evidence Shared Skill in use.

Examples demonstrate consumers, capture, artifact storage, redaction, sealing,
scope, resolution, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Capturing An HTTP Transaction

The HTTP Client captures a transaction as evidence.

## Capture Request

```yaml
type: http-transaction
inputs:
  method: GET
  url: https://app.example.com/robots.txt
outputs:
  status_code: 200
metadata:
  duration_ms: 118
scope: assessment
artifacts:
  - name: response-body
    content_type: text/plain
    content_ref: staging://http/req-4001-body
    size_bytes: 342
```

## Capture Result

```yaml
outcome: captured
evidence_ref: evidence-http-4001
integrity:
  digest: sha-256:1a2b3c...
redaction:
  applied: false
  fields: []
```

The response body is stored as an artifact by reference and the record is
sealed.

---

# Example 2 — Automatic Redaction

A captured request contains an authorization header.

## Capture Request

```yaml
type: http-transaction
inputs:
  method: POST
  url: https://api.example.com/login
  headers:
    authorization: "Bearer eyJ..."
outputs:
  status_code: 200
scope: session
```

## Capture Result

```yaml
outcome: captured
evidence_ref: evidence-http-4002
redaction:
  applied: true
  fields:
    - inputs.headers.authorization
```

The secret is redacted before persistence; only the redaction record remains.

---

# Example 3 — Integrity Sealing And Verification

A sealed record is later resolved and verified.

## Resolution Request

```yaml
evidence_ref: evidence-http-4001
scope: assessment
```

## Resolution Result

```yaml
outcome: resolved
evidence:
  type: http-transaction
  integrity:
    verified: true
```

The integrity seal is verified before the evidence is returned.

---

# Example 4 — Tamper Detection

A stored record has been altered outside the platform.

## Resolution Result

```yaml
outcome: error
error:
  category: Integrity
  code: tamper_detected
  evidence_ref: evidence-http-4001
  retryable: false
```

The evidence is not returned as valid; the integrity error is preserved for
audit.

---

# Example 5 — Scope Isolation

Evidence captured in one assessment is not resolvable in another.

## Configuration

```yaml
scope_policy:
  allow_cross_assessment: false
```

## Cross-Assessment Resolution

```yaml
outcome: out_of_scope
```

Scope isolation prevents cross-assessment leakage.

---

# Example 6 — Correlation With Findings And Logs

A finding, a log event, and a report all reference the same evidence.

```
evidence-http-4001

├── referenced by finding-xss-0007
├── referenced by log-000123
└── referenced by report section 4.2
```

Correlation is achieved through the stable evidence reference rather than
duplication.

---

# Example 7 — Retention And Disposal

Evidence exceeding retention is disposed of with an audit record.

## Result

```yaml
event: EvidenceDisposed
evidence_ref: evidence-http-4001
dispose_policy: archive
disposal_recorded: true
```

Disposal preserves an audit record even after the evidence is archived.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Logging](../logging/README.md)
- [Reporting](../reporting/README.md)
