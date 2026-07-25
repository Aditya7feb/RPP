# DNS Client Interface

**File:** `skills/shared/dns-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The DNS Client Interface defines the canonical contract through which platform components perform DNS operations.

It provides a stable, implementation-independent interface for DNS resolution, reverse lookups, DNS security validation, caching, resolver selection, and evidence generation.

All consumers SHALL interact with DNS exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Versioned
- Deterministic
- Observable
- Secure
- Resolver Independent
- Backward Compatible

---

# Relationship

```
Master Agent

↓

Workflow

↓

Domain Skill

↓

DNS Client Interface

↓

DNS Client Shared Skill

↓

DNS Adapter

↓

DNS Resolver
```

Consumers SHALL NOT communicate directly with DNS libraries, utilities, or resolvers.

---

# Interface Overview

The interface consists of

```
Metadata

↓

DNS Request

↓

Execution Options

↓

Resolver Context

↓

DNS Response

↓

Evidence

↓

Metrics

↓

Errors
```

---

# Metadata

Every DNS invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables traceability and auditing.

---

# DNS Request

Every request SHALL define

```yaml
operation:

resolver:

queries:

options:
```

---

# Supported Operations

The DNS Client SHALL support

```
dns.resolve

dns.resolve.batch

dns.resolve.chain

dns.reverse.lookup

dns.wildcard.detect

dns.dnssec.validate

dns.caa.lookup

dns.cache.lookup

dns.cache.store

dns.cache.invalidate
```

Additional operations MAY be introduced without breaking existing consumers.

---

# Query Definition

Each DNS query SHALL specify

```yaml
name:

record_type:

class:
```

Supported classes SHOULD include

- IN
- CH

Additional classes MAY be supported.

---

# Resolver Context

DNS operations SHALL execute within a Resolver Context.

Example

```yaml
resolver:

  resolver_id:

  transport:

  dnssec_enabled:

  cache_enabled:
```

Resolver implementations SHALL remain opaque to consumers.

---

# Execution Options

Execution options MAY include

```yaml
timeout:

retry_policy:

follow_cname:

validate_dnssec:

cache_policy:
```

---

# Batch Requests

Batch requests SHALL contain

```yaml
queries:

parallel:

preserve_order:
```

Consumers MAY request parallel execution.

---

# Reverse Lookup

Reverse lookup requests SHALL specify

```yaml
ip_address:
```

Returned PTR records SHALL be normalized.

---

# Wildcard Detection

Wildcard detection requests MAY include

```yaml
domain:

sample_size:

confidence_threshold:
```

Returned values SHALL include a confidence assessment.

---

# DNSSEC Validation

Validation requests SHALL specify

```yaml
domain:

record_type:
```

Returned information MAY include

- Validation Status
- Trust Chain
- Signature Status

---

# DNS Response

Successful operations SHALL return a normalized DNS Response.

Example

```yaml
status:

records:

resolver:

response_time:

ttl:

metadata:
```

Raw resolver output SHALL NOT be exposed.

---

# Record Structure

Each record SHALL expose

```yaml
name:

type:

class:

ttl:

value:
```

Additional metadata MAY be included.

---

# Evidence

DNS operations SHALL expose structured evidence.

Evidence MAY include

- Query
- Resolver
- Response
- TTL
- DNSSEC Status
- Response Time

Evidence SHALL conform to the canonical Evidence schema.

---

# Metrics

DNS metrics MAY include

```yaml
query_duration:

resolver_latency:

cache_hit:

record_count:
```

Metrics SHOULD integrate with platform observability.

---

# Error Contract

Errors SHALL conform to

```
skills/core/error-handling.md
```

Typical categories include

- Resolver
- Configuration
- Network
- Timeout
- DNSSEC
- Cache
- Internal

---

# Security Requirements

The DNS Client Interface SHALL

- Respect configured resolver policies
- Support secure DNS transports
- Prevent resolver leakage between assessments
- Normalize all DNS responses
- Preserve auditability

---

# Compatibility

Consumers SHALL remain independent of

- dig
- host
- nslookup
- dnsx
- language-specific DNS libraries

The DNS Response SHALL remain stable across implementations.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL include

- Metadata
- DNS Request
- Resolver Context
- Execution Options
- DNS Response
- Evidence
- Error Handling

---

# Quality Requirements

The DNS Client Interface SHALL

✓ Be resolver independent

✓ Produce normalized responses

✓ Support secure transports

✓ Preserve evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY support

- DNS-over-HTTPS
- DNS-over-TLS
- DNS-over-QUIC
- EDNS
- Resolver federation
- Distributed resolution

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant DNS Client Interface provides a stable, implementation-independent contract for DNS operations across the Robust PenTest Platform.

It enables consistent DNS resolution, response normalization, security validation, evidence generation, and observability while abstracting resolver implementations and DNS tooling.