# Web Security Capability Tier

**File:** `skills/web-security/README.md`

**Version:** 1.0.0

---

# Purpose

The Web Security tier provides reusable, implementation-independent capabilities
that analyze web-application security within the Robust PenTest Platform (RPP).
These capabilities produce Observations, Findings, and Evidence references.

This tier comprises the following capabilities.

- [Security Headers (CSP)](csp/README.md)
- [CORS](cors/README.md)
- [Clickjacking](clickjacking/README.md)
- [Open Redirect](open-redirect/README.md)
- [Cache Poisoning](cache-poisoning/README.md)
- [XSS](xss/README.md)
- [SQL Injection](sqli/README.md)
- [Command Injection](command-injection/README.md)
- [SSTI](ssti/README.md)
- [SSRF](ssrf/README.md)
- [XXE](xxe/README.md)
- [IDOR](idor/README.md)
- [Path Traversal](path-traversal/README.md)
- [File Upload](file-upload/README.md)
- [Deserialization](deserialization/README.md)

---

# Ownership Boundary

Web Security capabilities identify weaknesses and produce Findings and Evidence
references. Payload-driven validation that changes target state is owned by the
Active Testing tier and requires human approval; it is not performed by this tier
unbidden.

---

# Role in the Canonical Pipeline

Web Security capabilities contribute Observations, Evidence, and Findings to the
pipeline **Observation → Evidence → Finding → Risk → Recommendation**.

---

# Canonical Schemas

Web Security capabilities consume and produce
[observation](../../schemas/observation.md),
[finding](../../schemas/finding.md),
[evidence](../../schemas/evidence.md),
[http-transaction](../../schemas/http-transaction.md),
[http-request](../../schemas/http-request.md), and
[http-response](../../schemas/http-response.md), and reference
[scope](../../schemas/scope.md) and
[rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- Orchestrated by the [Web Security Agent](../../agents/web-security/README.md).
- Shared infrastructure under [skills/shared](../shared/README.md).
