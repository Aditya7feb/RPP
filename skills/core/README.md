# Skills

The `skills/` directory contains the reusable capabilities executed by agents within the Robust PenTest Platform (RPP).

Skills represent the smallest reusable unit of work that performs a specific security, networking, reconnaissance, validation, analysis, or reporting operation.

Unlike agents, skills do not make orchestration decisions. They execute well-defined operations and return standardized results.

---

# Purpose

This directory defines

- Skill architecture
- Skill lifecycle
- Skill execution model
- Input and output contracts
- Dependency management
- Confidence model
- Error handling
- Approval requirements
- Skill implementation guidelines
- Reference examples

Individual skill implementations are organized into separate directories.

---

# What is a Skill?

A Skill is a reusable capability that performs one specific task.

Examples include

- Send an HTTP request
- Parse HTML
- Resolve DNS
- Perform TLS inspection
- Execute Nmap
- Run Nuclei
- Enumerate GraphQL schema
- Capture screenshots
- Parse JavaScript
- Extract secrets
- Validate SQL Injection
- Generate a report section

A skill should solve **one problem well**.

---

# Skills vs Agents

Agents coordinate work.

Skills perform work.

```
Master Agent
      │
      ▼
Recon Agent
      │
      ▼
HTTP Skill

DNS Skill

TLS Skill

HTML Parser

Technology Detector
```

Multiple agents MAY reuse the same skill.

A skill SHALL NOT depend on a specific agent.

---

# Design Principles

Every skill SHALL be

- Reusable
- Stateless
- Deterministic
- Composable
- Observable
- Versioned
- Independently testable

---

# Skill Characteristics

A skill SHOULD

- Solve one problem
- Accept structured inputs
- Produce structured outputs
- Report confidence
- Report metrics
- Report errors
- Produce evidence when applicable

---

# Skill Categories

Typical categories include

## Networking

- DNS
- HTTP
- TCP
- UDP
- TLS
- ICMP

---

## Discovery

- Technology Detection
- Service Detection
- Endpoint Discovery
- Directory Discovery

---

## Authentication

- JWT
- OAuth
- API Keys
- Session Analysis

---

## Web Security

- XSS
- SQL Injection
- CSRF
- SSRF
- XXE
- SSTI
- File Upload
- Deserialization

---

## API Security

- REST
- GraphQL
- SOAP
- gRPC

---

## Cloud

- Azure
- AWS
- GCP

---

## Infrastructure

- Kubernetes
- Docker
- Linux
- Windows
- Active Directory

---

## Analysis

- HTML Parsing
- JavaScript Analysis
- Secret Detection
- Fingerprinting

---

## Reporting

- Report Generation
- Evidence Packaging
- Risk Aggregation

---

# Skill Structure

Each skill SHOULD follow a common directory structure.

Example

```text
skills/

    http/

        README.md

        prompt.md

        input-output.md

        execution.md

        examples.md

        troubleshooting.md
```

Implementations MAY include additional documentation.

---

# Relationship

```
Assessment

↓

Task

↓

Agent

↓

Skill

↓

Evidence

↓

Finding
```

---

# Execution Model

Skills SHALL

1. Receive structured input.
2. Validate input.
3. Execute work.
4. Collect evidence.
5. Report observations.
6. Return standardized output.

Skills SHALL NOT perform orchestration.

---

# Inputs

Skills SHOULD consume

- Assessment context
- Task information
- Runtime configuration
- Target information
- Previous evidence
- Technology inventory

---

# Outputs

Skills SHOULD produce

- Evidence
- Technologies
- Metrics
- Recommendations
- Errors
- Confidence
- Agent Response compatible output

---

# Dependencies

A skill MAY invoke another skill when appropriate.

Example

```
HTTP Skill

↓

HTML Parser

↓

Technology Detector
```

Dependency chains SHOULD remain shallow and well-defined.

---

# Versioning

Every skill SHALL maintain

- Name
- Version
- Author
- Changelog
- Compatibility information

Breaking changes SHOULD increment the major version.

---

# Documentation Requirements

Every skill SHOULD include

- Purpose
- Inputs
- Outputs
- Execution model
- Dependencies
- Error handling
- Examples
- Limitations
- Security considerations

---

# Relationship to Schemas

Skills SHALL use the canonical schemas defined in

```
schemas/
```

Including

- Assessment
- Task
- Finding
- Evidence
- Technology
- Agent Response

Skills SHALL NOT define alternative object formats.

---

# Quality Requirements

Every skill SHALL

✓ Perform one well-defined capability

✓ Produce deterministic outputs where practical

✓ Return structured results

✓ Report confidence

✓ Produce evidence when applicable

✓ Be independently testable

✓ Be reusable across agents

✓ Remain implementation-independent

---

# Future Extensions

Future versions MAY introduce

- Distributed execution
- Remote skill execution
- Marketplace packaging
- Capability discovery
- Skill signing
- Dependency resolution
- Semantic version constraints

Backward compatibility SHOULD be preserved.

---

# Success Criteria

A compliant skill is a reusable, self-contained capability that performs a single security-related operation and integrates seamlessly with every agent within the Robust PenTest Platform.

Collectively, the skills in this directory form the execution capabilities used by all agents while remaining independent of orchestration logic.