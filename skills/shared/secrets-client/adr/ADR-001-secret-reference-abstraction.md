# ADR-001 — Secret Reference Abstraction

**File:** `skills/shared/secrets-client/adr/ADR-001-secret-reference-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform requires secrets — API tokens, database credentials,
proxy credentials, and keys — to interact with targets. Secrets are the most
sensitive material the platform handles, and a single exposure can compromise an
engagement or a customer environment.

If each skill fetched secret values directly, the platform would suffer

- Widespread copies of secret values across the codebase
- Risk of secrets appearing in logs, evidence, and results
- Inconsistent lease and rotation handling
- No central enforcement of non-exposure

The platform requires a single, canonical, implementation-independent secrets
abstraction that never exposes values to general consumers.

---

# Decision

The platform SHALL provide a dedicated Secrets Client shared skill that
centralizes secret resolution and brokered application behind a stable interface.

The Secrets Client shared skill SHALL

- Resolve secrets by opaque reference, returning handles rather than values
- Broker application of secrets at the point of use through the
  [Authentication](../../authentication/README.md) package without exposing
  values
- Track leases, versions, and rotation
- Bound handle lifetime and clear values on expiry
- Produce non-sensitive evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

General consumers SHALL obtain and apply secrets exclusively through the
[Secrets Client Interface](../interface.md) and the Authentication broker, never
by value. The Secrets Client SHALL NEVER return a secret value through the
interface, in evidence, in logs, or in errors.

---

# Alternatives Considered

## Returning Secret Values To Consumers

The client could return raw values.

Rejected because every returned value multiplies exposure risk and undermines
central protection. Non-exposure is an absolute requirement.

## Per-Skill Secret Fetching

Each skill could fetch from stores directly.

Rejected because it scatters secrets, complicates rotation, and risks leakage in
logs and evidence.

## Caching Secret Values

Secret values could be cached for performance.

Rejected because cached values can be persisted or logged. Only opaque handles
with bounded lifetimes are cached, and values are cleared on expiry.

---

# Consequences

## Positive

- Secret values never cross into general consumers, logs, or evidence
- Central lease, rotation, and non-exposure enforcement
- Consistent brokered application at the point of use
- Auditable secret access without exposure

## Negative

- Consumers MUST use handles and brokered application, not values
- An additional shared dependency is introduced
- Brokering adds a point-of-use indirection

The negative consequences are outweighed by the security benefits.

---

# Compliance

Consumers SHALL

- Use handles and brokered application, never values
- Tolerate rotation through handles
- Never log or persist secrets
- Never bypass the broker

The [Logging](../../logging/README.md) and [Evidence](../../evidence/README.md)
shared packages provide defense-in-depth redaction, but the Secrets Client is the
primary guarantee of non-exposure.

---

# Future Compatibility

Future versions MAY add dynamic secret generation, envelope encryption, and
just-in-time brokered credentials. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility and non-exposure.

---

# Related Documents

- [Secrets Client README](../README.md)
- [Secrets Client Interface](../interface.md)
- [Secrets Client Execution Model](../execution.md)
- [Secrets Client Error Model](../error-model.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
