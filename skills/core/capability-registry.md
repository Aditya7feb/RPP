# Capability Registry

**File:** `skills/core/capability-registry.md`

**Version:** 1.0.0

---

# Purpose

The Capability Registry defines the canonical namespace for capabilities within the Robust PenTest Platform (RPP).

Rather than allowing skills to invent arbitrary capability names, the registry establishes a standardized vocabulary that enables consistent planning, dependency resolution, skill discovery, and execution.

Every capability exposed by a skill SHOULD be registered within this document.

---

# Design Principles

Capabilities SHALL be

- Canonical
- Stable
- Unique
- Hierarchical
- Versioned
- Discoverable
- Implementation Independent

Capabilities represent behaviors, not implementations.

---

# Why a Registry?

Without a registry, different skills may expose equivalent capabilities using different names.

Examples

```
HTTP Request

Send HTTP

HTTPRequest

http.send

request.http
```

All of these represent the same behavior.

The registry eliminates ambiguity.

---

# Naming Convention

Capabilities SHALL follow hierarchical naming.

```
<domain>.<subcategory>.<operation>
```

Examples

```
network.http.send

network.http.parse_headers

network.dns.resolve

security.discovery.technology.detect

security.validation.sqli.verify
```

---

# Registry Organization

Capabilities are grouped by domain.

```
Networking

Discovery

Authentication

Session Management

Fingerprinting

Web Security

API Security

Infrastructure

Cloud

Reporting

Utility
```

---

# Networking

## HTTP

```
network.http.send

network.http.follow_redirects

network.http.parse_headers

network.http.parse_cookies

network.http.parse_body

network.http.upload

network.http.download
```

---

## DNS

```
network.dns.resolve

network.dns.reverse_lookup

network.dns.zone_transfer

network.dns.enumerate

network.dns.record_lookup
```

---

## TLS

```
network.tls.inspect

network.tls.validate

network.tls.certificate.extract

network.tls.cipher.enumerate

network.tls.protocol.detect
```

---

## TCP

```
network.tcp.connect

network.tcp.banner_grab
```

---

# Discovery

```
security.discovery.host

security.discovery.port

security.discovery.endpoint

security.discovery.directory

security.discovery.api

security.discovery.technology

security.discovery.cms

security.discovery.framework

security.discovery.javascript

security.discovery.parameters
```

---

# Fingerprinting

```
security.fingerprint.webserver

security.fingerprint.runtime

security.fingerprint.framework

security.fingerprint.cms

security.fingerprint.waf

security.fingerprint.cdn

security.fingerprint.language
```

---

# Authentication

```
security.auth.jwt.decode

security.auth.jwt.validate

security.auth.oauth.inspect

security.auth.session.inspect

security.auth.cookie.inspect

security.auth.api_key.validate
```

---

# Session Management

```
security.session.analyze

security.session.fixation

security.session.timeout

security.session.rotation
```

---

# Web Security

## SQL Injection

```
security.validation.sqli.detect

security.validation.sqli.verify

security.validation.sqli.exploit
```

---

## Cross Site Scripting

```
security.validation.xss.detect

security.validation.xss.verify
```

---

## SSRF

```
security.validation.ssrf.detect

security.validation.ssrf.verify
```

---

## SSTI

```
security.validation.ssti.detect

security.validation.ssti.verify
```

---

## File Upload

```
security.validation.file_upload.detect

security.validation.file_upload.verify
```

---

## IDOR

```
security.validation.idor.detect

security.validation.idor.verify
```

---

## CORS

```
security.validation.cors.analyze
```

---

## CSP

```
security.validation.csp.analyze
```

---

# API Security

```
security.api.graphql.enumerate

security.api.graphql.introspection

security.api.rest.enumerate

security.api.soap.inspect

security.api.grpc.inspect
```

---

# Infrastructure

```
security.infrastructure.port_scan

security.infrastructure.service_detect

security.infrastructure.os_detect

security.infrastructure.banner_grab
```

---

# Cloud

```
security.cloud.azure.enumerate

security.cloud.aws.enumerate

security.cloud.gcp.enumerate
```

---

# Analysis

```
analysis.html.parse

analysis.javascript.parse

analysis.headers.parse

analysis.cookies.parse

analysis.response.compare

analysis.secret.detect
```

---

# Reporting

```
report.summary.generate

report.finding.generate

report.evidence.package

report.risk.aggregate
```

---

# Utility

```
utility.encoding.base64

utility.encoding.url

utility.hash.sha256

utility.regex.extract

utility.diff.compare
```

---

# Capability Metadata

Each registered capability SHOULD define

```yaml
id:

name:

description:

category:

introduced_in:

deprecated:

replacement:
```

---

# Capability Lifecycle

Capabilities progress through

```
Proposed

↓

Registered

↓

Stable

↓

Deprecated

↓

Removed
```

Deprecated capabilities SHOULD include migration guidance.

---

# Versioning

Capability identifiers SHALL remain stable.

Behavior MAY evolve without changing the identifier.

Breaking semantic changes SHALL require a new capability identifier.

---

# Ownership

Each capability SHOULD identify

```yaml
owner:

maintainer:

reviewer:
```

Ownership promotes consistency and long-term maintenance.

---

# Validation Rules

A registered capability SHALL

- Have a unique identifier
- Follow the naming convention
- Belong to a category
- Include a description
- Be implementation independent

---

# Quality Requirements

The registry SHALL

✓ Provide a canonical namespace

✓ Eliminate duplicate capability names

✓ Support discovery

✓ Support dependency resolution

✓ Support planning

✓ Remain implementation independent

---

# Future Extensions

Future versions MAY include

- Capability aliases
- Capability maturity levels
- Performance metadata
- Policy annotations
- Compliance mappings
- Skill implementation references

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Capability Registry provides a stable and universally understood vocabulary for describing the behaviors that skills expose.

It enables consistent planning, orchestration, dependency resolution, and interoperability across the Robust PenTest Platform while allowing multiple implementations to expose the same capability.