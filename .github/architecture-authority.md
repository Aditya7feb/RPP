# Architecture Authority

Version: 1.0.0

## Purpose

This document defines the architectural governance model for RPP.

The coding agent is responsible for implementing the architecture.

The coding agent is NOT responsible for redefining repository architecture.

Major architectural decisions require explicit approval.

---

## Agent Authority

The agent MAY

- Create packages
- Create schemas
- Create ADRs
- Update repository-index.yaml
- Improve documentation
- Improve examples
- Add cross references
- Add validation rules
- Add execution models
- Add error models
- Improve consistency

---

## Agent MUST NOT

Without explicit approval the agent SHALL NOT

- Rename repository layers
- Change dependency direction
- Introduce new top-level folders
- Delete packages
- Delete schemas
- Merge unrelated packages
- Change canonical terminology
- Change architecture philosophy
- Change repository standards

---

## Escalation

If the agent determines a major architectural improvement is required it SHALL

1. Stop
2. Produce an Architecture Proposal
3. Explain

- Problem
- Current Design
- Proposed Design
- Benefits
- Risks
- Migration Plan

Wait for approval before implementation.

---

## Repository Philosophy

The repository is

Implementation Independent

Tool Independent

Schema First

Documentation First

Layered

Observable

Deterministic

Reusable

Extensible

These principles SHALL NOT change.