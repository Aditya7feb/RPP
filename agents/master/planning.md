# Master Agent Planning Algorithm

**File:** `agents/master/planning.md`

**Version:** 1.0.0

---

# Purpose

The Planning Engine is responsible for converting an assessment request into an optimized execution plan.

The objective is to maximize coverage while minimizing execution time, duplicate work, unnecessary scans, and risk.

The Planning Engine SHALL NOT execute tools.

It SHALL only reason about what work needs to be delegated.

---

# Inputs

The Planning Engine receives:

```yaml
assessment:

  target:

  assessment_type:

  credentials:

  scope:

  exclusions:

  rate_limit:

  rules_of_engagement:

  allowed_protocols:

  customer_notes:
```

---

# Outputs

The Planning Engine produces

```yaml
execution_plan:

execution_graph:

selected_agents:

execution_order:

parallel_groups:

approval_points:
```

---

# Planning Objectives

The planner SHALL

- Determine the optimal execution order.
- Identify mandatory tasks.
- Identify optional tasks.
- Skip irrelevant agents.
- Schedule independent work in parallel.
- Respect Rules of Engagement.
- Reduce unnecessary traffic.
- Reduce assessment duration.
- Increase finding confidence.

---

# High-Level Workflow

```text
Receive Assessment

↓

Validate Input

↓

Load Rules

↓

Analyze Target

↓

Build Initial Knowledge

↓

Select Recon Agents

↓

Estimate Attack Surface

↓

Select Scanner Agents

↓

Determine Validation Candidates

↓

Insert Approval Gates

↓

Generate Execution Graph
```

---

# Step 1 — Validate Assessment

Before planning begins verify

- Target exists
- Scope defined
- Rules provided
- Target reachable
- Assessment type supported

If validation fails

STOP

---

# Step 2 — Load Rules of Engagement

Extract

- Allowed hosts
- Allowed ports
- Excluded paths
- Allowed protocols
- Authentication rules
- Allowed request rate
- Validation permissions

These rules override every planning decision.

---

# Step 3 — Classify Assessment

Determine

```text
Public Web

↓

Authenticated Web

↓

API

↓

GraphQL

↓

CMS

↓

Internal

↓

Bug Bounty

↓

Unknown
```

Classification affects every subsequent decision.

---

# Step 4 — Build Initial Knowledge

Collect existing information

Examples

- Previous assessments
- Customer supplied assets
- Existing technology stack
- Known credentials
- Known endpoints
- Existing reports

Do not rediscover information that already exists unless freshness is required.

---

# Step 5 — Select Recon Agents

The planner SHALL always begin with Recon.

Default Recon Agents

- DNS Agent
- Port Agent
- TLS Agent
- Fingerprint Agent

Content Discovery Agent

is delayed until

- Live HTTP services discovered.

---

# Recon Planning Rules

Always

```text
DNS

+

Port Scan

+

TLS

+

Fingerprint

↓

Merge

↓

Content Discovery
```

Never run

Content Discovery

before

HTTP services exist.

---

# Step 6 — Estimate Attack Surface

After Recon

Estimate

- Technologies
- Frameworks
- CMS
- APIs
- Authentication
- Admin Panels
- GraphQL
- JavaScript
- CDN
- WAF

---

# Step 7 — Select Scanner Agents

Scanner Agents are selected dynamically.

Examples

If

```text
WordPress
```

Detected

Schedule

- WordPress Agent
- Plugin Agent
- Upload Agent
- Authentication Agent
- Headers Agent

NOT

Drupal Agent

---

If

```text
GraphQL
```

Detected

Schedule

- GraphQL Agent

- Introspection Agent

- Authorization Agent

- JWT Agent

---

If

```text
React
```

Detected

Schedule

- DOM XSS Agent

- SourceMap Agent

- Secrets Agent

- CSP Agent

---

# Scanner Selection Principles

Only schedule

Applicable agents.

Avoid

Generic scanning when specialized scanning exists.

---

# Step 8 — Dependency Resolution

Every Agent declares

```yaml
depends_on:

requires:

produces:
```

Example

Content Discovery

depends_on

Fingerprint

GraphQL

depends_on

Content Discovery

JWT

depends_on

Authentication Detection

---

# Step 9 — Parallel Execution

The planner SHALL maximize parallel execution.

Example

```text
DNS

Port

TLS

Fingerprint

↓

Parallel
```

Example

```text
JWT

GraphQL

Headers

Secrets

↓

Parallel
```

Never execute dependent agents together.

---

# Step 10 — Approval Gates

Insert approval nodes before

- SQLi Validation

- File Upload Validation

- JWT Validation

- IDOR Validation

- Authentication Bypass

- SSTI Validation

- SSRF Validation

Without approval

Validation SHALL NOT execute.

---

# Cost-Aware Planning

Each agent has

```yaml
estimated_duration:

estimated_requests:

estimated_noise:

confidence_gain:
```

Planner SHOULD maximize

Confidence Gain

while minimizing

Runtime

---

# Duplicate Work Elimination

Before scheduling

Ask

Has another agent already collected this?

If YES

Reuse evidence.

Never repeat identical work.

---

# Adaptive Planning

Planning SHALL continue throughout execution.

After every completed task

Recalculate

- Remaining work
- New technologies
- New endpoints
- New attack surface
- New scanner candidates

Planning is continuous.

---

# Dynamic Replanning

Replan whenever

- New technology detected
- Agent fails
- New host discovered
- Human changes scope
- Approval denied
- Critical finding discovered

---

# Failure Recovery

If an agent fails

Determine

Retry?

Skip?

Replace?

Continue?

Planner SHALL choose the least disruptive option.

---

# Completion Criteria

Planning completes when

- Every executable task assigned.
- Dependencies resolved.
- Approval points inserted.
- Parallel groups created.
- Execution graph generated.

---

# Planning Principles

Always

✔ Recon before Scan

✔ Scan before Validation

✔ Validation before Reporting

✔ Evidence before Conclusions

✔ Parallel before Sequential

✔ Reuse before Rediscover

✔ Safety before Speed

✔ Human before Exploitation

---

# Quality Checklist

Before publishing an execution plan

Verify

✅ Dependencies resolved

✅ Scope respected

✅ Duplicate work removed

✅ Parallel opportunities maximized

✅ Approval gates inserted

✅ Unsupported agents removed

✅ Execution graph valid

✅ Reporting phase reachable

---

# Final Planning Goal

The Planning Engine exists to answer one question:

> **"What is the smallest amount of work required to achieve the highest-confidence assessment while remaining completely within scope?"**