# SSH Client Examples

**File:** `skills/shared/ssh-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
SSH Client Shared Skill in use.

Examples demonstrate transport negotiation, host-key trust, authentication,
bounded execution, governance, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Algorithm And Host-Key Probe

An SSH-server assessment skill connects, records algorithms, and pins the host
key.

## Invocation

```yaml
metadata:
  request_id: req-9601
  assessment_id: asmt-42
  task_id: task-ssh-probe
  skill_id: ssh-assessment
host: bastion.example.com
port: 22
trust_policy: trust_on_first_use
known_host_ref: knownhosts-asmt-42
username: audit
method: public_key
credential_ref: cred-ssh-audit
operations: []
```

## Result

```yaml
outcome: completed
algorithms:
  kex: curve25519-sha256
  cipher: aes256-gcm
  mac: hmac-sha2-256
host_key:
  fingerprint: SHA256:9x...
  trust_decision: pinned
authenticated: true
```

Algorithms are recorded as data; whether any is weak is determined by domain
skills.

---

# Example 2 — Strict Host-Key Rejection

Under `strict`, a changed host key is rejected.

## Result

```yaml
outcome: host_key_rejected
error:
  category: HostKey
  code: host_key_rejected
  fingerprint: SHA256:different...
  retryable: false
```

The session fails safely; the fingerprint is preserved for audit.

---

# Example 3 — Bounded Command Execution

An authorized configuration-review command is executed with bounded output.

## Configuration

```yaml
execution:
  allow_command_execution: true
bounds:
  max_output_bytes: 2MB
```

## Operation

```yaml
operations:
  - kind: exec
    command: sshd -T
```

## Result

```yaml
operation_results:
  - kind: exec
    exit_status: 0
    output_ref: artifact://ssh/req-9601-sshd-config
    truncated: false
```

Command output is stored by reference and bounded.

---

# Example 4 — Execution Not Authorized

An `exec` operation is attempted while execution is disabled.

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: rejected
  retryable: false
```

Command execution is intrusive and requires explicit authorization.

---

# Example 5 — Bounded Authentication Attempts

Authentication attempts are bounded to prevent brute-force behavior.

## Configuration

```yaml
authentication:
  max_attempts: 3
```

## Result When Exhausted

```yaml
outcome: auth_failed
error:
  category: Authentication
  code: auth_failed
  retryable: false
```

The shared skill does not perform credential guessing; brute-force belongs to a
dedicated authorized domain skill.

---

# Example 6 — Jump-Host Traversal

The session is routed through a jump host via the proxy skill.

## Governance References

```yaml
proxy_id: proxy-ssh-jump
```

The [Proxy](../proxy/README.md) shared skill provides traversal without exposing
implementation detail.

---

# Example 7 — Evidence Record

A single session produces the following evidence.

```yaml
evidence:
  type: ssh-session
  host: bastion.example.com:22
  algorithms:
    kex: curve25519-sha256
    cipher: aes256-gcm
  host_key_fingerprint: SHA256:9x...
  trust_decision: pinned
  auth_method: public_key
  commands_executed: 1
  duration_ms: 640
  decided_at: 2026-07-25T16:00:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes credentials and keys,
and supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
- [Authentication](../authentication/README.md)
