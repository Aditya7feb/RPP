# Browser Error Model

**File:** `skills/shared/browser/error-model.md`

**Version:** 1.0.0

---

# Purpose

The Browser Error Model defines how browser automation failures are detected, classified, normalized, reported, and recovered within the Robust PenTest Platform (RPP).

It extends the platform-wide error framework defined in:

```
skills/core/error-handling.md
```

Browser-specific exceptions from Playwright, Selenium, WebDriver, CDP, or any future browser adapter SHALL be normalized into canonical Browser Errors.

---

# Design Principles

Browser errors SHALL be

- Deterministic
- Structured
- Observable
- Recoverable where appropriate
- Secure
- Framework Independent
- Browser Independent

---

# Error Lifecycle

```
Failure Detected

↓

Classify

↓

Normalize

↓

Capture Evidence

↓

Determine Recovery

↓

Publish Event

↓

Return Canonical Error
```

---

# Error Categories

Browser errors SHALL belong to one of the following categories.

| Category | Description |
|----------|-------------|
| Configuration | Invalid browser configuration |
| Browser | Browser launch or runtime failure |
| Context | Browser Context failure |
| Page | Page lifecycle failure |
| Navigation | Navigation failure |
| DOM | DOM interaction failure |
| JavaScript | Script execution failure |
| Storage | Cookie or storage failure |
| Network | Browser network failure |
| Evidence | Evidence collection failure |
| Authentication | Browser authentication integration failure |
| Timeout | Operation timeout |
| Resource | Resource exhaustion |
| Policy | Browser policy violation |
| Internal | Unexpected Browser Shared Skill failure |

---

# Canonical Error Structure

Every browser error SHALL expose

```yaml
error_id:

category:

code:

message:

severity:

recoverable:

retryable:

timestamp:

request_id:

browser_context:

page:

evidence:
```

---

# Configuration Errors

Examples

- Unsupported browser engine
- Invalid Browser Profile
- Invalid timeout configuration
- Invalid resource limits

Execution SHALL terminate before browser launch.

---

# Browser Errors

Examples

- Browser executable unavailable
- Browser startup failure
- Browser crash
- Browser disconnected

Browser implementation details SHALL be abstracted.

---

# Context Errors

Examples

- Context creation failure
- Context already closed
- Invalid Browser Context
- Context corruption

Browser Context identifiers SHALL remain opaque.

---

# Page Errors

Examples

- Page creation failure
- Page unexpectedly closed
- Popup handling failure
- Invalid page reference

Page identifiers SHALL remain implementation independent.

---

# Navigation Errors

Examples

- Navigation timeout
- Invalid URL
- Redirect limit exceeded
- Navigation interrupted

Navigation history SHOULD be preserved in evidence.

---

# DOM Errors

Examples

- Element not found
- Multiple matching elements
- Stale element reference
- Invalid selector

Selector implementation details SHOULD remain abstracted.

---

# JavaScript Errors

Examples

- Script timeout
- JavaScript exception
- Serialization failure
- Unsupported execution context

Stack traces MAY be captured in evidence when permitted.

---

# Storage Errors

Examples

- Cookie import failure
- Cookie export failure
- Local Storage unavailable
- IndexedDB unavailable

Sensitive storage contents SHALL NEVER be logged.

---

# Network Errors

Examples

- Request interception failure
- HAR generation failure
- WebSocket capture failure
- Resource loading failure

Captured requests SHOULD integrate with Evidence.

---

# Evidence Errors

Examples

- Screenshot failure
- DOM snapshot failure
- HAR capture failure
- Console log collection failure

Evidence failures SHALL NOT invalidate otherwise successful browser execution unless required by policy.

---

# Authentication Errors

Examples

- Authentication Context invalid
- Cookie restoration failed
- Session restoration failed
- Authentication expired

Authentication SHALL remain delegated to the Authentication Shared Skill.

---

# Timeout Errors

Examples

- Browser launch timeout
- Navigation timeout
- JavaScript timeout
- Overall execution timeout

Timeout duration SHOULD be recorded.

---

# Resource Errors

Examples

- Maximum browser instances exceeded
- Maximum contexts exceeded
- Memory limit exceeded
- Disk space exhausted

Resource limits SHALL be configurable.

---

# Policy Errors

Examples

- Browser reuse prohibited
- Context isolation violation
- Unauthorized browser profile
- Evidence collection prohibited

Policy violations SHALL identify the violated policy without exposing sensitive configuration.

---

# Internal Errors

Examples

- Unexpected runtime exception
- Adapter failure
- Serialization failure
- Execution state corruption

Internal implementation details SHALL NOT be exposed.

---

# Severity Levels

Suggested severities

| Severity | Meaning |
|----------|---------|
| Low | Minor browser degradation |
| Medium | Current browser operation failed |
| High | Browser automation unavailable |
| Critical | Platform unable to execute browser automation safely |

---

# Retry Guidance

Retryable examples

- Browser startup interruption
- Temporary navigation failure
- Resource loading interruption
- Stale DOM reference

Non-retryable examples

- Invalid browser configuration
- Unsupported browser operation
- Policy violation
- Invalid selector syntax

Retry decisions SHALL follow platform retry policy.

---

# Evidence Requirements

Browser errors SHOULD preserve

- Browser Profile
- Browser Context identifier
- Current URL
- Page metadata
- Navigation history
- Console messages
- JavaScript exceptions
- Screenshot (when possible)
- DOM snapshot (when possible)

Evidence SHALL conform to the canonical Evidence schema.

---

# Observability

The Browser Shared Skill SHOULD publish

- BrowserLaunchFailed
- ContextCreationFailed
- NavigationFailed
- DOMOperationFailed
- JavaScriptExecutionFailed
- ScreenshotFailed
- BrowserClosedUnexpectedly

Events SHALL integrate with the platform Execution State.

---

# Logging

Logs SHOULD include

```yaml
request_id:

assessment_id:

task_id:

browser_context:

page:

operation:

error_category:

error_code:

duration:
```

Sensitive information SHALL be redacted.

---

# Recovery Expectations

Recovery MAY include

- Browser restart
- Context recreation
- Page recreation
- Navigation retry
- DOM operation retry
- Browser failover

Recovery SHALL respect platform execution policy.

---

# Validation Rules

A compliant Browser Error Model SHALL

- Produce canonical browser errors
- Normalize framework-specific exceptions
- Preserve evidence
- Support retry classification
- Publish observable events
- Protect sensitive information

---

# Quality Requirements

The Browser Error Model SHALL

✓ Normalize browser engine failures

✓ Normalize automation framework failures

✓ Preserve Browser Context abstraction

✓ Support deterministic classification

✓ Capture browser evidence

✓ Integrate with platform error handling

✓ Remain browser independent

---

# Future Extensions

Future versions MAY support

- Distributed browser recovery
- Browser health scoring
- Browser pool failover
- Cross-browser retry strategies
- Automated browser diagnostics

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Browser Error Model provides a consistent, browser-independent mechanism for representing browser automation failures across all supported browser engines and automation frameworks.

It enables standardized reporting, reliable recovery, secure evidence preservation, and seamless integration with the Robust PenTest Platform's execution and observability architecture.