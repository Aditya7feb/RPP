# Authentication Interface

**File:** `skills/shared/authentication/interface.md`

**Version:** 1.0.0

---

# Purpose

The Authentication Interface defines the canonical contract through which platform components interact with the Authentication Shared Skill.

It standardizes authentication requests, session operations, token management, and authentication context retrieval while remaining independent of any authentication mechanism or identity provider.

All consumers SHALL interact exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Typed
- Mechanism Independent
- Versioned
- Observable
- Secure
- Backward Compatible

---

# Relationship

```
Master Agent

↓

Workflow

↓

Domain Skill

↓

Authentication Interface

↓

Authentication Shared Skill

↓

Identity Provider / Secret Store / HTTP Client
```

Consumers SHALL NOT communicate directly with identity providers or secret stores.

---

# Interface Overview

The interface consists of

```
Metadata

↓

Authentication Request

↓

Execution Options

↓

Execution Context

↓

Authentication Context

↓

Errors

↓

Evidence

↓

Metrics
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Authentication Request

Every request SHALL include

```yaml
operation:

profile:

options:
```

---

## Supported Operations

The Authentication Shared Skill SHALL support

```
authenticate

reauthenticate

session.create

session.resume

session.refresh

session.invalidate

token.issue

token.refresh

token.validate

token.revoke

context.validate
```

---

# Authentication Profile

Authentication SHALL reference a reusable profile.

Example

```yaml
profile:

  id: cms-admin
```

Consumers SHALL NOT provide raw credentials.

---

# Execution Options

Optional execution settings MAY include

```yaml
force_reauthentication:

allow_session_reuse:

allow_token_refresh:

validate_only:
```

Execution options influence behavior without modifying the authentication profile.

---

# Execution Context

The interface SHALL accept execution context.

Example

```yaml
assessment:

workflow:

variables:

existing_session:

existing_context:
```

Execution context SHALL remain read-only.

---

# Authentication Context

Successful authentication SHALL return a normalized Authentication Context.

Example

```yaml
authentication_context:

  context_id:

  authentication_type:

  identity:

  session_reference:

  credential_reference:

  expires_at:

  state:
```

Consumers SHALL depend only on this object.

---

## Identity

Identity metadata MAY include

```yaml
subject:

username:

tenant:

roles:
```

Sensitive attributes SHALL be omitted unless explicitly required.

---

## Session Reference

Example

```yaml
session_reference:

  session_id:

  cookie_store:

  csrf_reference:
```

Session internals SHALL remain opaque to consumers.

---

## Credential Reference

Example

```yaml
credential_reference:

  provider:

  reference:

  expires_at:
```

Credential values SHALL NOT be exposed.

---

# Token Metadata

Where applicable, token metadata MAY include

```yaml
issuer:

audience:

issued_at:

expires_at:

scopes:
```

Raw tokens SHALL only be exposed when execution requires them.

---

# Session Operations

Session operations SHALL return

```yaml
session_id:

status:

expires_at:
```

Session storage SHALL remain internal to the Authentication Shared Skill.

---

# Validation Response

Validation operations SHALL return

```yaml
valid:

reason:

expires_at:
```

---

# Evidence

Authentication operations SHALL expose structured evidence.

Evidence MAY include

- Authentication mechanism
- Profile identifier
- Session identifier (redacted)
- Authentication timestamps
- Policy decisions

Secrets SHALL NEVER appear in evidence.

---

# Metrics

Authentication metrics MAY include

```yaml
authentication_duration:

session_reuse:

token_refreshes:

credential_resolution_time:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to

```
skills/core/error-handling.md
```

Typical categories include

- Validation
- Authentication
- Authorization
- Configuration
- Secret Resolution
- Session
- Token
- Policy

---

# Security Requirements

The Authentication Interface SHALL

- Never expose plaintext secrets
- Never expose secret provider internals
- Redact sensitive values
- Enforce policy restrictions
- Minimize credential visibility

---

# Compatibility

Consumers SHALL remain independent of

- OAuth2
- API Keys
- Basic Authentication
- Cookie Authentication
- Client Certificates
- Future authentication mechanisms

The Authentication Context SHALL remain stable across implementations.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL include

- Metadata
- Authentication Request
- Authentication Profile
- Execution Context
- Authentication Context
- Error Handling
- Evidence

---

# Quality Requirements

The Authentication Interface SHALL

✓ Be mechanism independent

✓ Produce normalized Authentication Contexts

✓ Protect sensitive credentials

✓ Support session reuse

✓ Support token lifecycle operations

✓ Preserve observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY support

- Federated identities
- Delegated authentication
- Hardware-backed credentials
- Risk-based authentication
- Passwordless authentication
- Identity federation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Authentication Interface provides a stable, implementation-independent contract through which all platform components perform authentication operations.

It enables consistent credential management, session handling, and authentication workflows while abstracting identity-provider complexity and protecting sensitive information.