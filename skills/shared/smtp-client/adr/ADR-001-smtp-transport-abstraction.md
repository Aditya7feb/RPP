# ADR-001 — SMTP Transport Abstraction

**File:** `skills/shared/smtp-client/adr/ADR-001-smtp-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with mail servers to assess their
configuration and security posture. SMTP is a stateful, line-oriented protocol
with capability negotiation, opportunistic `STARTTLS`, authentication, and reply
codes, and message transmission has real-world side effects.

If each skill spoke SMTP over raw sockets, the platform would suffer

- Duplicated protocol-conversation logic
- Inconsistent TLS upgrade and confidentiality handling
- Risk of authenticating over cleartext or leaking credentials
- Risk of sending unsolicited mail
- Divergent reply-code mapping and evidence

The platform requires a single, canonical, implementation-independent SMTP
transport that reuses the TCP and TLS shared skills and enforces confidentiality
and authorization.

---

# Decision

The platform SHALL provide a dedicated SMTP Client shared skill that centralizes
SMTP conversations behind a stable interface.

The SMTP Client shared skill SHALL

- Establish sessions through the [TCP Client](../../tcp-client/README.md)
- Negotiate capabilities and upgrade via `STARTTLS` through the
  [TLS Client](../../tls-client/README.md)
- Authenticate through the [Authentication](../../authentication/README.md)
  package, never over cleartext when confidentiality is required
- Exchange commands and map reply codes to canonical outcomes, preserving the
  reply code
- Treat message transmission as intrusive, gated by authorization
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform SMTP transport exclusively through the
[SMTP Client Interface](../interface.md). The SMTP Client SHALL NOT detect
vulnerabilities such as open relays; that interpretation belongs to domain
skills.

---

# Alternatives Considered

## Per-Skill SMTP Over Raw Sockets

Each skill could speak SMTP directly.

Rejected because it duplicates logic and risks cleartext authentication,
credential leakage, and unsolicited mail.

## Detecting Open Relays In The Transport Layer

The SMTP Client could classify open-relay behavior.

Rejected because finding generation belongs to domain skills. The SMTP Client
conducts the conversation and reports reply codes as data.

## Optional TLS Without A Required Mode

TLS could be purely opportunistic.

Rejected because some assessments require confidentiality. A `starttls_required`
mode that fails rather than downgrades is mandatory for safe authenticated
sessions.

---

# Consequences

## Positive

- Uniform SMTP conversations reusing TCP and TLS handling
- Enforced confidentiality and protected credentials
- Message transmission gated as intrusive
- Consistent reply-code mapping and evidence

## Negative

- Consumers MUST perform SMTP through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform SMTP through the SMTP Client Interface
- Require TLS for authenticated sessions
- Reference credentials rather than inlining secrets
- Send mail only when authorized
- Interpret reply codes at the domain layer

---

# Future Compatibility

Future versions MAY add delivery-status handling, pipelining, and
internationalized addresses. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [SMTP Client README](../README.md)
- [SMTP Client Interface](../interface.md)
- [SMTP Client Execution Model](../execution.md)
- [SMTP Client Error Model](../error-model.md)
- [TCP Client](../../tcp-client/README.md)
- [TLS Client](../../tls-client/README.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
