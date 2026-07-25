# Proxy Configuration Schema

**File:** `schemas/proxy-configuration.md`

**Version:** 1.0.0

---

# Purpose

The Proxy Configuration Schema defines the canonical, implementation-independent
representation of an outbound proxy configuration within the Robust PenTest
Platform (RPP).

A proxy configuration describes how outbound operations are routed through an
intermediary: the proxy protocol, endpoint, selection rules, bypass rules, and
authentication reference. It is consumed by the
[Proxy](../skills/shared/proxy/README.md) shared package and referenced by every
package that performs outbound operations, including the
[HTTP Client](../skills/shared/http-client/README.md),
[TLS Client](../skills/shared/tls-client/README.md), and
[DNS Client](../skills/shared/dns-client/README.md).

A Proxy Configuration object represents configuration and intent only. It SHALL
NOT contain runtime state, security interpretation, findings, or embedded
secrets.

---

# Design Principles

A Proxy Configuration SHALL be

- Declarative
- Deterministic given the same inputs
- Transport independent
- Reusable across packages
- Safe to reference
- Free of embedded secrets

---

# Identity

Every Proxy Configuration SHALL contain

```yaml
proxy_id:

schema_version:
```

`proxy_id` SHALL be unique within an assessment or configuration namespace.

`schema_version` SHALL be `1.0.0`.

---

# Classification

Every Proxy Configuration SHALL contain

```yaml
name:

description:
```

`name` SHALL be a stable, human-readable identifier such as `corporate-egress`.

`description` SHALL summarize the intended use of the configuration.

---

# Protocol

Every Proxy Configuration SHALL contain

```yaml
protocol:
```

`protocol` SHALL be one of

```
http

https

socks4

socks5
```

`protocol` describes the wire protocol used to reach the proxy endpoint, not the
protocol of the tunneled operation.

---

# Endpoint

Every Proxy Configuration SHALL contain

```yaml
endpoint:
```

`endpoint` SHALL contain

```yaml
host:

port:
```

`host` SHALL be a hostname or address of the proxy.

`port` SHALL be an integer from `1` through `65535`.

---

# Authentication

A Proxy Configuration MAY contain

```yaml
authentication:
```

`authentication` SHALL contain

```yaml
scheme:

credential_ref:
```

`scheme` SHALL be one of

```
none

basic

bearer

ntlm
```

`credential_ref` SHALL be an opaque reference to a credential resolved by the
[Authentication](../skills/shared/authentication/README.md) shared package.

`credential_ref` SHALL NOT contain secret material. Secrets SHALL never appear
in a Proxy Configuration object.

---

# Selection Rules

A Proxy Configuration MAY contain

```yaml
applies_to:
```

`applies_to` SHALL contain

```yaml
schemes:

hosts:

ports:
```

`schemes` SHALL be an array of operation schemes, such as `http`, `https`, or
`dns`, to which the proxy applies.

`hosts` SHALL be an array of host patterns to which the proxy applies.

`ports` SHALL be an array of ports to which the proxy applies.

When `applies_to` is absent, the proxy SHALL apply to all outbound operations
within its scope.

---

# Bypass Rules

A Proxy Configuration MAY contain

```yaml
bypass:
```

`bypass` SHALL contain

```yaml
hosts:

cidrs:

loopback:

link_local:
```

`hosts` SHALL be an array of host patterns that SHALL NOT be routed through the
proxy.

`cidrs` SHALL be an array of address ranges excluded from proxying.

`loopback` SHALL be a boolean. When `true`, loopback destinations SHALL bypass
the proxy.

`link_local` SHALL be a boolean. When `true`, link-local destinations SHALL
bypass the proxy.

---

# TLS Interception Awareness

A Proxy Configuration MAY contain

```yaml
tls:
```

`tls` SHALL contain

```yaml
intercepting:

trust_anchor_ref:
```

`intercepting` SHALL be a boolean declaring whether the proxy terminates and
re-originates TLS.

`trust_anchor_ref` SHALL be an opaque reference to the trust material required
to validate an intercepting proxy, resolved outside this schema.

When `intercepting` is `true`, the
[TLS Client](../skills/shared/tls-client/README.md) SHALL be informed so that
certificate validation reflects the interception boundary rather than reporting
a spurious weakness.

---

# Failure Behavior

A Proxy Configuration MAY contain

```yaml
on_failure:
```

`on_failure` SHALL be one of

```
fail

direct
```

`fail` SHALL cause outbound operations to fail when the proxy is unreachable.

`direct` SHALL permit a direct connection when the proxy is unreachable and
SHALL be used only where Rules of Engagement allow direct egress.

The default behavior SHALL be `fail`.

---

# Extensions

A Proxy Configuration MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Proxy Configuration object SHALL contain

- `proxy_id`
- `schema_version`
- `name`
- `description`
- `protocol`
- `endpoint.host`
- `endpoint.port`

---

# Validation Rules

A valid Proxy Configuration object SHALL satisfy

- `protocol` is one of the allowed protocols
- `endpoint.port` is an integer from `1` through `65535`
- `authentication.scheme`, when present, is one of the allowed schemes
- `authentication.credential_ref` is present when `scheme` is not `none`
- `on_failure`, when present, is one of the allowed behaviors
- `tls.trust_anchor_ref` is present when `tls.intercepting` is `true`
- No secret material appears in any field, including `extensions`

---

# Relationships

```
Proxy Configuration

├── referenced by HTTP Client configuration
├── referenced by TLS Client configuration
├── referenced by DNS Client configuration
├── consumed by Proxy shared package
├── references a credential resolved by Authentication
└── informs TLS Client of interception boundaries
```

A Proxy Configuration is referenced by a package configuration through a proxy
reference. Credentials are resolved indirectly through the
[Authentication](../skills/shared/authentication/README.md) shared package.
Interception awareness is communicated to the
[TLS Client](../skills/shared/tls-client/README.md).

---

# Example Object

```yaml
proxy_id: proxy-corporate-egress
schema_version: 1.0.0
name: corporate-egress
description: >
  Corporate forwarding proxy for HTTP and HTTPS egress with authentication and
  loopback bypass.
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
bypass:
  hosts:
    - "*.internal.example.com"
  cidrs:
    - 10.0.0.0/8
  loopback: true
  link_local: true
tls:
  intercepting: false
on_failure: fail
```

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields such as additional proxy protocols
or selection criteria.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
