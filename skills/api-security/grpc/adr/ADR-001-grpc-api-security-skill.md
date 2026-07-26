# ADR-001 — gRPC API Security Skill

**File:** `skills/api-security/grpc/adr/ADR-001-grpc-api-security-skill.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

The RPP platform assesses gRPC APIs, which differ materially from REST, GraphQL, and
SOAP. gRPC uses a binary protocol over HTTP/2, exposes services and methods through
optional server reflection, supports unary and streaming calls, and communicates
errors through status codes and detail. Its security weaknesses are specific: server
reflection may over-disclose services and methods, channels may accept cleartext
transport, method- and object-level authorization may be unenforced, message-size and
streaming limits may be absent, and status detail may leak implementation
information.

These concerns are not addressed by the REST, GraphQL, or SOAP skills, nor by the
Discovery or TLS Analysis skills, whose responsibilities are to inventory Assets and
evaluate general transport posture rather than to evaluate gRPC API authorization and
consumption behavior.

The platform requires a dedicated, tool-independent gRPC API Security Skill that
consumes canonical Assets, drives the shared gRPC Client, gates every action through
the Policy Engine, and emits evidence-backed Findings — without duplicating the
Discovery, TLS Analysis, or Web Security skills, and without performing destructive or
disruptive testing.

---

# Decision

We SHALL provide a gRPC API Security Skill in the API Security tier with the following
properties.

- It consumes the `api`, `endpoint`, and `service`
  [Assets](../../../../schemas/asset.md) produced by Discovery and MAY reference a
  discovered service descriptor.
- It drives the [gRPC Client](../../../shared/grpc-client/README.md) and SHALL NOT
  open connections directly.
- It consults the [Policy Engine](../../../shared/policy-engine/README.md) before
  every target-facing action and honors `allow`, `requires_approval`, and `deny`
  decisions.
- It evaluates gRPC-specific weaknesses: reflection exposure (CWE-200), cleartext
  transport (CWE-319), method- and object-level authorization (CWE-285), missing
  resource-consumption limits (CWE-770), and status-detail disclosure (CWE-209),
  aligned to the OWASP API Security Top 10 (2023).
- It uses two authorized controlled identities for authorization testing, performs
  minimal confirmations, and never enumerates or exfiltrates other principals' data.
- It bounds message-size and streaming probes to avoid denial of service.
- It emits [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md), each backed by
  [Evidence](../../../../schemas/evidence.md).
- It delegates general TLS posture to TLS Analysis and generic injection testing to
  the Web Security skills.

---

# Consequences

## Positive

- gRPC-specific weaknesses are assessed within a single, cohesive skill.
- Authorization and resource-consumption testing is bounded, controlled, and
  non-destructive.
- The skill remains tool independent and reuses shared infrastructure and canonical
  schemas.
- Responsibilities remain cleanly separated from Discovery, TLS Analysis, and Web
  Security.

## Negative

- Authorization testing depends on the availability of two controlled identities;
  without them, those checks are skipped.
- Descriptor availability or reflection may bound method-driven checks.

## Neutral

- Streaming-specific abuse modeling and interceptor authorization evaluation are
  deferred to future extensions.

---

# Alternatives Considered

- Extending the REST skill to cover gRPC. Rejected because gRPC's protocol, reflection,
  streaming, and status semantics differ materially and would blur the REST skill's
  responsibilities.
- Handling gRPC transport within TLS Analysis. Rejected because TLS Analysis evaluates
  general transport posture, not gRPC API authorization and consumption behavior.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [gRPC Client](../../../shared/grpc-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
