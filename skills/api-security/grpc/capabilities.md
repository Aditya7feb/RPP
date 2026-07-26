# gRPC API Security Skill Capabilities

**File:** `skills/api-security/grpc/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the gRPC API Security Skill. Each
capability is scope-confined, policy-gated, evidence-backed, and tool independent.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| GRPC-1 | Reflection exposure analysis | api, endpoint | Reflection Findings |
| GRPC-2 | Transport security analysis | endpoint | Transport Findings |
| GRPC-3 | Method authorization analysis | api, identities_ref | Authorization Findings |
| GRPC-4 | Object-level authorization analysis | api, identities_ref | Authorization Findings |
| GRPC-5 | Resource-consumption analysis | api, descriptor_ref | Consumption Findings |
| GRPC-6 | Status-detail disclosure analysis | api | Disclosure Findings |
| GRPC-7 | Evidence recording | Observations | Evidence references |

---

# GRPC-1 — Reflection Exposure Analysis

The skill SHALL evaluate whether server reflection is enabled and discloses service
and method detail that SHOULD NOT be exposed in production. It SHALL classify
confirmed exposure as CWE-200 and reference OWASP API8:2023 – Security
Misconfiguration.

---

# GRPC-2 — Transport Security Analysis

The skill SHALL evaluate whether the gRPC channel enforces transport encryption. A
channel that accepts cleartext transport SHALL be classified as CWE-319. The boundary
with TLS Analysis is precise: this skill owns transport enforcement — whether the API
requires a secure channel and rejects cleartext — while TLS Analysis owns TLS
configuration quality, certificate validation, protocol versions, and cipher strength.
This skill SHALL NOT assess TLS configuration quality.

---

# GRPC-3 — Method Authorization Analysis

The skill SHALL evaluate whether method-level (function-level) authorization is
enforced by invoking bounded methods across two controlled identities. Missing
enforcement SHALL be classified as CWE-285 and reference OWASP API5:2023 – Broken
Function Level Authorization.

---

# GRPC-4 — Object-Level Authorization Analysis

The skill SHALL evaluate whether object-level authorization is enforced by requesting
minimally identified objects owned by one identity while authenticated as another.
Missing enforcement SHALL be classified as CWE-285 and reference OWASP API1:2023 –
Broken Object Level Authorization. Confirmation SHALL be minimal and SHALL NOT
enumerate other principals' data.

---

# GRPC-5 — Resource-Consumption Analysis

The skill SHALL evaluate whether message-size and streaming limits constrain resource
consumption using bounded, incrementally larger probes. Missing limits SHALL be
classified as CWE-770 and reference OWASP API4:2023 – Unrestricted Resource
Consumption. Probes SHALL NOT be unbounded and SHALL never cause denial of service.

---

# GRPC-6 — Status-Detail Disclosure Analysis

The skill SHALL evaluate whether gRPC status detail discloses implementation
information such as stack traces or internal identifiers. Confirmed disclosure SHALL
be classified as CWE-209.

---

# GRPC-7 — Evidence Recording

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
supporting ones to [Evidence](../../../schemas/evidence.md), redacting sensitive
content and recording only minimal controlled confirmation.

---

# Capability Boundaries

The skill SHALL NOT

- Open gRPC connections directly
- Discover services or methods
- Analyze general TLS posture
- Test generic injection
- Enumerate or exfiltrate other principals' data
- Perform destructive exploitation

---

# Traceability

Each capability maps to execution stages in
[execution.md](execution.md) and to interface operations in
[interface.md](interface.md).
