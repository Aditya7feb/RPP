# Database Client Examples

**File:** `skills/shared/database-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Database Client Shared Skill in use.

Examples demonstrate parameterized execution, encryption, transactions, result
bounding, governance, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Parameterized Read

A configuration-review skill runs a parameterized read over an encrypted
connection.

## Invocation

```yaml
metadata:
  request_id: req-9701
  assessment_id: asmt-42
  task_id: task-db-review
  skill_id: db-assessment
engine: postgresql
host: db.example.com
port: 5432
database: appdb
tls_mode: required
credential_ref: cred-db-audit
statements:
  - text: "SELECT usename FROM pg_user WHERE usesuper = $1"
    parameters:
      - true
    kind: read
```

## Result

```yaml
outcome: completed
tls_established: true
statement_results:
  - rows: 2
    result_ref: artifact://db/req-9701-superusers
```

The value is bound as a parameter; it is never interpolated into the statement
text.

---

# Example 2 — Injection Payload As A Parameter

A SQL-injection testing skill supplies a payload safely as a parameter.

## Invocation

```yaml
statements:
  - text: "SELECT id FROM items WHERE name = $1"
    parameters:
      - "' OR '1'='1"
    kind: read
```

## Result

```yaml
outcome: completed
statement_results:
  - rows: 0
```

The payload is treated as data. The domain skill compares behavior across
payloads to assess injection; the client itself never concatenates input.

---

# Example 3 — Interpolation Rejected

A statement that embeds a value directly is rejected.

## Invocation

```yaml
statements:
  - text: "SELECT id FROM items WHERE name = 'admin'"
    parameters: []
    kind: read
    embedded_value: true
```

## Result

```yaml
outcome: rejected
error:
  category: Validation
  code: interpolation_detected
  retryable: false
```

The parameterization boundary prevents injection regardless of caller input.

---

# Example 4 — Required Encryption Unavailable

Encryption is required but the engine connection cannot negotiate TLS.

## Result

```yaml
outcome: encryption_required_unavailable
error:
  category: Security
  code: encryption_required_unavailable
  retryable: false
```

The operation fails rather than connecting in cleartext.

---

# Example 5 — Write Blocked

A write statement is attempted while writes are disabled.

## Configuration

```yaml
execution:
  allow_write_statements: false
```

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: write_blocked
  retryable: false
```

Data modification is intrusive and requires authorization.

---

# Example 6 — Transactional Write With Rollback

An authorized transactional write rolls back on failure.

## Flow

```
BEGIN

INSERT ... (statement 1) → ok

UPDATE ... (statement 2) → constraint error

ROLLBACK
```

## Result

```yaml
outcome: completed
transaction_outcome: rolled_back
statement_results:
  - affected: 1
  - error:
      category: Statement
      code: statement_error
      engine_code: "23505"
```

The transaction rolls back to preserve consistency; no partial effect remains.

---

# Example 7 — Evidence Record

A single operation produces the following evidence.

```yaml
evidence:
  type: database-operation
  engine: postgresql
  target: db.example.com:5432/appdb
  tls_established: true
  statements:
    - kind: read
      parameter_count: 1
      rows: 2
  duration_ms: 58
  decided_at: 2026-07-25T16:30:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes credentials and
parameter values, and supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
