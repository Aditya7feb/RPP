# DNS Client Shared Skill

**File:** `skills/shared/dns-client/README.md`

**Version:** 1.0.0

---

# Purpose

The DNS Client Shared Skill provides a standardized, implementation-independent interface for performing Domain Name System (DNS) operations within the Robust PenTest Platform (RPP).

It enables domain skills to perform reliable DNS resolution, enumeration, validation, and analysis without depending on specific DNS utilities or libraries.

Consumers SHALL delegate all DNS operations to this shared skill.

---

# Goals

The DNS Client Shared Skill SHALL

- Abstract DNS implementations
- Support standard DNS record resolution
- Support configurable resolvers
- Support DNS security features
- Support evidence collection
- Support deterministic execution
- Integrate with platform observability

---

# Non-Goals

The DNS Client Shared Skill SHALL NOT

- Detect vulnerabilities
- Perform subdomain brute-forcing
- Execute reconnaissance strategies
- Interpret DNS findings
- Replace Recon or Fingerprinting skills

Those responsibilities belong to higher-level domain skills.

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

DNS Client Shared Skill

├── Resolver Manager
├── Cache Manager
├── DNSSEC Validator
├── Evidence Manager
├── Event Manager

↓

DNS Adapter

↓

DNS Resolver
```

---

# Responsibilities

The DNS Client Shared Skill is responsible for

- DNS resolution
- Resolver management
- Record normalization
- DNSSEC validation
- Wildcard detection support
- Reverse lookups
- Evidence generation
- Metrics collection

---

# Supported DNS Records

The shared skill SHALL support retrieval of

- A
- AAAA
- CNAME
- MX
- TXT
- NS
- SOA
- PTR
- SRV
- CAA

Future record types MAY be introduced.

---

# DNS Resolution Lifecycle

```
Receive Request

↓

Resolve Configuration

↓

Select Resolver

↓

Execute DNS Query

↓

Normalize Response

↓

Capture Evidence

↓

Publish Events

↓

Return Result
```

---

# Resolver Management

Resolvers MAY include

- System Resolver
- Internal Resolver
- Public Resolver
- DNS-over-HTTPS (DoH)
- DNS-over-TLS (DoT)

Resolver selection SHALL be policy driven.

---

# Caching

The shared skill MAY support

- Positive cache
- Negative cache
- TTL-aware cache
- Cache invalidation

Cache behavior SHALL remain configurable.

---

# DNSSEC

Where supported, the shared skill MAY

- Validate DNSSEC signatures
- Report validation status
- Capture trust chain information

Validation SHALL not alter returned DNS data.

---

# Reverse Resolution

The shared skill SHALL support

- IPv4 PTR lookups
- IPv6 PTR lookups

Returned values SHALL be normalized.

---

# Wildcard Detection Support

The shared skill MAY provide utilities to

- Detect wildcard DNS behavior
- Identify synthesized responses
- Report wildcard confidence

Interpretation remains the responsibility of higher-level skills.

---

# Evidence

The shared skill SHOULD capture

- Query
- Resolver
- Record Type
- Response
- TTL
- DNSSEC Status
- Response Time

Evidence SHALL conform to the canonical Evidence schema.

---

# Events

The shared skill SHOULD publish

- QueryStarted
- QueryCompleted
- QueryFailed
- CacheHit
- CacheMiss
- DNSSECValidated

Events SHALL integrate with Execution State.

---

# Dependencies

The DNS Client Shared Skill depends on

- Configuration Model
- Execution Model
- Error Handling
- Logging
- Evidence

---

# Outputs

Typical outputs MAY include

- DNS Records
- Resolver Metadata
- TTL Information
- DNSSEC Status
- Response Metadata

Outputs SHALL remain implementation independent.

---

# Security Principles

The DNS Client Shared Skill SHALL

- Respect approved resolver policies
- Support secure DNS transports
- Preserve auditability
- Prevent resolver leakage across assessments
- Normalize all responses

---

# Best Practices

Consumers SHOULD

- Use centralized DNS resolution
- Reuse configured resolvers
- Capture DNS evidence
- Respect TTL where appropriate
- Validate DNSSEC when available

---

# Anti-Patterns

Consumers SHOULD NOT

- Execute DNS utilities directly
- Hardcode resolver addresses
- Parse raw DNS tool output
- Duplicate caching logic
- Implement resolver-specific behavior

---

# Future Extensions

Future versions MAY support

- EDNS
- ECS (EDNS Client Subnet)
- DNS-over-QUIC
- Resolver health scoring
- Resolver failover
- Distributed DNS querying

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant DNS Client Shared Skill provides a secure, reusable, and implementation-independent DNS abstraction for the Robust PenTest Platform.

It enables consistent DNS resolution, normalization, evidence generation, and observability while remaining independent of DNS utilities, libraries, and resolver implementations.