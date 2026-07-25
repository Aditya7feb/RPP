# Skill Interface Specification

**File:** `skills/core/interface.md`

**Version:** 1.0.0

---

# Purpose

The Skill Interface Specification defines the standard interface that every skill within the Robust PenTest Platform (RPP) SHALL implement.

The interface defines how skills receive data, expose configuration, produce results, communicate errors, and interact with the execution engine.

This specification is independent of programming language, runtime, or execution framework.

---

# Design Principles

Every skill interface SHALL be

- Consistent
- Predictable
- Strongly typed
- Self-describing
- Backward compatible
- Language independent

The interface defines the contract between the Master Agent and a Skill.

---

# Relationship

```
Master Agent

↓

Execution Engine

↓

Skill Interface

↓

Skill Implementation
```

The Master Agent SHALL communicate only through the defined interface.

Implementation details SHALL remain hidden.

---

# Interface Overview

Every skill SHALL expose

```
Metadata

↓

Input

↓

Configuration

↓

Execution Context

↓

Execution

↓

Output

↓

Errors

↓

Metrics
```

---

# Skill Metadata

Every skill SHALL expose immutable metadata.

Example

```yaml
skill_id:

name:

version:

category:

description:

supported_capabilities:
```

Metadata SHALL be available without executing the skill.

---

# Input Contract

Every skill SHALL define

```yaml
required_inputs:

optional_inputs:
```

Example

```yaml
required_inputs:

- target

- assessment

- task
```

---

# Input Validation

Inputs SHALL be validated before execution.

Validation SHOULD verify

- Required fields
- Data types
- Value ranges
- Scope
- Target compatibility
- Configuration completeness

Invalid input SHALL prevent execution.

---

# Configuration

Every configurable parameter SHALL be declared.

Example

```yaml
configuration:

timeout:

retry_count:

follow_redirects:

verify_tls:

proxy:

rate_limit:
```

Configuration SHALL be validated during initialization.

---

# Execution Context

Every skill SHALL receive an execution context.

The context MAY include

```yaml
assessment:

task:

technology_inventory:

previous_findings:

previous_evidence:

runtime:

authentication:

session:

variables:
```

Skills SHALL consume the provided context instead of recreating it.

---

# Context Propagation

Skills MAY pass context to dependent skills.

Examples include

- Authentication tokens
- Cookies
- Technology inventory
- Endpoint inventory
- Discovered hosts
- Session identifiers

Context SHALL remain scoped to the current assessment.

---

# Output Contract

Every skill SHALL return a standardized response.

Outputs MAY include

```yaml
status:

summary:

findings:

evidence:

technologies:

recommendations:

warnings:

metrics:
```

Outputs SHALL conform to the Agent Response Schema.

---

# Partial Results

Long-running skills MAY return partial results.

Examples

```
Host Discovery

↓

Discovered Hosts

↓

Continue Scanning
```

Partial results SHALL remain valid Agent Responses.

---

# Error Contract

Errors SHALL be structured.

Example

```yaml
severity:

component:

message:

recoverable:

recommendation:
```

Errors SHALL NOT be returned as unstructured text.

---

# Progress Updates

Long-running skills SHOULD expose

```yaml
progress:

current_operation:

items_processed:

estimated_remaining:
```

Progress updates SHOULD be consumable by the Execution State.

---

# Resource Declaration

Skills SHOULD expose expected resource usage.

Example

```yaml
cpu:

memory:

network:

disk:
```

This information MAY assist scheduling decisions.

---

# Secrets Handling

Sensitive values SHALL NOT be embedded in skill outputs.

Examples include

- API Keys
- Passwords
- Access Tokens
- Client Secrets
- Private Keys

Sensitive values SHOULD be referenced through secure runtime mechanisms.

---

# Environment Requirements

A skill MAY declare runtime requirements.

Example

```yaml
requirements:

network_access:

browser:

docker:

kali:

python:

dotnet:
```

The execution engine SHALL verify compatibility before execution.

---

# Compatibility

Skills SHALL declare

```yaml
minimum_platform_version:

supported_execution_modes:

supported_operating_systems:
```

---

# Interface Stability

The interface SHALL follow semantic versioning.

Breaking interface changes SHALL increment the major version.

Skills SHOULD remain compatible with previous interface versions whenever practical.

---

# Validation Rules

A compliant skill interface SHALL define

- Metadata
- Input contract
- Output contract
- Configuration
- Execution context
- Error contract
- Compatibility information

---

# Quality Requirements

Every skill interface SHALL

✓ Be implementation independent

✓ Define all required inputs

✓ Produce standardized outputs

✓ Validate configuration

✓ Support structured errors

✓ Preserve execution context

✓ Protect sensitive information

✓ Integrate with the canonical schemas

---

# Future Extensions

Future versions MAY include

- Streaming interfaces
- Event-driven interfaces
- Remote execution interfaces
- Service discovery
- Capability negotiation
- Interface signing
- Protocol-specific bindings

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Interface provides a stable and implementation-independent contract between the Master Agent and every skill.

It enables skills written in different languages and executed in different environments to interoperate seamlessly while preserving consistency, observability, and portability across the Robust PenTest Platform.