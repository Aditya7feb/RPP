# Master Agent Delegation Policy

**File:** `agents/master/delegation.md`

**Version:** 1.0.0

---

# Purpose

The Delegation Policy defines how the Master Agent selects, schedules and coordinates specialist agents.

The Master Agent SHALL NOT perform specialist work.

Its responsibility is to identify the most appropriate specialist and delegate work.

---

# Guiding Principle

Every task must be owned by exactly one primary specialist.

The Master Agent must never execute specialist logic.

---

# Delegation Workflow

```
Identify Work

↓

Determine Capability Required

↓

Find Matching Agent

↓

Validate Dependencies

↓

Create Task

↓

Assign Task

↓

Wait for Completion

↓

Collect Results

↓

Update Assessment State
```

---

# Delegation Rules

The Master Agent SHALL delegate based on capability rather than agent name.

Example

```
Capability

↓

DNS Enumeration

↓

DNS Agent
```

NOT

```
Always use Recon Agent
```

---

# Capability Registry

Every registered agent SHALL expose

```yaml
agent:

  id:

  name:

  version:

  category:

  capabilities:

  supported_targets:

  dependencies:

  outputs:

  confidence:
```

Example

```yaml
agent:

  name: DNS Agent

  capabilities:

    - dns

    - mx

    - txt

    - ns

    - subdomains
```

---

# Capability Matching

Example

Assessment requires

```
TLS Analysis
```

Planner searches

```
Capability

TLS
```

Returns

```
TLS Agent
```

---

# Agent Selection Priority

When multiple agents support the same capability

Choose

1. Highest Version

2. Highest Confidence

3. Lowest Estimated Runtime

4. Lowest Noise

5. Most Specific Capability

Example

Preferred

```
JWT Agent
```

instead of

```
Generic Authentication Agent
```

---

# Recon Delegation

The following agents MAY execute simultaneously

- DNS Agent
- Port Agent
- TLS Agent
- Fingerprint Agent

Content Discovery

depends on

Fingerprint Agent.

---

# Scanner Delegation

Scanner Agents SHALL only execute after Recon completes.

Example

Technology detected

```
React
```

↓

Delegate

- DOM XSS Agent

- Secrets Agent

- CSP Agent

---

Technology detected

```
WordPress
```

↓

Delegate

- WordPress Agent

- Plugin Agent

- Upload Agent

- Authentication Agent

---

Technology detected

```
Drupal
```

↓

Delegate

- Drupal Agent

- CVE Agent

---

Technology detected

```
ASP.NET
```

↓

Delegate

- IIS Agent

- ASP.NET Agent

- ViewState Agent

---

Technology detected

```
Spring Boot
```

↓

Delegate

- Spring Agent

- Actuator Agent

- Swagger Agent

---

# Validation Delegation

Validation Agents require approval.

Before delegating

Verify

```text
Approval Granted?
```

YES

↓

Delegate

NO

↓

Skip Validation

---

# Reporting Delegation

Reporting Agent SHALL execute only when

- Recon complete

- Scanning complete

- Validation complete OR skipped

- Evidence merged

---

# Parallel Delegation

Independent work SHALL execute in parallel.

Example

```
DNS

Port

TLS

Fingerprint
```

Parallel

---

Example

```
JWT

Headers

Secrets

CSP
```

Parallel

---

# Sequential Delegation

Dependent work SHALL execute sequentially.

Example

```
Fingerprint

↓

Content Discovery

↓

GraphQL Detection

↓

GraphQL Scanner
```

---

# Dynamic Delegation

The Master Agent SHALL continuously discover new work.

Example

Content Discovery finds

```
/graphql
```

↓

Immediately delegate

```
GraphQL Agent
```

without restarting planning.

---

# Conditional Delegation

Delegate only when conditions are satisfied.

Example

```
Authentication Detected

↓

JWT Scanner
```

---

Example

```
No Authentication

↓

Do NOT schedule JWT Agent
```

---

# Retry Delegation

Retry only when

- Temporary MCP Failure

- Timeout

- Agent Crash

Do NOT retry when

- Scope Violation

- Approval Denied

- Unsupported Target

---

# Delegation Constraints

The Master Agent SHALL NOT

- Delegate duplicate work

- Delegate outside scope

- Delegate destructive validation

- Delegate unsupported targets

- Delegate without dependencies

---

# Evidence Ownership

Every delegated task remains owned by the specialist.

The Master Agent aggregates evidence.

It SHALL NEVER modify evidence.

---

# Conflict Resolution

When two agents return conflicting findings

The Master Agent SHALL

1. Compare evidence

2. Compare confidence

3. Request another specialist if necessary

4. Preserve both findings until resolved

---

# Delegation Quality Checklist

Before assigning a task verify

✅ Correct capability

✅ Correct specialist

✅ Dependencies complete

✅ Scope valid

✅ No duplicate work

✅ Approval satisfied

✅ Required evidence available

---

# Guiding Principles

Always

- Delegate by capability

- Prefer specialists over generic agents

- Maximize parallel execution

- Respect dependencies

- Preserve evidence ownership

- Never duplicate work

- Continuously adapt to new discoveries