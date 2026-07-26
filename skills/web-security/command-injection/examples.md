# Command Injection Examples

**File:** `skills/web-security/command-injection/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Command
Injection Skill. Examples illustrate the interface and outputs; they contain no
implementation code.

---

# Example 1 — Time-Based Command Injection

## Request

```yaml
target: https://app.example.com
payload_set_ref: cmdi-probes-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cmdi-5001
    title: Command injection confirmed by bounded induced delay
    weakness: CWE-78
    risk_ref: risk-cmdi-3001
    evidence_refs:
      - evidence-cmdi-7001
observations:
  - id: obs-cmdi-4001
    kind: time-signal-analysis
evidence:
  - id: evidence-cmdi-7001
    observation_ref: obs-cmdi-4001
status: completed
metrics:
  injection_points_tested: 5
  findings: 1
```

The `host` parameter induces a bounded conditional delay observed repeatedly,
confirming command injection without running a harmful command.

---

# Example 2 — Out-Of-Band Command Injection

## Request

```yaml
target: https://app.example.com
payload_set_ref: cmdi-probes-bounded
collector_ref: oob-collector-controlled
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings:
  - id: finding-cmdi-5002
    title: Command injection confirmed by out-of-band interaction
    weakness: CWE-78
    risk_ref: risk-cmdi-3002
    evidence_refs:
      - evidence-cmdi-7002
status: completed
metrics:
  injection_points_tested: 5
  findings: 1
```

An injected benign probe triggers an interaction to the controlled collector,
confirming command execution out-of-band.

---

# Example 3 — Requires Approval

## Request

```yaml
target: https://app.example.com
payload_set_ref: cmdi-probes-bounded
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: awaiting_approval
metrics:
  approvals_requested: 1
```

Command injection testing is high impact; the Rules of Engagement require approval,
so the skill defers until approval is granted.

---

# Example 4 — Policy Denial

## Request

```yaml
target: https://out-of-scope.example.net
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: denied
metrics:
  policy_denials: 1
```

The target is out of scope. The Policy Engine denies the action and no testing is
performed.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Timing Schema](../../../schemas/http-timing.md)
