# Assessment Schema

**File:** `schemas/assessment.md`

**Version:** 1.0.0

---

# Purpose

The Assessment Schema defines the canonical representation of a penetration testing assessment within the Robust PenTest Platform (RPP).

Every assessment SHALL conform to this schema.

The Assessment is the root object of the platform.

All Tasks, Findings, Evidence, Reports, Technologies, and Approvals belong to exactly one Assessment.

---

# Design Principles

The Assessment SHALL be

- Unique
- Immutable in identity
- Traceable
- Auditable
- Versioned
- Extensible

---

# Object Overview

```
Assessment

├── Scope
├── Rules of Engagement
├── Execution Plan
├── Tasks
├── Findings
├── Evidence
├── Technologies
├── Reports
├── Audit
└── Metadata
```

---

# Identity

Every assessment SHALL include

```yaml
assessment_id:

name:

description:

created_by:

created_at:

schema_version:
```

The identifier SHALL remain constant for the lifetime of the assessment.

---

# Scope

The assessment SHALL define

```yaml
scope:

  domains:

  hosts:

  ip_ranges:

  applications:

  api_endpoints:

  exclusions:
```

The scope determines what may be tested.

No agent SHALL execute work outside the defined scope.

---

# Rules of Engagement

Each assessment SHALL reference

```yaml
rules_of_engagement:

  validation_allowed:

  exploitation_allowed:

  rate_limit:

  authentication:

  maintenance_window:

  prohibited_actions:
```

These rules SHALL govern every agent decision.

---

# Lifecycle

An assessment progresses through the following phases.

```
CREATED

↓

PLANNING

↓

RECON

↓

SCANNING

↓

VALIDATION

↓

REPORTING

↓

COMPLETED

↓

ARCHIVED
```

Only valid transitions SHALL be permitted.

---

# Status

Allowed values

```
CREATED

PLANNING

RUNNING

WAITING_APPROVAL

PAUSED

FAILED

COMPLETED

ARCHIVED

CANCELLED
```

---

# Progress

```yaml
progress:

  total_tasks:

  completed_tasks:

  running_tasks:

  queued_tasks:

  failed_tasks:

  skipped_tasks:

  percentage:
```

Progress SHALL be derived from task state.

---

# Technology Inventory

```yaml
technologies:

  servers:

  frameworks:

  languages:

  databases:

  cms:

  authentication:

  cloud:

  waf:

  cdn:
```

This inventory SHALL evolve during execution.

---

# Asset Inventory

```yaml
assets:

  domains:

  subdomains:

  hosts:

  services:

  ports:

  endpoints:

  javascript:

  repositories:
```

---

# Child Objects

The assessment owns

```yaml
execution_plan:

tasks:

findings:

evidence:

reports:

approvals:
```

Child objects SHALL reference the parent assessment.

---

# Risk Summary

```yaml
risk:

  critical:

  high:

  medium:

  low:

  informational:

  verified:
```

The summary SHALL be automatically calculated.

---

# Audit Metadata

```yaml
audit:

  created_at:

  updated_at:

  completed_at:

  archived_at:

  last_activity:
```

Audit information SHALL be immutable.

---

# Relationships

```
Assessment

↓

Execution Plan

↓

Tasks

↓

Findings

↓

Evidence

↓

Reports
```

All objects SHALL maintain referential integrity.

---

# Validation Rules

An assessment SHALL be considered valid when

- Assessment ID exists
- Scope exists
- Rules of Engagement exist
- Status is valid
- Child references are valid
- Schema version exists

---

# Future Extensions

Future versions MAY add

- Compliance mappings
- Threat models
- Risk acceptance
- Asset ownership
- Business context

without breaking existing implementations.

---

# Success Criteria

A compliant Assessment object provides a single, authoritative source of truth for the entire penetration testing engagement.

No other object SHALL duplicate assessment-level metadata.