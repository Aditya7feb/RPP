# ADR-001 — FTP Transport Abstraction

**File:** `skills/shared/ftp-client/adr/ADR-001-ftp-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with FTP servers to assess their
configuration and security posture. FTP is a dual-channel protocol with a
control channel and separate data channels, supports explicit TLS (FTPS),
anonymous and credentialed authentication, and reply codes, and file
modification has real-world side effects.

If each skill spoke FTP over raw sockets, the platform would suffer

- Duplicated dual-channel coordination logic
- Inconsistent FTPS upgrade and confidentiality handling
- Risk of cleartext authentication or credential leakage
- Risk of unauthorized file modification
- Divergent reply-code mapping and evidence

The platform requires a single, canonical, implementation-independent FTP
transport that reuses the TCP and TLS shared skills and enforces confidentiality
and authorization.

---

# Decision

The platform SHALL provide a dedicated FTP Client shared skill that centralizes
FTP conversations behind a stable interface.

The FTP Client shared skill SHALL

- Establish control and data channels through the
  [TCP Client](../../tcp-client/README.md)
- Upgrade via explicit FTPS through the [TLS Client](../../tls-client/README.md)
- Authenticate through the [Authentication](../../authentication/README.md)
  package, supporting anonymous access where requested
- Prefer passive mode and gate active mode
- Treat write and delete operations as intrusive, gated by authorization
- Exchange commands and map reply codes to canonical outcomes, preserving the
  reply code
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform FTP transport exclusively through the
[FTP Client Interface](../interface.md). The FTP Client SHALL NOT detect
vulnerabilities such as anonymous write access; that interpretation belongs to
domain skills.

---

# Alternatives Considered

## Per-Skill FTP Over Raw Sockets

Each skill could speak FTP directly.

Rejected because it duplicates dual-channel logic and risks cleartext
authentication, credential leakage, and unauthorized modification.

## Detecting Weaknesses In The Transport Layer

The FTP Client could classify anonymous-write or other weaknesses.

Rejected because finding generation belongs to domain skills. The FTP Client
conducts the conversation and reports reply codes and access facts as data.

## Preferring Active Mode

Active mode could be the default.

Rejected because passive mode simplifies proxy and firewall traversal and is
safer by default. Active mode is gated and opt-in.

---

# Consequences

## Positive

- Uniform FTP conversations reusing TCP and TLS handling
- Enforced confidentiality and protected credentials
- File modification gated as intrusive
- Consistent reply-code mapping and evidence

## Negative

- Consumers MUST perform FTP through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform FTP through the FTP Client Interface
- Require TLS for non-anonymous authenticated sessions
- Prefer passive mode
- Perform writes only when authorized
- Interpret reply codes and access facts at the domain layer

---

# Future Compatibility

Future versions MAY add structured MLSD listings, resume transfers, and implicit
FTPS profiles. These extensions SHALL preserve the existing interface and SHALL
maintain backward compatibility.

---

# Related Documents

- [FTP Client README](../README.md)
- [FTP Client Interface](../interface.md)
- [FTP Client Execution Model](../execution.md)
- [FTP Client Error Model](../error-model.md)
- [TCP Client](../../tcp-client/README.md)
- [TLS Client](../../tls-client/README.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
