# RPP Copilot Instructions

**File:** `.github/copilot-instructions.md`

**Version:** 1.0.0

---

# Repository Purpose

This repository is the documentation-first, implementation-independent knowledge
base for the **Robust PenTest Platform (RPP)**.

It defines the canonical architecture — schemas, shared infrastructure, domain
skills, workflows, and the master agent — that allows multiple execution
backends (Native, Kali MCP, Docker, Cloud APIs, Browser Automation) to be used
interchangeably.

This repository intentionally contains **no implementation code**. It defines
*what* the platform does and *how components relate*, never *how a specific tool
performs the work*.

Every contributor, human or AI, MUST read `MASTER_PLAN.md`,
`repository-index.yaml`, `.github/repository-manifest.yaml`, and
`.github/agent-playbook.md` before generating or modifying content.

---

# Documentation Standards

Every document MUST

- be authored in Markdown
- be production quality with no placeholders and no TODOs
- use RFC 2119 terminology
- cross-reference related schemas, packages, and ADRs
- define extension points
- include realistic examples
- be internally consistent and free of contradictions
- expose only canonical interfaces, never tool or library implementations

Documents SHALL answer, where relevant: Why, What, When, How, Inputs, Outputs,
Dependencies, Errors, Extension points, and Examples.

---

# Directory Structure

```
RPP/
  MASTER_PLAN.md              Development plan and phases
  repository-index.yaml       Machine-readable inventory (update every change)
  .github/                    Governance: manifest, playbook, these instructions
  schemas/                    Canonical, implementation-independent data schemas
  skills/
    core/                     Cross-cutting models (config, execution, errors...)
    shared/                   Reusable shared infrastructure packages
  agents/                     Master agent and sub-agent responsibilities
  workflows/                  Reusable, domain-specific workflow definitions
  tools/                      Tool adapter references (implementation boundary)
  templates/                  Reusable document templates
  examples/  prompts/  reports/  knowledge/
```

New skills live under `skills/shared/` (reusable) or the appropriate domain tier
described in `MASTER_PLAN.md`. New schemas live under `schemas/`.

---

# RFC 2119 Terminology Rules

Use `MUST`, `SHALL`, `SHOULD`, `MAY`, and their negations with their precise RFC
2119 meaning.

- `MUST` / `SHALL` — an absolute requirement
- `SHOULD` — a strong recommendation with justifiable exceptions
- `MAY` — genuinely optional

Never use ambiguous words as normative terms: avoid `maybe`, `probably`,
`usually`, `sometimes`, `kind of`. Normative statements SHALL be deterministic.

---

# Markdown Style Guide

- One top-level `# Title` per file, followed by `**File:**` and `**Version:**`
  metadata lines and a `---` rule.
- Use `#` section headings separated by `---` horizontal rules, matching the
  established shared-package documents.
- Use fenced code blocks for architecture diagrams, YAML field snippets, and
  example objects. YAML snippets describe **structure**, not executable code.
- Use tables for capability summaries, outcome mappings, and precedence.
- Wrap prose at a readable width and keep sentences direct and declarative.
- Refer to other documents with relative Markdown links, never bare paths.

---

# Naming Conventions

- Directories and files: lowercase with hyphen separators
  (`rate-limiter`, `error-model.md`).
- ADR files: `adr/ADR-001-<slug>.md`, `<slug>` in lowercase hyphen form.
- Schema files: singular, canonical concept name (`retry-policy.md`,
  `cache-entry.md`).
- Identifiers in examples: stable, prefixed, hyphenated
  (`ratelimitpolicy-default-http`, `evidence-http-4001`).
- Canonical object type names are stable and reused verbatim across documents.

---

# Schema Conventions

Every schema document MUST define, in this order where applicable:

- Purpose
- Design Principles
- Identity and Classification fields
- Field Definitions (grouped by concern)
- Required Fields
- Validation Rules
- Relationships
- Example Object
- Extension Points
- Versioning Notes

Schemas represent configuration, data, or intent only. They SHALL NOT contain
runtime state (belongs to execution-state), security interpretation, findings,
or secrets. `schema_version` SHALL follow semantic versioning; unknown optional
fields SHALL be ignored by consumers for forward compatibility.

---

# Cross-Reference Conventions

- Link to related schemas, shared packages, ADRs, and examples using relative
  paths, verifying depth precisely.
- From `skills/shared/<pkg>/FILE.md`: schemas are `../../../schemas/`, core is
  `../../core/`, sibling package is `../<pkg>/`.
- From `skills/shared/<pkg>/adr/FILE.md`: schemas are `../../../../schemas/`,
  core is `../../../core/`, sibling package is `../../<pkg>/`.
- Never duplicate documentation; reference the canonical source instead.
- All relative links MUST resolve. A repository with broken links is
  non-compliant.

---

# Package Layout

Every package (shared or domain) MUST contain

```
README.md
capabilities.md
interface.md
configuration.md
execution.md
error-model.md
examples.md
adr/ADR-001-<slug>.md
```

- `README.md` — purpose, goals, non-goals, architecture, responsibilities,
  lifecycle, dependencies, consumers, security, best practices, anti-patterns,
  related documents, schemas, ADRs, future extensions, success criteria.
- `capabilities.md` — enumerated capabilities with a summary table.
- `interface.md` — the stable, implementation-independent contract.
- `configuration.md` — declarative configuration and precedence.
- `execution.md` — the deterministic execution model, stage by stage.
- `error-model.md` — canonical error categories and outcome mapping.
- `examples.md` — realistic, implementation-free examples.
- `adr/ADR-001-<slug>.md` — the primary architectural decision.

---

# Quality Checklist

Before marking any document or package complete, verify:

- ✓ Production quality; no placeholders or TODOs
- ✓ Markdown only; no implementation code
- ✓ RFC 2119 terminology used correctly
- ✓ All cross-references resolve
- ✓ Schemas reused rather than duplicated
- ✓ Examples included and realistic
- ✓ Extension points documented
- ✓ Layering preserved; no upward or cyclic dependencies
- ✓ Terminology consistent with existing documents
- ✓ `repository-index.yaml` updated (status, schemas, dependencies, metrics)

---

# Rules for Creating New Skills

Before creating a skill, confirm:

- It satisfies a real repository need, not merely a plausible one.
- The capability is not already provided by an existing skill or shared package.
- It belongs to the correct layer (Discovery, Authentication, Web Security, API,
  Cloud, Reporting, or Agents).
- It consumes shared infrastructure and canonical schemas rather than tools.
- It introduces no circular dependencies.

Domain skills MUST use shared infrastructure, consume canonical schemas, produce
findings and evidence references, and remain tool independent. Domain skills
MUST NOT invoke tools, call `curl`/`OpenSSL`/`httpx`/`requests`, execute CLIs, or
parse CLI output.

---

# Rules for Creating Shared Infrastructure

Create shared infrastructure when a capability is needed by multiple skills.
Shared packages MUST

- expose stable, implementation-independent interfaces
- hide implementations behind adapters
- consume canonical schemas
- generate evidence and integrate with observability
- remain free of vulnerability detection, findings, risk decisions, and
  exploitation logic

If only one skill needs the capability, keep it inside that skill until a second
consumer emerges.

---

# Rules for Schemas

- Search `schemas/` before creating a new schema. Reuse where an existing schema
  represents the concept.
- Create a schema only when the concept has an independent lifecycle, is
  required by multiple packages, and represents a canonical object.
- Never create schemas for implementation details.
- Split oversized schemas; merge duplicates. Prefer references over embedding.

---

# Anti-Patterns

The following are prohibited:

- Placing detection or finding logic inside shared infrastructure.
- Exposing tools, CLIs, libraries, or framework APIs through interfaces.
- Duplicating schemas, capabilities, terminology, or documentation.
- Introducing upward or cyclic dependencies.
- Hardcoding values that belong in a referenced policy or schema.
- Emitting or persisting secrets in logs, evidence, or reports.
- Leaving broken cross-references or an out-of-date `repository-index.yaml`.
- Preserving weak abstractions solely because they already exist.

---

# Commit Message Conventions

Use Conventional Commits with an RPP scope:

```
<type>(<scope>): <imperative summary>
```

- `type` — one of `feat`, `fix`, `docs`, `refactor`, `schema`, `adr`, `chore`.
- `scope` — the affected package or area, such as `rate-limiter`, `schemas`,
  `agents`, or `index`.
- Summary — imperative mood, lowercase, no trailing period.

Examples

```
feat(rate-limiter): add rate limiter shared package and policy schema
schema(cache-entry): add canonical cache entry schema
fix(http-client): correct evidence schema link depth in ADR
docs(index): update package status and metrics
```

Each significant architectural change SHALL be accompanied by an ADR and an
updated `repository-index.yaml`.

---

# Success Criteria

The repository is compliant when it is self-consistent, implementation
independent, tool independent, extensible, documentation first, and suitable for
both autonomous AI agents and human contributors, with an accurate
`repository-index.yaml` and no broken references.