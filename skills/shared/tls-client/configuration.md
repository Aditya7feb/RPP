# TLS Client Configuration Model

**File:** `skills/shared/tls-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

The TLS Client Configuration Model defines how TLS behavior is resolved, validated, applied, and recorded.

Configuration controls protocol versions, validation policy, trust stores, client authentication, timeouts, retry behavior, session reuse, evidence collection, and adapter selection.

---

# Design Principles

TLS configuration SHALL be

- Explicit
- Deterministic
- Immutable per request
- Auditable
- Policy driven
- Secure by default
- Adapter independent

---

# Configuration Resolution

Configuration precedence SHALL be

```
Operation

↓

Workflow

↓

Skill

↓

Assessment

↓

Platform

↓

Defaults
```

Higher-precedence configuration SHALL override lower-precedence configuration.

The resolved configuration SHALL be immutable for the request and recorded by reference in evidence.

---

# Configuration Shape

Example

```yaml
tls_client:
  protocol:
    minimum_version: TLSv1.2
    maximum_version: TLSv1.3
    alpn_protocols: [h2, http/1.1]
  validation:
    policy: strict
    hostname_verification: true
    trust_store_profile: platform-default
    check_revocation: false
  timeouts:
    connect_ms: 5000
    handshake_ms: 10000
    total_ms: 15000
  retry:
    max_attempts: 1
    retryable_categories: [Network, Timeout]
  session:
    reuse_enabled: true
    isolation_scope: assessment
  evidence:
    mode: summary
```

---

# Protocol Configuration

Protocol configuration MAY include

```yaml
minimum_version:

maximum_version:

alpn_protocols:

cipher_suites:

signature_algorithms:
```

`minimum_version` SHALL NOT be greater than `maximum_version`.

Defaults SHALL be

```yaml
minimum_version: TLSv1.2

maximum_version: TLSv1.3
```

Cipher suites and signature algorithms, when configured, SHALL use IANA names and SHALL be compatible with the enabled protocol versions.

---

# Validation Configuration

Validation configuration SHALL support

```yaml
policy:

hostname_verification:

trust_store_profile:

check_revocation:
```

Supported policy values

```
strict

report_only

disabled
```

`strict` SHALL require a trusted chain and hostname match.

`report_only` SHALL complete validation and report failures without rejecting the connection.

`disabled` SHALL be explicitly set, SHALL produce `validation.status: not_checked`, and SHOULD require assessment policy authorization.

---

# Timeout Configuration

Timeout configuration MAY include

```yaml
connect_ms:

handshake_ms:

validation_ms:

total_ms:
```

Timeouts SHALL be positive integers in milliseconds.

`total_ms` SHALL be at least each component timeout.

---

# Retry Configuration

Retry configuration MAY include

```yaml
max_attempts:

retryable_categories:
```

`max_attempts` SHALL be an integer from 1 through 5.

Retries MAY occur for transient network and timeout failures when configured.

Retries SHALL NOT occur for certificate, hostname, policy, or client-authentication failures.

---

# Session Configuration

Session configuration MAY include

```yaml
reuse_enabled:

isolation_scope:
```

`isolation_scope` SHALL be one of

```
connection

task

assessment
```

Session reuse SHALL be disabled across assessments.

---

# Evidence Configuration

Evidence configuration SHALL support

```yaml
mode:
```

Supported evidence modes

```
none

summary

full_handshake_metadata
```

`summary` SHALL be the default.

`none` MAY be used only if assessment policy permits and SHALL still emit minimal operational audit metadata.

---

# Adapter Selection

An adapter MAY be selected by an opaque `adapter_profile`.

Consumers SHALL NOT select a concrete TLS library.

Adapter profiles SHALL declare supported protocol versions, extensions, and validation capabilities.

---

# Security Requirements

TLS configuration SHALL

- Default to secure protocol versions
- Require explicit validation policy
- Avoid hidden validation bypasses
- Prevent cross-assessment session reuse
- Avoid embedding secret material
- Preserve auditability

---

# Validation Rules

A valid TLS configuration SHALL

- Resolve before network activity
- Use supported protocol versions
- Use a valid validation policy
- Use positive timeout values
- Keep retry policy bounded
- Keep session reuse within isolation scope
- Use an allowed evidence mode

---

# Future Extensions

Future versions MAY support

- Adapter capability negotiation
- Per-target trust profiles
- Certificate-pinning policy
- OCSP and CRL policy profiles
- QUIC/TLS configuration

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TLS Client Configuration Model provides deterministic, auditable, secure-by-default configuration for TLS operations across the Robust PenTest Platform.

It enables consistent TLS behavior while preserving policy control, adapter independence, and evidence traceability.
