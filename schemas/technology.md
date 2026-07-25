# Technology Schema

**File:** `schemas/technology.md`

**Version:** 1.0.0

---

# Purpose

The Technology Schema defines the canonical representation of technologies identified during a penetration testing assessment.

Technologies include operating systems, web servers, frameworks, programming languages, CMS platforms, libraries, cloud services, authentication mechanisms, and security products.

Technology detection forms the basis for adaptive planning and technology-specific testing.

Every discovered technology SHALL conform to this schema.

---

# Design Principles

A Technology object SHALL be

- Evidence-backed
- Versioned
- Traceable
- Reproducible
- Extensible
- Implementation-independent

Technology SHALL never be inferred without supporting evidence.

---

# Relationship

```
Assessment
    │
    ├── Technology Inventory
    │       │
    │       ├── Planning
    │       ├── Scanner Selection
    │       ├── Validation
    │       └── Reporting
```

---

# Identity

Every Technology SHALL include

```yaml
technology_id:

assessment_id:

schema_version:
```

---

# Basic Information

Every Technology SHALL define

```yaml
name:

category:

vendor:

version:

edition:
```

Example

```yaml
name: Apache HTTP Server

category: Web Server

vendor: Apache Software Foundation

version: 2.4.58
```

---

# Supported Categories

```
Operating System

Web Server

Framework

Programming Language

Runtime

CMS

Database

API Framework

Authentication

Cloud Provider

Container

Orchestrator

WAF

CDN

Load Balancer

Identity Provider

Security Product

Reverse Proxy

Message Queue

Storage

Monitoring

Other
```

---

# Detection Metadata

Every Technology SHALL record

```yaml
detected_by:

agent:

tool:

detected_at:
```

---

# Detection Method

Example values

```
HTTP Header

TLS Certificate

Response Fingerprint

JavaScript

HTML Source

API Response

DNS Record

Port Scan

Banner Grabbing

Manual Validation
```

Multiple methods MAY support the same Technology.

---

# Confidence

Allowed values

```
Low

Medium

High

Verified
```

Confidence SHALL follow the Master Agent Confidence Model.

---

# Evidence

Every Technology SHALL reference

```yaml
evidence:

- evidence_id
- evidence_id
```

A Technology SHALL NOT exist without supporting evidence.

---

# Location

Technology SHALL specify where it was observed.

```yaml
host:

endpoint:

service:

port:
```

Example

```yaml
host: app.example.com

port: 443

service: HTTPS
```

---

# Discovery Sources

Technology MAY be identified by

- Recon Agents
- Scanner Agents
- Validation Agents
- Human Analyst

All sources SHALL be recorded.

---

# Fingerprinting

Technology fingerprinting SHOULD include

```yaml
fingerprints:

headers:

cookies:

html:

javascript:

tls:

dns:
```

---

# Version Information

Technology versions SHALL include

```yaml
version:

version_source:

version_confidence:
```

Example

```
Apache

↓

Server Header

↓

Medium Confidence
```

---

# Relationships

Technologies MAY reference

```yaml
parent:

children:

dependencies:

related:
```

Example

```
NGINX

↓

PHP-FPM

↓

Laravel
```

---

# Security Relevance

Technology MAY include

```yaml
end_of_life:

known_cves:

supported:

security_notes:
```

This information MAY assist planning but SHALL NOT automatically create Findings.

---

# Scanner Mapping

Technology MAY reference

```yaml
recommended_agents:

recommended_skills:

recommended_tools:
```

Example

```
Technology

↓

Spring Boot

↓

Recommended Scanner

Spring Agent
```

---

# Lifecycle

```
Detected

↓

Confirmed

↓

Correlated

↓

Used For Planning

↓

Reported
```

---

# Deduplication

Multiple detections of the same Technology SHALL be merged.

Example

```
httpx

↓

Apache
```

+

```
WhatWeb

↓

Apache
```

↓

Single Technology Object

Evidence from both tools SHALL be preserved.

---

# Validation Rules

A valid Technology SHALL contain

- Technology ID
- Assessment ID
- Name
- Category
- Detection Metadata
- Confidence
- At least one Evidence reference

---

# Quality Requirements

Technology SHALL

✓ Be evidence-backed

✓ Have confidence

✓ Record detection source

✓ Record detection method

✓ Preserve version information when available

✓ Reference supporting evidence

---

# Future Extensions

Future versions MAY include

- CPE identifiers
- SBOM references
- Package manager metadata
- Container image information
- Software supply chain metadata
- Dependency graphs

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Technology object provides an accurate, evidence-backed inventory of technologies discovered during an assessment.

The Technology inventory SHALL serve as the authoritative source for adaptive planning, scanner selection, validation, and reporting.