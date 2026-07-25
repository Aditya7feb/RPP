# DNS Client Capability Model

**File:** `skills/shared/dns-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical capabilities provided by the DNS Client Shared Skill.

Capabilities describe reusable DNS operations that may be composed by domain skills, workflows, and agents throughout the Robust PenTest Platform (RPP).

Capabilities define **what** the DNS Client provides rather than **how** DNS operations are implemented.

---

# Design Principles

DNS capabilities SHALL be

- Reusable
- Deterministic
- Observable
- Secure
- Composable
- Implementation Independent

---

# Capability Categories

```
Resolver Management

↓

DNS Resolution

↓

Reverse Resolution

↓

DNS Security

↓

Caching

↓

Normalization

↓

Evidence

↓

Observability
```

---

# Capability Registry

---

# Resolver Management

## dns.resolver.select

Select the appropriate DNS resolver.

Responsibilities

- Apply resolver policy
- Validate resolver availability
- Select transport
- Return resolver reference

Outputs

- Resolver Reference

---

## dns.resolver.validate

Validate resolver health.

Checks MAY include

- Reachability
- Response time
- Supported transports
- DNSSEC support

---

## dns.resolver.health

Collect resolver health metrics.

Outputs

- Availability
- Latency
- Failure statistics

---

# DNS Resolution

## dns.resolve

Resolve DNS records.

Supported record types

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

Outputs

- Normalized DNS Response

---

## dns.resolve.batch

Resolve multiple DNS queries.

Responsibilities

- Parallel execution
- Result aggregation
- Ordering preservation

---

## dns.resolve.chain

Resolve complete DNS chains.

Examples

```
A

↓

CNAME

↓

Final Address
```

---

# Reverse Resolution

## dns.reverse.lookup

Perform reverse DNS lookup.

Supports

- IPv4
- IPv6

Outputs

- PTR Records

---

# Wildcard Detection

## dns.wildcard.detect

Determine whether wildcard DNS is present.

Responsibilities

- Generate comparison queries
- Analyze responses
- Calculate confidence

Outputs

- Wildcard Status
- Confidence Score

---

# DNS Security

## dns.dnssec.validate

Validate DNSSEC information.

Outputs MAY include

- Validation Status
- Trust Chain
- Signature Information

---

## dns.caa.lookup

Retrieve CAA records.

Outputs

- Authorized Certificate Authorities

---

# Response Normalization

## dns.normalize

Convert implementation-specific responses into canonical DNS Response objects.

Responsibilities

- Normalize records
- Normalize TTL
- Normalize metadata
- Preserve response integrity

Consumers SHALL only receive normalized responses.

---

# Caching

## dns.cache.lookup

Retrieve cached DNS responses.

---

## dns.cache.store

Store DNS responses.

TTL SHALL be respected.

---

## dns.cache.invalidate

Invalidate cached entries.

---

# Evidence

## dns.evidence.capture

Capture DNS evidence.

Evidence MAY include

- Query
- Resolver
- Response
- TTL
- Response Time
- DNSSEC Status

Outputs

- Evidence Reference

---

# Observability

## dns.events.publish

Publish DNS lifecycle events.

Examples

- QueryStarted
- QueryCompleted
- QueryFailed
- CacheHit
- CacheMiss
- DNSSECValidated

---

## dns.metrics.collect

Collect DNS metrics.

Examples

- Query Duration
- Cache Hit Rate
- Resolver Latency
- DNSSEC Validation Time

---

# Capability Composition

Example

```
Subdomain Enumeration Skill

↓

DNS Client

├── dns.resolve.batch
├── dns.normalize
├── dns.cache.store
└── dns.evidence.capture
```

Capabilities SHOULD compose rather than duplicate functionality.

---

# Dependencies

The DNS Client Shared Skill depends on

- Configuration Model
- Execution Model
- Logging
- Evidence
- Error Handling

---

# Constraints

The DNS Client SHALL NOT

- Execute reconnaissance workflows
- Detect vulnerabilities
- Perform brute-force enumeration
- Expose resolver-specific APIs
- Return raw tool output

---

# Versioning

Capability identifiers SHALL remain stable across minor releases.

Breaking capability changes SHALL require a major version increment.

---

# Validation Rules

A compliant implementation SHALL

- Publish supported capabilities
- Produce normalized DNS responses
- Respect resolver policies
- Preserve evidence
- Support observability

---

# Quality Requirements

The DNS Capability Model SHALL

✓ Support all standard DNS record types

✓ Support multiple resolver implementations

✓ Support secure transports

✓ Produce normalized responses

✓ Capture evidence

✓ Support observability

✓ Remain implementation independent

---

# Future Extensions

Future versions MAY support

- DNS-over-HTTPS
- DNS-over-TLS
- DNS-over-QUIC
- ECS (EDNS Client Subnet)
- Resolver federation
- Geo-aware resolution

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant DNS Capability Model provides a standardized, reusable set of DNS operations for the Robust PenTest Platform.

It enables consistent DNS resolution, normalization, security validation, caching, evidence generation, and observability while remaining independent of DNS libraries, utilities, and resolver implementations.