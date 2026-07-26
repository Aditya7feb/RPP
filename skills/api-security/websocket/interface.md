# WebSocket API Security Skill Interface

**File:** `skills/api-security/websocket/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the
WebSocket API Security Skill. The interface describes intent, not transport or
tooling.

---

# Interface Overview

The skill exposes a single logical operation, `assess`, that evaluates WebSocket
security for an in-scope API and returns Findings with Evidence references.

---

# Operation: assess

## Request

```yaml
assess:
  target:
  assets:
  identities_ref:
  allowed_origins_ref:
  scope_id:
  roe_id:
  options:
    check_origin_validation:
    check_handshake_authentication:
    check_message_authorization:
    check_transport:
    check_error_disclosure:
```

`target` SHALL be an in-scope WebSocket endpoint.

`assets` reference the `api` and `endpoint`
[Assets](../../../schemas/asset.md) under test.

`identities_ref` MAY reference two authorized controlled identities by reference only.

`allowed_origins_ref` MAY reference the set of legitimate Origins expected to be
accepted.

`options` toggle individual analyses. Omitted options SHALL default to the
configuration defaults.

## Response

```yaml
assess_result:
  target:
  findings:
  evidence_refs:
  observations:
  decision_summary:
```

`findings` reference [Finding](../../../schemas/finding.md) objects, each with
[Risk](../../../schemas/risk.md).

`evidence_refs` reference [Evidence](../../../schemas/evidence.md).

`decision_summary` summarizes Policy Engine decisions, including any deferred actions.

---

# Preconditions

- `target` SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.
- Where provided, `identities_ref` SHALL reference authorized controlled identities.

---

# Postconditions

- Every returned Finding SHALL reference supporting Evidence.
- No out-of-scope target SHALL have been contacted.
- Message exchanges SHALL have remained bounded.

---

# Error Semantics

Error categories and outcomes are defined in
[error-model.md](error-model.md). The interface SHALL surface deterministic outcomes
and SHALL NOT leak transport or tooling detail.

---

# Interface Stability

The `assess` operation is stable. Additional options MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields for
forward compatibility.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
