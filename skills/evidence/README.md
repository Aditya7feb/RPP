# Evidence Capability Tier

**File:** `skills/evidence/README.md`

**Version:** 1.0.0

---

# Purpose

The Evidence tier provides reusable, implementation-independent capabilities that **collect**
and **correlate** evidence within the Robust PenTest Platform (RPP).

Evidence capabilities gather durable evidence from targets and prior execution — screenshots,
HTTP archives, network traces, files, certificates, and logs — and correlate observations and
evidence chronologically. They **do not** interpret results, produce Findings, or classify
Risk; and they **do not** implement the durable evidence lifecycle, which is owned by the shared
[Evidence](../shared/evidence/README.md) infrastructure.

This tier comprises the following capabilities.

- [Screenshot Capture](screenshot-capture/README.md)
- [HTTP Archive](http-archive/README.md)
- [Network Trace](network-trace/README.md)
- [Artifact Collection](artifact-collection/README.md)
- [Log Collection](log-collection/README.md)
- [Timeline](timeline/README.md)

---

# Evidence Lifecycle

The Evidence tier participates in the canonical pipeline
`Observation → Evidence → Finding → Risk` as a collector and correlator of evidence.

The durable evidence lifecycle — **packaging, integrity, archival, retention, and promotion** —
is a set of **lifecycle mechanics owned by the shared
[Evidence](../shared/evidence/README.md) infrastructure**, not by any Evidence-tier capability.
Evidence capabilities **invoke** this lifecycle; they do not own its implementation.

## Promotion

**Promotion is the transition from transient execution artifacts and Observations into durable
Evidence managed by the shared `evidence` infrastructure.** Promotion is part of the shared
Evidence lifecycle. Evidence capabilities invoke promotion when they collect evidence, but the
promotion mechanism — durable persistence, integrity, and retention — is implemented by the
shared `evidence` infrastructure, not by the capability.

---

# Ownership Boundaries

The canonical ownership model is as follows.

| Layer | Owns |
|-------|------|
| Active Testing | payload generation, payload execution, Observations, transient execution Artifacts |
| Evidence tier | evidence collection, evidence correlation, evidence preservation, invocation of the shared Evidence lifecycle |
| Shared `evidence` infrastructure | packaging, integrity, archival, retention, promotion |
| Domain Security | consumes Observations and Evidence, confirms vulnerabilities, produces Findings and Risk |
| Reporting | consumes Findings and Evidence |

Evidence capabilities SHALL NOT produce Findings, classify Risk, or interpret evidence.

---

# Capability Responsibilities

| Capability | Responsibility |
|------------|----------------|
| Screenshot Capture | browser screenshots and rendered page captures |
| HTTP Archive | HAR, HTTP request/response archival, HTTP evidence |
| Network Trace | packet and flow captures, transport-level evidence |
| Artifact Collection | files, certificates, and other collected artifacts |
| Log Collection | application, service, and infrastructure logs |
| Timeline | chronological correlation of observations and evidence (correlation only) |

Timeline SHALL NOT perform vulnerability inference, Finding generation, Risk analysis, or
prioritization; it is descriptive, not analytical.

---

# Data Flow

```
Active Testing              Evidence tier                   Domain Security      Reporting
──────────────              ─────────────                   ───────────────      ─────────
Generated → Executed →      collect · correlate · preserve  consume Observations consume
Successful Payloads         invoke shared Evidence          + Evidence           Findings
+ Observations         ───► lifecycle (promotion,      ───► confirm · Findings ─► + Evidence
+ transient Artifacts       integrity, retention)           + Risk
```

Active Testing produces transient artifacts and Observations; the Evidence tier collects and
correlates them and invokes the shared Evidence lifecycle to promote them into durable Evidence;
Domain Security interprets Observations and Evidence into Findings and Risk; Reporting consumes
Findings and Evidence.

---

# Policy Enforcement

Target-facing collection capabilities (Screenshot Capture, HTTP Archive, Network Trace) SHALL
consult the [Policy Engine](../shared/policy-engine/README.md) before every target-facing action
and SHALL remain non-destructive. Collection and correlation of already-captured data are not
target-facing.

---

# Canonical Schemas

- [Evidence](../../schemas/evidence.md)
- [Artifact](../../schemas/artifact.md)
- [Observation](../../schemas/observation.md)
- [Certificate](../../schemas/certificate.md)
- [Certificate Chain](../../schemas/certificate-chain.md)
- [HTTP Transaction](../../schemas/http-transaction.md)
- [Metrics](../../schemas/metrics.md)

The Evidence tier introduces no new canonical schemas.

---

# Related

- [Shared Infrastructure](../shared/README.md)
- [Evidence (shared)](../shared/evidence/README.md)
- [Logging (shared)](../shared/logging/README.md)
- [Policy Engine](../shared/policy-engine/README.md)

---

# Success Criteria

The Evidence tier is compliant when its capabilities collect and correlate evidence under a
policy-gated, non-destructive model, invoke the shared Evidence lifecycle for durable
persistence, introduce no new schemas, and produce no Findings or Risk, leaving interpretation to
Domain Security capabilities and the durable evidence lifecycle to the shared `evidence`
infrastructure.
