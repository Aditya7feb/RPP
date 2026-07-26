# ADR-001 — Command Injection Skill

**File:** `skills/web-security/command-injection/adr/ADR-001-command-injection-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Web Security phase requires a domain skill that evaluates whether an in-scope
application passes user-controllable input into operating-system command execution.
Command injection (CWE-78) allows an attacker to execute arbitrary commands on the
host, typically leading to full system compromise.

Confirming command injection safely is delicate: naive payloads could run harmful
commands. The skill therefore confirms injectability using bounded, non-destructive
signals — a bounded induced execution delay or an out-of-band interaction to a
controlled collector — and SHALL NOT run harmful commands.

The skill follows the Web Security-tier pattern: consume the `web-application`,
`endpoint`, and `api` [Assets](../../../../schemas/asset.md) produced by Discovery,
consult the [Policy Engine](../../../shared/policy-engine/README.md) before every
target-facing action, drive the [HTTP Client](../../../shared/http-client/README.md),
and produce [Findings](../../../../schemas/finding.md) with
[Risk](../../../../schemas/risk.md) along the
Observation → Evidence → Analysis → Finding → Risk pipeline, classifying weaknesses
with canonical identifiers such as CWE-78. It reuses the canonical
[HTTP Timing](../../../../schemas/http-timing.md) representation.

---

# Decision

The platform SHALL provide a Command Injection Skill in the Web Security tier that

- Injects bounded probes and observes bounded time-based and out-of-band signals
  through the HTTP Client
- Confirms injectability without running harmful commands or altering the system
- Consults the Policy Engine before every target-facing action and proceeds only on
  `allow`, deferring on `requires_approval`, within the attached rate ceiling, and
  commonly requiring approval given the high impact
- Records [Observations](../../../../schemas/observation.md) and promotes them to
  [Evidence](../../../../schemas/evidence.md) with the confirming signal recorded
- Emits Findings with Risk for command injection weaknesses, never without Evidence,
  classified with canonical weakness identifiers such as CWE-78

The skill SHALL be tool independent, SHALL NOT perform HTTP input or output
directly, and SHALL NOT run harmful commands, alter the system, or establish
persistence.

---

# Alternatives Considered

## Combining All Injection Classes

Command injection could share a skill with SQL and template injection.

Rejected because command injection has distinct signals, host-level impact, and
safe-probe strategies. Separate skills keep each focused and independently
governable.

## Running Commands To Prove Impact

The skill could run commands to demonstrate impact.

Rejected because running commands is destructive and dangerous. Bounded delay and
out-of-band confirmation prove injectability without harmful execution.

## Requiring Out-Of-Band Confirmation Always

The skill could rely solely on out-of-band confirmation.

Rejected because a controlled collector is not always available or in scope.
Bounded time-based confirmation is the default, with out-of-band confirmation used
where an authorized collector is provided.

---

# Consequences

## Positive

- Produces evidence-backed command injection Findings safely
- Reuses the Web Security-tier skill pattern and canonical timing schema
- Enforces scope, Rules of Engagement, and pacing through the Policy Engine
- Confirms injectability without harmful execution

## Negative

- Introduces dependencies on the Policy Engine and HTTP Client
- Time-based confirmation requires careful bounding and noise reduction

The negative consequences are outweighed by safety and reliability.

---

# Compliance

The skill SHALL

- Consult the Policy Engine before every target-facing action
- Confirm injectability with benign, bounded signals only
- Never run harmful commands or alter the system
- Bound time-based probe delays
- Reference managed probe sets and authorized collectors only
- Back every Finding with Evidence
- Classify weaknesses with canonical identifiers such as CWE-78
- Never act on out-of-scope targets
- Never issue HTTP requests directly

---

# Future Compatibility

Future versions MAY add argument-injection classification, operating-system-aware
signal modeling, and richer out-of-band channels. These extensions SHALL preserve
the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Command Injection README](../README.md)
- [Command Injection Interface](../interface.md)
- [Command Injection Execution Model](../execution.md)
- [Command Injection Error Model](../error-model.md)
- [HTTP Client](../../../shared/http-client/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [HTTP Timing Schema](../../../../schemas/http-timing.md)
