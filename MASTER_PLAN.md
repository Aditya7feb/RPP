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

Scope

Rules of Engagement

Asset

Asset Relationship

Observation

Risk

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

Status: Completed. The Discovery layer SHALL comprise the eleven implemented
skills below. Each skill consumes shared infrastructure and canonical schemas,
consults the Policy Engine before every target-facing action, and produces
canonical Assets, Asset Relationships, Observations, Evidence, Findings, and Risk.

## Implemented

DNS Enumeration

Subdomain Discovery

Port Discovery

TLS Analysis

Content Discovery

Technology Fingerprinting

Virtual Host Discovery

API Discovery

Endpoint Enumeration

Asset Discovery

Recon

---

## Scope Decisions

The following capabilities named in earlier planning were consolidated or
deferred. These are scoping decisions only; no capability is lost.

Directory Enumeration SHALL be provided by Content Discovery. Directory and path
enumeration is one discovery vector among several that yield endpoint and
web-application Assets, so it is delivered as a capability of Content Discovery
rather than as a separate skill.

Certificate Enumeration SHALL be provided by TLS Analysis. Certificate discovery
and interpretation are inseparable from TLS posture analysis, so certificate
Assets are produced by TLS Analysis rather than by a separate skill.

Cloud Asset Discovery SHALL be deferred to Phase 7 (Cloud Security). Cloud asset
enumeration depends on cloud-provider capabilities that belong to the Cloud tier,
not to network-facing Discovery, and SHALL be defined there.

---

# Phase 4

Authentication Skills

Status: Completed. The Authentication layer SHALL comprise the eight implemented
skills below. Each skill consumes Discovery Assets and canonical schemas, consults
the Policy Engine before every target-facing action, produces Observations,
Evidence, Findings, and Risk, and never persists credentials or secrets.

## Implemented

Session Management

API Keys

CSRF

JWT

mTLS

OAuth2

OIDC

SAML

---

## Scope Decisions

The following capabilities named in earlier planning were consolidated or deferred.
These are scoping decisions only; no capability is lost.

Basic Authentication, Bearer Authentication, and Cookie Authentication SHALL be
covered as authentication mechanisms within the Session Management and API Keys
skills rather than as separate skills. These are credential-transport schemes whose
weaknesses (cleartext transport, weak validation, insecure cookie attributes) are
evaluated by the existing skills.

Password Reset and Account Registration SHALL be deferred to the Web Security tier
(Phase 5). These are application-workflow flows whose weaknesses are evaluated as
business-logic and input-handling concerns rather than authentication-mechanism
concerns.

Authorization Models, including RBAC and ABAC, SHALL be deferred to a dedicated
Authorization tier. Authorization decisions are distinct from authentication and are
evaluated after identity is established; they SHALL be defined in that tier rather
than in Authentication.

---

# Phase 5

Web Security Skills

Status: Completed. The Web Security layer SHALL comprise the fifteen implemented
skills below. Each skill consumes Discovery Assets and canonical schemas, consults
the Policy Engine before every target-facing action, confirms weaknesses with
bounded non-destructive evidence, and produces Observations, Evidence, Findings, and
Risk classified with canonical weakness identifiers.

## Implemented

Clickjacking

Content Security Policy

CORS

Open Redirect

XSS

SQL Injection

Command Injection

Path Traversal

SSTI

XXE

SSRF

IDOR

File Upload

Deserialization

Cache Poisoning

---

## Scope Decisions

The following capabilities named in earlier planning were consolidated or deferred.
These are scoping decisions only; no capability is lost.

SSTI SHALL provide Template Injection; the two names denote the same server-side
template injection capability, delivered by the SSTI skill.

Session Fixation and Session Hijacking SHALL be provided by the Session Management
skill in the Authentication tier, which evaluates session identifier rotation,
binding, and invalidation.

Race Conditions and Business Logic SHALL be deferred to a dedicated Business Logic
capability. These are application-workflow concerns whose evaluation depends on
per-application logic modeling rather than a single canonical weakness vector, and
SHALL be defined when that capability is introduced.

Prototype Pollution SHALL be deferred to a future Web Security extension. It is a
JavaScript-runtime-specific weakness whose safe confirmation strategy will be defined
when that extension is introduced.

HTTP Request Smuggling and Host Header Injection SHALL be deferred to a future Web
Security extension focused on request-parsing and routing weaknesses, which require
front-end and back-end parsing-differential modeling defined at that time.

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