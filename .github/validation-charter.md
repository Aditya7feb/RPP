# Validation Charter

Version: 1.0.0

## Purpose

This document defines the mandatory quality gates for the Robust PenTest Platform (RPP).

A package SHALL NOT be marked as `completed` until every validation gate passes.

---

# Validation Philosophy

Validation is mandatory.

Completeness is preferred over speed.

Architectural correctness is preferred over convenience.

Documentation quality is treated as a first-class deliverable.

---

# Package Validation

Every package SHALL contain:

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/
  - ADR-001.md

No additional mandatory files may be omitted.

---

# Documentation Validation

Every document SHALL:

- use consistent terminology
- follow repository naming conventions
- avoid placeholders
- contain no TODOs
- contain no FIXME markers
- contain no incomplete sections
- use relative links only
- include cross-references where appropriate

---

# Schema Validation

Every new schema SHALL:

- have a unique canonical name
- not duplicate an existing schema
- define its purpose
- define required fields
- define optional fields
- define relationships
- define validation rules
- include at least one example
- define extension points
- include version information

---

# Dependency Validation

The repository SHALL maintain an acyclic dependency graph.

Validation MUST verify:

- no circular dependencies
- no upward dependencies
- no missing dependencies
- no duplicate dependencies
- dependency direction follows repository architecture

---

# Cross Reference Validation

Every referenced document SHALL exist.

Validation MUST verify:

- relative links resolve
- package references exist
- schema references exist
- ADR references exist

Broken links SHALL fail validation.

---

# Architecture Validation

Every package SHALL:

- belong to exactly one architectural layer
- expose only canonical interfaces
- remain implementation independent
- remain tool independent
- follow repository layering rules

---

# ADR Validation

Every package SHALL contain at least one ADR.

Every ADR SHALL include:

- Context
- Decision
- Consequences

---

# Examples Validation

Every package SHALL include examples demonstrating:

- successful execution
- failure scenarios
- edge cases (where applicable)

Examples SHALL remain implementation independent.

---

# Error Model Validation

Every package SHALL define:

- expected failures
- validation failures
- runtime failures
- recovery behaviour

---

# Security Validation

Documentation SHALL NOT:

- expose secrets
- hardcode credentials
- recommend unsafe defaults
- require implementation-specific behaviour
- bypass repository policies

---

# Repository Validation

After every completed package verify:

- repository-index.yaml updated
- package status updated
- schema inventory updated
- dependency graph updated
- completion metrics updated

---

# Consistency Validation

Repository terminology SHALL remain consistent.

Validation SHALL detect:

- duplicate concepts
- conflicting terminology
- overlapping capabilities
- duplicate schemas

---

# Definition of Done

A package is considered complete only when:

- every mandatory file exists
- every quality gate passes
- no broken references remain
- documentation is internally consistent
- repository metadata has been updated
- self-review has completed successfully

Only then MAY the package status be changed to:

status: completed

---

# Continuous Validation

The implementation agent SHALL:

1. Validate before generation.
2. Validate during generation.
3. Validate after generation.
4. Repair any failures automatically.
5. Repeat validation until all checks pass.

A package SHALL NEVER be marked complete while any validation fails.