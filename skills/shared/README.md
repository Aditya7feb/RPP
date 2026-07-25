# Shared Skills

**File:** `skills/shared/README.md`

**Version:** 1.0.0

---

# Purpose

Shared Skills provide reusable capabilities that are consumed by multiple domain-specific skills within the Robust PenTest Platform (RPP).

Unlike domain skills, shared skills are not responsible for identifying vulnerabilities or producing security findings directly. Instead, they encapsulate common functionality such as HTTP communication, browser automation, authentication, parsing, evidence management, and reporting.

The shared layer minimizes duplication, standardizes behavior, and simplifies maintenance.

---

# Design Principles

Shared skills SHALL be

- Reusable
- Stateless where practical
- Well-defined
- Independently testable
- Capability-focused
- Technology agnostic
- Platform independent

Shared skills SHALL avoid domain-specific security logic.

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

Shared Skill

↓

Tool

↓

Target
```

---

# Responsibilities

Shared skills are responsible for

- Common execution logic
- Protocol handling
- Data parsing
- Authentication
- Evidence management
- Reporting support
- Retry logic
- Rate limiting
- Session handling

They SHALL NOT determine whether a vulnerability exists.

---

# Domain Skills vs Shared Skills

| Domain Skill | Shared Skill |
|--------------|--------------|
| SQL Injection | HTTP Client |
| XSS | Browser |
| TLS Analysis | Certificate Parser |
| GraphQL | JSON Parser |
| JWT | JWT Decoder |
| DNS | DNS Resolver |

---

# Shared Skill Categories

The following categories are recommended.

```
HTTP

Browser

Authentication

Parsers

Encoding

Evidence

Reporting

Networking

Utilities

Rate Limiting

Retry

Session

Caching

Logging
```

---

# Recommended Repository Structure

```
skills/

shared/

    http-client/

    browser/

    authentication/

    dns-client/

    tls-client/

    parsers/

        html/

        javascript/

        json/

        xml/

        graphql/

    encoding/

        base64/

        url/

        jwt/

    retry/

    rate-limiter/

    evidence/

    reporting/

    logging/

    cache/

    utilities/
```

---

# Dependency Rules

Domain skills SHOULD depend on shared skills.

Shared skills SHOULD NOT depend on domain skills.

This ensures a directed dependency graph.

```
Shared

↓

Domain

✗ Invalid
```

---

# Capability Ownership

Every shared skill SHALL expose one or more canonical capabilities.

Example

```
HTTP Client

↓

network.http.send

↓

Consumed By

TLS

GraphQL

SQLi

XSS

JWT

CMS

Recon
```

---

# Shared Skill Lifecycle

Shared skills SHALL follow the same lifecycle defined in

```
skills/core/lifecycle.md
```

No lifecycle variations are introduced.

---

# Execution Model

Shared skills SHALL implement the execution model defined in

```
skills/core/execution-model.md
```

---

# Interface Requirements

Shared skills SHALL implement the standard skill interface.

```
Metadata

↓

Input

↓

Execution

↓

Output

↓

Errors
```

---

# Error Handling

Shared skills SHALL return structured errors.

Errors SHALL conform to

```
skills/core/error-handling.md
```

---

# Confidence

Shared skills MAY assign confidence to observations they generate.

Final finding confidence SHALL remain the responsibility of domain skills and the Master Agent.

---

# Approval

Shared skills SHOULD NOT require approval.

Approval decisions SHALL normally occur at the domain skill level.

Exceptions MAY include

- Credential usage
- External service interaction
- Cloud resource modification

---

# Testing

Every shared skill SHOULD provide

- Unit tests
- Integration tests
- Mock execution examples
- Failure scenarios

---

# Versioning

Shared skills SHALL follow semantic versioning.

Breaking capability changes SHALL increment the major version.

---

# Documentation Requirements

Every shared skill SHOULD include

- README
- Capabilities
- Interface
- Examples
- Limitations
- Dependencies
- Troubleshooting

---

# Best Practices

Shared skills SHOULD

- Perform one responsibility well
- Expose reusable capabilities
- Hide implementation details
- Avoid side effects
- Preserve execution context
- Produce structured outputs

---

# Anti-Patterns

Shared skills SHOULD NOT

- Detect vulnerabilities
- Generate security findings
- Depend on domain skills
- Modify assessment scope
- Perform approval decisions
- Hardcode tool implementations

---

# Future Extensions

Future versions MAY include

- Distributed shared services
- Remote execution
- Shared capability caching
- Protocol adapters
- Multi-language implementations
- Capability marketplaces

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Shared Skills layer provides reusable, implementation-independent capabilities that eliminate duplication across domain skills while preserving consistency, maintainability, and interoperability throughout the Robust PenTest Platform.