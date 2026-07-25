# ADR-001 — Database Transport Abstraction

**File:** `skills/shared/database-client/adr/ADR-001-database-transport-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with database servers to assess their
configuration and, where authorized, to support injection testing. Database
access spans many engines, involves credentials and often sensitive data, and
carries the risk of introducing injection vulnerabilities into the platform
itself if queries are built by concatenation.

If each skill opened database connections and built queries directly, the
platform would suffer

- Duplicated connection and result-handling logic
- Inconsistent transport encryption
- Risk of credential leakage and sensitive-data exposure
- Risk of the platform introducing injection through concatenation
- Risk of unauthorized data or schema modification

The platform requires a single, canonical, implementation-independent database
transport that enforces parameterization, encryption, and authorization.

---

# Decision

The platform SHALL provide a dedicated Database Client shared skill that
centralizes database access behind a stable interface.

The Database Client shared skill SHALL

- Establish connections through the [TCP Client](../../tcp-client/README.md)
- Encrypt transport through the [TLS Client](../../tls-client/README.md) where
  supported, refusing cleartext where required
- Authenticate through the [Authentication](../../authentication/README.md)
  package
- Execute statements using bound parameters, never interpolating values into
  statement text
- Manage explicit transactions and gate data and schema modification as
  intrusive
- Bound result sets and produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform database access exclusively through the
[Database Client Interface](../interface.md). The Database Client SHALL NOT
detect injection or other vulnerabilities; that interpretation belongs to domain
skills, which SHALL supply payloads as parameters to remain safe.

---

# Alternatives Considered

## Per-Skill Database Access

Each skill could open connections and build queries directly.

Rejected because it duplicates logic and risks credential leakage and
platform-introduced injection through concatenation.

## Allowing String-Concatenated Queries

The client could accept fully-formed query strings with embedded values.

Rejected because it would allow the platform itself to introduce injection.
Parameterization is a mandatory safety boundary; injection testing is performed
by supplying payloads as parameters and comparing behavior.

## Detecting Injection In The Transport Layer

The Database Client could classify injection.

Rejected because finding generation belongs to domain skills. The Database Client
provides safe parameterized execution and reports results as data.

---

# Consequences

## Positive

- Uniform database access reusing TCP and TLS handling
- Parameterization prevents platform-introduced injection
- Enforced encryption and protected credentials
- Data and schema modification gated as intrusive
- Consistent evidence and bounded results

## Negative

- Consumers MUST perform database access through the interface
- An additional shared dependency is introduced
- Injection testing must be expressed through parameters and behavior comparison

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform database access through the Database Client Interface
- Supply values as bound parameters, never interpolated
- Require encryption for sensitive engines
- Reference credentials rather than inlining them
- Perform writes and schema changes only when authorized

---

# Future Compatibility

Future versions MAY add prepared-statement handles, streaming cursors, and
connection pooling. These extensions SHALL preserve the existing interface and
SHALL maintain backward compatibility.

---

# Related Documents

- [Database Client README](../README.md)
- [Database Client Interface](../interface.md)
- [Database Client Execution Model](../execution.md)
- [Database Client Error Model](../error-model.md)
- [TCP Client](../../tcp-client/README.md)
- [TLS Client](../../tls-client/README.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
