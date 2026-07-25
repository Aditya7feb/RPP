# Authentication Configuration

**File:** `skills/shared/authentication/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration parameters supported by the Authentication Shared Skill.

It extends the platform-wide configuration model defined in:

```
skills/core/configuration-model.md
```

Authentication configuration specifies how authentication profiles, credential providers, session behavior, and token lifecycle are configured without exposing implementation details.

---

# Relationship

```
Platform Configuration

↓

Authentication Configuration

↓

Authentication Shared Skill

↓

Identity Provider / Secret Store
```

---

# Design Principles

Authentication configuration SHALL be

- Secure
- Declarative
- Provider Independent
- Immutable During Execution
- Policy Aware
- Auditable

---

# Configuration Categories

Authentication configuration is organized into

```
Profiles

↓

Credential Resolution

↓

Session Management

↓

Token Management

↓

Secret Providers

↓

Policy

↓

Observability
```

---

# Authentication Profiles

## default_profile

Default authentication profile used when none is explicitly specified.

Type

```
Reference
```

Example

```yaml
default_profile: anonymous
```

---

## allow_profile_override

Allow execution requests to override the configured profile.

Type

```
Boolean
```

Default

```
true
```

---

# Credential Resolution

## credential_provider

Default credential provider.

Supported values MAY include

```
Secret Manager

Environment Variables

Vault

Runtime Parameters

Assessment Configuration
```

---

## cache_credentials

Cache resolved credentials for the duration of execution.

Type

```
Boolean
```

Default

```
true
```

---

## credential_cache_ttl

Credential cache lifetime.

Type

```
Duration
```

Default

```
15m
```

---

# Session Management

## enable_session_reuse

Reuse authenticated sessions when possible.

Type

```
Boolean
```

Default

```
true
```

---

## session_timeout

Maximum session lifetime.

Type

```
Duration
```

Default

```
30m
```

---

## auto_refresh_session

Automatically refresh active sessions before expiration.

Type

```
Boolean
```

Default

```
true
```

---

## isolate_sessions

Prevent session sharing across assessments.

Type

```
Boolean
```

Default

```
true
```

---

# Token Management

## auto_refresh_tokens

Automatically refresh access tokens.

Type

```
Boolean
```

Default

```
true
```

---

## refresh_before_expiry

Time before expiration when refresh should occur.

Type

```
Duration
```

Default

```
5m
```

---

## validate_tokens

Validate token metadata before use.

Type

```
Boolean
```

Default

```
true
```

---

## revoke_on_completion

Revoke tokens after assessment completion when supported.

Type

```
Boolean
```

Default

```
false
```

---

# Secret Providers

## secret_provider

Reference to the platform secret provider.

Type

```
Reference
```

Examples

```
azure-keyvault

hashicorp-vault

aws-secrets-manager
```

---

## allow_environment_secrets

Permit environment variables as a credential source.

Type

```
Boolean
```

Default

```
false
```

---

## redact_secret_values

Redact sensitive values in logs, evidence, and metrics.

Type

```
Boolean
```

Default

```
true
```

---

# Policy

## maximum_login_attempts

Maximum authentication attempts before failure.

Type

```
Integer
```

Default

```
3
```

---

## lock_profile_after_failure

Temporarily disable a profile after repeated failures.

Type

```
Boolean
```

Default

```
false
```

---

## allow_fallback_profiles

Permit fallback to alternate authentication profiles.

Type

```
Boolean
```

Default

```
false
```

---

## permitted_authentication_types

Restrict supported authentication mechanisms.

Type

```
Array<String>
```

Example

```yaml
- oauth2
- api-key
- mtls
```

---

# Observability

## publish_authentication_events

Publish authentication lifecycle events.

Type

```
Boolean
```

Default

```
true
```

---

## capture_authentication_metrics

Collect operational metrics.

Type

```
Boolean
```

Default

```
true
```

---

## capture_session_events

Record session lifecycle events.

Type

```
Boolean
```

Default

```
true
```

---

# Evidence

## preserve_authentication_metadata

Capture authentication metadata as evidence.

Type

```
Boolean
```

Default

```
true
```

---

## preserve_token_metadata

Store non-sensitive token metadata.

Type

```
Boolean
```

Default

```
true
```

---

## preserve_session_metadata

Store non-sensitive session metadata.

Type

```
Boolean
```

Default

```
true
```

---

# Security Constraints

Implementations SHALL

- Never persist plaintext credentials
- Redact secrets
- Validate referenced profiles
- Validate provider compatibility
- Respect platform policy
- Isolate authentication state between assessments unless explicitly permitted

---

# Configuration Dependencies

The Authentication Shared Skill integrates with

```
Configuration Model

↓

Secret Providers

↓

Logging

↓

Evidence

↓

HTTP Client (for HTTP-based flows)

↓

Browser (for interactive flows)
```

---

# Validation Rules

A compliant configuration SHALL

- Validate profile references
- Validate provider references
- Validate timeout values
- Validate token policies
- Reject conflicting settings
- Reject unsupported authentication types

---

# Quality Requirements

The Authentication Configuration SHALL

✓ Be provider independent

✓ Protect secrets

✓ Support reusable profiles

✓ Enable secure session reuse

✓ Integrate with platform policy

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY support

- Hardware-backed credentials
- Dynamic provider selection
- Risk-based authentication
- Multi-factor authentication (MFA)
- Passwordless authentication
- Federated identity providers

---

# Success Criteria

A compliant Authentication Configuration provides a secure, reusable, and provider-independent mechanism for configuring authentication behavior across the Robust PenTest Platform.

It enables consistent profile management, credential resolution, session lifecycle management, and policy enforcement while protecting sensitive information.