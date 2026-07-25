# Workflow Definition Schema

**File:** `schemas/workflow-definition.md`

**Version:** 1.0.0

---

# Purpose

The Workflow Definition Schema defines the canonical, implementation-independent
representation of a reusable assessment workflow template within the Robust
PenTest Platform (RPP).

A workflow definition describes an ordered, parameterized template of skill
invocations and control flow that the planning phase instantiates into a
concrete [Execution Plan](execution-plan.md). It is executed by the
[Workflow Runtime](../skills/shared/workflow-runtime/README.md) shared package.

A Workflow Definition is a reusable template. It SHALL NOT contain
assessment-specific runtime state. Assessment-specific resolution belongs to the
[Execution Plan](execution-plan.md), and runtime state belongs to the
[Execution State](execution-state.md).

---

# Design Principles

A Workflow Definition SHALL be

- Declarative
- Reusable across assessments
- Parameterized
- Deterministic in structure
- Tool independent
- Free of embedded secrets

---

# Identity

Every Workflow Definition SHALL contain

```yaml
workflow_id:

schema_version:

name:

version:
```

`workflow_id` SHALL be unique within a workflow namespace.

`schema_version` SHALL be `1.0.0`.

`name` SHALL be a stable, human-readable identifier such as `web-app-baseline`.

`version` SHALL be the semantic version of the workflow definition itself.

---

# Classification

Every Workflow Definition SHALL contain

```yaml
description:

domain:
```

`description` SHALL summarize the workflow's purpose.

`domain` SHALL identify the target domain, such as `web-app`, `rest-api`,
`graphql`, or `wordpress`.

---

# Parameters

A Workflow Definition MAY contain

```yaml
parameters:
```

`parameters` SHALL be an array of parameter descriptors.

Each descriptor SHALL contain

```yaml
name:

type:

required:

default:
```

`type` SHALL be a canonical parameter type such as `string`, `number`,
`boolean`, `target`, or `list`.

Parameters SHALL NOT define secrets. Secret inputs SHALL be referenced
indirectly through credential references resolved at execution time.

---

# Inputs

Every Workflow Definition SHALL contain

```yaml
inputs:
```

`inputs` SHALL declare the scope and targets the workflow operates on, such as a
target reference and an assessment reference.

`inputs` SHALL reference canonical objects rather than embedding them.

---

# Steps

Every Workflow Definition SHALL contain

```yaml
steps:
```

`steps` SHALL be an ordered array of step descriptors.

Each step SHALL contain

```yaml
step_id:

skill:

capability:

parameters:

depends_on:
```

`skill` SHALL identify the domain or shared skill invoked, by canonical
identifier.

`capability` SHALL identify the specific capability invoked on that skill.

`parameters` SHALL bind workflow parameters and prior step outputs to the skill
invocation.

`depends_on` SHALL be an array of `step_id` values that MUST complete before the
step runs.

A step SHALL NOT reference tools, CLIs, or implementations.

---

# Control Flow

A step MAY contain

```yaml
condition:

for_each:

on_error:
```

`condition` SHALL be a declarative predicate gating step execution.

`for_each` SHALL iterate the step over a collection produced by a prior step or
parameter.

`on_error` SHALL be one of

```
fail

continue

skip_remaining
```

`on_error` SHALL default to `fail`.

---

# Approval Gates

A Workflow Definition MAY contain

```yaml
approval_gates:
```

`approval_gates` SHALL be an array of gate descriptors that pause execution
pending authorization, each referencing an
[Approval](approval.md) requirement.

Approval gates SHALL be placed before steps that perform intrusive or
irreversible actions.

---

# Policies

A Workflow Definition MAY contain

```yaml
policies:
```

`policies` SHALL reference execution policies such as rate-limit, retry, and
proxy policy identifiers applied to steps.

Policies SHALL reference canonical policy schemas rather than embedding values.

---

# Outputs

Every Workflow Definition SHALL contain

```yaml
outputs:
```

`outputs` SHALL declare the findings, evidence, and artifacts the workflow is
expected to produce, referenced by canonical schema.

---

# Extensions

A Workflow Definition MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Workflow Definition object SHALL contain

- `workflow_id`
- `schema_version`
- `name`
- `version`
- `description`
- `domain`
- `inputs`
- `steps`
- `outputs`

Each step SHALL contain

- `step_id`
- `skill`
- `capability`

---

# Validation Rules

A valid Workflow Definition object SHALL satisfy

- `step_id` values are unique
- Every `depends_on` references an existing `step_id`
- The step dependency graph is acyclic
- `on_error`, when present, is one of the allowed values
- Every referenced parameter is declared in `parameters`
- No step references a tool, CLI, or implementation
- Every approval gate precedes at least one intrusive step
- No secret material appears in any field, including `extensions`

---

# Relationships

```
Workflow Definition

├── instantiated into an Execution Plan (planning)
├── executed by the Workflow Runtime
├── references skills and capabilities
├── references policy schemas
├── references Approval requirements
└── declares Finding, Evidence, and Artifact outputs
```

A Workflow Definition is a reusable template. During planning it is instantiated
into an [Execution Plan](execution-plan.md) bound to a specific assessment. The
[Workflow Runtime](../skills/shared/workflow-runtime/README.md) executes the
resulting plan, producing [Execution State](execution-state.md).

---

# Example Object

```yaml
workflow_id: workflow-web-app-baseline
schema_version: 1.0.0
name: web-app-baseline
version: 1.0.0
description: >
  Baseline discovery and safe web-application checks against a single target.
domain: web-app
parameters:
  - name: target
    type: target
    required: true
  - name: max_depth
    type: number
    required: false
    default: 2
inputs:
  target_ref: parameter:target
  assessment_ref: context:assessment_id
steps:
  - step_id: resolve-dns
    skill: dns-enumeration
    capability: enumerate-records
    parameters:
      target: parameter:target
  - step_id: probe-tls
    skill: tls-analysis
    capability: analyze-endpoint
    depends_on:
      - resolve-dns
  - step_id: discover-content
    skill: content-discovery
    capability: enumerate-paths
    depends_on:
      - probe-tls
    parameters:
      depth: parameter:max_depth
approval_gates:
  - before: discover-content
    approval_ref: approval-active-scan
policies:
  rate_limit: ratelimitpolicy-default-http
  retry: retrypolicy-default-network
outputs:
  findings: schema:finding
  evidence: schema:evidence
extensions: {}
```

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields such as additional control-flow
constructs.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
