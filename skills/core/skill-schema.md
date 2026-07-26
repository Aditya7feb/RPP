# Skill Schema

**File:** `skills/skill-schema.md`

**Version:** 1.0.0

---

# Purpose

The Skill Schema defines the canonical representation of a skill within the Robust PenTest Platform (RPP).

A Skill represents a reusable capability that performs a single, well-defined operation.

Every skill within RPP SHALL conform to this schema.

---

# Design Principles

A Skill SHALL be

- Single-purpose
- Reusable
- Stateless
- Deterministic
- Composable
- Observable
- Versioned
- Independently testable
- Agent-independent

---

# Relationship

```
Agent
    │
    ├── Skill
    │      │
    │      ├── Inputs
    │      ├── Outputs
    │      ├── Dependencies
    │      ├── Capabilities
    │      └── Documentation
```

---

# Identity

Every Skill SHALL define

```yaml
skill_id:

name:

version:

category:

schema_version:
```

The combination of `skill_id` and `version` SHALL uniquely identify a skill.

---

# Metadata

Every Skill SHALL include

```yaml
display_name:

description:

author:

maintainer:

created_at:

last_updated:
```

---

# Purpose

Each Skill SHALL describe

```yaml
purpose:

problem_statement:

expected_outcome:
```

The purpose SHALL explain

- What problem the skill solves
- What it does
- What it intentionally does not do

---

# Categories

Example categories include

```
Networking

Reconnaissance

Fingerprinting

Scanning

Validation

Authentication

Web Security

API Security

Cloud

Infrastructure

Reporting

Analysis

Utility

Other
```

Additional categories MAY be introduced.

---

# Capabilities

Each Skill SHALL define

```yaml
capabilities:

- capability
```

Example

```yaml
capabilities:

- Send HTTP Request

- Parse Headers

- Follow Redirects
```

Capabilities SHOULD describe observable behavior.

---

# Inputs

Every Skill SHALL declare

```yaml
required_inputs:

optional_inputs:
```

Examples

```
Target URL

Hostname

Headers

Credentials

Evidence References

Technology References
```

---

# Outputs

Every Skill SHALL declare

```yaml
outputs:

produces_evidence:

produces_findings:

produces_technologies:
```

Outputs SHALL reference canonical schemas.

---

# Dependencies

Skills MAY depend on

```yaml
required_skills:

optional_skills:

external_tools:
```

Example

```
HTTP Skill

↓

HTML Parser

↓

Technology Detector
```

Circular dependencies SHALL NOT exist.

---

# Supported Targets

Each Skill SHALL define

```yaml
supported_targets:

- Web Application

- API

- Host

- Network

- Cloud Resource
```

---

# Execution Constraints

Skills MAY define

```yaml
timeout:

maximum_runtime:

retry_supported:

parallel_safe:
```

---

# Configuration

Configurable options SHOULD be declared.

```yaml
configuration:

- name

- default

- required
```

Configuration SHALL be validated before execution.

---

# Preconditions

Skills MAY define

```yaml
requires_authentication:

required_technologies:

required_permissions:
```

Example

```
GraphQL Endpoint

↓

GraphQL Introspection Skill
```

---

# Postconditions

Skills SHOULD define

```yaml
expected_outputs:

follow_up_actions:
```

Example

```
Technology Identified

↓

Schedule Framework Scanner
```

---

# Confidence

Each Skill SHALL define

```yaml
confidence_model:

confidence_sources:
```

Confidence SHALL align with

```
skills/core/confidence-model.md
```

---

# Error Model

Skills SHALL describe

```yaml
recoverable_errors:

non_recoverable_errors:
```

Errors SHALL be returned using the Agent Response schema.

---

# Security Considerations

Each Skill SHOULD document

```yaml
security_notes:

required_approvals:

safe_execution:
```

Examples

- Passive only
- Requires approval
- Generates network traffic
- State changing

---

# Compatibility

Skills SHALL define

```yaml
minimum_platform_version:

supported_agents:

supported_environments:
```

---

# Documentation

Every Skill SHALL include

```yaml
readme:

examples:

limitations:

references:
```

---

# Versioning

Versioning SHALL follow semantic versioning.

```
MAJOR.MINOR.PATCH
```

Breaking changes SHALL increment the major version.

---

# Validation Rules

A valid Skill SHALL contain

- Skill ID
- Name
- Version
- Category
- Purpose
- Inputs
- Outputs
- Capabilities
- Schema Version

---

# Quality Requirements

Every Skill SHALL

✓ Solve one problem

✓ Declare inputs

✓ Declare outputs

✓ Declare dependencies

✓ Be independently testable

✓ Be reusable

✓ Be implementation-independent

✓ Integrate with canonical schemas

---

# Future Extensions

Future versions MAY include

- Capability negotiation
- Performance benchmarks
- Remote execution metadata
- Trust levels
- Digital signatures
- Marketplace metadata
- Licensing information

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill provides a complete, standardized description of a reusable capability, including its purpose, interfaces, dependencies, operational constraints, and integration points.

It SHALL serve as the authoritative metadata definition for all skills within the Robust PenTest Platform.