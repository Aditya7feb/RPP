# Authentication Capability Model

**File:** `skills/shared/authentication/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical capabilities provided by the Authentication Shared Skill.

Capabilities represent reusable authentication operations that may be composed by domain skills, shared skills, workflows, and agents throughout the Robust PenTest Platform (RPP).

Capabilities describe **what** the Authentication Shared Skill can perform, not **how** those operations are implemented.

---

# Design Principles

Authentication capabilities SHALL be

- Reusable
- Composable
- Stateless where possible
- Secure
- Observable
- Implementation Independent

---

# Capability Categories

```
Profile Management

↓

Credential Resolution

↓

Authentication

↓

Session Management

↓

Token Management

↓

Authorization Context

↓

Secret Resolution

↓

Evidence

↓

Observability
```

---

# Capability Registry

---

## Profile Management

### auth.profile.resolve

Resolve an authentication profile from the configured source.

#### Responsibilities

- Locate profile
- Validate profile
- Resolve configuration
- Return normalized profile

#### Inputs

- Profile ID

#### Outputs

- Authentication Profile

---

### auth.profile.validate

Validate an authentication profile before execution.

Checks MAY include

- Required fields
- Supported authentication type
- Secret references
- Policy compliance

---

# Credential Resolution

### auth.credentials.resolve

Resolve credentials referenced by an authentication profile.

Credential sources MAY include

- Secret Manager
- Environment Variables
- Runtime Parameters
- Assessment Configuration

Credentials SHALL NOT be returned in plaintext unless required for execution.

---

### auth.credentials.validate

Validate resolved credentials.

Examples

- Required values present
- Certificate integrity
- Token format
- Secret availability

---

# Authentication

### auth.authenticate

Authenticate using the configured mechanism.

Supported mechanisms MAY include

- Basic
- OAuth2
- API Key
- Cookie
- Client Certificate
- Custom Provider

Output SHALL be a normalized Authentication Context.

---

### auth.reauthenticate

Re-establish authentication after expiration or failure.

This capability MAY

- Refresh tokens
- Renew sessions
- Perform a new login

---

# Session Management

### auth.session.create

Create a new authenticated session.

Outputs MAY include

- Cookie Store
- CSRF Tokens
- Session Identifier
- Expiration

---

### auth.session.resume

Resume an existing session.

The session SHALL be validated before reuse.

---

### auth.session.refresh

Refresh an active session.

Refresh MAY include

- Cookie renewal
- Session extension
- Token refresh

---

### auth.session.invalidate

Invalidate an existing session.

Examples

- Logout
- Token revocation
- Cookie cleanup

---

# Token Management

### auth.token.issue

Obtain an access token.

Supported flows MAY include

- OAuth2 Client Credentials
- Authorization Code
- Device Code
- Custom Providers

---

### auth.token.refresh

Refresh an access token.

Refresh SHALL preserve associated session state where appropriate.

---

### auth.token.validate

Validate

- Expiration
- Signature (where applicable)
- Audience
- Issuer
- Required claims

---

### auth.token.revoke

Invalidate an issued token where supported.

---

# Authorization Context

### auth.context.build

Construct a normalized Authentication Context.

The context MAY include

- Identity
- Authentication Type
- Session Reference
- Expiration
- Active Credentials
- Security Metadata

Consumers SHALL depend only on the Authentication Context.

---

### auth.context.validate

Verify that an Authentication Context is still valid.

Checks MAY include

- Expiration
- Revocation
- Session validity
- Policy compliance

---

# Secret Resolution

### auth.secret.resolve

Resolve secrets from an approved secret provider.

The Authentication Shared Skill SHALL never expose provider-specific APIs.

---

### auth.secret.rotate

Support credential rotation.

Rotation MAY occur

- Automatically
- On policy trigger
- On explicit request

---

# Evidence

### auth.evidence.capture

Capture authentication-related evidence.

Evidence MAY include

- Authentication mechanism
- Session identifier (redacted)
- Token metadata (non-sensitive)
- Authentication timestamps
- Policy decisions

Secrets SHALL NEVER be captured as evidence.

---

# Observability

### auth.events.publish

Publish authentication lifecycle events.

Examples

- Authentication Started
- Authentication Completed
- Authentication Failed
- Session Created
- Session Refreshed
- Session Expired
- Token Refreshed

---

### auth.metrics.collect

Collect operational metrics.

Examples

- Authentication latency
- Token refresh count
- Session reuse count
- Authentication failures
- Credential resolution latency

---

# Capability Composition

Example dependency graph

```
Domain Skill

↓

auth.authenticate

├── auth.profile.resolve
├── auth.credentials.resolve
├── auth.session.create
├── auth.context.build
└── auth.evidence.capture
```

Capabilities SHOULD compose rather than duplicate functionality.

---

# Dependency Relationships

The Authentication Shared Skill depends on

- Configuration Model
- Error Handling
- Execution Model
- Logging
- Evidence

HTTP-based authentication flows MAY additionally depend on

- HTTP Client

Browser-based authentication flows MAY additionally depend on

- Browser

---

# Constraints

Authentication capabilities SHALL NOT

- Persist plaintext credentials
- Expose implementation-specific credential formats
- Bypass platform policy
- Leak secrets through logs or evidence

---

# Versioning

Capability identifiers SHALL remain stable across minor releases.

Breaking capability changes SHALL require a major version increment.

---

# Validation Rules

A compliant implementation SHALL

- Publish all supported capabilities
- Produce normalized Authentication Contexts
- Preserve implementation independence
- Protect sensitive credentials
- Capture required evidence

---

# Quality Requirements

The Authentication Capability Model SHALL

✓ Support multiple authentication mechanisms

✓ Produce normalized outputs

✓ Protect sensitive information

✓ Enable session reuse

✓ Support credential rotation

✓ Integrate with platform observability

✓ Remain implementation independent

---

# Future Extensions

Future versions MAY introduce capabilities for

- OpenID Connect (OIDC)
- SAML
- Kerberos
- NTLM
- WebAuthn
- Hardware-backed credentials
- Federated identity providers

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Authentication Capability Model provides a standardized set of reusable authentication operations that can be composed by any consumer within the Robust PenTest Platform.

It enables secure, consistent, and extensible authentication workflows while remaining independent of specific authentication protocols or credential providers.