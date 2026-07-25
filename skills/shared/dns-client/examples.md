# DNS Client Examples

**File:** `skills/shared/dns-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document illustrates representative usage patterns for the DNS Client Shared Skill.

Examples demonstrate how consumers interact with the DNS Client Interface while remaining independent of DNS libraries, operating system utilities, or resolver implementations.

These examples are illustrative and SHALL NOT prescribe implementation details.

---

# Design Goals

Examples SHOULD demonstrate

- Proper interface usage
- Resolver abstraction
- Configuration inheritance
- Evidence generation
- Error handling
- Batch execution
- Security validation

---

# Example 1 — Resolve IPv4 Address

## Scenario

The Recon Skill needs the IPv4 addresses for a target domain.

### Consumer

```
Recon Skill

↓

DNS Client

↓

Normalized DNS Response
```

### Request

```yaml
operation: dns.resolve

query:

  name: example.com

  record_type: A
```

### Expected Result

```yaml
status: success

records:

  - type: A

    value: 93.184.216.34
```

Evidence SHALL be generated.

---

# Example 2 — Resolve IPv6 Address

```yaml
operation: dns.resolve

query:

  name: example.com

  record_type: AAAA
```

Expected output

```
AAAA Records
```

---

# Example 3 — Retrieve Mail Servers

```yaml
operation: dns.resolve

query:

  name: example.com

  record_type: MX
```

Expected output

```
MX Records
```

---

# Example 4 — Resolve TXT Records

Useful for

- SPF
- Verification tokens
- Miscellaneous TXT entries

```yaml
operation: dns.resolve

query:

  name: example.com

  record_type: TXT
```

---

# Example 5 — Follow CNAME Chain

```
example.com

↓

CNAME

↓

service.example.net

↓

A Record
```

Request

```yaml
operation: dns.resolve.chain
```

Expected output

```
Complete normalized resolution chain
```

---

# Example 6 — Reverse Lookup

```yaml
operation: dns.reverse.lookup

ip_address:

  203.0.113.25
```

Expected output

```
PTR Record
```

---

# Example 7 — Batch Resolution

The Fingerprinting Skill resolves multiple hosts simultaneously.

```yaml
operation: dns.resolve.batch

queries:

- api.example.com

- admin.example.com

- mail.example.com

parallel: true
```

Expected behavior

- Parallel execution
- Ordered results
- Independent failures

---

# Example 8 — DNSSEC Validation

The TLS Skill validates DNSSEC before certificate analysis.

```yaml
operation: dns.dnssec.validate

domain:

  example.com
```

Expected output

```yaml
dnssec:

  status: valid
```

---

# Example 9 — Retrieve CAA Records

```yaml
operation: dns.caa.lookup

domain:

  example.com
```

Expected output

```
CAA Records
```

---

# Example 10 — Wildcard Detection

The Content Discovery Skill verifies wildcard DNS.

```yaml
operation: dns.wildcard.detect

domain:

  example.com
```

Expected output

```yaml
wildcard:

  detected: false

confidence:

  0.97
```

---

# Example 11 — Cache Hit

The requested record already exists in cache.

Execution

```
Cache Lookup

↓

Valid TTL

↓

Return Cached Response

↓

Capture Evidence
```

Resolver communication SHOULD be skipped.

---

# Example 12 — Resolver Failover

Primary resolver becomes unavailable.

Execution

```
Primary Resolver

↓

Unavailable

↓

Secondary Resolver

↓

Successful Resolution
```

Evidence SHOULD capture the failover event.

---

# Example 13 — Timeout Recovery

A resolver exceeds the configured timeout.

Execution

```
Resolver Timeout

↓

Retry Policy

↓

Successful Retry
```

Retry SHALL comply with platform retry policies.

---

# Example 14 — Policy Violation

Assessment policy only permits approved internal resolvers.

Consumer requests

```
Public Resolver
```

Expected result

```
Policy Error

↓

Execution Terminated
```

No DNS query SHALL be executed.

---

# Example 15 — Recon Workflow

```
Recon Skill

↓

Resolve A

↓

Resolve AAAA

↓

Resolve CNAME

↓

Resolve NS

↓

Resolve SOA

↓

Capture Evidence
```

The DNS Client performs only DNS operations.

Recon interprets the results.

---

# Example 16 — TLS Workflow

```
TLS Skill

↓

Resolve A

↓

Resolve AAAA

↓

Resolve CAA

↓

DNSSEC Validation

↓

Certificate Analysis
```

---

# Example 17 — SSRF Workflow

```
SSRF Skill

↓

Resolve Internal Host

↓

Validate Response

↓

Continue SSRF Analysis
```

---

# Example 18 — Fingerprinting Workflow

```
Fingerprinting Skill

↓

Resolve Host

↓

Normalize Records

↓

Combine with HTTP Results

↓

Technology Detection
```

---

# Example 19 — Evidence Collection

Generated evidence MAY include

```yaml
query:

resolver:

transport:

record_type:

response:

ttl:

dnssec:

duration:
```

Evidence SHALL conform to the canonical Evidence schema.

---

# Example 20 — Event Timeline

```
QueryStarted

↓

ResolverSelected

↓

CacheMiss

↓

QueryExecuted

↓

ResponseNormalized

↓

EvidenceCaptured

↓

QueryCompleted
```

---

# Best Practices

Consumers SHOULD

- Use Resolver Profiles
- Reuse DNS Client operations
- Enable evidence generation
- Respect cache policies
- Normalize all responses
- Validate DNSSEC where appropriate

---

# Anti-Patterns

Consumers SHOULD NOT

- Execute dig directly
- Execute nslookup directly
- Parse raw resolver output
- Hardcode resolver addresses
- Implement resolver-specific logic
- Duplicate caching behavior

---

# Cross-Skill Integration

The DNS Client is intended to be reused by

- Recon
- Fingerprinting
- TLS
- SSRF
- Content Discovery
- CORS
- GraphQL
- Authentication
- File Upload
- Port Discovery

All DNS operations SHOULD pass through the shared DNS Client.

---

# Success Criteria

A compliant DNS Client implementation enables every platform component to perform DNS operations through a single, standardized, observable, and implementation-independent interface.

Examples demonstrate consistent resolver usage, response normalization, evidence generation, security validation, and interoperability across the Robust PenTest Platform.