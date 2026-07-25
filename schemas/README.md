# RPP Canonical Schemas

**Directory:** `schemas/`

**Version:** 1.0.0

---

# Purpose

This directory contains the canonical data models used throughout the Robust PenTest Platform (RPP).

These schemas define the common language shared by every component of the platform.

All agents, skills, workflows, reports, templates, and future implementations SHALL reference these schemas.

No component SHALL redefine these objects independently.

---

# Design Goals

The schema definitions are intended to be

- Human readable
- Implementation independent
- Language agnostic
- Versioned
- Extensible
- Backward compatible where practical

These documents describe the logical structure of the platform rather than a specific programming language or serialization format.

---

# Relationship to Agents

Agents describe **behavior**.

Schemas describe **data**.

Example

```
Agent

↓

Creates Task

↓

Task follows task.md

↓

Returns Findings

↓

Finding follows finding.md

↓

References Evidence

↓

Evidence follows evidence.md
```

Agents SHALL never create proprietary object definitions.

---

# Relationship to Skills

Skills consume and produce canonical objects.

Example

```
Recon Skill

↓

Receives

Assessment

↓

Produces

Technology

Evidence

Finding
```

---

# Relationship to Reports

Reports SHALL reference canonical schemas.

Example

```
Report

↓

Finding

↓

Evidence

↓

Technology

↓

Assessment
```

No report SHALL define its own finding structure.

---

# Schema Hierarchy

```
Assessment

├── Execution Plan
├── Tasks
├── Technologies
├── Findings
├── Evidence
├── Approvals
├── Reports
└── Audit Metadata
```

---

# Available Schemas

## assessment.md

Defines

- Assessment metadata
- Scope
- Progress
- Status
- Technology inventory
- Asset inventory

---

## task.md

Defines

- Unit of work
- Ownership
- Dependencies
- Execution state
- Priority

---

## finding.md

Defines

- Security finding
- Severity
- Confidence
- Root cause
- Recommendations
- Evidence references

---

## evidence.md

Defines

- Evidence metadata
- Integrity
- Ownership
- Correlation
- Chain of custody

---

## certificate.md

Defines

- Parsed X.509 certificate metadata
- Subject and issuer identity
- Validity period
- Public key and signature details
- Certificate evidence references

---

## certificate-chain.md

Defines

- Ordered certificate chains
- Leaf and issuer relationships
- Trust anchor references
- Chain completeness
- Certificate evidence references

---

## tls-connection.md

Defines

- TLS connection lifecycle
- Target transport metadata
- Handshake references
- Session references
- Validation and evidence references

---

## tls-handshake.md

Defines

- Negotiated TLS protocol version
- Cipher suite
- ALPN protocol
- SNI usage
- Handshake timing and evidence

---

## tls-session.md

Defines

- TLS session identity
- Session reuse status
- Resumption metadata
- Session isolation scope
- Expiration and evidence references

---

## tls-validation-result.md

Defines

- Certificate validation status
- Hostname validation status
- Trust-chain evaluation
- Revocation result
- Validation reasons and evidence

---

## http-request.md

Defines

- Outbound HTTP request
- Method, URL, and HTTP version
- Headers, query, cookies, and body
- Authentication and execution options
- Request evidence references

---

## http-response.md

Defines

- Normalized HTTP response
- Status, headers, and cookies
- Body, MIME type, and encoding
- Redirect, TLS, and timing references
- Response evidence references

---

## http-header.md

Defines

- Single HTTP header field
- Name, value, and normalization
- Direction and ordering
- Multi-value handling
- Sensitivity and redaction

---

## http-cookie.md

Defines

- Single HTTP cookie
- Name, value, and scope attributes
- Expiry and persistence
- Security attributes
- Cookie evidence references

---

## http-session.md

Defines

- HTTP session state
- Cookie store and authentication
- Connection reuse and isolation
- Session lifecycle
- Session evidence references

---

## http-transaction.md

Defines

- Complete HTTP exchange
- Request and response linkage
- Redirect, timing, and TLS references
- Outcome and metrics
- Transaction evidence references

---

## http-redirect.md

Defines

- HTTP redirect chain
- Ordered hops and status codes
- Method changes
- Loop detection and termination
- Redirect evidence references

---

## http-timing.md

Defines

- HTTP timing metrics
- Per-phase durations
- Total duration
- Retry timing
- Timing evidence references

---

## technology.md

Defines

- Technology inventory
- Frameworks
- Languages
- Servers
- Libraries
- Detection confidence

---

## approval.md

Defines

- Human approval requests
- Approval decisions
- Expiration
- Audit trail

---

## execution-plan.md

Defines

- Assessment execution graph
- Dependencies
- Scheduling
- Parallel execution
- Milestones

---

## execution-state.md

Defines

- Runtime state
- Progress
- Active tasks
- Queued tasks
- Failed tasks

---

## agent-response.md

Defines

- Agent outputs
- Status
- Findings
- Evidence
- Errors
- Metadata

---

## report.md

Defines

- Executive summary
- Technical findings
- Risk summary
- Recommendations
- References

---

# Versioning

Every schema SHALL contain

- Schema Version
- Last Updated
- Change History (optional)

Schema versions SHALL evolve independently from agent versions.

---

# Naming Rules

Schema names SHALL use lowercase.

Examples

```
assessment.md

finding.md

evidence.md

task.md
```

Object names SHALL remain stable across versions whenever practical.

---

# Design Principles

Every schema SHALL

- Have a single responsibility
- Avoid duplication
- Be implementation independent
- Be self-contained
- Reference other schemas rather than redefining them

---

# Cross References

Schemas are expected to reference one another.

Example

```
Assessment

↓

Task

↓

Finding

↓

Evidence
```

These relationships SHALL be documented explicitly.

---

# Future Machine-Readable Definitions

This repository currently contains human-readable specifications.

Future versions MAY include

```
JSON Schema

OpenAPI Components

Protocol Buffers

Avro

TypeScript Types

Python Models

C# Models
```

These machine-readable definitions SHALL remain consistent with the canonical Markdown specifications.

---

# Compliance

An implementation is considered schema-compliant when

- It uses the canonical object definitions
- It does not redefine shared objects
- It preserves required relationships
- It maintains version compatibility

---

# Guiding Principles

The `schemas/` directory is the authoritative definition of data within RPP.

Agents define behavior.

Skills define capabilities.

Tools perform operations.

Schemas define the data that binds them together.

Every platform component SHALL speak the same language by using these canonical schemas.
