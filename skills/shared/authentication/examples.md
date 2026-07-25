# Authentication Examples

**File:** `skills/shared/authentication/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides representative examples of how platform components interact with the Authentication Shared Skill.

The examples illustrate profile resolution, authentication context generation, session reuse, token lifecycle management, evidence generation, and error handling.

All examples are conceptual and implementation independent.

---

# Example 1 — Basic Authentication

## Scenario

A CMS skill authenticates using a Basic Authentication profile.

### Request

```yaml
metadata:
  request_id: req-001

operation: authenticate

profile:
  id: cms-basic
```

### Response

```yaml
authentication_context:
  context_id: auth-001

  authentication_type: basic

  state: authenticated
```

---

# Example 2 — OAuth2 Client Credentials

## Scenario

A GraphQL skill authenticates using OAuth2.

```yaml
operation: authenticate

profile:
  id: graphql-oauth
```

Returned Authentication Context

```yaml
authentication_context:

  authentication_type: oauth2

  expires_at: 2026-01-01T12:00:00Z
```

---

# Example 3 — API Key Authentication

## Scenario

A REST API requires an API Key.

```yaml
profile:
  id: payment-api
```

The Authentication Shared Skill resolves the API Key and applies it according to the profile configuration.

---

# Example 4 — Session Reuse

## Scenario

An authenticated CMS session already exists.

```yaml
operation: session.resume

profile:
  id: cms-admin
```

The shared skill validates the existing session before returning it.

---

# Example 5 — Token Refresh

## Scenario

An access token is approaching expiration.

```yaml
operation: token.refresh

profile:
  id: graph-api
```

The Authentication Context is updated without requiring consumer changes.

---

# Example 6 — Session Refresh

## Scenario

An authenticated browser session is nearing expiration.

```yaml
operation: session.refresh

profile:
  id: browser-admin
```

The session is renewed according to policy.

---

# Example 7 — Client Certificate Authentication

## Scenario

An internal service requires mutual TLS.

```yaml
profile:
  id: internal-mtls
```

The Authentication Shared Skill retrieves the client certificate and performs mutual authentication.

---

# Example 8 — Secret Resolution

## Scenario

Credentials are stored in an approved secret provider.

```yaml
credential_provider:
  azure-keyvault
```

The consumer never receives direct access to the underlying secret provider.

---

# Example 9 — Authentication Context

Example normalized Authentication Context

```yaml
authentication_context:

  context_id: auth-001

  identity:

    username: administrator

  authentication_type: oauth2

  session_reference:

    session_id: session-123

  expires_at: 2026-01-01T12:00:00Z

  state: authenticated
```

Consumers rely only on this object.

---

# Example 10 — HTTP Client Integration

```
HTTP Client

↓

Authentication Shared Skill

↓

Authentication Context

↓

HTTP Request
```

The HTTP Client never performs authentication directly.

---

# Example 11 — Browser Integration

```
Browser Skill

↓

Authentication Shared Skill

↓

Authenticated Browser Session
```

Browser automation reuses the same Authentication Context.

---

# Example 12 — Authentication Failure

Returned error

```yaml
category: Authentication

retryable: false

recoverable: false
```

The consumer receives a canonical authentication error.

---

# Example 13 — Provider Failure

Returned error

```yaml
category: Identity Provider

retryable: true
```

Provider-specific errors remain hidden.

---

# Example 14 — Session Expiration

```
Authenticated

↓

Expired

↓

Session Refresh

↓

Authenticated
```

The refresh process is transparent to consumers.

---

# Example 15 — Skill Composition

```
GraphQL Skill

↓

Authentication Shared Skill

├── Profile Resolution

├── Credential Resolution

├── Session Manager

├── Token Manager

└── Evidence
```

The GraphQL skill delegates all authentication responsibilities.

---

# Example 16 — Evidence

Authentication evidence

```yaml
evidence:

  authentication_type:

  profile:

  authentication_timestamp:

  session_reference:

  policy:
```

Sensitive information is redacted.

---

# Example 17 — Authentication Events

Generated events

```
AuthenticationStarted

↓

CredentialsResolved

↓

AuthenticationSucceeded

↓

SessionCreated

↓

AuthenticationCompleted
```

These events integrate with the platform execution state.

---

# Best Practices

Consumers SHOULD

- Use reusable authentication profiles
- Reuse Authentication Contexts
- Allow automatic token refresh
- Reuse active sessions
- Store credentials only in approved secret providers
- Capture authentication evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Embed credentials in skill definitions
- Perform manual login logic
- Refresh tokens independently
- Duplicate session management
- Log secrets
- Store plaintext credentials

---

# Validation Checklist

A compliant consumer

✓ Uses Authentication Profiles

✓ Uses the Authentication Interface

✓ Consumes Authentication Contexts

✓ Delegates session management

✓ Delegates token lifecycle management

✓ Preserves evidence

✓ Remains provider independent

---

# Success Criteria

A compliant consumer interacts with the Authentication Shared Skill exclusively through its published interface.

It delegates credential management, authentication, session lifecycle management, and token handling while relying only on normalized Authentication Contexts.