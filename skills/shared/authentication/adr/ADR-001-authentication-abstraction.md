# ADR-001 — Authentication Abstraction

**File:** `skills/shared/authentication/adr/ADR-001-authentication-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform authenticates to targets using many mechanisms:
basic, bearer, cookie, API key, OAuth2, OIDC, SAML, and mTLS. Authentication is
required by nearly every network-facing skill and involves sensitive
credentials.

If each skill handled authentication directly, the platform would suffer

- Inconsistent credential handling and refresh
- Risk of credential leakage in logs and evidence
- Duplicated session-reuse logic
- Tight coupling to specific identity mechanisms

The platform requires a single, canonical, implementation-independent mechanism
for acquiring and applying credentials.

---

# Decision

The platform SHALL provide a dedicated Authentication shared skill that
centralizes credential acquisition, refresh, and application behind a stable
interface.

The Authentication shared skill SHALL

- Support multiple authentication mechanisms behind a uniform interface
- Protect secrets and never expose them to consumers, logs, or evidence
- Reuse authenticated sessions where policy permits
- Support credential rotation and refresh
- Preserve auditability

Consumers SHALL obtain and apply credentials exclusively through the
[Authentication Interface](../interface.md) using opaque credential references.
Secret material SHALL never cross the interface in plaintext to consumers.

---

# Alternatives Considered

## Per-Skill Authentication

Each skill could authenticate directly.

Rejected because it duplicates logic and multiplies the risk of credential
leakage.

## Embedding Credentials In Requests

Skills could embed credentials inline.

Rejected because it scatters secrets across the platform and prevents central
rotation, protection, and audit.

---

# Consequences

## Positive

- Uniform, secure authentication across skills
- Centralized secret protection and rotation
- Consistent session reuse
- Auditable credential usage

## Negative

- Consumers MUST resolve credentials through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by the security and consistency
benefits.

---

# Compliance

Consumers SHALL apply credentials through the Authentication Interface using
opaque references and SHALL NOT embed, log, or persist secrets.

---

# Future Compatibility

Future versions MAY add federation, hardware-backed key storage, and additional
mechanisms. These extensions SHALL preserve the existing interface and SHALL
maintain backward compatibility.

---

# Related Documents

- [Authentication README](../README.md)
- [Authentication Interface](../interface.md)
- [Authentication Execution Model](../execution.md)
- [Authentication Error Model](../error-model.md)
