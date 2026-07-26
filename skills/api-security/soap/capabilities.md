# SOAP API Security Capabilities

**File:** `skills/api-security/soap/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the SOAP API Security Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[SOAP API Security Interface](interface.md).

---

# Capability Model

```
Authorization

Operation Probing

WSDL Exposure Analysis

WS-Security Analysis

Action Authorization Analysis

Message Safety Analysis

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every target-facing action.

---

## Scope Confinement

The skill SHALL test only in-scope targets.

---

# Operation Probing Capabilities

## Controlled Operation Probing

The skill SHALL submit bounded SOAP operations using authorized controlled identities
through the [HTTP Client](../../shared/http-client/README.md).

---

# WSDL Exposure Analysis Capabilities

## WSDL Exposure Analysis

The skill SHALL determine whether WSDL and operation detail are exposed without
authentication.

---

# WS-Security Analysis Capabilities

## WS-Security Enforcement Analysis

The skill SHALL determine whether WS-Security message-level authentication and
integrity are enforced.

---

# Action Authorization Analysis Capabilities

## Action Authorization Analysis

The skill SHALL determine whether SOAP action and operation-level authorization are
enforced across identities.

---

# Message Safety Analysis Capabilities

## Message Handling Analysis

The skill SHALL determine whether XML message handling is safe at the service
boundary, referring in-depth external-entity testing to the XXE skill.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify SOAP security weaknesses from observed behavior and classify
them using canonical identifiers and OWASP API Security Top 10 (2023) references.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only minimal controlled
confirmation recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including operations tested and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover services or endpoints
- Perform in-depth XML external entity testing
- Test generic injection
- Enumerate or exfiltrate other principals' data
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Controlled Operation Probing | Operation Probing | SHALL |
| WSDL Exposure Analysis | WSDL Exposure Analysis | SHALL |
| WS-Security Enforcement Analysis | WS-Security Analysis | SHALL |
| Action Authorization Analysis | Action Authorization Analysis | SHALL |
| Message Handling Analysis | Message Safety Analysis | SHALL |
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
- [Policy Engine](../../shared/policy-engine/README.md)
