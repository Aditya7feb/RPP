# ADR-001 — SSH Transport Abstraction

**File:** `skills/shared/ssh-client/adr/ADR-001-ssh-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with SSH servers to assess their
configuration and, where authorized, perform post-authentication review. SSH is
a layered protocol with transport algorithm negotiation, host-key verification,
multiple authentication methods, and multiplexed channels, and remote command
execution has real-world side effects.

If each skill negotiated SSH directly, the platform would suffer

- Duplicated transport and channel logic
- Inconsistent host-key trust handling
- Risk of credential and private-key leakage
- Risk of unauthorized command execution
- Divergent evidence and governance

The platform requires a single, canonical, implementation-independent SSH
transport that enforces host-key trust and authorization.

---

# Decision

The platform SHALL provide a dedicated SSH Client shared skill that centralizes
SSH sessions behind a stable interface.

The SSH Client shared skill SHALL

- Establish the transport through the [TCP Client](../../tcp-client/README.md)
- Negotiate and record transport algorithms as data
- Verify host keys against a configured trust policy
- Authenticate through the [Authentication](../../authentication/README.md)
  package, bounding attempts
- Open channels for commands, subsystems, and forwarding, gating intrusive
  execution
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform SSH transport exclusively through the
[SSH Client Interface](../interface.md). The SSH Client SHALL NOT detect weak
algorithms or brute-force credentials; those responsibilities belong to
dedicated, authorized domain skills.

---

# Alternatives Considered

## Per-Skill SSH Handling

Each skill could negotiate SSH directly.

Rejected because it duplicates transport and channel logic and risks credential
leakage and unauthorized execution.

## Detecting Weak Algorithms In The Transport Layer

The SSH Client could classify weak algorithms.

Rejected because finding generation belongs to domain skills. The SSH Client
records negotiated algorithms as data.

## Silent Host-Key Acceptance

The SSH Client could accept unknown host keys automatically.

Rejected because silent acceptance undermines trust and auditability. A trust
policy with `strict` as the safe default is mandatory.

## Credential Guessing In The Transport

The SSH Client could iterate credentials.

Rejected because brute-force is an intrusive activity requiring dedicated
authorization and belongs in a domain skill, not the transport. The transport
bounds attempts to prevent inadvertent brute-force behavior.

---

# Consequences

## Positive

- Uniform SSH sessions reusing TCP handling
- Enforced host-key trust and protected credentials
- Command execution gated as intrusive
- Consistent evidence and governance

## Negative

- Consumers MUST perform SSH through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform SSH through the SSH Client Interface
- Use `strict` host-key trust outside discovery contexts
- Reference credentials and keys rather than inlining them
- Execute commands only when authorized
- Interpret algorithms and host keys at the domain layer

---

# Future Compatibility

Future versions MAY add certificate-based authentication, multiplexed session
reuse, and structured SFTP operations. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [SSH Client README](../README.md)
- [SSH Client Interface](../interface.md)
- [SSH Client Execution Model](../execution.md)
- [SSH Client Error Model](../error-model.md)
- [TCP Client](../../tcp-client/README.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
