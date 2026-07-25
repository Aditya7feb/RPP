# Evidence Schema

**File:** `schemas/evidence.md`

**Version:** 1.0.0

---

# Purpose

The Evidence Schema defines the canonical representation of evidence collected during a penetration testing assessment.

Evidence represents any artifact that supports, validates, or disproves a security finding.

Evidence is the foundation of trust within the Robust PenTest Platform (RPP).

Every Finding SHALL reference one or more Evidence objects.

---

# Design Principles

Evidence SHALL be

- Immutable
- Traceable
- Verifiable
- Timestamped
- Reproducible
- Auditable
- Versioned

Original evidence SHALL NEVER be modified.

---

# Relationship

```
Assessment
    │
    ├── Task
    │      │
    │      ├── Finding
    │      │      │
    │      │      └── Evidence
```

---

# Identity

Every Evidence object SHALL include

```yaml
evidence_id:

assessment_id:

task_id:

schema_version:
```

Evidence IDs SHALL be globally unique within an assessment.

---

# Classification

Evidence SHALL define

```yaml
category:

type:

source:
```

---

# Supported Categories

```
HTTP

NETWORK

DNS

TLS

APPLICATION

FILE

SCREENSHOT

LOG

CONFIGURATION

MANUAL

METADATA

TOOL_OUTPUT
```

---

# Supported Types

Examples include

```
HTTP Request

HTTP Response

Certificate

Packet Capture

Screenshot

JSON Response

HTML Response

Terminal Output

Tool Report

Log Entry

Configuration File

JavaScript File
```

Additional types MAY be introduced in future schema versions.

---

# Ownership

Every Evidence object SHALL record

```yaml
collected_by:

agent:

tool:
```

Example

```yaml
collected_by: TLS Agent

agent: Recon

tool: openssl
```

---

# Target

Evidence SHALL identify

```yaml
target:

host:

endpoint:

parameter:
```

---

# Collection Metadata

Every Evidence SHALL contain

```yaml
collected_at:

collection_method:

execution_id:
```

---

# Integrity

Evidence SHALL preserve integrity.

```yaml
hash:

hash_algorithm:

size:

encoding:
```

Recommended

```
SHA-256
```

or stronger.

---

# Content

Evidence SHALL reference

```yaml
content_type:

storage_location:

preview:
```

Examples

```
application/json

text/html

image/png

application/pcap
```

Large artifacts SHOULD be stored externally.

The schema SHOULD reference them.

---

# Relationships

Evidence MAY reference

```yaml
related_evidence:

derived_from:

supports_findings:
```

---

# Derived Evidence

Evidence MAY be derived.

Example

```
JavaScript File

↓

Extracted Secret

↓

Derived Evidence
```

The original Evidence SHALL remain unchanged.

---

# Confidence

Evidence MAY include

```yaml
confidence:

confidence_reason:
```

Evidence confidence contributes to Finding confidence.

---

# Sensitive Data

Evidence MAY contain sensitive information.

```yaml
contains_sensitive_data:

redacted:

encryption_required:
```

Sensitive values SHOULD be

- Masked
- Redacted
- Encrypted

when appropriate.

---

# Chain of Custody

Evidence SHALL record

```yaml
created_by:

processed_by:

referenced_by:

reported_by:
```

Every transition SHALL be auditable.

---

# Lifecycle

```
Collected

↓

Validated

↓

Stored

↓

Referenced

↓

Archived
```

Evidence SHALL remain immutable throughout the lifecycle.

---

# Storage

The schema SHALL NOT dictate storage technology.

Implementations MAY use

- Filesystem
- Database
- Object Storage
- Cloud Storage
- Evidence Vault

The schema SHALL only reference the location.

---

# Validation Rules

A valid Evidence object SHALL contain

- Evidence ID
- Assessment ID
- Task ID
- Category
- Type
- Source
- Collection Metadata
- Integrity Metadata
- Storage Reference

---

# Quality Requirements

Evidence SHALL

✓ Be reproducible

✓ Be traceable

✓ Preserve integrity

✓ Maintain ownership

✓ Record timestamps

✓ Reference the original artifact

✓ Support one or more Findings

---

# Common Examples

## HTTP Request

```yaml
category: HTTP

type: Request
```

---

## HTTP Response

```yaml
category: HTTP

type: Response
```

---

## TLS Certificate

```yaml
category: TLS

type: Certificate
```

---

## Screenshot

```yaml
category: SCREENSHOT

type: PNG
```

---

## Tool Output

```yaml
category: TOOL_OUTPUT

type: Nuclei JSON
```

---

# Future Extensions

Future schema versions MAY include

- Digital signatures
- Immutable storage references
- Evidence classification labels
- Compliance metadata
- AI annotations

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Evidence object provides a complete, immutable, and verifiable record of an observation collected during an assessment.

Every reported Finding SHALL be independently verifiable through its associated Evidence.