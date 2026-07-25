# Skill Capability Model

**File:** `skills/core/capability-model.md`

**Version:** 1.0.0

---

# Purpose

The Capability Model defines how skills advertise, expose, and constrain their functional behavior within the Robust PenTest Platform (RPP).

A capability represents a discrete action that a skill is able to perform.

Capabilities provide a common vocabulary for planning, orchestration, dependency resolution, and adaptive execution.

Agents SHALL make planning decisions based on capabilities rather than implementation details.

---

# Design Principles

Capabilities SHALL be

- Explicit
- Observable
- Discoverable
- Versioned
- Reusable
- Testable
- Independent of implementation

Capabilities describe **what** a skill can do, not **how** it performs the work.

---

# Relationship

```
Agent

↓

Task

↓

Required Capability

↓

Skill Selection

↓

Skill Execution
```

The Master Agent SHOULD resolve skills through capabilities whenever possible.

---

# What is a Capability?

A capability is a single functional behavior exposed by a skill.

Examples

- Send HTTP Request
- Parse HTML
- Resolve DNS
- Inspect TLS Certificate
- Capture Screenshot
- Parse JWT
- Execute Port Scan
- Enumerate GraphQL Schema
- Detect CMS
- Verify SQL Injection

Capabilities SHALL describe observable behavior.

---

# Capability Levels

Capabilities MAY be classified by abstraction.

## Atomic

Single operation.

Examples

- Resolve DNS
- Parse Cookie
- Send Request

---

## Composite

Combination of multiple atomic capabilities.

Examples

```
Technology Fingerprinting

↓

HTTP Request

↓

HTML Parsing

↓

Header Analysis

↓

Framework Detection
```

---

## Domain

Higher-level capability groups.

Examples

- Web Discovery
- Authentication Testing
- API Analysis
- Infrastructure Enumeration

---

# Capability Declaration

Every Skill SHALL declare

```yaml
capabilities:

- id:
  name:
  description:
  category:
```

Example

```yaml
capabilities:

- id: http.send

  name: Send HTTP Request

  category: Networking
```

Capability identifiers SHOULD remain stable across versions.

---

# Capability Categories

Example categories include

```
Networking

Discovery

Fingerprinting

Parsing

Authentication

Authorization

Scanning

Validation

Reporting

Analysis

Utility
```

Additional categories MAY be introduced.

---

# Capability Metadata

Each capability SHOULD define

```yaml
name:

description:

category:

version:

introduced_in:
```

---

# Inputs

Capabilities SHOULD declare

```yaml
required_inputs:

optional_inputs:
```

Example

```
URL

Headers

Cookies

Authentication

Timeout
```

---

# Outputs

Capabilities SHOULD define

```yaml
outputs:

produces_evidence:

produces_findings:

produces_technologies:
```

Outputs SHALL reference canonical schemas.

---

# Preconditions

Capabilities MAY require

```yaml
authentication:

technology:

permissions:

network_access:
```

Example

```
GraphQL Introspection

↓

Requires GraphQL Endpoint
```

---

# Postconditions

Capabilities SHOULD describe expected outcomes.

Examples

```
HTTP Request

↓

HTTP Response Available
```

```
Technology Detection

↓

Technology Object Created
```

---

# Side Effects

Capabilities SHALL declare whether execution

```yaml
passive:

state_changing:

network_activity:

authentication_required:
```

Examples

Passive

- DNS Lookup
- TLS Inspection

State Changing

- File Upload
- Password Reset
- User Creation

---

# Safety Classification

Every capability SHALL define its operational impact.

Supported classifications

```
Passive

Low Impact

Medium Impact

High Impact

Destructive
```

The Master Agent SHOULD use this classification during planning and approval workflows.

---

# Approval Requirements

Capabilities MAY require approval.

```yaml
approval_required:

approval_type:

reason:
```

Examples

- Exploitation
- Authenticated Testing
- Data Modification

---

# Capability Composition

Capabilities MAY depend on other capabilities.

Example

```
Technology Detection

├── HTTP Request
├── Header Parsing
├── HTML Parsing
└── JavaScript Analysis
```

Circular capability dependencies SHOULD NOT exist.

---

# Capability Discovery

Agents SHOULD discover skills by capability.

Example

```
Required

↓

Parse HTML

↓

Available Skills

- HTML Parser
- Technology Detector
```

Multiple skills MAY expose the same capability.

---

# Capability Versioning

Capability behavior MAY evolve.

Each capability SHOULD expose

```yaml
version:

deprecated:

replacement:
```

Deprecated capabilities SHOULD remain available until removed in a major release.

---

# Validation Rules

A valid capability SHALL define

- Identifier
- Name
- Category
- Description
- Inputs
- Outputs
- Safety Classification

---

# Quality Requirements

A capability SHALL

✓ Represent one observable behavior

✓ Be reusable

✓ Be independently testable

✓ Declare inputs

✓ Declare outputs

✓ Declare operational impact

✓ Support orchestration

---

# Future Extensions

Future versions MAY include

- Capability negotiation
- Performance characteristics
- Cost estimation
- AI-assisted capability selection
- Capability scoring
- Policy-based capability filtering

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Capability Model provides a standardized description of the behaviors that skills expose.

It enables the Master Agent to select, compose, validate, and orchestrate skills based on functional requirements rather than implementation details, improving modularity, extensibility, and long-term maintainability across the Robust PenTest Platform.