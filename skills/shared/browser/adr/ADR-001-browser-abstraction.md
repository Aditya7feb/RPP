# ADR-001 — Browser Abstraction

**File:** `skills/shared/browser/adr/ADR-001-browser-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must interact with rendered web applications that
depend on client-side JavaScript, dynamic DOM construction, and browser-specific
behavior. Browser automation can be performed through many engines and
frameworks and across different execution environments.

If each skill drove a browser directly, the platform would suffer

- Divergent automation behavior across engines
- Inconsistent evidence such as screenshots and DOM captures
- Duplicated session and lifecycle management
- Tight coupling to specific automation frameworks

The platform requires a single, canonical, implementation-independent browser
automation capability.

---

# Decision

The platform SHALL provide a dedicated Browser shared skill that centralizes
browser automation behind a stable interface.

The Browser shared skill SHALL

- Abstract browser engines and automation frameworks behind adapters
- Manage browser lifecycle and sessions
- Execute client-side interactions deterministically where possible
- Integrate with the [Authentication](../../authentication/README.md) shared
  package for authenticated contexts
- Capture browser evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)
- Remain free of vulnerability detection and finding generation

Consumers SHALL perform browser automation exclusively through the
[Browser Interface](../interface.md). Adapter implementations SHALL remain hidden
from consumers.

---

# Alternatives Considered

## Per-Skill Browser Automation

Each skill could drive a browser directly.

Rejected because it duplicates lifecycle logic and produces inconsistent
evidence.

## Using The HTTP Client For Rendered Applications

The HTTP Client could serve rendered applications.

Rejected because the HTTP Client does not execute client-side JavaScript or
render the DOM. Browser automation is a distinct capability.

---

# Consequences

## Positive

- Uniform browser automation across skills
- Consistent browser evidence
- Centralized session and lifecycle management
- Implementation independence through adapters

## Negative

- Consumers MUST route automation through the interface
- An additional shared dependency is introduced

The negative consequences are outweighed by consistency and reuse.

---

# Compliance

Consumers SHALL perform browser automation through the Browser Interface and
SHALL NOT drive browser engines directly or parse framework output.

---

# Future Compatibility

Future versions MAY add headful debugging capture, network interception
descriptors, and additional engines. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Browser README](../README.md)
- [Browser Interface](../interface.md)
- [Browser Execution Model](../execution.md)
- [Browser Error Model](../error-model.md)
- [Authentication](../../authentication/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
