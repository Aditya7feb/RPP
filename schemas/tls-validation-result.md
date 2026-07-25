# TLS Validation Result Schema

**File:** `schemas/tls-validation-result.md`

**Version:** 1.0.0

---

# Purpose

The TLS Validation Result Schema defines the canonical representation of certificate and hostname validation performed for a TLS connection.

A TLS Validation Result SHALL state the validation policy used so consumers do not infer validation from a successful handshake.

---

# Design Principles

A TLS Validation Result SHALL be

- Explicit
- Policy aware
- Evidence backed
- Traceable
- Adapter independent
- Separate from finding severity
- Safe for consumers

---

# Identity

Every TLS Validation Result SHALL contain

```yaml
validation_id:

schema_version:
```

Validation IDs SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Relationship to Connection

Every TLS Validation Result SHALL contain

```yaml
connection_id:
```

`connection_id` SHALL reference the TLS connection being validated.

---

# Policy

Every TLS Validation Result SHALL contain

```yaml
policy:
```

Allowed values

```
strict

report_only

disabled
```

---

# Status

Every TLS Validation Result SHALL contain

```yaml
status:
```

Allowed values

```
valid

invalid

not_checked

indeterminate
```

`disabled` policy SHALL use `not_checked`.

---

# Timing

Every TLS Validation Result SHALL contain

```yaml
validated_at:
```

`validated_at` SHALL be an RFC 3339 UTC timestamp.

---

# Hostname Validation

TLS Validation Results MAY contain

```yaml
hostname:

hostname_match:
```

`hostname` SHALL be required when hostname verification was requested.

`hostname_match` SHALL be required when `hostname` is present.

---

# Chain Validation

TLS Validation Results MAY contain

```yaml
chain_trusted:

certificate_chain_id:
```

`chain_trusted` SHALL be required for `strict` and `report_only` policies after chain validation.

`certificate_chain_id` SHALL reference the evaluated Certificate Chain when available.

---

# Time Validation

TLS Validation Results MAY contain

```yaml
time_valid:
```

`time_valid` SHALL be required when certificate time validation was performed.

---

# Revocation

Every TLS Validation Result SHALL contain

```yaml
revocation_checked:
```

TLS Validation Results MAY contain

```yaml
revocation_status:
```

Allowed revocation status values

```
good

revoked

unknown

not_available
```

`revocation_status` SHALL be required when `revocation_checked` is true.

---

# Reasons

Every TLS Validation Result SHALL contain

```yaml
reasons:
```

`reasons` SHALL be an array of canonical reason codes.

Allowed reason codes include

- UNTRUSTED_CHAIN
- HOSTNAME_MISMATCH
- CERTIFICATE_EXPIRED
- CERTIFICATE_NOT_YET_VALID
- CERTIFICATE_REVOKED
- REVOCATION_UNKNOWN
- MISSING_PEER_CERTIFICATE
- VALIDATION_NOT_PERFORMED

`reasons` SHALL be empty only for `valid`.

---

# Evidence

Every TLS Validation Result SHALL contain

```yaml
evidence:
```

Evidence IDs SHALL conform to `schemas/evidence.md`.

---

# Extensions

TLS Validation Results MAY contain

```yaml
extensions:
```

Extensions SHALL contain namespaced, non-secret adapter metadata.

---

# Example

```yaml
validation_id: tlsval-01
schema_version: 1.0.0
connection_id: tlsconn-01
policy: strict
status: valid
validated_at: '2026-07-25T10:00:01Z'
hostname: api.example.com
hostname_match: true
chain_trusted: true
time_valid: true
revocation_checked: false
reasons: []
certificate_chain_id: tlschain-01
evidence:
  - evidence-tls-01
```

---

# Validation Rules

A valid TLS Validation Result SHALL contain

- Validation ID
- Schema Version
- Connection ID
- Policy
- Status
- Validation Timestamp
- Revocation Checked Status
- Reason Codes
- Evidence References

`status: valid` SHALL require `chain_trusted: true` and `hostname_match: true` whenever hostname verification was requested.

---

# Success Criteria

A compliant TLS Validation Result object records exactly what validation was requested and what outcome was observed.

It enables consumers to distinguish successful TLS negotiation from trusted TLS validation while keeping finding interpretation outside the schema.
