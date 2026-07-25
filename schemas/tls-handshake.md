# TLS Handshake Schema

**File:** `schemas/tls-handshake.md`

**Version:** 1.0.0

---

# Purpose

The TLS Handshake Schema defines the canonical representation of the negotiated, peer-observed outcome of a TLS exchange.

A TLS Handshake SHALL be produced by the TLS Client and SHALL NOT assert security conclusions.

---

# Design Principles

A TLS Handshake SHALL be

- Traceable
- Peer observed
- Normalized
- Adapter independent
- Evidence backed
- Separate from validation conclusions

---

# Identity

Every TLS Handshake SHALL contain

```yaml
handshake_id:

schema_version:
```

Handshake IDs SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Relationship to Connection

Every TLS Handshake SHALL contain

```yaml
connection_id:
```

`connection_id` SHALL reference `TLS Connection.connection_id`.

---

# Timing

Every TLS Handshake SHALL contain

```yaml
started_at:

completed_at:
```

Timestamps SHALL be RFC 3339 UTC timestamps.

`completed_at` SHALL be on or after `started_at`.

---

# Negotiated Protocol

Every TLS Handshake SHALL contain

```yaml
negotiated_protocol:
```

`negotiated_protocol` SHALL use an IANA-style TLS version such as `TLSv1.2` or `TLSv1.3`.

---

# Cipher Suite

Every TLS Handshake SHALL contain

```yaml
cipher_suite:
```

`cipher_suite` SHALL use an IANA TLS cipher-suite name.

The cipher suite SHALL be compatible with the negotiated protocol.

---

# Key Exchange

TLS Handshakes MAY contain

```yaml
key_exchange_group:
```

`key_exchange_group` SHALL identify the negotiated named group when observable.

Example

```yaml
key_exchange_group: x25519
```

---

# Signature Algorithm

TLS Handshakes MAY contain

```yaml
signature_algorithm:
```

`signature_algorithm` SHALL represent the peer certificate or handshake signature algorithm when observable.

---

# Server Name Indication

TLS Handshakes MAY contain

```yaml
server_name_indication:
```

`server_name_indication` SHALL be the sent SNI hostname.

DNS names SHALL be normalized to lowercase.

---

# ALPN

TLS Handshakes MAY contain

```yaml
negotiated_alpn:
```

`negotiated_alpn` SHALL be the selected ALPN identifier.

Values SHALL be 1 to 255 ASCII bytes when present.

---

# Peer Certificate Presence

Every TLS Handshake SHALL contain

```yaml
peer_certificate_present:
```

`peer_certificate_present` indicates whether the peer supplied a certificate during the handshake.

---

# Resumption

Every TLS Handshake SHALL contain

```yaml
resumed:
```

`resumed` SHALL represent handshake-confirmed session resumption status.

---

# Extensions

TLS Handshakes MAY contain

```yaml
extensions:
```

Extensions SHALL contain namespaced adapter metadata only.

Extensions SHALL NOT contain private keys, pre-shared keys, session-ticket secrets, or decrypted application data.

---

# Example

```yaml
handshake_id: tlshs-01
schema_version: 1.0.0
connection_id: tlsconn-01
started_at: '2026-07-25T10:00:00Z'
completed_at: '2026-07-25T10:00:01Z'
negotiated_protocol: TLSv1.3
cipher_suite: TLS_AES_256_GCM_SHA384
key_exchange_group: x25519
server_name_indication: api.example.com
negotiated_alpn: h2
peer_certificate_present: true
resumed: false
```

---

# Validation Rules

A valid TLS Handshake object SHALL contain

- Handshake ID
- Schema Version
- Connection ID
- Start Timestamp
- Completion Timestamp
- Negotiated Protocol
- Cipher Suite
- Peer Certificate Presence
- Resumption Status

---

# Success Criteria

A compliant TLS Handshake object records the factual TLS negotiation outcome in a stable, adapter-independent format.

It enables consumers to use TLS negotiation metadata without depending on raw adapter output or inferring security conclusions.
