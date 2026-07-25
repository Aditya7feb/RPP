# Proxy Execution Model

**File:** `skills/shared/proxy/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Proxy Shared Skill.

The execution model describes how the shared skill processes a routing request
from configuration resolution through tunnel establishment, operation execution,
and result propagation.

The model is deterministic given the same configuration and inputs.

---

# Execution Overview

```
Receive Invocation

↓

Resolve Configuration

↓

Evaluate Bypass

↓

Apply Governance

↓

Select Proxy

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

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Proxy Shared Skill SHALL resolve the effective proxy set and behavior using
the precedence defined in [configuration.md](configuration.md).

An inline override SHALL be validated before use.

---

# Stage 2 — Bypass Evaluation

The Proxy Shared Skill SHALL evaluate bypass rules for the destination.

A destination matching any bypass host, CIDR, loopback, or link-local rule SHALL
use a direct channel, subject to governance.

Bypass evaluation SHALL precede selection.

---

# Stage 3 — Governance

The Proxy Shared Skill SHALL apply governance.

When `allow_direct_egress` is `false`, a destination that would otherwise use a
direct channel through bypass, no-match, or fallback SHALL instead fail unless a
matching proxy is available.

Destinations whose scheme appears in `require_proxy_schemes` SHALL be proxied.

---

# Stage 4 — Proxy Selection

The Proxy Shared Skill SHALL select the most specific matching
[Proxy Configuration](../../../schemas/proxy-configuration.md).

Where no proxy matches, the configured `when_no_match` behavior SHALL apply,
subject to governance.

---

# Stage 5 — Tunnel Establishment

The Proxy Shared Skill SHALL establish a tunnel using the selected proxy
protocol.

If the proxy is unreachable, the configured `on_failure` behavior SHALL apply.

- `fail` SHALL propagate a canonical connection error
- `direct` SHALL fall back to a direct channel only where governance permits

---

# Stage 6 — Proxy Authentication

Where the selected proxy defines `authentication`, the Proxy Shared Skill SHALL
resolve the credential through the [Authentication](../authentication/README.md)
shared package.

Secret material SHALL never be logged or recorded.

---

# Stage 7 — Interception Notification

When the selected proxy sets `tls.intercepting`, the Proxy Shared Skill SHALL
notify the [TLS Client](../tls-client/README.md) of the interception boundary
before the operation executes.

---

# Stage 8 — Operation Execution

The Proxy Shared Skill SHALL invoke the caller-provided operation callback
exactly once, bound to the established channel.

The Proxy Shared Skill SHALL NOT inspect or modify the operation implementation
or payload.

---

# Stage 9 — Evidence and Events

The Proxy Shared Skill SHOULD emit routing evidence and lifecycle events
according to configuration.

Evidence SHALL NOT contain proxy credentials.

---

# Determinism

Given identical configuration and destination, the Proxy Shared Skill SHALL
produce identical routing decisions.

---

# Concurrency

The Proxy Shared Skill SHALL support concurrent routing of independent
operations.

Tunnel state SHALL be scoped to a single operation unless a pooling extension
explicitly shares it.

---

# Interaction With Other Shared Skills

- The [Rate Limiter](../rate-limiter/README.md) SHOULD gate operations before
  tunnel establishment so that proxied traffic remains within rate ceilings.
- The [TLS Client](../tls-client/README.md) SHALL validate the tunneled endpoint
  certificate, informed by interception awareness.
- The [Authentication](../authentication/README.md) shared package SHALL resolve
  proxy credentials.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed tunnel SHALL be torn down and SHALL NOT leak partial channel state to
the caller.

---

# Execution Outputs

The execution model SHALL produce

- A normalized routing result
- A routing decision record
- Proxy metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Proxy Configuration Schema](../../../schemas/proxy-configuration.md)
- [Execution Model](../../core/execution-model.md)
