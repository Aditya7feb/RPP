# ADR-001 — Cloud Storage Abstraction

**File:** `skills/shared/cloud-storage-client/adr/ADR-001-cloud-storage-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform accesses object storage to discover cloud assets,
assess bucket exposure, and stage evidence. Object storage spans multiple
providers, holds sensitive data, and exposes access metadata such as public-access
flags and encryption status.

If each skill called provider storage services directly, the platform would
suffer

- Duplicated object-operation logic
- Inconsistent or absent scope confinement
- Risk of storing unencrypted sensitive data
- Risk of leaking presigned references and keys
- Divergent evidence and governance

The platform requires a single, canonical, implementation-independent
object-storage abstraction that confines scope and enforces encryption.

---

# Decision

The platform SHALL provide a dedicated Cloud Storage Client shared skill that
centralizes object-storage access behind a stable interface.

The Cloud Storage Client shared skill SHALL

- Confine operations to authorized buckets and prefixes
- List, read, write, stat, delete, and presign with bounds
- Enforce server-side encryption for writes where mandated
- Resolve client-side keys through the
  [Secrets Client](../../secrets-client/README.md) without exposure
- Observe and report access metadata as data
- Authenticate through the [Authentication](../../authentication/README.md)
  package
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform object-storage access exclusively through the
[Cloud Storage Client Interface](../interface.md). The Cloud Storage Client SHALL
NOT detect public-bucket or other misconfigurations; that interpretation belongs
to cloud domain skills.

---

# Alternatives Considered

## Per-Skill Provider Calls

Each skill could call provider storage services directly.

Rejected because it duplicates logic and risks inconsistent confinement and
unencrypted storage.

## Classifying Public Buckets In The Client

The client could classify public buckets as findings.

Rejected because finding generation belongs to cloud domain skills. The client
reports access metadata as data.

## Optional Encryption

Encryption could be purely optional.

Rejected because object storage often holds sensitive data. Required encryption
that fails rather than storing plaintext is mandatory where mandated.

---

# Consequences

## Positive

- Uniform, confined object access across providers
- Encryption enforced where mandated
- Access metadata reported consistently as data
- Presigned references and keys protected
- Consistent evidence and bounds

## Negative

- Consumers MUST perform object access through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform object access through the Cloud Storage Client Interface
- Operate within authorized scopes
- Require encryption for writes
- Never persist object contents or presigned references in evidence
- Interpret access metadata at the cloud domain layer

---

# Future Compatibility

Future versions MAY add multipart transfers, versioned-object inspection, and
lifecycle-policy observation. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Cloud Storage Client README](../README.md)
- [Cloud Storage Client Interface](../interface.md)
- [Cloud Storage Client Execution Model](../execution.md)
- [Cloud Storage Client Error Model](../error-model.md)
- [Authentication](../../authentication/README.md)
- [Secrets Client](../../secrets-client/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
