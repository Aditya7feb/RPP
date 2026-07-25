# RPP (Robust PenTest Platform)
# Master Development Plan

Version: 1.0

---

# Vision

RPP is an implementation-independent, documentation-first knowledge platform for building autonomous penetration testing agents.

The repository defines:

- Canonical schemas
- Agent responsibilities
- Shared infrastructure
- Domain skills
- Execution models
- Evidence models
- Reporting models

It intentionally does NOT implement scanners or exploitation tools.

Instead, it defines the architecture that allows multiple execution backends (Native, Kali MCP, Cloud APIs, Browser Automation, etc.) to be used interchangeably.

---

# Core Principles

1. Documentation First
2. Tool Independent
3. Implementation Independent
4. Schema First
5. Reusable Shared Infrastructure
6. Deterministic Outputs
7. Observable Execution
8. Audit Friendly
9. Extensible
10. Production Quality

---

# Repository Structure

RPP/

```
agents/
schemas/
skills/
tool-adapters/
templates/
docs/
```

---

# Documentation Standards

Every document MUST

- be Markdown
- be production quality
- contain no TODOs
- contain no placeholders
- use RFC2119 terminology
- cross-reference related schemas
- define extension points
- include examples
- be internally consistent

---

# Package Standards

Every package MUST contain

```
README.md
capabilities.md
interface.md
configuration.md
execution.md
error-model.md
examples.md

adr/
```

Every ADR directory MUST contain at least

```
ADR-001
```

explaining the primary architectural decision.

---

# Canonical Development Order

The repository SHALL be developed in the following order.

---

# Phase 0

Repository

- Standards
- Contributing
- Versioning
- Glossary
- Architecture
- Naming

Status:

COMPLETE

---

# Phase 1

Schemas

Status:

ONGOING

Schemas include

Assessment

Task

Finding

Evidence

Technology

Execution State

Execution Plan

Agent Response

Report

Approval

HTTP

TLS

DNS

Browser

Authentication

Workflow

Reporting

Logging

Payload

Artifact

Metrics

Transaction

Session

Cookie

Header

Cache

Proxy

Retry

---

# Phase 2

Shared Infrastructure

## Completed

DNS Client

Authentication

Browser

TLS Client

HTTP Client

---

## Remaining

Proxy

Retry

Rate Limiter

Cache

Encoding

Serialization

Parsers

Logging

Evidence

Reporting

Workflow Runtime

TCP Client

UDP Client

WebSocket Client

gRPC Client

SMTP Client

FTP Client

SSH Client

Database Client

Filesystem Client

Secrets Client

Queue Client

Message Bus Client

Cloud Storage Client

Container Client

Kubernetes Client

---

# Phase 3

Discovery Skills

Recon

Port Discovery

DNS Enumeration

TLS Analysis

Content Discovery

Technology Fingerprinting

Directory Enumeration

Virtual Host Discovery

Asset Discovery

API Discovery

Subdomain Discovery

Endpoint Enumeration

Cloud Asset Discovery

Certificate Enumeration

---

# Phase 4

Authentication Skills

Session Management

JWT

OAuth2

OIDC

SAML

API Keys

Basic Authentication

Bearer Authentication

Cookie Authentication

mTLS

CSRF

Password Reset

Account Registration

Authorization Models

RBAC

ABAC

---

# Phase 5

Web Security Skills

XSS

SQL Injection

SSRF

SSTI

XXE

IDOR

Open Redirect

Path Traversal

Command Injection

File Upload

Template Injection

Race Conditions

Business Logic

Prototype Pollution

HTTP Request Smuggling

Deserialization

CORS

CSP

Clickjacking

Host Header Injection

Cache Poisoning

Session Fixation

Session Hijacking

---

# Phase 6

API Security

REST

SOAP

GraphQL

gRPC

WebSocket

Async APIs

OpenAPI

Swagger

Rate Limiting

API Gateway

---

# Phase 7

Cloud Security

AWS

Azure

GCP

Kubernetes

Docker

Terraform

Helm

Istio

Ingress

Secrets

IAM

Metadata Services

---

# Phase 8

Active Testing

Payload Generation

Fuzzing

Wordlists

Mutation Engine

Parameter Mining

Input Generation

Replay Engine

Traffic Recording

Traffic Comparison

---

# Phase 9

Evidence

Screenshot Collection

HAR

HTTP Archive

Network Trace

Certificate Archive

Response Archive

File Archive

Logs

Metrics

Timeline

---

# Phase 10

Reporting

Finding Correlation

Risk Scoring

CVSS

OWASP Mapping

MITRE ATT&CK Mapping

Executive Reports

Technical Reports

Evidence Bundles

SARIF

JSON

Markdown

PDF

---

# Phase 11

Master Agent

Planning

Reasoning

Delegation

Scheduling

Approval

Execution Policies

Confidence Models

Decision Trees

Communication

Knowledge Retrieval

Memory

Context Management

---

# Dependency Graph

```

Schemas

↓

Shared Infrastructure

↓

Discovery

↓

Authentication

↓

Web Security

↓

API Security

↓

Cloud

↓

Reporting

↓

Master Agent

```

No layer SHALL depend upon a higher layer.

---

# Architecture Rules

Domain Skills MUST NEVER

- invoke tools directly
- call curl
- call OpenSSL
- call requests
- call browser APIs
- parse CLI output

Instead they MUST depend on Shared Infrastructure.

---

# Shared Infrastructure Rules

Shared packages SHALL expose stable interfaces.

Implementations SHALL be hidden behind adapters.

---

# Tool Adapter Rules

Supported adapters include

Native

Kali MCP

Docker

Cloud APIs

Browser Automation

Future adapters

Consumers MUST remain unaware of the adapter implementation.

---

# Schema Rules

Every schema MUST define

Purpose

Fields

Required Fields

Validation Rules

Relationships

Examples

Versioning

Extension Points

---

# ADR Rules

Every package SHALL include

ADR-001

explaining

- why the abstraction exists
- why alternatives were rejected
- future compatibility
- tradeoffs

---

# Quality Gates

Every generated package MUST satisfy

✓ production quality

✓ markdown only

✓ no placeholders

✓ no TODOs

✓ examples included

✓ cross references included

✓ schema references valid

✓ extension points documented

✓ architecture consistent

✓ merge ready

---

# Expected Repository Size

Estimated packages

60–80

Estimated schemas

120–180

Estimated documentation pages

900–1500

Estimated markdown documents

1500–2500

---

# Agent Instructions

The coding agent SHALL

1. Read repository standards before generation.

2. Read neighboring packages before creating a new package.

3. Reuse existing schemas whenever possible.

4. Never duplicate concepts.

5. Create canonical abstractions.

6. Never expose implementation details.

7. Produce merge-ready documentation.

8. Maintain consistent terminology across the repository.

9. Keep dependencies acyclic.

10. Update cross-references when introducing new packages.

---

# Success Criteria

The repository SHALL become the canonical knowledge base for building autonomous penetration testing systems independent of language, framework, operating system, or execution backend.