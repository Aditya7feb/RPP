# WebSocket API Security Skill Capabilities

**File:** `skills/api-security/websocket/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the WebSocket API Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| WS-1 | Origin validation analysis | endpoint, allowed_origins_ref | CSWSH Findings |
| WS-2 | Handshake authentication analysis | endpoint | Authentication Findings |
| WS-3 | Message authorization analysis | api, identities_ref | Authorization Findings |
| WS-4 | Transport security analysis | endpoint | Transport Findings |
| WS-5 | Error and close-frame disclosure analysis | endpoint | Disclosure Findings |
| WS-6 | Evidence recording | Observations | Evidence references |

---

# WS-1 — Origin Validation Analysis

The skill SHALL evaluate whether the WebSocket handshake validates the Origin header.
A handshake accepted with an unexpected or foreign Origin indicates susceptibility to
Cross-Site WebSocket Hijacking (CSWSH). The skill SHALL classify confirmed missing
validation as CWE-346 and reference OWASP API2:2023 – Broken Authentication.

---

# WS-2 — Handshake Authentication Analysis

The skill SHALL evaluate whether the WebSocket handshake requires authentication. A
handshake accepted without valid credentials SHALL be classified as CWE-306 and
reference OWASP API2:2023 – Broken Authentication.

---

# WS-3 — Message Authorization Analysis

The skill SHALL evaluate whether message-level authorization is enforced by exchanging
bounded messages across two controlled identities. Missing enforcement SHALL be
classified as CWE-285 and reference OWASP API1:2023 or API5:2023 as applicable.
Confirmation SHALL be minimal and SHALL NOT enumerate other principals' data.

---

# WS-4 — Transport Security Analysis

The skill SHALL evaluate whether the connection uses secure transport (`wss://`). A
connection established over cleartext (`ws://`) SHALL be classified as CWE-319.
General TLS posture is delegated to TLS Analysis.

---

# WS-5 — Error And Close-Frame Disclosure Analysis

The skill SHALL evaluate whether error frames or close-frame reasons disclose
implementation information such as stack traces or internal identifiers. Confirmed
disclosure SHALL be classified as CWE-209.

---

# WS-6 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive
content and recording only minimal controlled confirmation.

---

# Capability Boundaries

The skill SHALL NOT

- Open WebSocket connections directly
- Discover endpoints
- Analyze general TLS posture
- Test generic payload injection
- Enumerate or exfiltrate other principals' data
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in
[execution.md](execution.md) and to interface operations in
[interface.md](interface.md).
