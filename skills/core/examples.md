# Skill Examples

**File:** `skills/core/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides reference examples demonstrating how the Skill Core specifications are applied when designing, implementing, and executing skills within the Robust PenTest Platform (RPP).

These examples are normative references intended to promote consistency across all skills.

Examples SHALL illustrate architectural patterns rather than implementation-specific code.

---

# Example Overview

This document demonstrates

- Skill Definition
- Capability Declaration
- Dependency Declaration
- Execution Context
- Execution Flow
- Error Handling
- Confidence Evaluation
- Approval Requirements
- Agent Response

---

# Example 1 — Passive HTTP Fingerprinting

## Purpose

Identify technologies used by a web application through passive observation.

---

## Skill Metadata

```yaml
id: skill.http.fingerprint

name: HTTP Fingerprinting

version: 1.0.0

category: Fingerprinting
```

---

## Capabilities

```yaml
provides:

- security.discovery.technology

- network.http.send

- analysis.headers.parse
```

---

## Dependencies

```yaml
requires:

- network.http.send

optional:

- analysis.javascript.parse
```

---

## Inputs

```yaml
target:

headers:

cookies:
```

---

## Outputs

```yaml
technologies:

evidence:

confidence:
```

---

## Execution Flow

```
Receive Target

↓

HTTP Request

↓

Parse Headers

↓

Identify Technologies

↓

Generate Evidence

↓

Return Agent Response
```

---

## Confidence

```
Evidence

↓

Headers

↓

Technology

↓

High Confidence
```

---

## Approval

Approval Required

```
None
```

Passive fingerprinting is considered a safe capability.

---

# Example 2 — SQL Injection Verification

## Purpose

Validate a previously identified SQL Injection candidate.

---

## Capabilities

```yaml
requires:

- security.validation.sqli.detect

provides:

- security.validation.sqli.verify
```

---

## Dependencies

```yaml
Finding

↓

Possible SQLi

↓

Verification
```

---

## Approval

Required

```
Operator Approval
```

Reason

```
Potentially state-changing requests
```

---

## Execution Flow

```
Receive Finding

↓

Validate Inputs

↓

Execute Verification

↓

Collect Evidence

↓

Determine Confidence

↓

Generate Finding
```

---

## Possible Outcomes

```
Verified

False Positive

Inconclusive
```

---

## Confidence

```
Verified Exploit

↓

Verified
```

---

# Example 3 — TLS Certificate Inspection

## Purpose

Analyze a server certificate and supported TLS configuration.

---

## Capabilities

```yaml
provides:

- network.tls.inspect

- network.tls.certificate.extract
```

---

## Inputs

```yaml
hostname:

port:
```

---

## Outputs

```yaml
certificate:

cipher_suites:

protocols:

evidence:
```

---

## Confidence

```
Certificate Retrieved Successfully

↓

Verified
```

Cryptographic validation provides deterministic evidence.

---

## Approval

```
None
```

---

# Example 4 — GraphQL Discovery

## Purpose

Discover GraphQL endpoints and supported features.

---

## Capabilities

```yaml
provides:

- security.api.graphql.enumerate
```

---

## Dependencies

```
HTTP Capability

↓

Endpoint Discovery
```

---

## Possible Results

- GraphQL Endpoint Found
- Introspection Enabled
- Introspection Disabled
- GraphQL Not Present

---

## Confidence

Multiple successful GraphQL requests increase confidence.

---

# Example 5 — Skill Failure

## Scenario

DNS resolution fails before execution.

---

## Error

```yaml
category: Network

severity: Error

recoverable: true
```

---

## Outcome

```
Retry

↓

Successful

↓

Continue Execution
```

Evidence SHALL be preserved across retries.

---

# Example 6 — Dependency Failure

## Scenario

Authentication is required but no session exists.

---

## Execution

```
Authentication Missing

↓

Dependency Failed

↓

Execution Skipped
```

---

## Agent Response

```yaml
status: Skipped

reason: Missing Dependency
```

---

# Example 7 — Confidence Aggregation

Three independent observations identify WordPress.

```
HTTP Headers

↓

Generator Tag

↓

Known Asset

↓

WordPress
```

Confidence

```
High
```

Multiple independent observations improve certainty.

---

# Example 8 — Approval Workflow

```
Discovery

↓

Potential Exploitation

↓

Approval Required

↓

Approved

↓

Execution Continues
```

Execution SHALL pause while awaiting approval.

---

# Example 9 — Dynamic Dependency Resolution

```
Technology Detection

↓

GraphQL

↓

New Task Created

↓

GraphQL Enumeration
```

The Execution Plan is updated dynamically.

---

# Example 10 — Complete Skill Lifecycle

```
Registered

↓

Selected

↓

Initialized

↓

Validated

↓

Prepared

↓

Executing

↓

Collecting Evidence

↓

Generating Results

↓

Completed

↓

Cleanup
```

This example demonstrates the standard lifecycle defined in `lifecycle.md`.

---

# Cross-Reference Matrix

| Example | Demonstrates |
|----------|--------------|
| Passive HTTP Fingerprinting | Capability declaration, confidence, passive execution |
| SQL Injection Verification | Dependencies, approval, verification |
| TLS Inspection | Deterministic evidence |
| GraphQL Discovery | Technology-driven execution |
| Skill Failure | Error handling and retry |
| Dependency Failure | Dependency model |
| Confidence Aggregation | Confidence model |
| Approval Workflow | Approval model |
| Dynamic Dependencies | Adaptive planning |
| Complete Lifecycle | Lifecycle model |

---

# Best Practices

Skill authors SHOULD

- Declare capabilities explicitly
- Define all dependencies
- Validate inputs before execution
- Produce structured outputs
- Preserve evidence
- Return structured errors
- Explain confidence decisions
- Respect approval requirements
- Avoid implementation-specific assumptions

---

# Anti-Patterns

Skill authors SHOULD NOT

- Hardcode dependencies
- Invent new capability names
- Return unstructured errors
- Modify execution context unexpectedly
- Discard collected evidence
- Bypass approval requirements
- Assume previous skills have executed

---

# References

This document complements

- `README.md`
- `skill-schema.md`
- `capability-model.md`
- `capability-registry.md`
- `lifecycle.md`
- `execution-model.md`
- `interface.md`
- `dependency-model.md`
- `error-handling.md`
- `confidence-model.md`
- `approval-model.md`

---

# Success Criteria

A compliant skill SHOULD resemble one or more examples in this document while adhering to the architectural contracts defined throughout the Skill Core specifications.

These examples provide a common reference for designing interoperable, observable, and maintainable skills within the Robust PenTest Platform.