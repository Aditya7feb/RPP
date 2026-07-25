# Master Agent Examples

**File:** `agents/master/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides reference execution examples for the Master Agent.

These examples are illustrative and demonstrate expected behavior. They are not implementation-specific and should not be interpreted as executable workflows.

---

# Example 1 - Basic Web Application Assessment

## Scope

```
https://example.com
```

## Assessment Flow

```
Assessment Created

↓

Planning

↓

Recon

↓

Technology Detection

↓

Content Discovery

↓

Scanner Selection

↓

Parallel Scanning

↓

Evidence Correlation

↓

Report Generation
```

## Delegation

| Capability | Assigned Agent |
|------------|----------------|
| DNS Enumeration | DNS Agent |
| Port Discovery | Port Agent |
| TLS Analysis | TLS Agent |
| Technology Detection | Fingerprinting Agent |
| Content Discovery | Content Discovery Agent |

---

# Example 2 - Technology Driven Scanning

Recon discovers

```
React

NGINX

JWT Authentication
```

Master Agent schedules

```
React Agent

↓

JWT Agent

↓

Security Header Agent

↓

CSP Agent

↓

API Discovery Agent
```

The Master Agent SHALL avoid scheduling unrelated scanners such as

- WordPress Agent
- Drupal Agent
- IIS Agent

---

# Example 3 - Dynamic Replanning

Initial execution

```
Recon

↓

Content Discovery
```

Content Discovery discovers

```
/graphql
```

Master Agent immediately adds

```
GraphQL Discovery Agent

↓

GraphQL Scanner

↓

Introspection Agent
```

The assessment SHALL continue without restarting the execution plan.

---

# Example 4 - Parallel Execution

Independent work

```
DNS

TLS

Port Scan

HTTP Fingerprinting
```

These tasks execute simultaneously.

Dependent work

```
Technology Detection

↓

Technology-specific Scanners
```

must wait until fingerprinting completes.

---

# Example 5 - Duplicate Finding Merge

Agent A reports

```
Reflected XSS

/login?q=
```

Agent B reports

```
Reflected Cross Site Scripting

/login?q=
```

Expected behavior

- One finding
- Combined evidence
- Confidence increased
- Both agents credited

---

# Example 6 - Conflicting Findings

JWT Agent

```
Algorithm Confusion Possible
```

Validation Agent

```
Unable to Reproduce
```

Master Agent

- Preserves both findings
- Lowers confidence
- Requests additional review if justified
- Does not discard evidence

---

# Example 7 - Human Approval

Scanner reports

```
Possible SQL Injection
```

Confidence

```
HIGH
```

Master Agent

```
Pause

↓

Approval Request

↓

Approved

↓

Validation Agent

↓

VERIFIED
```

If approval is rejected

```
Finding remains

UNVERIFIED
```

---

# Example 8 - Failure Recovery

TLS Agent

```
Timeout
```

Master Agent

```
Retry

↓

Success
```

If retries exceed policy

```
Mark Failed

↓

Continue Remaining Assessment
```

The assessment SHALL not terminate unless the failure prevents further execution.

---

# Example 9 - Scope Violation

Content Discovery identifies

```
https://external.example.org
```

Rules of Engagement

```
Only example.com
```

Master Agent

- Rejects the task
- Records the attempted discovery
- Does not delegate external scanning

---

# Example 10 - Final Assessment

Assessment completes with

```
Technologies

- React
- NGINX
- JWT

Attack Surface

- 12 Endpoints
- 3 APIs
- 4 JavaScript Files

Findings

- 1 Critical
- 2 High
- 5 Medium
- 3 Low

Validated

- 2

Evidence

- 147 Artifacts
```

The Master Agent requests report generation only after verifying

- Assessment complete
- Evidence complete
- Confidence calculated
- Findings merged
- Approval workflow complete

---

# Expected Characteristics

A compliant Master Agent should

- Delegate rather than execute
- Adapt to new discoveries
- Preserve all evidence
- Respect dependencies
- Avoid duplicate work
- Require approval where necessary
- Produce deterministic outputs
- Maintain a complete audit trail

---

# Common Anti-Patterns

The following behaviors are considered incorrect

❌ Running specialist tools directly

❌ Reporting findings without evidence

❌ Ignoring Rules of Engagement

❌ Running validation without approval

❌ Repeating completed tasks

❌ Discarding conflicting evidence

❌ Merging unrelated findings

❌ Trusting tool output without verification

---

# Success Criteria

The examples in this document should be reproducible by any compliant implementation of the Master Agent, regardless of the underlying runtime, framework, or programming language.