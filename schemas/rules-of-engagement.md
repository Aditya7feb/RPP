# Rules of Engagement Schema

**File:** `schemas/rules-of-engagement.md`

**Version:** 1.0.0

---

# Purpose

The Rules of Engagement Schema defines the canonical, implementation-independent
representation of the actions permitted during an assessment within the Robust
PenTest Platform (RPP).

Rules of Engagement (RoE) declare **what actions are permitted** against
in-scope [Assets](asset.md). RoE is defined independently from
[Scope](scope.md), which declares **what may be tested**. Together, Scope and RoE
form the complete authorization boundary of an assessment.

RoE is consulted by the [Policy Engine](../skills/shared/policy-engine/README.md)
before any capability acts. No capability SHALL perform an action that RoE does
not permit.

An RoE object represents authorization configuration only. It SHALL NOT contain
findings, risk, or secrets.

---

# Design Principles

Rules of Engagement SHALL be

- Declarative
- Deterministic in evaluation
- Authoritative for permitted actions
- Independent from Scope
- Conservative by default
- Auditable
- Implementation independent

---

# Identity

Every RoE SHALL contain

```yaml
roe_id:

assessment_id:

schema_version:
```

`roe_id` SHALL be unique within a configuration namespace.

`assessment_id` SHALL reference the owning [assessment](assessment.md).

`schema_version` SHALL be `1.0.0`.

---

# Action Permissions

Every RoE SHALL contain

```yaml
permissions:
```

`permissions` SHALL contain

```yaml
passive_allowed:

active_allowed:

validation_allowed:

exploitation_allowed:

intrusive_allowed:
```

Each field SHALL be a boolean.

`passive_allowed` governs non-interacting observation.

`active_allowed` governs benign interaction such as banner and content
retrieval.

`validation_allowed` governs safe confirmation of a suspected weakness.

`exploitation_allowed` governs actions that exercise a weakness.

`intrusive_allowed` governs actions with side effects such as writes, message
sends, or workload execution.

Permissions SHALL default to the most conservative value (`false`) when
unspecified.

---

# Action Classes

Every RoE SHALL contain

```yaml
permitted_action_classes:

prohibited_actions:
```

`permitted_action_classes` SHALL enumerate the canonical action classes allowed,
such as `discovery`, `fingerprinting`, `authentication-testing`, or
`injection-testing`.

`prohibited_actions` SHALL enumerate actions that SHALL NEVER be performed, such
as `denial-of-service`, `data-destruction`, or `phishing`.

`prohibited_actions` SHALL take precedence over every permission and action
class.

---

# Approval Requirements

Every RoE SHALL contain

```yaml
approval_required_for:
```

`approval_required_for` SHALL enumerate action classes that require an explicit
[approval](approval.md) before execution, such as `exploitation` or
`intrusive`.

Actions listed here SHALL be gated by the
[Policy Engine](../skills/shared/policy-engine/README.md) pending approval.

---

# Time And Rate Constraints

An RoE MAY contain

```yaml
maintenance_windows:

rate_limit_policy_id:
```

`maintenance_windows` SHALL be an array of permitted time windows during which
active or intrusive actions MAY occur.

`rate_limit_policy_id` SHALL reference a
[Rate Limit Policy](rate-limit-policy.md) expressing the Rules of Engagement rate
ceiling.

Outside a required maintenance window, active and intrusive actions SHALL be
denied.

---

# Data Handling Constraints

An RoE MAY contain

```yaml
data_handling:
```

`data_handling` SHALL contain

```yaml
exfiltration_allowed:

pii_handling:

evidence_redaction_required:
```

`exfiltration_allowed` SHALL be a boolean and SHALL default to `false`.

`evidence_redaction_required` SHALL be a boolean and SHOULD default to `true`.

Data handling constraints SHALL be honored by every capability that captures
evidence.

---

# Extensions

An RoE MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid RoE object SHALL contain

- `roe_id`
- `assessment_id`
- `schema_version`
- `permissions.passive_allowed`
- `permissions.active_allowed`
- `permissions.validation_allowed`
- `permissions.exploitation_allowed`
- `permissions.intrusive_allowed`
- `permitted_action_classes`
- `prohibited_actions`
- `approval_required_for`

---

# Validation Rules

A valid RoE object SHALL satisfy

- Every permission is a boolean and defaults to `false` when unspecified
- `prohibited_actions` overrides every permission and action class
- `approval_required_for` references recognized action classes
- `rate_limit_policy_id`, when present, references a valid Rate Limit Policy
- Active and intrusive actions are denied outside required maintenance windows
- No secret material appears in `extensions`

---

# Relationships To Other Schemas

```
Assessment

├── Scope (what may be tested)
└── Rules of Engagement (what actions are permitted)
       ├── references a Rate Limit Policy ceiling
       ├── references Approval requirements
       └── consulted by the Policy Engine
```

RoE belongs to exactly one [assessment](assessment.md). It references a
[Rate Limit Policy](rate-limit-policy.md) ceiling and
[approval](approval.md) requirements, and it is consulted, together with
[Scope](scope.md), by the
[Policy Engine](../skills/shared/policy-engine/README.md).

---

# Example Object

```yaml
roe_id: roe-asmt-42
assessment_id: asmt-42
schema_version: 1.0.0
permissions:
  passive_allowed: true
  active_allowed: true
  validation_allowed: true
  exploitation_allowed: false
  intrusive_allowed: false
permitted_action_classes:
  - discovery
  - fingerprinting
  - authentication-testing
prohibited_actions:
  - denial-of-service
  - data-destruction
  - phishing
approval_required_for:
  - exploitation
  - intrusive
maintenance_windows:
  - start: 2026-07-26T02:00:00Z
    end: 2026-07-26T06:00:00Z
rate_limit_policy_id: ratelimitpolicy-roe-ceiling
data_handling:
  exfiltration_allowed: false
  pii_handling: redact
  evidence_redaction_required: true
extensions: {}
```

---

# Extension Points

- New action classes MAY be introduced for emerging testing domains.
- Consumers SHALL ignore unknown optional fields for forward compatibility.

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional constraints or action classes.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
