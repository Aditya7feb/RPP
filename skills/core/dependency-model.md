
# Skill Dependency Model

**File:** `skills/core/dependency-model.md`

**Version:** 1.0.0

---

# Purpose

The Skill Dependency Model defines how skills declare, discover, validate, and satisfy dependencies within the Robust PenTest Platform (RPP).

Dependencies enable the platform to construct execution graphs, perform adaptive planning, avoid redundant work, and execute skills in the correct order.

The dependency model defines logical relationships rather than implementation details.

---

# Design Principles

Dependencies SHALL be

- Explicit
- Declarative
- Discoverable
- Versioned
- Validatable
- Acyclic
- Independent of implementation

A skill SHALL never assume that another skill has already executed.

---

# Relationship

```
Assessment

↓

Execution Plan

↓

Task

↓

Required Capability

↓

Dependency Resolution

↓

Skill Execution
```

Dependency resolution SHALL occur before skill execution.

---

# Dependency Types

A skill MAY depend on

- Capabilities
- Technologies
- Evidence
- Findings
- Configuration
- Runtime Environment
- External Tools
- Authentication
- Human Approval

Dependencies SHALL be declared explicitly.

---

# Capability Dependencies

Skills SHOULD depend on capabilities instead of specific skills.

Example

```
Requires

↓

HTTP Request Capability

↓

Resolved To

↓

HTTP Skill
```

This enables implementation replacement without changing dependent skills.

---

# Technology Dependencies

Execution MAY require detected technologies.

Example

```
Technology

↓

GraphQL

↓

Enable

↓

GraphQL Enumeration
```

Another example

```
Technology

↓

WordPress

↓

Enable

↓

WordPress Scanner
```

Technology dependencies SHALL reference Technology objects.

---

# Evidence Dependencies

Skills MAY require previously collected evidence.

Example

```
TLS Certificate

↓

Certificate Analyzer
```

or

```
HTTP Response

↓

Technology Detection
```

Evidence SHALL reference the canonical Evidence schema.

---

# Finding Dependencies

Validation skills MAY require existing findings.

Example

```
Possible SQL Injection

↓

SQLi Validator
```

Finding dependencies SHALL reference Finding objects.

---

# Authentication Dependencies

Some skills require authenticated execution.

Example

```
Session

↓

Privilege Testing
```

Authentication SHALL be validated before execution.

---

# Approval Dependencies

Certain capabilities require approval.

Examples

- Exploitation
- Authenticated Testing
- State-Changing Operations

Execution SHALL pause until approval is granted.

---

# Environment Dependencies

Skills MAY require

```yaml
requirements:

docker:

browser:

kali:

python:

dotnet:

java:
```

The execution engine SHALL verify environment compatibility.

---

# External Tool Dependencies

Skills MAY rely on external tools.

Example

```yaml
external_tools:

- nmap

- nuclei

- ffuf

- playwright
```

The execution engine SHOULD verify availability before execution.

---

# Dependency Declaration

Every dependency SHOULD define

```yaml
dependency_id:

type:

name:

required:

version:

reason:
```

Example

```yaml
dependency_id: capability.http.send

type: Capability

required: true
```

---

# Dependency Resolution

The scheduler SHALL resolve dependencies before execution.

Resolution SHALL verify

- Availability
- Compatibility
- Version
- Execution State
- Approval State

Execution SHALL NOT begin until mandatory dependencies are satisfied.

---

# Optional Dependencies

Dependencies MAY be optional.

Example

```
Playwright

↓

Enhanced Screenshot Quality
```

If unavailable, execution MAY continue with reduced functionality.

---

# Dependency Graph

Dependencies SHALL form a directed graph.

```
HTTP Request

↓

HTML Parser

↓

Technology Detection

↓

CMS Detection

↓

CMS Scanner
```

The graph SHALL NOT contain cycles.

---

# Circular Dependencies

Circular dependencies SHALL be rejected.

Example

```
Skill A

↓

Skill B

↓

Skill A
```

Such dependency chains SHALL be considered invalid.

---

# Dynamic Dependencies

Dependencies MAY emerge during execution.

Examples

- Technology Discovery
- Newly Identified Endpoint
- Authentication Success
- Host Discovery

The Execution Plan MAY be updated dynamically.

---

# Dependency States

Each dependency MAY be

```
Unknown

Pending

Satisfied

Unavailable

Failed

Skipped
```

Dependency state SHOULD be tracked in the Execution State.

---

# Version Compatibility

Dependencies SHOULD declare compatible versions.

Example

```yaml
minimum_version:

maximum_version:

preferred_version:
```

The execution engine SHOULD resolve compatible implementations automatically.

---

# Failure Handling

If a mandatory dependency fails

Execution SHALL

- Stop dependent execution
- Record failure
- Update Execution State
- Return structured error

Optional dependency failures SHALL NOT necessarily stop execution.

---

# Dependency Events

Resolution SHOULD generate events.

Examples

- Dependency Discovered
- Dependency Satisfied
- Dependency Failed
- Dependency Updated
- Dependency Removed

These events SHOULD update the Execution State.

---

# Quality Requirements

The dependency model SHALL

✓ Declare dependencies explicitly

✓ Support capability-based resolution

✓ Prevent circular dependencies

✓ Support dynamic dependency discovery

✓ Validate compatibility

✓ Support optional dependencies

✓ Integrate with execution planning

---

# Validation Rules

A compliant dependency declaration SHALL

- Define dependency type
- Define dependency identifier
- Specify whether it is required
- Support version compatibility
- Avoid circular references

---

# Future Extensions

Future versions MAY include

- Automatic dependency optimization
- Remote dependency resolution
- Dependency caching
- Policy-aware dependency selection
- Distributed capability discovery
- Marketplace-provided implementations

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Dependency Model provides a standardized mechanism for declaring and resolving the relationships that govern skill execution.

It enables adaptive planning, capability-based orchestration, and reliable execution while preserving modularity, extensibility, and implementation independence throughout the Robust PenTest Platform.