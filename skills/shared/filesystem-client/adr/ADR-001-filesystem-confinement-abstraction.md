# ADR-001 — Filesystem Confinement Abstraction

**File:** `skills/shared/filesystem-client/adr/ADR-001-filesystem-confinement-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform reads and writes files for evidence staging,
artifact storage, and authorized configuration review across local, remote, and
container backends. Uncontrolled filesystem access carries the risk of path
traversal, symlink escape, sensitive-data exposure, and unauthorized
modification.

If each skill accessed paths directly, the platform would suffer

- Inconsistent or absent path confinement
- Risk of traversal and symlink escape
- Divergent size and depth bounds
- Risk of unauthorized writes and deletes
- Divergent evidence and governance

The platform requires a single, canonical, implementation-independent filesystem
abstraction that confines access and gates modification.

---

# Decision

The platform SHALL provide a dedicated Filesystem Client shared skill that
centralizes file access behind a stable interface.

The Filesystem Client shared skill SHALL

- Resolve operations against configured roots
- Confine every path within its root and reject traversal
- Reject symbolic links resolving outside a root
- Read, write, list, stat, and delete with bounded sizes and depth
- Authenticate to remote backends through the
  [Authentication](../../authentication/README.md) package
- Gate write and delete as intrusive
- Produce evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)

Consumers SHALL perform filesystem access exclusively through the
[Filesystem Client Interface](../interface.md). The Filesystem Client SHALL NOT
detect insecure permissions or other vulnerabilities; that interpretation belongs
to domain skills.

---

# Alternatives Considered

## Per-Skill Filesystem Access

Each skill could access paths directly.

Rejected because it risks inconsistent confinement, traversal, and unauthorized
modification.

## Trusting Caller Paths

The client could assume caller paths are safe.

Rejected because paths often derive from target data. Confinement and
canonicalization are mandatory safety boundaries.

## Detecting Insecure Permissions In The Client

The client could classify insecure permissions.

Rejected because finding generation belongs to domain skills. The client reports
metadata as data.

---

# Consequences

## Positive

- Uniform, confined file access across backends
- Traversal and symlink escape prevented at the boundary
- Modification gated as intrusive
- Consistent evidence and bounds

## Negative

- Consumers MUST perform file access through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by safety and consistency.

---

# Compliance

Consumers SHALL

- Perform file access through the Filesystem Client Interface
- Operate within the narrowest sufficient root
- Never assume caller paths are safe
- Perform writes and deletes only when authorized
- Interpret metadata at the domain layer

---

# Future Compatibility

Future versions MAY add streaming descriptors, change-watch subscriptions, and
extended attribute inspection. These extensions SHALL preserve the existing
interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Filesystem Client README](../README.md)
- [Filesystem Client Interface](../interface.md)
- [Filesystem Client Execution Model](../execution.md)
- [Filesystem Client Error Model](../error-model.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
