# Certificate Schema

**File:** `schemas/certificate.md`

**Version:** 1.0.0

---

# Purpose

The Certificate Schema defines the canonical representation of a parsed X.509 certificate observed by the TLS Client.

A Certificate is a factual artifact. It SHALL NOT imply that the certificate is trusted.

Trust decisions SHALL be represented by `schemas/tls-validation-result.md`.

---

# Design Principles

A Certificate object SHALL be

- Traceable
- Immutable
- Evidence backed
- Implementation independent
- Normalized
- Safe to store
- Separate from validation conclusions

---

# Identity

Every Certificate SHALL contain

```yaml
certificate_id:

schema_version:
```

Certificate IDs SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Fingerprint

Every Certificate SHALL contain

```yaml
sha256_fingerprint:
```

The fingerprint SHALL be exactly 64 hexadecimal characters.

Uppercase or lowercase hexadecimal characters MAY be used.

---

# Subject and Issuer

Every Certificate SHALL contain

```yaml
subject:

issuer:
```

`subject` SHALL be a normalized RFC 4514 distinguished name.

`subject` MAY be empty only if the certificate does not contain a subject.

`issuer` SHALL be a normalized RFC 4514 distinguished name.

---

# Serial Number

Every Certificate SHALL contain

```yaml
serial_number:
```

The serial number SHALL be a non-empty hexadecimal value without a `0x` prefix.

---

# Validity Period

Every Certificate SHALL contain

```yaml
not_before:

not_after:
```

Timestamps SHALL be RFC 3339 UTC timestamps.

`not_after` SHALL be later than `not_before`.

---

# Public Key

Every Certificate SHALL contain

```yaml
public_key_algorithm:
```

Certificates MAY contain

```yaml
public_key_size_bits:
```

`public_key_algorithm` SHALL use an IANA or widely recognized algorithm name such as `RSA`, `ECDSA`, or `Ed25519`.

`public_key_size_bits` SHALL be a positive integer when meaningful for the algorithm.

---

# Signature

Every Certificate SHALL contain

```yaml
signature_algorithm:
```

The signature algorithm SHALL use a normalized certificate signature algorithm name.

---

# Subject Alternative Names

Every Certificate SHALL contain

```yaml
subject_alternative_names:
```

The value SHALL be an array of zero or more DNS names, IP literals, URI names, or other supported name forms.

DNS names SHALL be normalized to lowercase.

---

# Certificate Authority Status

Every Certificate SHALL contain

```yaml
is_ca:
```

`is_ca` SHALL represent the Basic Constraints CA value.

---

# Key Usage

Certificates MAY contain

```yaml
key_usage:

extended_key_usage:
```

`key_usage` SHALL be an array of normalized X.509 key-usage names.

`extended_key_usage` SHALL be an array of OIDs or normalized EKU names.

---

# Evidence

Certificates MAY contain

```yaml
raw_der_evidence_id:
```

`raw_der_evidence_id` SHALL reference the original DER artifact when raw certificate evidence is collected.

Evidence SHALL conform to `schemas/evidence.md`.

---

# Extensions

Certificates MAY contain

```yaml
extensions:
```

Extensions SHALL be namespaced parsed fields not covered by this schema.

Extensions SHALL NOT contain private keys or secret material.

---

# Example

```yaml
certificate_id: cert-leaf-01
schema_version: 1.0.0
sha256_fingerprint: 45f5b4b6c90b5a0b7df11b0e4d3f5df3594b18fd7d4bcb599e0a81d437f81d52
subject: CN=api.example.com
issuer: CN=Example Issuing CA,O=Example Trust
serial_number: 04AF12C9
not_before: '2026-06-01T00:00:00Z'
not_after: '2027-06-01T23:59:59Z'
public_key_algorithm: ECDSA
public_key_size_bits: 256
signature_algorithm: ecdsa-with-SHA256
subject_alternative_names:
  - api.example.com
  - www.api.example.com
is_ca: false
extended_key_usage:
  - serverAuth
raw_der_evidence_id: evidence-cert-der-01
```

---

# Validation Rules

A valid Certificate object SHALL contain

- Certificate ID
- Schema Version
- SHA-256 Fingerprint
- Subject
- Issuer
- Serial Number
- Validity Period
- Public Key Algorithm
- Signature Algorithm
- Subject Alternative Names
- CA Status

---

# Success Criteria

A compliant Certificate object provides a normalized, evidence-backed representation of an observed X.509 certificate.

It enables TLS consumers to reason over certificate facts without confusing certificate observation with trust validation.
