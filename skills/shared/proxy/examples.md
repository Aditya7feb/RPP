# Proxy Examples

**File:** `skills/shared/proxy/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Proxy Shared Skill in use.

Examples demonstrate consumers, configurations, selection, bypass, interception
awareness, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Corporate Egress Proxy

An HTTP operation is routed through a corporate forwarding proxy.

## Configuration

```yaml
proxy_id: proxy-corporate-egress
protocol: http
endpoint:
  host: proxy.internal.example.com
  port: 8080
authentication:
  scheme: basic
  credential_ref: cred-proxy-egress
applies_to:
  schemes:
    - http
    - https
```

## Invocation

```yaml
metadata:
  request_id: req-2001
  assessment_id: asmt-42
  task_id: task-http-probe
  skill_id: content-discovery
destination:
  scheme: https
  host: app.example.com
  port: 443
operation: <send-http-request-callback>
proxy_id: proxy-corporate-egress
```

## Result

```yaml
outcome: executed
routing:
  decision: proxied
  proxy_id: proxy-corporate-egress
  destination: app.example.com:443
  interception: false
```

The request is tunneled through the proxy and executed.

---

# Example 2 — Bypass For Internal Hosts

A destination matching a bypass rule is routed directly.

## Configuration

```yaml
proxy_id: proxy-corporate-egress
bypass:
  hosts:
    - "*.internal.example.com"
  loopback: true
```

## Result For internal.example.com

```yaml
outcome: bypassed
routing:
  decision: direct
  destination: api.internal.example.com:443
```

The internal host bypasses the proxy and connects directly.

---

# Example 3 — Intercepting Proxy And TLS Awareness

A testing proxy terminates TLS. The Proxy Shared Skill informs the TLS Client.

## Configuration

```yaml
proxy_id: proxy-testing-intercept
protocol: http
endpoint:
  host: 127.0.0.1
  port: 8888
tls:
  intercepting: true
  trust_anchor_ref: trust-testing-ca
```

## Result

```yaml
outcome: executed
routing:
  decision: proxied
  proxy_id: proxy-testing-intercept
  interception: true
```

The [TLS Client](../tls-client/README.md) validates the endpoint using the
declared trust anchor and does not report the interception as a spurious
certificate weakness.

---

# Example 4 — Governance Blocks Direct Egress

Governance prohibits direct egress. An unmatched destination fails rather than
connecting directly.

## Configuration

```yaml
proxy:
  default_behavior:
    when_no_match: fail
  governance:
    allow_direct_egress: false
    require_proxy_schemes:
      - http
      - https
```

## Result For An Unmatched Host

```yaml
outcome: blocked
error:
  category: Governance
  code: direct_egress_blocked
  retryable: false
```

No proxy matched and direct egress is prohibited, so the operation is blocked.

---

# Example 5 — Proxy Unreachable With Fail Behavior

The configured proxy is unreachable and `on_failure` is `fail`.

## Result

```yaml
outcome: proxy_unreachable
error:
  category: Connection
  code: proxy_unreachable
  proxy_id: proxy-corporate-egress
  retryable: true
```

The operation fails with a canonical connection error. When combined with
[Retry](../retry/README.md), it MAY be retried, each attempt acquiring a fresh
permit from the [Rate Limiter](../rate-limiter/README.md).

---

# Example 6 — SOCKS5 Tunnel For Non-HTTP Operation

A TLS handshake is tunneled through a SOCKS5 proxy.

## Configuration

```yaml
proxy_id: proxy-socks
protocol: socks5
endpoint:
  host: gateway.example.net
  port: 1080
applies_to:
  schemes:
    - https
    - tls
```

## Result

```yaml
outcome: executed
routing:
  decision: proxied
  proxy_id: proxy-socks
  destination: mail.example.net:443
```

The tunneled operation protocol is independent of the SOCKS5 proxy protocol.

---

# Example 7 — Evidence Record

A single routing decision produces the following evidence.

```yaml
evidence:
  type: proxy-routing
  proxy_id: proxy-corporate-egress
  destination: app.example.com:443
  decision: proxied
  interception: false
  decided_at: 2026-07-25T11:00:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes credentials, and
supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Proxy Configuration Schema](../../../schemas/proxy-configuration.md)
- [TLS Client](../tls-client/README.md)
