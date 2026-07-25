# RPP Agent Playbook

**Version:** 1.0.0

---

# Purpose

This document defines how AI coding agents SHOULD think, plan, and generate content for the Robust PenTest Platform (RPP).

Unlike `repository-manifest.yaml`, which defines repository rules, this playbook defines the agent's operating methodology.

Every AI agent contributing to RPP MUST follow this playbook before generating or modifying repository content.

---

# Primary Objective

Produce production-quality documentation that is:

- Implementation independent
- Tool independent
- Schema driven
- Architecturally consistent
- Reusable
- Merge ready

The objective is NOT to generate as many files as possible.

The objective is to preserve architectural integrity.

---

# Agent Workflow

Every task SHALL follow this sequence.

```
Understand Request
        ↓
Read Repository Standards
        ↓
Read Related Packages
        ↓
Read Existing Schemas
        ↓
Identify Dependencies
        ↓
Design
        ↓
Generate
        ↓
Self Review
        ↓
Update Repository Index
```

Never skip any step.

---

# Before Starting Any Task

The agent MUST read:

```
MASTER_PLAN.md

repository-index.yaml

.github/repository-manifest.yaml

.github/copilot-instructions.md
```

If modifying an existing package, also read:

- README
- ADRs
- Neighboring packages
- Related schemas

---

# Thinking Model

Before generating documentation, ask:

## Why does this package exist?

Never create a package because it "sounds useful."

It MUST satisfy a repository need.

---

## Is this functionality already available?

Reuse existing:

- schemas
- shared infrastructure
- terminology
- abstractions

Avoid duplication.

---

## Which layer owns this responsibility?

Never place logic into the wrong layer.

Example:

❌ HTTP Client performs XSS detection

✅ XSS Skill consumes HTTP Client

---

## Should this become a shared package?

If multiple skills need the same capability:

Create shared infrastructure.

Otherwise:

Keep it inside the domain skill.

---

# Layer Ownership

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

Agents

Dependencies MUST always flow downward.

---

# Package Creation Checklist

Before creating a package verify:

- Does it belong in this layer?
- Does a similar package already exist?
- Are schemas reusable?
- Can existing interfaces be extended?
- Is a new shared abstraction required?
- Does it introduce circular dependencies?

Only proceed when all answers are satisfactory.

---

# Schema Strategy

Prefer reuse.

Create a new schema ONLY when:

- Existing schemas cannot represent the concept.
- The concept has independent lifecycle.
- Multiple packages require it.
- It represents a canonical object.

Never create schemas for implementation details.

---

# Interface Strategy

Interfaces define capabilities.

Interfaces DO NOT expose tools.

Good

```
SendRequest()

ResolveHost()

ValidateCertificate()
```

Bad

```
curl()

RunOpenSSL()

RunNmap()
```

---

# Tool Independence

Consumers MUST never know whether execution uses:

- Native libraries
- Kali MCP
- Browser automation
- Docker
- Cloud APIs

Adapters hide implementation.

---

# Documentation Philosophy

Every document should answer:

Why?

What?

When?

How?

Inputs?

Outputs?

Dependencies?

Errors?

Extension points?

Examples?

---

# Writing Style

Prefer:

Clear

Direct

Deterministic

Normative

Avoid:

Marketing language

Ambiguity

Vendor-specific terminology

Implementation details

---

# RFC2119

Use

MUST

SHALL

SHOULD

MAY

Avoid:

maybe

probably

usually

sometimes

---

# Cross References

Every package SHOULD reference:

Related schemas

Related shared packages

Related ADRs

Related examples

Never duplicate documentation.

Reference it.

---

# ADR Guidance

Every package SHALL include

ADR-001

The ADR explains:

Why the abstraction exists.

Alternatives considered.

Trade-offs.

Future compatibility.

---

# Examples

Every package MUST contain realistic examples.

Examples SHALL demonstrate:

Consumer

Shared infrastructure

Schemas

Evidence

Expected outputs

---

# Error Model

Every package SHALL classify errors.

Typical categories:

Configuration

Validation

Connection

Execution

Authentication

Authorization

Transport

Timeout

Adapter

Internal

Unknown

---

# Evidence Philosophy

Everything important should be observable.

Evidence SHOULD include:

Inputs

Outputs

Metadata

Timings

Artifacts

Relationships

Evidence references

---

# Dependency Rules

Never create circular dependencies.

Good

```
DNS

↓

TLS

↓

HTTP

↓

Browser

↓

Recon
```

Bad

```
Recon

↓

HTTP

↓

Recon
```

---

# Self Review Checklist

Before finishing verify:

- Production quality
- No placeholders
- No TODOs
- No implementation code
- Cross references valid
- Examples complete
- Schemas reused
- Terminology consistent
- Layering preserved
- Dependencies valid

---

# Repository Evolution

When adding new functionality ask:

Can an existing package be extended?

If yes:

Extend it.

Otherwise:

Create a new package.

Never duplicate capability.

---

# Versioning

Breaking interface changes require:

Major version increment

New ADR

Migration documentation

Schema updates

Repository index update

---

# Updating Repository State

After completing work:

Update

repository-index.yaml

Mark package status.

Update dependencies.

Register new schemas.

Register ADRs.

---

# Commit Philosophy

One package per commit.

A commit SHOULD represent one logical architectural change.

Good

```
feat(shared/http-client): add HTTP Client package
```

Bad

```
misc updates
```

---

# Anti-Patterns

Never:

Duplicate schemas

Create tool-specific interfaces

Hardcode vendor behaviour

Mix infrastructure with security logic

Skip ADRs

Skip examples

Ignore repository standards

Expose implementation details

Introduce cyclic dependencies

---

# Decision Tree

Need reusable capability?

↓

YES

↓

Shared Infrastructure

↓

Need canonical object?

↓

YES

↓

Schema

↓

Need architectural explanation?

↓

ADR

↓

Need examples?

↓

Always YES

---

# Definition of Done

A package is complete only if:

- Documentation is production ready
- Required package files exist
- ADR exists
- Schemas are complete
- Examples exist
- Error model exists
- Execution model exists
- Cross references are valid
- Repository index updated
- Merge ready

Anything less is incomplete.

---

# Guiding Principle

The repository should describe **how autonomous penetration testing systems are architected**, not how a specific tool or programming language works.

Every contribution SHOULD move the repository toward becoming the canonical, implementation-independent knowledge base for autonomous security testing.