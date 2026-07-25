# Recon Skill

**File:** `skills/discovery/recon/README.md`

**Version:** 1.0.0

---

# Purpose

The Recon Skill is the Discovery-tier orchestrator of the Robust PenTest Platform
(RPP). It composes the individual Discovery skills into a single, coherent
reconnaissance workflow, driving them through the shared
[Workflow Runtime](../../shared/workflow-runtime/README.md) with approval gates
before every active phase.

Recon does not probe targets itself and does not deduplicate the asset graph. It
sequences the specialized Discovery skills — DNS Enumeration, Subdomain Discovery,
Port Discovery, TLS Analysis, Content Discovery, Fingerprinting, Virtual Host
Discovery, API Discovery, Endpoint Enumeration, and Asset Discovery — into an
ordered, policy-aware plan and consolidates their canonical outputs into a single
Discovery result.

Recon is the entry point a Recon Agent invokes to perform reconnaissance against
an authorized [Scope](../../../schemas/scope.md).

---

# Goals

The Recon Skill SHALL

- Compose the Discovery skills into an ordered reconnaissance workflow
- Drive execution through the
  [Workflow Runtime](../../shared/workflow-runtime/README.md) using a
  [Workflow Definition](../../../schemas/workflow-definition.md)
- Separate passive phases from active phases with approval gates
- Consult the [Policy Engine](../../shared/policy-engine/README.md) for scope and
  phase authorization
- Invoke Asset Discovery to consolidate the produced asset graph
- Aggregate Findings, Observations, and Evidence from all composed skills
- Remain tool independent and perform no probing itself

---

# Non-Goals

The Recon Skill SHALL NOT

- Probe, scan, resolve, or request any target directly
- Reimplement any capability of a composed Discovery skill
- Deduplicate or merge Assets itself (that is Asset Discovery)
- Grant approvals (it requests them through the Policy Engine and approval flow)
- Test Assets for vulnerabilities
- Invoke command-line tools or parse their output

Probing belongs to the specialized skills; consolidation belongs to Asset
Discovery; vulnerability testing belongs to later tiers.

---

# Design Principles

The Recon Skill SHALL be

- Compositional — it sequences skills, it does not perform their work
- Policy-aware — every phase is authorized before it runs
- Approval-gated — active phases require explicit authorization
- Deterministic given the same Scope, configuration, and skill outputs
- Evidence-preserving — it aggregates, never discards, evidence
- Tool independent

---

# Architecture

```
Recon Agent

↓

Recon Skill (orchestrator)

├── Plan Builder            → Workflow Definition
├── Phase Authorizer        → Policy Engine
├── Workflow Driver         → Workflow Runtime
│     ├── passive phase → DNS / Subdomain / passive Fingerprinting
│     ├── [approval gate]
│     └── active phase  → Port / TLS / Content / VHost / API / Endpoint
├── Consolidation Step      → Asset Discovery
└── Result Aggregator       → Evidence

↓

Consolidated Discovery Result (Assets · Relationships · Findings · Evidence)
```

Recon holds no transport dependency. It depends on the Workflow Runtime and the
Policy Engine, and it references the composed Discovery skills as workflow steps.

---

# Responsibilities

The Recon Skill is responsible for

- Building a [Workflow Definition](../../../schemas/workflow-definition.md) that
  orders the Discovery skills into passive and active phases
- Requesting phase authorization from the
  [Policy Engine](../../shared/policy-engine/README.md)
- Inserting approval gates before active phases
- Driving the workflow through the
  [Workflow Runtime](../../shared/workflow-runtime/README.md)
- Invoking Asset Discovery to consolidate the asset graph
- Aggregating [Findings](../../../schemas/finding.md),
  [Observations](../../../schemas/observation.md), and
  [Evidence](../../../schemas/evidence.md) from all composed skills
- Returning a single consolidated Discovery result

---

# Discovery Lifecycle

```
Receive Scope And Configuration

↓

Build Reconnaissance Workflow Definition

↓

Authorize Passive Phase (Policy Engine)

↓

Run Passive Discovery Skills (Workflow Runtime)

↓

[Approval Gate — active phase requires authorization]

↓

Authorize Active Phase (Policy Engine)

↓

Run Active Discovery Skills (Workflow Runtime)

↓

Consolidate Asset Graph (Asset Discovery)

↓

Aggregate Findings And Evidence

↓

Return Consolidated Discovery Result
```

Active phases SHALL NOT begin until their approval gate is satisfied.

---

# Inputs

The skill accepts

```yaml
scope_id:

roe_id:

targets:

profile:

assessment_id:
```

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md). `targets` are the
seed in-scope targets. `profile` selects a reconnaissance profile that determines
which phases and skills are composed.

---

# Produced Assets

The Recon Skill produces no Assets of its own. It returns the consolidated
[Assets](../../../schemas/asset.md) and
[Asset Relationships](../../../schemas/asset-relationship.md) produced by the
composed Discovery skills and reconciled by Asset Discovery.

---

# Produced Findings

The Recon Skill produces no Findings of its own beyond orchestration-level
Observations. It aggregates the [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md) emitted by the composed skills, each retaining its
own supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The Recon Skill SHALL request authorization from the
[Policy Engine](../../shared/policy-engine/README.md) before each phase and SHALL
insert an approval gate before every active phase. A phase SHALL run only when its
authorization decision permits it. Where a decision is `requires_approval`, the
skill SHALL pause the workflow until the approval is granted through the platform
approval flow. Individual composed skills additionally enforce policy on every
action.

---

# Dependencies

The Recon Skill depends on

- [Workflow Runtime](../../shared/workflow-runtime/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)

The Recon Skill composes, as workflow steps, the Discovery skills:
[DNS Enumeration](../dns-enumeration/README.md),
[Subdomain Discovery](../subdomain-discovery/README.md),
[Port Discovery](../port-discovery/README.md),
[TLS Analysis](../tls-analysis/README.md),
[Content Discovery](../content-discovery/README.md),
[Fingerprinting](../fingerprinting/README.md),
[Virtual Host Discovery](../virtual-host-discovery/README.md),
[API Discovery](../api-discovery/README.md),
[Endpoint Enumeration](../endpoint-enumeration/README.md), and
[Asset Discovery](../asset-discovery/README.md).

The Recon Skill SHALL NOT depend on any shared network client.

---

# Consumers

Typical consumers include

- The Recon Agent, which invokes reconnaissance against an authorized Scope
- Workflows that begin an assessment with a reconnaissance phase
- Reporting, through the aggregated Findings and Evidence

---

# Outputs

Typical outputs MAY include

- A consolidated Discovery result — Assets, Relationships, Findings, Evidence
- Orchestration Observations describing phase execution and approvals
- The executed Workflow Definition reference for auditability

Outputs SHALL remain implementation independent.

---

# Security Principles

The Recon Skill SHALL

- Perform no probing itself
- Authorize every phase through the Policy Engine
- Gate every active phase behind an explicit approval
- Preserve all Evidence from composed skills
- Never weaken the policy constraints of any composed skill
- Preserve auditability of phase execution and approvals

---

# Best Practices

Consumers SHOULD

- Provide a complete Scope and Rules of Engagement
- Select a reconnaissance profile matched to the engagement
- Rely on the approval gates rather than pre-authorizing active phases blindly
- Treat the consolidated result as the canonical Discovery output

---

# Anti-Patterns

Consumers SHOULD NOT

- Ask Recon to probe targets directly
- Bypass approval gates for active phases
- Duplicate Asset Discovery consolidation downstream
- Compose skills outside the Workflow Runtime

---

# Documentation Requirements

This skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-recon-orchestrator-skill.md

---

# Related Packages

- [Workflow Runtime](../../shared/workflow-runtime/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Asset Discovery](../asset-discovery/README.md)
- [DNS Enumeration](../dns-enumeration/README.md)
- [Port Discovery](../port-discovery/README.md)

---

# Canonical Schemas

- [Workflow Definition](../../../schemas/workflow-definition.md)
- [Asset](../../../schemas/asset.md)
- [Asset Relationship](../../../schemas/asset-relationship.md)
- [Finding](../../../schemas/finding.md)
- [Evidence](../../../schemas/evidence.md)
- [Scope](../../../schemas/scope.md)

---

# Architecture Decisions

- [ADR-001 — Recon Orchestrator Skill](adr/ADR-001-recon-orchestrator-skill.md)

---

# Future Extensions

Future versions MAY support

- Adaptive reconnaissance profiles driven by intermediate findings
- Iterative re-reconnaissance as new Assets emerge
- Parallel phase execution within policy limits
- Handoff of the consolidated graph to later assessment tiers

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Recon Skill composes the Discovery skills into an ordered, policy-aware
reconnaissance workflow with approval gates before active phases, consolidates
their outputs into a single evidence-backed Discovery result, and performs no
probing itself, invoking no tools directly.
