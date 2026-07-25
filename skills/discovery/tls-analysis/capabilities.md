# TLS Analysis Capabilities

**File:** `skills/discovery/tls-analysis/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the TLS Analysis Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[TLS Analysis Interface](interface.md).

---

# Capability Model

```
Authorization

Handshake Analysis

Certificate Evaluation

Asset Construction

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every action.

---

## Scope Confinement

The skill SHALL analyze only in-scope services.

---

# Handshake Analysis Capabilities

## Protocol Analysis

The skill SHALL analyze offered protocol versions through the
[TLS Client](../../shared/tls-client/README.md).

---

## Cipher Analysis

The skill SHALL analyze offered cipher suites.

---

# Certificate Evaluation Capabilities

## Chain Retrieval

The skill SHALL retrieve and evaluate certificate chains.

---

## Validation-Outcome Interpretation

The skill SHALL interpret validation outcomes reported by the TLS Client as
weaknesses where appropriate.

---

## Interception Awareness

The skill SHALL honor interception boundaries reported by the TLS Client.

---

# Asset Construction Capabilities

## Certificate Asset Production

The skill SHALL produce canonical `certificate`
[Assets](../../../schemas/asset.md).

---

## Relationship Production

The skill SHALL relate certificates to their `service` Assets.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify TLS weaknesses such as deprecated protocols, weak
ciphers, and invalid certificates.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md).

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including services analyzed, certificates
evaluated, and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Negotiate TLS directly
- Assign trust verdicts in the transport layer
- Exploit weaknesses
- Produce a Finding without Evidence
- Act on out-of-scope services

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Protocol Analysis | Handshake Analysis | SHALL |
| Cipher Analysis | Handshake Analysis | SHALL |
| Chain Retrieval | Certificate Evaluation | SHALL |
| Validation-Outcome Interpretation | Certificate Evaluation | SHALL |
| Interception Awareness | Certificate Evaluation | SHALL |
| Certificate Asset Production | Asset Construction | SHALL |
| Relationship Production | Asset Construction | SHALL |
| Weakness Identification | Weakness Analysis | SHALL |
| Finding Production | Weakness Analysis | SHALL |
| Observation And Evidence | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [TLS Client](../../shared/tls-client/README.md)
