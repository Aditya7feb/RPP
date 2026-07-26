# WebSocket API Security Skill Examples

**File:** `skills/api-security/websocket/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the WebSocket API
Security Skill. Identifiers are stable and illustrative.

---

# Example 1 — Missing Origin Validation (CSWSH)

## Request

```yaml
assess:
  target: wss://api.example.com/socket
  assets:
    - asset-api-3101
    - asset-endpoint-3102
  allowed_origins_ref: origins-set-2301
  scope_id: scope-2301
  roe_id: roe-2301
  options:
    check_origin_validation: true
```

## Result

```yaml
assess_result:
  target: wss://api.example.com/socket
  findings:
    - finding-ws-4101
  evidence_refs:
    - evidence-ws-5101
  decision_summary:
    allow: 2
    denied: 0
```

## Finding

```yaml
finding-ws-4101:
  weakness: CWE-346
  owasp_api: "API2:2023 - Broken Authentication"
  title: WebSocket handshake accepts foreign Origin (CSWSH)
  asset: asset-api-3101
  risk:
    severity: high
  evidence:
    - evidence-ws-5101
  notes: >
    Confirmed with a single controlled foreign Origin. No session data was read.
```

---

# Example 2 — Unauthenticated Handshake

## Request

```yaml
assess:
  target: wss://api.example.com/socket
  assets:
    - asset-endpoint-3102
  scope_id: scope-2301
  roe_id: roe-2301
  options:
    check_handshake_authentication: true
```

## Result

```yaml
assess_result:
  target: wss://api.example.com/socket
  findings:
    - finding-ws-4102
  evidence_refs:
    - evidence-ws-5102
  decision_summary:
    allow: 1
    denied: 0
```

## Finding

```yaml
finding-ws-4102:
  weakness: CWE-306
  owasp_api: "API2:2023 - Broken Authentication"
  title: WebSocket handshake accepted without authentication
  asset: asset-endpoint-3102
  risk:
    severity: high
  evidence:
    - evidence-ws-5102
```

---

# Example 3 — Missing Message-Level Authorization

## Request

```yaml
assess:
  target: wss://api.example.com/socket
  assets:
    - asset-api-3101
  identities_ref: identities-set-2301
  scope_id: scope-2301
  roe_id: roe-2301
  options:
    check_message_authorization: true
```

## Result

```yaml
assess_result:
  target: wss://api.example.com/socket
  findings:
    - finding-ws-4103
  evidence_refs:
    - evidence-ws-5103
  decision_summary:
    allow: 3
    denied: 0
```

## Finding

```yaml
finding-ws-4103:
  weakness: CWE-285
  owasp_api: "API1:2023 - Broken Object Level Authorization"
  title: Low-privilege identity receives messages for another principal
  asset: asset-api-3101
  risk:
    severity: high
  evidence:
    - evidence-ws-5103
  notes: >
    Confirmed with a single controlled subscription. No further data was
    enumerated.
```

---

# Example 4 — Cleartext Transport

## Result

```yaml
assess_result:
  target: ws://api.example.com/socket
  findings:
    - finding-ws-4104
  evidence_refs:
    - evidence-ws-5104
  decision_summary:
    allow: 1
    denied: 0
```

## Finding

```yaml
finding-ws-4104:
  weakness: CWE-319
  owasp_api: "API8:2023 - Security Misconfiguration"
  title: WebSocket connection established over cleartext transport
  asset: asset-endpoint-3102
  risk:
    severity: medium
  evidence:
    - evidence-ws-5104
```

---

# Example 5 — Deferred For Approval

## Result

```yaml
assess_result:
  target: wss://api.example.com/socket
  findings: []
  evidence_refs:
    - evidence-ws-5105
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

Message authorization testing required approval and was deferred rather than executed.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
