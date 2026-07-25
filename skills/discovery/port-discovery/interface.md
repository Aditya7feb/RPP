# Port Discovery Interface

**File:** `skills/discovery/port-discovery/interface.md`

**Version:** 1.0.0

---

# Purpose

The Port Discovery Interface defines the canonical contract through which the
platform invokes port discovery and receives canonical Assets, Observations, and
Findings.

The interface standardizes the probe request, the produced domain objects, and
result propagation while remaining independent of any transport implementation.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Implementation Independent
- Versioned
- Observable
- Backward Compatible
- Policy-Gated

---

# Relationship

```
Recon Agent

↓

Port Discovery Interface

↓

Port Discovery Skill

↓

Policy Engine + TCP/UDP Client + Evidence
```

The interface SHALL NOT expose or depend on transport implementation internals.

---

# Interface Overview

```
Metadata

↓

Probe Request

↓

Policy References

↓

Execution Context

↓

Discovery Result

↓

Produced Objects

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Probe Request

Every invocation SHALL define

```yaml
target:

ports:

protocols:

timing:
```

`target` SHALL be an in-scope host or address.

`ports` SHALL declare the port set or ranges.

`protocols` SHALL declare `tcp`, `udp`, or both.

`timing` MAY declare a pacing profile bounded by the policy rate ceiling.

---

# Policy References

Every invocation SHALL reference

```yaml
scope_id:

roe_id:
```

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
with these references before each probe.

---

# Execution Context

The skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Discovery Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

assets:

relationships:

observations:

findings:

metrics:

error:
```

`outcome` SHALL be one of

```
completed

partial

denied

timed_out
```

`assets` SHALL reference produced `port` and `service`
[Assets](../../../schemas/asset.md).

`relationships` SHALL reference produced
[Asset Relationships](../../../schemas/asset-relationship.md).

`observations` and `findings` SHALL reference produced
[Observations](../../../schemas/observation.md) and
[Findings](../../../schemas/finding.md).

`denied` SHALL indicate the Policy Engine denied the probe.

---

# Produced Objects

Produced objects SHALL conform to their canonical schemas and SHALL be
referenced, not inlined.

Every produced Asset and Finding SHALL carry provenance to its Evidence.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Port Discovery error model](error-model.md).

A Policy Engine denial SHALL produce a `denied` outcome, not an error retry.

---

# Compatibility

The interface SHALL remain stable across transport implementations and consumers.

Consumers SHALL require no modification when the transport implementation changes.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Probe Request with an in-scope target and bounded ports
- Policy References
- Execution Context
- Discovery Result
- Error Handling

---

# Quality Requirements

The Port Discovery Interface SHALL

✓ Remain implementation independent

✓ Produce canonical domain objects

✓ Enforce policy gating

✓ Support structured errors

✓ Preserve evidence provenance

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Adaptive timing descriptors
- Service-version hints for Fingerprinting
- IPv6 sweep requests

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Port Discovery Interface provides a stable,
implementation-independent contract through which the platform obtains canonical,
evidence-backed service Assets and exposure Findings, gated by the Policy Engine,
across the Robust PenTest Platform.
