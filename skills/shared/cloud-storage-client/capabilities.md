# Cloud Storage Client Capabilities

**File:** `skills/shared/cloud-storage-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Cloud Storage Client
Shared Skill. Capabilities describe *what* the shared skill provides, not *how*
it is implemented.

Each capability is implementation independent and consumed through the
[Cloud Storage Client Interface](interface.md).

---

# Capability Model

```
Scope

Objects

Encryption

Access Metadata

Presigned References

Governance

Observability
```

---

# Scope Capabilities

## Scope Confinement

The Cloud Storage Client SHALL confine operations to authorized buckets and
prefixes.

---

## Provider Abstraction

The Cloud Storage Client SHALL abstract provider differences behind a uniform
interface.

---

# Object Capabilities

## List

The Cloud Storage Client SHALL list objects with bounded volume.

---

## Read And Stat

The Cloud Storage Client SHALL read objects with bounded size and return
metadata.

---

## Write And Delete

The Cloud Storage Client SHALL write and delete objects with authorization.

---

## Intrusive Gating

The Cloud Storage Client SHALL gate write, delete, and policy changes as
intrusive.

---

# Encryption Capabilities

## Encryption Enforcement

The Cloud Storage Client SHALL enforce server-side encryption for writes where
mandated.

---

## Key Protection

The Cloud Storage Client SHALL resolve client-side keys through the
[Secrets Client](../secrets-client/README.md) without exposure.

---

# Access-Metadata Capabilities

## Metadata Observation

The Cloud Storage Client SHALL observe and report access metadata as data.

---

# Presigned Reference Capabilities

## Bounded Presigned References

The Cloud Storage Client SHALL generate and consume presigned references with
bounded lifetimes.

---

## Reference Protection

The Cloud Storage Client SHALL redact presigned references from evidence.

---

# Governance Capabilities

## Rate Governance

The Cloud Storage Client SHALL acquire a rate permit per operation through the
[Rate Limiter](../rate-limiter/README.md).

---

## Retry Governance

The Cloud Storage Client MAY retry transient provider failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The Cloud Storage Client SHOULD capture operation evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Cloud Storage Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Cloud Storage Client SHOULD expose metrics including operations, bytes read,
bytes written, and objects listed.

---

# Capability Boundaries

The Cloud Storage Client SHALL NOT

- Detect public-bucket or other misconfigurations as findings
- Produce findings
- Access unauthorized buckets
- Store unencrypted data where required
- Persist object contents or presigned references

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Scope Confinement | Scope | SHALL |
| Provider Abstraction | Scope | SHALL |
| List | Objects | SHALL |
| Read And Stat | Objects | SHALL |
| Write And Delete | Objects | SHALL |
| Intrusive Gating | Objects | SHALL |
| Encryption Enforcement | Encryption | SHALL |
| Key Protection | Encryption | SHALL |
| Metadata Observation | Access Metadata | SHALL |
| Bounded Presigned References | Presigned References | SHALL |
| Reference Protection | Presigned References | SHALL |
| Rate Governance | Governance | SHALL |
| Retry Governance | Governance | MAY |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Secrets Client](../secrets-client/README.md)
