# ADR-001 — Server-Side Template Injection Skill

**File:** `skills/web-security/ssti/adr/ADR-001-ssti-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application evaluates user-controllable input as a server-side template expression.
Server-side template injection (CWE-1336) can escalate to remote code execution
depending on the template engine, making it a high-impact weakness.

Confirming template injection safely requires demonstrating expression evaluation
without escalating to code execution. The skill therefore confirms evaluation using
bounded expression markers — such as a bounded arithmetic expression that returns its
computed result — and SHALL NOT escalate to code execution.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-1336.

---

# Decision

The platform SHALL provide a Server-Side Template Injection Skill in the Web Security
tier that

- Injects bounded expression markers and observes evaluation through the HTTP Client
- Analyzes whether markers are evaluated and which engine class is indicated
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the high impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with the evaluated marker recorded
- Emits Findings with Risk for template injection weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-1336

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT escalate to code execution or run system commands.

---

# Alternatives Considered

## Combining Template Injection With Cross-Site Scripting

Server-side and client-side template injection could share a skill.

Rejected because server-side template injection evaluates on the server with
potential code-execution impact, while client-side injection executes in the browser.
The XSS skill owns client-side execution; this skill owns server-side evaluation.

## Escalating To Code Execution To Prove Impact

The skill could execute code to demonstrate impact.

Rejected because code execution is destructive and dangerous. Bounded expression
evaluation confirms injection safely; sandbox-escape exposure is deferred to a
stricter, explicitly approved future capability.

## Combining All Injection Classes

Template, SQL, and command injection could share one skill.

Rejected because each class has distinct evaluation semantics and safe-probe
strategies. Separate skills keep each focused.

---

# Consequences

## Positive

- Produces evidence-backed template injection Findings safely
- Reuses the Web Security-tier skill pattern
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms evaluation without code execution

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Engine-class indication requires careful, bounded analysis

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm evaluation with bounded expression markers only
- Never escalate to code execution
- Reference managed marker sets, never inline code-execution payloads
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-1336
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add engine-specific evaluation modeling and sandbox-escape
exposure assessment under stricter approval. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Server-Side Template Injection README](../README.md)
- [Server-Side Template Injection Interface](../interface.md)
- [Server-Side Template Injection Execution Model](../execution.md)
- [Server-Side Template Injection Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Schema](../../../../schemas/asset.md)
