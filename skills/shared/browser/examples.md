# Browser Examples

**File:** `skills/shared/browser/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides representative examples demonstrating how platform components interact with the Browser Shared Skill.

Examples illustrate browser lifecycle management, Browser Context usage, authentication integration, browser automation, evidence generation, and observability.

All examples are conceptual and implementation independent.

---

# Example 1 — Launch Browser

## Scenario

A domain skill requires browser automation.

### Request

```yaml
operation: browser.launch

browser_profile: chromium-default
```

### Response

```yaml
status: success

browser_context:

  context_id: browser-001

  state: running
```

---

# Example 2 — Navigate to Target

## Scenario

Navigate to the application homepage.

```yaml
operation: browser.navigate

browser_context:

  context_id: browser-001

parameters:

  url: https://example.com
```

Result

```yaml
status: success

page:

  url: https://example.com
```

---

# Example 3 — Execute JavaScript

## Scenario

Retrieve the current document title.

```yaml
operation: browser.script.execute

parameters:

  script: document.title
```

Result

```yaml
result:

  value: Example Application
```

---

# Example 4 — Query DOM

## Scenario

Locate the login form.

```yaml
operation: browser.dom.query

parameters:

  selector: form

  selector_type: css
```

Result

```yaml
elements_found: 1
```

---

# Example 5 — Fill Login Form

```yaml
sequence:

- browser.dom.modify

- browser.dom.modify

- browser.dom.modify
```

Logical flow

```
Username

↓

Password

↓

Submit
```

---

# Example 6 — Apply Authentication Context

Authentication Context

```yaml
authentication_context:

  context_id: auth-123
```

The Browser Shared Skill restores

- Cookies
- Local Storage
- Session
- Authentication State

No login automation is required.

---

# Example 7 — Capture Screenshot

```yaml
operation: browser.screenshot.capture
```

Result

```yaml
artifact:

  type: screenshot

  reference: evidence-001
```

---

# Example 8 — Capture HAR

```yaml
operation: browser.har.capture
```

Result

```yaml
artifact:

  type: har

  reference: evidence-002
```

---

# Example 9 — Network Interception

```yaml
operation: browser.network.capture

parameters:

  capture_requests: true

  capture_responses: true
```

Captured artifacts include

- HTTP Requests
- HTTP Responses
- Redirect Chain

---

# Example 10 — Browser Context Reuse

```
Assessment

↓

Browser Context

↓

Page A

↓

Page B

↓

Page C
```

Multiple pages share one Browser Context while maintaining isolation from other assessments.

---

# Example 11 — XSS Skill Integration

```
XSS Skill

↓

Browser Shared Skill

↓

Navigate

↓

Inject Payload

↓

Execute JavaScript

↓

Capture Screenshot

↓

Collect Evidence
```

The XSS skill delegates browser automation entirely.

---

# Example 12 — CSP Validation

```
Browser

↓

Navigate

↓

Console Messages

↓

CSP Violations

↓

Evidence
```

Console output becomes structured evidence.

---

# Example 13 — File Upload Validation

```
Browser

↓

Navigate

↓

Select File

↓

Upload

↓

Observe Requests

↓

Capture Response
```

---

# Example 14 — Browser Evidence

Generated evidence

```yaml
evidence:

- Screenshot

- DOM Snapshot

- HTML

- HAR

- Console Logs

- Performance Metrics
```

---

# Example 15 — Multi-Tab Workflow

```
Browser Context

├── Login Page

├── Dashboard

└── Admin Panel
```

All pages remain within the same Browser Context.

---

# Example 16 — Browser Failure

Returned error

```yaml
category: Navigation

retryable: true
```

The Browser Shared Skill returns a canonical Browser Error.

---

# Example 17 — Browser Events

Generated events

```
BrowserStarted

↓

ContextCreated

↓

PageCreated

↓

NavigationCompleted

↓

ScriptExecuted

↓

ScreenshotCaptured

↓

BrowserClosed
```

Events update the platform Execution State.

---

# Example 18 — Browser Cleanup

```
Execution Complete

↓

Close Pages

↓

Dispose Context

↓

Release Resources

↓

Browser Closed
```

Cleanup executes after both success and failure.

---

# Best Practices

Consumers SHOULD

- Reuse Browser Contexts where appropriate
- Delegate authentication to the Authentication Shared Skill
- Capture screenshots at important checkpoints
- Preserve browser evidence
- Close browser resources promptly
- Use Browser Profiles instead of inline configuration

---

# Anti-Patterns

Consumers SHOULD NOT

- Launch a browser for every operation
- Manage browser engines directly
- Perform authentication manually
- Expose browser implementation details
- Ignore cleanup
- Store browser state outside platform policy

---

# Validation Checklist

A compliant consumer

✓ Uses the Browser Interface

✓ Uses Browser Contexts

✓ Delegates browser lifecycle

✓ Delegates authentication

✓ Preserves browser isolation

✓ Captures browser evidence

✓ Supports cleanup

---

# Success Criteria

A compliant consumer interacts exclusively with the Browser Shared Skill through the Browser Interface.

Browser lifecycle management, navigation, DOM interaction, JavaScript execution, authentication integration, evidence collection, and cleanup remain centralized, reusable, and implementation independent.