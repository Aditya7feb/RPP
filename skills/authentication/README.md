# Authentication Capability Tier

**File:** `skills/authentication/README.md`

**Version:** 1.0.0

---

# Purpose

The Authentication tier provides reusable, implementation-independent capabilities
that analyze identity, credential, session, and token security within the Robust
PenTest Platform (RPP). These capabilities produce Observations, Findings, and
Evidence references.

This tier comprises the following capabilities.

- [API Keys](api-keys/README.md)
- [Sessions](sessions/README.md)
- [JWT](jwt/README.md)
- [OAuth2](oauth2/README.md)
- [OIDC](oidc/README.md)
- [SAML](saml/README.md)
- [mTLS](mtls/README.md)
- [CSRF](csrf/README.md)

---

# Ownership Boundary

Authentication capabilities analyze identity and session posture and produce
Findings and Evidence references. Intrusive authentication-bypass validation is
owned by the Active Testing tier and requires human approval; it is not performed
by this tier unbidden.

---

# Role in the Canonical Pipeline

Authentication capabilities contribute Observations, Evidence, and Findings to the
pipeline **Observation → Evidence → Finding → Risk → Recommendation**.

---

# Canonical Schemas

Authentication capabilities consume and produce
[observation](../../schemas/observation.md),
[finding](../../schemas/finding.md),
[evidence](../../schemas/evidence.md),
[http-session](../../schemas/http-session.md), and
[http-cookie](../../schemas/http-cookie.md), and reference
[scope](../../schemas/scope.md) and
[rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- Orchestrated by the [Authentication Agent](../../agents/authentication/README.md).
- Shared infrastructure under [skills/shared](../shared/README.md).
