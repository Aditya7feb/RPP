# Authentication Shared Skill

**File:** `skills/shared/authentication/README.md`

**Version:** 1.0.0

---

# Purpose

The Authentication Shared Skill provides a centralized mechanism for acquiring, managing, refreshing, and applying authentication credentials across the Robust PenTest Platform (RPP).

It abstracts authentication mechanisms from domain skills, enabling consistent, secure, and reusable authentication workflows.

Domain skills SHALL delegate authentication responsibilities to this shared skill.

---

# Goals

The Authentication Shared Skill SHALL

- Centralize authentication logic
- Reuse authenticated sessions
- Support multiple authentication mechanisms
- Protect sensitive credentials
- Enable credential rotation
- Maintain auditability
- Integrate with the platform execution model

---

# Non-Goals

The Authentication Shared Skill SHALL NOT

- Detect authentication vulnerabilities
- Perform authorization testing
- Manage business logic permissions
- Store secrets in plaintext
- Replace identity providers

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

Authentication Shared Skill

├── Credential Resolver
├── Session Manager
├── Token Manager
├── Profile Resolver
└── Secret Provider

↓

HTTP Client
```

---

# Responsibilities

The Authentication Shared Skill is responsible for

- Resolving authentication profiles
- Acquiring credentials
- Managing session state
- Refreshing expiring credentials
- Applying authentication to requests
- Protecting sensitive information
- Recording authentication events

---

# Authentication Lifecycle

```
Resolve Profile

↓

Acquire Credentials

↓

Validate

↓

Establish Session

↓

Apply Authentication

↓

Refresh (if required)

↓

Expire Session

↓

Cleanup
```

---

# Supported Authentication Mechanisms

The Authentication Shared Skill SHOULD support

## Basic Authentication

- Username
- Password

---

## Bearer Token

- Static Tokens
- Access Tokens

---

## OAuth 2.0

- Client Credentials
- Authorization Code
- Device Code
- Refresh Token

---

## API Keys

- Header
- Query Parameter
- Cookie

---

## Session Cookies

- Login Session
- Persistent Session

---

## Client Certificates

- Mutual TLS (mTLS)
- X.509 Certificates

---

## Custom Authentication

Organizations MAY implement custom authentication providers.

---

# Authentication Profiles

Authentication SHALL be represented using reusable profiles.

Example

```yaml
profile:
  id: cms-admin
  type: oauth2
```

Profiles SHALL be referenced by other skills.

---

# Credential Sources

Credentials MAY originate from

- Secret Managers
- Environment Variables
- Assessment Configuration
- Runtime Parameters
- External Identity Providers

Sensitive values SHALL NOT be embedded directly in skill definitions.

---

# Session Management

The Authentication Shared Skill SHALL manage

- Session Cookies
- CSRF Tokens
- Refresh Tokens
- Session Expiration
- Session Renewal

Sessions SHALL remain isolated between assessments unless explicitly configured otherwise.

---

# Secret Handling

Sensitive information includes

- Passwords
- API Keys
- Client Secrets
- Private Keys
- Refresh Tokens
- Access Tokens

The Authentication Shared Skill SHALL

- Resolve secrets securely
- Prevent plaintext logging
- Redact sensitive values
- Avoid exposing credentials to consumers

---

# Integration Points

The Authentication Shared Skill integrates with

```
HTTP Client

↓

Browser

↓

Retry

↓

Evidence

↓

Logging

↓

Configuration Model
```

---

# Outputs

Successful authentication MAY produce

- Authentication Context
- Access Token
- Session Identifier
- Cookie Store
- CSRF Token
- Expiration Metadata

Consumers SHALL receive only the information required for execution.

---

# Security Principles

The Authentication Shared Skill SHALL

- Follow least privilege
- Minimize credential exposure
- Support credential rotation
- Prevent credential leakage
- Support secure secret storage
- Maintain auditability

---

# Observability

Authentication events SHOULD include

- Authentication Started
- Authentication Succeeded
- Authentication Failed
- Session Created
- Session Refreshed
- Session Expired
- Credential Rotated

Sensitive information SHALL be excluded from logs and events.

---

# Dependencies

The Authentication Shared Skill depends on

- Configuration Model
- Execution Model
- Error Handling
- Logging
- Evidence
- HTTP Client (for HTTP-based authentication flows)

---

# Best Practices

Consumers SHOULD

- Reuse authentication profiles
- Reuse sessions where appropriate
- Allow automatic token refresh
- Store credentials in approved secret providers
- Avoid embedding credentials in requests

---

# Anti-Patterns

Consumers SHOULD NOT

- Hard-code passwords
- Duplicate login logic
- Re-authenticate unnecessarily
- Store credentials in evidence
- Log secrets
- Bypass shared authentication

---

# Future Extensions

Future versions MAY support

- OpenID Connect (OIDC)
- Kerberos
- NTLM
- SAML
- WebAuthn
- Hardware Security Modules (HSM)
- Federated Identity Providers

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Authentication Shared Skill provides a secure, reusable, and implementation-independent authentication service for all consumers within the Robust PenTest Platform.

It enables consistent credential management, session reuse, and secure authentication workflows while minimizing credential exposure and promoting platform-wide interoperability.