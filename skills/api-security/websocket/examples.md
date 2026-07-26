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
target: wss://api.example.com/socket
assets:
  - asset-api-3101
  - asset-endpoint-3102
allowed_origins_ref: ws-allowed-origins
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ws-5001
    title: WebSocket handshake accepts foreign Origin (CSWSH)
    weakness: CWE-1385
    owasp_api: API2:2023 - Broken Authentication
    risk_ref: risk-ws-3001
    evidence_refs:
      - evidence-ws-7001
observations:
  - id: obs-ws-4001
    kind: origin-validation-analysis
evidence:
  - id: evidence-ws-7001
    observation_ref: obs-ws-4001
status: completed
metrics:
  handshakes_tested: 4
  findings: 1
```

A single controlled foreign Origin is accepted at the handshake, confirming missing
Origin validation (CWE-1385, a specialization of CWE-346). No session data is read.

---

# Example 2 — Unauthenticated Handshake

## Request

```yaml
target: wss://api.example.com/socket
assets:
  - asset-endpoint-3102
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ws-5002
    title: WebSocket handshake accepted without authentication
    weakness: CWE-306
    owasp_api: API2:2023 - Broken Authentication
    risk_ref: risk-ws-3002
    evidence_refs:
      - evidence-ws-7002
observations:
  - id: obs-ws-4002
    kind: handshake-authentication-analysis
evidence:
  - id: evidence-ws-7002
    observation_ref: obs-ws-4002
status: completed
metrics:
  handshakes_tested: 4
  findings: 1
```

The handshake is accepted without valid credentials, confirming missing handshake
authentication.

---

# Example 3 — Missing Message-Level Authorization

## Request

```yaml
target: wss://api.example.com/socket
assets:
  - asset-api-3101
identities_ref: ws-test-identities
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ws-5003
    title: Low-privilege identity receives messages for another principal
    weakness: CWE-285
    owasp_api: API1:2023 - Broken Object Level Authorization
    risk_ref: risk-ws-3003
    evidence_refs:
      - evidence-ws-7003
observations:
  - id: obs-ws-4003
    kind: message-authorization-analysis
evidence:
  - id: evidence-ws-7003
    observation_ref: obs-ws-4003
status: completed
metrics:
  messages_tested: 5
  findings: 1
```

A single controlled subscription with the low-privilege identity receives another
principal's messages, confirming missing message-level authorization. No further data
is enumerated.

---

# Example 4 — Cleartext Transport

## Request

```yaml
target: ws://api.example.com/socket
assets:
  - asset-endpoint-3102
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-ws-5004
    title: WebSocket connection established over cleartext transport
    weakness: CWE-319
    owasp_api: API8:2023 - Security Misconfiguration
    risk_ref: risk-ws-3004
    evidence_refs:
      - evidence-ws-7004
status: completed
metrics:
  handshakes_tested: 1
  findings: 1
```

The connection is established over cleartext transport, indicating the API does not
enforce a secure channel.

---

# Example 5 — Requires Approval

## Request

```yaml
target: wss://api.example.com/socket
assets:
  - asset-api-3101
identities_ref: ws-test-identities
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

The Rules of Engagement require approval before active message-level authorization
testing; the skill defers until approval is granted.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
