# Browser Shared Skill

**File:** `skills/shared/browser/README.md`

**Version:** 1.0.0

---

# Purpose

The Browser Shared Skill provides a standardized, implementation-independent browser automation capability for the Robust PenTest Platform (RPP).

It enables domain skills to interact with rendered web applications through a real browser while abstracting browser engines, automation frameworks, and execution environments.

Consumers SHALL delegate browser automation responsibilities to this shared skill.

---

# Goals

The Browser Shared Skill SHALL

- Abstract browser implementations
- Support browser lifecycle management
- Support rendered web application testing
- Execute client-side JavaScript
- Capture browser evidence
- Manage browser sessions
- Integrate with Authentication Contexts
- Support deterministic automation

---

# Non-Goals

The Browser Shared Skill SHALL NOT

- Detect vulnerabilities
- Implement browser-specific exploit logic
- Perform authentication independently
- Replace the HTTP Client
- Store browser state outside platform policy

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

Browser Shared Skill

├── Browser Manager
├── Context Manager
├── Page Manager
├── Storage Manager
├── Evidence Manager
└── Event Manager

↓

Browser Adapter

↓

Browser Engine
```

---

# Responsibilities

The Browser Shared Skill is responsible for

- Browser lifecycle
- Browser context management
- Page lifecycle
- Navigation
- JavaScript execution
- DOM interaction
- Storage management
- Cookie management
- Screenshot capture
- Network observation
- Evidence generation

---

# Browser Lifecycle

```
Initialize

↓

Launch Browser

↓

Create Context

↓

Create Page

↓

Navigate

↓

Interact

↓

Capture Evidence

↓

Close Page

↓

Close Context

↓

Terminate Browser
```

---

# Supported Browser Engines

Implementations MAY support

- Chromium
- Firefox
- WebKit
- Remote Browser Grid

Additional browser engines MAY be added.

---

# Supported Automation Frameworks

The Browser Shared Skill SHALL remain independent of automation frameworks.

Possible adapters include

- Playwright
- Selenium
- WebDriver BiDi
- Chrome DevTools Protocol (CDP)
- Custom browser adapters

Consumers SHALL remain unaware of the underlying implementation.

---

# Browser Contexts

A Browser Context represents an isolated execution environment.

Contexts SHALL isolate

- Cookies
- Local Storage
- Session Storage
- IndexedDB
- Cache
- Permissions

Contexts SHALL be independently disposable.

---

# Page Management

The Browser Shared Skill SHALL support

- Page creation
- Page navigation
- Page refresh
- Tab management
- Window management
- Popup handling

---

# Navigation

Navigation SHALL support

- URL navigation
- Redirect handling
- Wait strategies
- Timeout policies
- Navigation history

---

# DOM Interaction

Supported operations MAY include

- Element lookup
- Attribute retrieval
- Text extraction
- Form interaction
- Event dispatch
- DOM snapshot generation

DOM interactions SHALL remain implementation independent.

---

# JavaScript Execution

Consumers MAY execute JavaScript within the active page.

Execution SHALL support

- Inline scripts
- Function invocation
- Return values
- Exception handling

JavaScript execution SHALL integrate with the platform execution model.

---

# Storage Management

The Browser Shared Skill SHALL manage

- Cookies
- Local Storage
- Session Storage
- IndexedDB

Storage SHALL remain isolated by Browser Context.

---

# Network Observation

The Browser Shared Skill MAY observe

- HTTP Requests
- HTTP Responses
- Redirect Chains
- WebSockets
- Resource Loading

Observation SHALL integrate with Evidence.

---

# Authentication Integration

The Browser Shared Skill SHALL integrate with

```
Authentication Shared Skill

↓

Authentication Context

↓

Authenticated Browser Context
```

Authentication SHALL remain external to browser automation.

---

# Evidence

The Browser Shared Skill SHOULD capture

- Screenshots
- DOM Snapshots
- HTML
- Console Logs
- Network Logs
- HAR Files
- Browser Metadata
- Performance Metrics

Evidence SHALL conform to the canonical Evidence schema.

---

# Browser Events

Typical browser events include

- Browser Started
- Context Created
- Page Created
- Navigation Started
- Navigation Completed
- Script Executed
- Screenshot Captured
- Context Closed
- Browser Closed

Events SHALL integrate with Execution State.

---

# Dependencies

The Browser Shared Skill depends on

- Configuration Model
- Execution Model
- Error Handling
- Authentication Shared Skill
- HTTP Client
- Logging
- Evidence

---

# Outputs

Typical outputs MAY include

- Browser Context
- Page Reference
- DOM Snapshot
- JavaScript Result
- Screenshot Reference
- HAR Reference
- Browser Metrics

Outputs SHALL remain implementation independent.

---

# Security Principles

The Browser Shared Skill SHALL

- Isolate browser contexts
- Protect authentication state
- Prevent cross-assessment contamination
- Support secure browser cleanup
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Reuse Browser Contexts where appropriate
- Reuse Authentication Contexts
- Capture screenshots at significant checkpoints
- Close browser resources promptly
- Preserve browser evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Launch browsers unnecessarily
- Manage browser engines directly
- Implement browser-specific logic
- Duplicate storage management
- Persist browser state outside platform policy

---

# Future Extensions

Future versions MAY support

- Mobile browser emulation
- Cross-browser parallel execution
- Remote browser clusters
- Browser recording
- AI-assisted visual comparison
- Accessibility inspection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Browser Shared Skill provides a secure, reusable, and implementation-independent browser automation capability for the Robust PenTest Platform.

It enables consistent browser lifecycle management, rendered application interaction, evidence capture, and authentication integration while remaining independent of browser engines and automation frameworks.