# ADR-001 — HTTP Transport Abstraction

**File:** `skills/shared/http-client/adr/ADR-001-transport-abstraction.md`

**Version:** 1.0.0

**Status:** Accepted

**Date:** 2026-07-25

---

# Context

The Robust PenTest Platform (RPP) performs the majority of its reconnaissance,
content discovery, fingerprinting, authentication, and exploitation activity
over HTTP and HTTPS.

Historically, security tooling implements HTTP directly inside each module.
A recon component calls `requests`, a fuzzer shells out to `curl`, a browser
skill drives a headless engine, and an exploitation module opens raw sockets.
Each of these implementations reinvents connection management, redirect
handling, cookie persistence, compression, TLS negotiation, proxy routing,
retries, and evidence capture.

This fragmentation produces several recurring problems.

- Inconsistent behavior across skills for the same target
- Divergent evidence formats that cannot be correlated
- Duplicate and conflicting retry, timeout, and proxy logic
- Credentials and secrets handled differently in every module
- No single place to enforce Rules of Engagement or scope restrictions
- Direct coupling between domain logic and a specific HTTP library
- Inability to switch transports (for example from `httpx` to a browser)
  without rewriting domain skills

The platform requires a single, canonical HTTP capability that every domain
skill consumes, and behind which the concrete HTTP engine can change without
affecting consumers.

---

# Decision

The RPP SHALL expose a single shared HTTP Client package located at
`skills/shared/http-client/`.

All HTTP and HTTPS communication performed by domain skills, workflows, and
agents SHALL be routed through the HTTP Client Interface defined in
[interface.md](../interface.md).

The concrete mechanism that places bytes on the wire SHALL be encapsulated
behind a Transport Interface, as defined in [transport.md](../transport.md),
and implemented by interchangeable Transport Adapters.

The following rules SHALL apply.

- Domain skills SHALL depend only on the HTTP Client Interface and canonical
  HTTP schemas.
- Domain skills SHALL NOT import, invoke, or shell out to any concrete HTTP
  implementation.
- The HTTP Client SHALL select and drive a Transport Adapter transparently.
- Transport Adapters SHALL translate the normalized request and response
  models and SHALL NOT leak implementation-specific objects.
- The HTTP Client SHALL delegate authentication, retry, rate limiting, DNS
  resolution, and TLS negotiation to the corresponding shared packages.

---

# Rationale

## Why HTTP is abstracted behind a shared package

A shared HTTP Client provides a single point at which the platform can enforce
consistency and policy.

- **Uniform behavior.** Every skill observes identical redirect, cookie,
  compression, and timeout semantics against a given target.
- **Correlated evidence.** All requests emit evidence conforming to the
  canonical [Evidence schema](../../../../schemas/evidence.md) and the HTTP
  schemas, enabling cross-skill correlation and reporting.
- **Policy enforcement.** Rules of Engagement, scope restrictions, rate limits,
  and audit logging are enforced in one place rather than replicated per skill.
- **Secret protection.** Credentials flow through the shared
  [Authentication](../../authentication/README.md) package and are never
  embedded in domain logic, reducing the risk of leakage.
- **Separation of concerns.** Domain skills reason about *what* to request and
  *what a response means*. The HTTP Client reasons about *how* to transmit and
  receive it. The HTTP Client SHALL NOT detect vulnerabilities, fingerprint
  technologies, or generate findings.

## Why domain skills MUST never call curl, requests, httpx, or browser APIs directly

Direct use of a concrete HTTP implementation couples domain logic to that
implementation and defeats every benefit above.

- Direct calls bypass canonical evidence capture, producing artifacts that
  cannot be correlated or audited.
- Direct calls bypass shared retry, rate limiting, and scope enforcement,
  risking policy and Rules of Engagement violations.
- Direct calls fragment authentication and secret handling.
- Direct calls prevent transport substitution, because domain code becomes
  bound to library-specific request and response objects.

Therefore domain skills SHALL NOT call `curl`, `requests`, `httpx`, `aiohttp`,
`libcurl`, Go `net/http`, Node `fetch`, browser automation APIs, or raw
sockets. They SHALL communicate exclusively through the HTTP Client Interface.

## Why adapters exist

Adapters exist to decouple the stable HTTP capability from the volatile,
environment-specific mechanism used to fulfill it.

- **Interchangeability.** A lightweight adapter (for example `httpx`) and a
  browser-based adapter (for example Playwright) expose the same interface, so
  the platform can render JavaScript-heavy targets or issue lightweight API
  calls without changing consumers.
- **Environment fit.** Different execution environments (local runner, Kali
  MCP, future cloud workers) can supply different adapters while preserving the
  contract.
- **Protocol evolution.** New protocol support such as HTTP/2 and future HTTP/3
  can be introduced through new or upgraded adapters without breaking domain
  skills.
- **Testability.** Adapters can be substituted with deterministic test doubles
  to validate skills in isolation.

---

# Consequences

## Positive

- Domain skills remain small, focused, and transport independent.
- HTTP behavior, evidence, and policy are consistent platform-wide.
- New transports and protocols are adopted without domain rewrites.
- Authentication, retry, rate limiting, DNS, and TLS are handled once.
- Evidence is uniformly captured and correlatable across skills.

## Negative

- A stable interface and normalized models SHALL be maintained, which adds
  design overhead compared to ad hoc HTTP calls.
- Adapter authors SHALL implement translation and error normalization for each
  supported engine.
- Advanced engine-specific features are exposed only through namespaced
  extension points rather than directly.

## Neutral

- The HTTP Client becomes a critical shared dependency and SHALL follow
  semantic versioning to protect consumers.

---

# Alternatives Considered

## Allow each skill to implement HTTP directly

Rejected. This is the status quo the platform is designed to eliminate. It
produces inconsistent behavior, fragmented evidence, duplicated policy logic,
and tight coupling to specific libraries.

## Standardize on a single HTTP library platform-wide

Rejected. A single library cannot satisfy every requirement. Lightweight
libraries cannot render JavaScript; browser engines are unsuitable for
high-volume API calls; some environments require specific runtimes. Binding the
platform to one library also blocks protocol evolution.

## Expose a thin pass-through wrapper over one library

Rejected. A pass-through that leaks library-specific request and response
objects would recreate coupling and prevent transport substitution, defeating
the purpose of the abstraction.

---

# Compliance

A component is compliant with this decision when

- It performs all HTTP and HTTPS communication through the HTTP Client
  Interface.
- It consumes only normalized request and response models and canonical HTTP
  schemas.
- It does not import or invoke any concrete HTTP implementation or browser API
  directly.
- It relies on the shared Authentication, Retry, Rate Limiter, DNS Client, and
  TLS Client packages rather than reimplementing their behavior.

---

# References

- [HTTP Client README](../README.md)
- [HTTP Client Interface](../interface.md)
- [HTTP Transport Architecture](../transport.md)
- [HTTP Client Execution Model](../execution.md)
- [HTTP Client Error Model](../error-model.md)
- [TLS Client](../../tls-client/README.md)
- [DNS Client](../../dns-client/README.md)
- [Authentication](../../authentication/README.md)
- [Browser](../../browser/README.md)
- [Evidence Schema](../../../../schemas/evidence.md)
