# Proxy Shared Skill

**File:** `skills/shared/proxy/README.md`

**Version:** 1.0.0

---

# Purpose

The Proxy Shared Skill provides the canonical, implementation-independent
mechanism for routing outbound operations through intermediaries within the
Robust PenTest Platform (RPP).

Rather than allowing individual skills and shared packages to implement their
own proxy handling, this shared skill centralizes proxy selection, bypass
evaluation, tunnel establishment, proxy authentication, and interception
awareness.

All packages that perform outbound operations SHALL delegate proxy decisions to
this shared skill.

---

# Goals

The Proxy Shared Skill SHALL

- Abstract proxy routing behind a stable interface
- Select the applicable proxy for an operation
- Evaluate bypass rules
- Establish tunnels through supported proxy protocols
- Apply proxy authentication without exposing secrets
- Inform the TLS Client of interception boundaries
- Generate proxy evidence
- Integrate with platform observability

---

# Non-Goals

The Proxy Shared Skill SHALL NOT

- Execute the tunneled operation itself
- Interpret tunneled payloads
- Detect vulnerabilities
- Produce security findings
- Own connection or session state beyond the tunnel
- Validate TLS certificates of the tunneled endpoint

The Proxy Shared Skill establishes and routes through a tunnel. The caller owns
the operation performed across it. Certificate validation remains the
responsibility of the [TLS Client](../tls-client/README.md).

---

# Design Principles

The Proxy Shared Skill SHALL be

- Deterministic given the same configuration and inputs
- Configuration driven
- Transport independent
- Observable
- Secure by default
- Scope aware

---

# Architecture

```
Master Agent

↓

Domain Skill or Shared Package

↓

Proxy Shared Skill

├── Proxy Selector
├── Bypass Evaluator
├── Tunnel Establisher
├── Proxy Authenticator
├── Interception Notifier
├── Evidence Manager
├── Event Manager

↓

Caller-Provided Operation
```

The Proxy Shared Skill establishes a routed channel but SHALL invoke the
operation only through a caller-supplied execution callback bound to that
channel. It SHALL remain unaware of the operation implementation.

---

# Responsibilities

The Proxy Shared Skill is responsible for

- Resolving the applicable
  [Proxy Configuration](../../../schemas/proxy-configuration.md)
- Evaluating selection and bypass rules for a destination
- Establishing a tunnel using the configured protocol
- Applying proxy authentication through the
  [Authentication](../authentication/README.md) shared package
- Informing the [TLS Client](../tls-client/README.md) when interception is
  active
- Applying failure behavior when a proxy is unreachable
- Emitting proxy lifecycle events
- Capturing proxy evidence

---

# Proxy Lifecycle

```
Receive Operation

↓

Resolve Configuration

↓

Evaluate Bypass

├── Bypass → Direct Channel

└── Proxy → Select Proxy

            ↓

            Establish Tunnel

            ↓

            Authenticate (if required)

            ↓

            Notify TLS Interception (if any)

↓

Execute Operation Over Channel

↓

Emit Evidence and Events
```

The complete routing decision SHOULD be preserved as evidence.

---

# Proxy Selection

The Proxy Shared Skill SHALL select a proxy by evaluating the `applies_to` rules
of each candidate
[Proxy Configuration](../../../schemas/proxy-configuration.md) against the
destination scheme, host, and port.

Where multiple proxies match, the most specific match SHALL be selected.

Where no proxy matches, a direct channel SHALL be used unless configuration
requires otherwise.

---

# Bypass Evaluation

Before selecting a proxy, the Proxy Shared Skill SHALL evaluate bypass rules.

A destination matching any `bypass` host, CIDR, loopback, or link-local rule
SHALL use a direct channel.

Bypass evaluation SHALL take precedence over selection.

---

# Supported Protocols

The Proxy Shared Skill SHALL support the protocols defined in the
[Proxy Configuration schema](../../../schemas/proxy-configuration.md)

- http
- https
- socks4
- socks5

The tunneled operation protocol SHALL remain independent of the proxy protocol.

---

# Proxy Authentication

Where a configuration defines `authentication`, the Proxy Shared Skill SHALL
resolve the credential through the
[Authentication](../authentication/README.md) shared package using the
`credential_ref`.

Secrets SHALL never be logged, embedded in evidence, or exposed to consumers.

---

# TLS Interception Awareness

When a configuration sets `tls.intercepting`, the Proxy Shared Skill SHALL
inform the [TLS Client](../tls-client/README.md) so that certificate validation
reflects the interception boundary.

The Proxy Shared Skill SHALL NOT itself accept or reject the tunneled endpoint
certificate.

---

# Failure Behavior

When a proxy is unreachable, the Proxy Shared Skill SHALL apply the configured
`on_failure` behavior.

- `fail` SHALL propagate a canonical connection error
- `direct` SHALL fall back to a direct channel only where Rules of Engagement
  permit direct egress

The default behavior SHALL be `fail`.

---

# Evidence

The Proxy Shared Skill SHOULD capture

- Proxy reference
- Destination
- Routing decision
- Bypass decision
- Interception flag
- Tunnel establishment outcome

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

Evidence SHALL NOT contain proxy credentials.

---

# Events

The Proxy Shared Skill SHOULD publish

- ProxySelected
- BypassApplied
- TunnelEstablished
- ProxyAuthenticated
- InterceptionDetected
- ProxyUnreachable
- DirectFallbackApplied

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Proxy Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Proxy Configuration Schema](../../../schemas/proxy-configuration.md)

The Proxy Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [DNS Client](../dns-client/README.md)
- Future network clients

---

# Outputs

Typical outputs MAY include

- A routed channel bound to the operation
- Routing decision
- Proxy metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Proxy Shared Skill SHALL

- Protect proxy credentials at all times
- Enforce bypass rules to prevent unintended egress
- Respect Rules of Engagement for direct fallback
- Communicate interception boundaries to preserve accurate TLS findings
- Preserve auditability

Routing traffic incorrectly can leak sensitive data or violate scope. The
shared skill SHALL make routing decisions explicit and auditable.

---

# Best Practices

Consumers SHOULD

- Reference shared proxy configurations rather than inlining values
- Rely on the shared skill for bypass evaluation
- Default `on_failure` to `fail`
- Capture proxy evidence
- Coordinate interception awareness with the TLS Client

---

# Anti-Patterns

Consumers SHOULD NOT

- Establish tunnels independently
- Embed proxy credentials in configuration
- Silently fall back to direct egress
- Ignore interception boundaries when validating certificates
- Route loopback destinations through a proxy

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-proxy-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [DNS Client](../dns-client/README.md)
- [Authentication](../authentication/README.md)

---

# Canonical Schemas

- [Proxy Configuration](../../../schemas/proxy-configuration.md)
- [Evidence](../../../schemas/evidence.md)
- [Execution State](../../../schemas/execution-state.md)

---

# Architecture Decisions

- [ADR-001 — Proxy Abstraction](adr/ADR-001-proxy-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Proxy chaining
- Per-assessment egress rotation
- Health-aware proxy pools
- PAC-style dynamic selection expressed as canonical rules

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Proxy Shared Skill provides a deterministic and
implementation-independent routing abstraction for the Robust PenTest Platform.

It enables consistent, auditable egress control across every shared package
while protecting credentials and preserving accurate TLS findings, without
embedding proxy logic in consumers.
