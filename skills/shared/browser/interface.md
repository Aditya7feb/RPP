# Browser Interface

**File:** `skills/shared/browser/interface.md`

**Version:** 1.0.0

---

# Purpose

The Browser Interface defines the canonical contract through which platform components interact with the Browser Shared Skill.

It standardizes browser lifecycle management, browser context management, page interaction, navigation, DOM operations, JavaScript execution, evidence collection, and browser observability while remaining independent of browser engines and automation frameworks.

All consumers SHALL interact exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Browser Independent
- Framework Independent
- Versioned
- Observable
- Secure
- Backward Compatible

---

# Relationship

```
Master Agent

↓

Workflow

↓

Domain Skill

↓

Browser Interface

↓

Browser Shared Skill

↓

Browser Adapter

↓

Browser Engine
```

Consumers SHALL NOT communicate directly with browser adapters or browser engines.

---

# Interface Overview

The interface consists of

```
Metadata

↓

Browser Request

↓

Execution Options

↓

Execution Context

↓

Browser Context

↓

Page Reference

↓

Operation Result

↓

Evidence

↓

Metrics

↓

Errors
```

---

# Metadata

Every browser invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables traceability and auditing.

---

# Browser Request

Every request SHALL define

```yaml
operation:

browser_context:

page:

parameters:
```

---

## Supported Operations

The Browser Shared Skill SHALL support

```
browser.launch

browser.close

browser.context.create

browser.context.dispose

browser.page.create

browser.page.close

browser.navigate

browser.dom.query

browser.dom.read

browser.dom.modify

browser.script.execute

browser.cookies.read

browser.cookies.write

browser.storage.read

browser.storage.write

browser.network.capture

browser.network.intercept

browser.screenshot.capture

browser.har.capture

browser.console.capture

browser.performance.capture
```

Future operations MAY be introduced without breaking existing consumers.

---

# Browser Context

Browser operations SHALL operate on a Browser Context.

Example

```yaml
browser_context:

  context_id:

  state:

  authentication_context:

  isolation_policy:
```

Consumers SHALL depend only on this object.

---

## Browser Context State

Possible states

```
Created

Running

Paused

Closing

Closed

Failed
```

---

# Page Reference

Operations targeting pages SHALL reference

```yaml
page:

  page_id:

  url:

  title:
```

Page identifiers SHALL remain opaque to consumers.

---

# Navigation Parameters

Navigation requests MAY include

```yaml
url:

wait_strategy:

timeout:

follow_redirects:
```

Supported wait strategies MAY include

- Load
- DOM Ready
- Network Idle
- Custom Event

---

# DOM Parameters

DOM operations MAY specify

```yaml
selector:

selector_type:

action:

value:
```

Supported selector types MAY include

- CSS
- XPath
- Text
- Accessibility

---

# JavaScript Parameters

Script execution SHALL support

```yaml
script:

arguments:

timeout:
```

Results SHALL be serialized into implementation-independent data structures.

---

# Storage Parameters

Storage operations MAY specify

```yaml
storage_type:

key:

value:
```

Supported storage types

- Cookies
- Local Storage
- Session Storage
- IndexedDB

---

# Network Capture

Capture requests MAY include

```yaml
capture_requests:

capture_responses:

capture_websockets:

capture_resources:
```

Network information SHALL integrate with the Evidence schema.

---

# Authentication Integration

Consumers MAY associate an Authentication Context with a Browser Context.

Example

```yaml
authentication_context:

  context_id:
```

The Browser Shared Skill SHALL restore authentication state without exposing implementation details.

---

# Operation Result

Successful operations SHALL return normalized results.

Example

```yaml
status:

browser_context:

page:

result:

execution_duration:
```

Transport-specific or framework-specific objects SHALL NOT be exposed.

---

# Evidence

Browser operations SHALL expose structured evidence.

Evidence MAY include

- Screenshot
- DOM Snapshot
- HTML
- Console Logs
- HAR
- Performance Metrics
- Network Activity

Evidence SHALL conform to the canonical Evidence schema.

---

# Metrics

Browser metrics MAY include

```yaml
navigation_duration:

render_duration:

script_duration:

resource_count:

dom_size:
```

Metrics SHOULD support platform observability.

---

# Error Contract

Errors SHALL conform to

```
skills/core/error-handling.md
```

Typical categories include

- Browser
- Context
- Navigation
- DOM
- JavaScript
- Network
- Timeout
- Configuration
- Authentication

---

# Security Requirements

The Browser Interface SHALL

- Preserve Browser Context isolation
- Protect Authentication Contexts
- Prevent cross-assessment state leakage
- Avoid exposing browser internals
- Support secure cleanup

---

# Compatibility

Consumers SHALL remain independent of

- Playwright
- Selenium
- WebDriver
- CDP
- Browser engine implementation

The Browser Context SHALL remain stable across implementations.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL include

- Metadata
- Browser Request
- Browser Context
- Execution Context
- Operation Result
- Error Handling
- Evidence

---

# Quality Requirements

The Browser Interface SHALL

✓ Be browser independent

✓ Be framework independent

✓ Preserve browser isolation

✓ Produce normalized Browser Contexts

✓ Support Authentication Context integration

✓ Capture browser evidence

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY support

- Mobile device emulation
- Multi-page orchestration
- Browser clustering
- Distributed browser execution
- Accessibility automation
- Visual regression workflows

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Browser Interface provides a stable, implementation-independent contract through which all platform components perform browser automation.

It enables consistent browser lifecycle management, DOM interaction, JavaScript execution, evidence collection, and authentication integration while abstracting browser implementation details and preserving platform interoperability.