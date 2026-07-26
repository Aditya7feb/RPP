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

API Security Skills

Status: Completed. The API Security layer SHALL comprise the five implemented skills
below. Each skill consumes the `api`, `endpoint`, and `service` Discovery Assets and
canonical schemas, consults the Policy Engine before every target-facing action,
tests authorization with two authorized controlled identities using minimal reads,
bounds resource-consumption probes to avoid denial of service, and produces
Observations, Evidence, Findings, and Risk classified with canonical weakness
identifiers and the OWASP API Security Top 10 (2023).

## Implemented

REST

GraphQL

SOAP

gRPC

WebSocket

## Scope Decisions

The following capabilities named in earlier planning were consolidated or deferred.
These are scoping decisions only; no capability is lost.

OpenAPI and Swagger SHALL be provided by the API Discovery skill in the Discovery
tier, which ingests API specification documents to inventory `api` and `endpoint`
Assets. They are specification formats consumed as discovery input rather than
independent API Security skills.

Rate Limiting SHALL be evaluated as Unrestricted Resource Consumption within each API
Security skill, aligned to OWASP API4:2023. Each skill confirms missing consumption
controls with bounded probes rather than delegating to a separate Rate Limiting
skill.

API Gateway SHALL be treated as a deployment topology rather than a distinct skill.
Gateway-fronted APIs are assessed through the same REST, GraphQL, SOAP, gRPC, and
WebSocket skills against the exposed surface.

Async APIs SHALL be deferred to a future API Security extension. Event-driven and
message-broker protocols require broker-specific transport adapters and safe-probing
strategies that SHALL be defined when that extension is introduced.

---

# Phase 7

Cloud Security Skills

Status: Completed. The Cloud Security layer SHALL comprise the six implemented skills
below. Each skill consumes per-provider shared clients that expose provider-native
metadata as data, consults the Policy Engine before every target-facing action,
interprets observed metadata without mutating the environment, and produces
Observations, Evidence, Findings, and Risk classified with canonical weakness
identifiers aligned to the applicable CIS Benchmark.

The supporting shared clients — AWS Client, Azure Client, GCP Client, and Container
Client — were introduced under the one-canonical-client-per-provider pattern and report
provider-native metadata as data without interpretation.

## Implemented

AWS

Azure

GCP

Kubernetes

Docker

Terraform

## Scope Decisions

The following capabilities named in earlier planning were consolidated or deferred.
These are scoping decisions only; no capability is lost.

Helm, Istio, and Ingress SHALL be assessed by the Kubernetes skill. Their resources are
Kubernetes workloads and configuration evaluated through the Kubernetes Client rather
than as separate skills.

IAM SHALL be assessed as an identity-and-access capability within each provider skill
(AWS, Azure, GCP), which interprets provider-native identity metadata. It is not a
separate skill.

Secrets SHALL be handled through the Secrets Client for credential resolution and
assessed as a secret-handling capability within the provider, Kubernetes, Docker, and
Terraform skills. It is not a separate skill.

Metadata Services SHALL be assessed as an instance-metadata capability within the AWS,
Azure, and GCP skills, which observe metadata-service reachability through their
provider clients. It is not a separate skill.

---

# Phase 8

Active Testing Capabilities

Status: Completed. Active Testing SHALL comprise the eight implemented capability packages
below, introduced as a dedicated capability tier at `skills/active-testing/`. These packages
are reusable security capabilities rather than transport or access clients; they remain
implementation-independent, emit only the canonical `payload`, `artifact`, and `metrics`
schemas alongside Observations, gate every target-facing action through the Policy Engine,
and produce no Findings or Risk. Domain capabilities interpret their outputs into Findings
and Risk.

The canonical `payload`, `artifact`, and `metrics` schemas were authored to support this
tier.

## Implemented

Payload Generation

Parameter Mining

Wordlists

Mutation Engine

Fuzzing

Replay

Traffic Recording

Traffic Comparison

## Scope Decisions

The following capabilities named in earlier planning were consolidated or deferred. These
are scoping decisions only; no capability is lost.

Input Generation SHALL be provided by the Payload Generation capability, which composes
inputs from templates, wordlist seeds, and mutation variants. The two names denote the same
input-composition capability.

Replay Engine SHALL be provided by the Replay capability, and Traffic Recording and Traffic
Comparison SHALL be provided by the correspondingly named capabilities.

---

# Phase 9

Evidence Capabilities

Status: Completed. The Evidence layer SHALL comprise the six implemented capability packages
below, introduced as a dedicated capability tier at `skills/evidence/`. These capabilities
collect and correlate evidence; they are policy-gated for target-facing collection, remain
implementation-independent, introduce no new canonical schemas, and produce no Findings or Risk.
The durable evidence lifecycle — packaging, integrity, archival, retention, and promotion — is a
set of lifecycle mechanics owned by the shared `evidence` infrastructure, which Evidence
capabilities invoke but do not implement.

## Implemented

Screenshot Capture

HTTP Archive

Network Trace

Artifact Collection

Log Collection

Timeline

## Scope Decisions

The following capabilities named in earlier planning were consolidated or deferred. These are
scoping decisions only; no capability is lost.

HAR, HTTP Archive, and Response Archive SHALL be provided by the HTTP Archive capability. HAR is a
serialization of HTTP evidence; response archival is HTTP evidence. They are one capability, not
three format packages.

Certificate Archive and File Archive SHALL be provided by the Artifact Collection capability, which
collects files, certificates, and other artifacts. They differ by artifact type, not by capability;
archival itself is a shared Evidence lifecycle mechanic, so the capability is named for its
responsibility, collection.

Metrics SHALL remain the canonical `metrics` schema emitted across tiers rather than becoming an
Evidence capability. A Metrics package would be a schema-only package.

Evidence Packaging SHALL NOT be a capability. Packaging, integrity, archival, retention, and
promotion are lifecycle mechanics owned by the shared `evidence` infrastructure, which Evidence
capabilities invoke.

---

# Phase 10

Reporting Capabilities

Status: Completed. The Reporting layer SHALL comprise the five implemented capability packages
below, introduced as a dedicated capability tier at `skills/reporting/`. These capabilities are
**read-only** over their inputs: Findings, canonical Risk, and Evidence are immutable and are never
created, modified, or replaced by Reporting. Canonical Risk is owned by Domain Security and remains
authoritative. Output formats are serializations, not capabilities. The tier introduces no new
canonical schemas.

## Implemented

Finding Correlation

Risk Analysis

Finding Mapping

Report Generation

Evidence Bundle

## Scope Decisions

The following capabilities named in earlier planning were consolidated or renamed. These are
scoping decisions only; no capability is lost.

Risk Scoring SHALL be provided by the Risk Analysis capability. The name reflects that the
capability performs normalization, aggregation, prioritization, and presentation analysis rather
than owning Risk. CVSS SHALL be one analytical method within Risk Analysis. Domain Security retains
ownership of canonical Risk, which is authoritative; where a calculated value differs, canonical
Risk prevails.

OWASP Mapping and MITRE ATT&CK Mapping SHALL be provided by the Finding Mapping capability. They are
the same enrichment concern applied to two frameworks.

Executive Reports and Technical Reports SHALL be provided by the Report Generation capability as
report types. SARIF, JSON, Markdown, and PDF SHALL be provided by Report Generation as output
serializations through the shared `reporting` package; they are not separate capabilities.

Evidence Bundles SHALL be provided by the Evidence Bundle capability, which assembles referenced
Evidence into a distributable bundle read-only.

---

# Phase 11

Master Agent Integration & Ownership Correction

Status: Completed. Phase 11 integrates the orchestration layer with the canonical architecture
rather than adding new capabilities. The Master Agent is defined as a pure orchestrator, normalized
into the canonical package structure at `agents/master/`, and the legacy agent taxonomy is replaced
by capability-oriented orchestration. No new schemas were introduced.

## Implemented

The Master Agent (`agents/master/`) SHALL be a canonical package comprising README, capabilities,
interface, configuration, execution, error-model, examples, and ADR-001. It owns planning,
reasoning, delegation, workflow coordination, approval gating, execution tracking, and completion,
and it owns no Findings, Evidence, Risk, or Reporting logic.

Orchestration SHALL target eight specialist tier agents, one per canonical capability tier:
Discovery, Authentication, Web Security, API Security, Cloud, Active Testing, Evidence, and
Reporting. Each specialist tier agent coordinates the capability packages within its tier; packages
remain implementation details inside each tier.

The Master Agent SHALL bind to the existing canonical schemas — assessment, scope,
rules-of-engagement, execution-plan, execution-state, task, agent-response, approval, and
workflow-definition — and the `task` schema SHALL be registered in the repository index.

The Master Agent SHALL invoke the Reporting pipeline in order — finding-correlation, risk-analysis,
report-generation, evidence-bundle — consuming outputs by reference only. Confidence SHALL reference
the canonical `skills/core/confidence-model`. Memory SHALL support orchestration only; capabilities
remain deterministic and never depend on orchestration memory.

## Scope Decisions

Planning, Reasoning, Delegation, Scheduling, Approval, Execution Policies, Communication, Memory, and
Context Management SHALL be orchestration concerns consolidated into the Master Agent canonical
package rather than separate agent folders.

Confidence Models SHALL NOT be redefined in the agent layer; the Master Agent references the
canonical Core confidence model, removing the prior duplication.

Knowledge Retrieval SHALL be treated as orchestration memory and context propagation, documented in
the Master Agent execution model, and is not a capability tier.

The legacy taxonomy — recon, scanners, exploit, execution, knowledge — SHALL be replaced by the
capability-oriented taxonomy. Migration SHALL proceed in two stages: first replace the taxonomy and
update all references, then remove the obsolete stub folders once no references remain.

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