# Certificate Chain Schema

**File:** `schemas/certificate-chain.md`

**Version:** 1.0.0

---

# Purpose

The Certificate Chain Schema defines the canonical representation of the ordered certificate path supplied by a TLS peer and any locally resolved trust anchor.

Certificate chains SHALL preserve peer order and SHALL distinguish peer-supplied certificates from locally trusted material.

---

# Design Principles

A Certificate Chain SHALL be

- Ordered
- Traceable
- Evidence backed
- Peer-observation preserving
- Implementation independent
- Separate from validation conclusions

---

# Identity

Every Certificate Chain SHALL contain

```yaml
chain_id:

schema_version:
```

Chain IDs SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Relationship to Connection

Every Certificate Chain SHALL contain

```yaml
connection_id:
```

`connection_id` SHALL reference the owning TLS Connection.

---

# Peer Certificates

Every Certificate Chain SHALL contain

```yaml
peer_certificates:
```

`peer_certificates` SHALL be an ordered array of one or more `certificate_id` values.

Index `0` SHALL be the leaf certificate.

Each certificate ID SHALL reference `schemas/certificate.md`.

---

# Trust Anchor

Certificate Chains MAY contain

```yaml
trust_anchor_certificate_id:
```

The trust anchor SHALL represent a locally selected anchor certificate.

The trust anchor SHALL NOT be represented as peer supplied unless the peer actually supplied it.

---

# Chain Completeness

Every Certificate Chain SHALL contain

```yaml
chain_complete:
```

`chain_complete` indicates whether validation could construct a chain to an anchor under the configured trust store.

---

# Peer Order Preservation

Every Certificate Chain SHALL contain

```yaml
peer_order_preserved:
```

`peer_order_preserved` SHALL be `true` for peer-observed chains.

---

# Observation Metadata

Every Certificate Chain SHALL contain

```yaml
observed_at:
```

`observed_at` SHALL be an RFC 3339 UTC timestamp.

---

# Evidence

Every Certificate Chain SHALL contain

```yaml
evidence:
```

Evidence IDs SHALL conform to `schemas/evidence.md`.

Evidence SHOULD include DER evidence when collection policy requires raw certificates.

---

# Extensions

Certificate Chains MAY contain

```yaml
extensions:
```

Extensions SHALL contain namespaced adapter metadata only.

Extensions SHALL NOT contain private keys or secret material.

---

# Example

```yaml
chain_id: tlschain-01
schema_version: 1.0.0
connection_id: tlsconn-01
peer_certificates:
  - cert-leaf-01
  - cert-intermediate-01
trust_anchor_certificate_id: cert-root-01
chain_complete: true
peer_order_preserved: true
observed_at: '2026-07-25T10:00:01Z'
evidence:
  - evidence-cert-der-01
  - evidence-tls-01
```

---

# Validation Rules

A valid Certificate Chain object SHALL contain

- Chain ID
- Schema Version
- Connection ID
- Peer Certificates
- Chain Complete Status
- Peer Order Preserved Status
- Observation Timestamp
- Evidence References

---

# Success Criteria

A compliant Certificate Chain object preserves the peer-observed certificate path while allowing validation logic to reference locally resolved trust anchors separately.

It enables consistent certificate-chain evidence, normalization, and validation across TLS adapters.
