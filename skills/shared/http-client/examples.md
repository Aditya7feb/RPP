# HTTP Client Examples

**File:** `skills/shared/http-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides illustrative examples of how the HTTP Client Shared Skill is used by domain skills, workflows, and agents within the Robust PenTest Platform (RPP).

Examples demonstrate interface usage, configuration, execution patterns, evidence generation, and error handling.

All examples are conceptual and implementation independent.

---

# Example 1 — Simple GET Request

## Scenario

A Recon skill retrieves the homepage of a target.

### Request

```yaml
metadata:
  request_id: req-001
  assessment_id: asm-001
  task_id: task-001
  skill_id: recon.http

request:
  method: GET
  url: https://example.com
```

### Expected Response

```yaml
status_code: 200

headers:
  content-type: text/html

body:
  "<html>...</html>"
```

---

# Example 2 — JSON API Request

## Scenario

A GraphQL discovery skill queries an API endpoint.

### Request

```yaml
request:
  method: POST

  url: https://api.example.com/graphql

  headers:
    Content-Type: application/json

  body:
    query: |
      {
        __schema {
          types {
            name
          }
        }
      }
```

---

# Example 3 — Multipart File Upload

## Scenario

A File Upload skill tests multipart handling.

### Request

```yaml
request:
  method: POST

  url: https://example.com/upload

  body:
    multipart:
      - field: file
        filename: test.txt

      - field: description
        value: sample
```

---

# Example 4 — Authenticated Request

## Scenario

A CMS skill reuses an authenticated session.

### Request

```yaml
authentication:
  profile: cms-admin

session:
  id: session-001

request:
  method: GET

  url: https://example.com/admin
```

The HTTP Client resolves credentials using the shared Authentication Skill.

---

# Example 5 — Custom Headers

## Scenario

Every outbound request includes organizational headers.

```yaml
headers:

  User-Agent: RPP

  X-RPP-Assessment: asm-001

  X-RPP-Trace: req-001
```

---

# Example 6 — Proxy Configuration

## Scenario

Traffic is routed through an assessment proxy.

```yaml
configuration:

  proxy_enabled: true

  proxy_profile: corp-proxy
```

The HTTP Client resolves the proxy configuration before transport selection.

---

# Example 7 — Redirect Handling

## Scenario

A target redirects multiple times.

```text
Target

↓

302

↓

301

↓

200
```

Returned response

```yaml
redirect_chain:

  - from: /
    to: /login

  - from: /login
    to: /dashboard
```

---

# Example 8 — Retry

## Scenario

A temporary network failure occurs.

```text
Attempt 1

↓

Timeout

↓

Retry Skill

↓

Attempt 2

↓

200 OK
```

Retry decisions are delegated to the shared Retry capability.

---

# Example 9 — TLS Inspection

## Scenario

A TLS skill requests certificate metadata.

Returned TLS information

```yaml
tls:

  protocol: TLS1.3

  cipher_suite: TLS_AES_256_GCM_SHA384

  certificate_chain:
    - leaf
    - intermediate
    - root
```

---

# Example 10 — Evidence Collection

Evidence generated during execution

```yaml
evidence:

  request:

  response:

  timing:

  tls:

  redirect_chain:
```

Evidence conforms to the canonical Evidence schema.

---

# Example 11 — Parallel Execution

## Scenario

A Content Discovery skill scans multiple endpoints concurrently.

```text
/api

├── /login

├── /admin

├── /graphql

└── /health
```

Each request executes independently while respecting

- Rate limits
- Transport limits
- Organizational policy

---

# Example 12 — Streaming Download

## Scenario

A large file is downloaded.

```yaml
configuration:

  stream: true
```

Streaming preserves

- Evidence
- Metrics
- Execution context

---

# Example 13 — Timeout

Returned error

```yaml
category: Timeout

retryable: true

recoverable: true
```

The Retry capability determines whether another attempt should be made.

---

# Example 14 — Transport Independence

The caller uses the same interface regardless of transport.

```text
Domain Skill

↓

HTTP Client Interface

↓

httpx Adapter
```

or

```text
Domain Skill

↓

HTTP Client Interface

↓

Playwright Adapter
```

No changes are required in the calling skill.

---

# Example 15 — Skill Composition

Example dependency graph

```text
GraphQL Skill

↓

HTTP Client

├── Authentication

├── Retry

├── Rate Limiter

├── Evidence

└── Transport
```

The GraphQL skill does not implement HTTP functionality itself.

---

# Best Practices

Skills SHOULD

- Use shared authentication profiles
- Use shared retry policies
- Reference shared proxy profiles
- Preserve evidence
- Validate requests before execution
- Use normalized responses only

---

# Anti-Patterns

Skills SHOULD NOT

- Build HTTP clients internally
- Perform manual retry loops
- Embed credentials directly
- Parse transport-specific objects
- Depend on adapter implementations
- Duplicate session management

---

# Validation Checklist

A compliant consumer

✓ Uses the HTTP Client Interface

✓ Uses normalized request objects

✓ Uses normalized response objects

✓ Preserves evidence

✓ Uses shared authentication

✓ Uses shared retry

✓ Remains transport independent

---

# Success Criteria

A compliant consumer interacts with the HTTP Client exclusively through its published interface, allowing reusable, observable, and implementation-independent HTTP communication throughout the Robust PenTest Platform.