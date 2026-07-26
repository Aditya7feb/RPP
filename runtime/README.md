# RPP Runtime — Kali MCP Integration

**Version:** 0.1.0

The first executable layer for the Robust PenTest Platform (RPP). It wires the
**Master Agent** to a **Kali MCP server** while conforming to the authoritative,
documentation-first architecture under [`schemas/`](../schemas), [`skills/`](../skills),
and [`agents/`](../agents). This directory contains implementation code only; it
does not modify the architecture.

The Master Agent remains a **pure orchestrator** and never executes a security
tool. All tool execution occurs through the Kali MCP server, reached exclusively
via the MCP integration layer.

---

## Integration Architecture

```text
                    ┌───────────────────────────────┐
                    │          Master Agent          │  pure orchestrator
                    │ plan · delegate · gate · track │  (agents/master)
                    └───────────────┬───────────────┘
                    task            │            agent-response
        ┌───────────────────────────┼────────────────────────────┐
        ▼                           ▼                            ▼
  Discovery Agent           Web Security Agent          Active Testing Agent   … (8 tiers)
        │                           │                            │
        └───────────────┬───────────┴──────────────┬────────────┘
                        ▼  (tool execution only)     ▼
                 ┌────────────────────────────────────────┐
                 │        MCP Integration Layer            │  Phase A boundary
                 │  discover · query · resolve · invoke ·  │  (rpp/mcp)
                 │  capture stdout/stderr/exit · normalise │
                 └───────────────┬────────────────────────┘
                                 ▼
                        Kali MCP Server (HTTP/SSE)
                                 │
                 every execution ▼
                 ┌────────────────────────────────────────┐
                 │  Evidence path (single)  → Reporting    │
                 │  rpp/evidence            → rpp/reporting│
                 └────────────────────────────────────────┘
```

Mapping to the requested phases:

| Phase | Concern | Module |
|-------|---------|--------|
| A | MCP integration layer | [`rpp/mcp/`](rpp/mcp) — `transport.py`, `client.py`, `registry.py`, `integration.py` |
| B | Master Agent + tier agents | [`rpp/agents/`](rpp/agents), [`rpp/orchestration/`](rpp/orchestration) |
| C | Evidence integration | [`rpp/evidence/collector.py`](rpp/evidence/collector.py) |
| D | Reporting integration | [`rpp/reporting/pipeline.py`](rpp/reporting/pipeline.py) |
| E | Configuration | [`rpp/config.py`](rpp/config.py), [`config/rpp.example.yaml`](config/rpp.example.yaml) |
| F | Safety (scope, RoE, approval) | [`rpp/safety/policy.py`](rpp/safety/policy.py) |

The rest of the repository is unaware of MCP: only `rpp/mcp/` knows the wire
protocol, and only the capability-tier agents call it. The Master Agent depends
on agents, safety, planning, and the reporting pipeline — never on MCP.

---

## Execution Flow

1. **Plan (WHAT).** The Master Agent builds an execution plan of canonical
   `Task` objects from a user-supplied target and a list of capabilities.
   Discovery is ordered first; intrusive Active Testing is flagged as gated.
2. **Scope / RoE (Phase F).** The target is validated against `Scope` and
   `RulesOfEngagement` before any dispatch. Out-of-scope targets fail fast.
3. **Delegate (WHO).** Each task is routed to the specialist tier agent that owns
   its capability. The agent resolves the capability to a concrete MCP tool via
   the capability registry.
4. **Approval gate (Phase F).** If a capability is intrusive (or listed in RoE),
   the Master Agent withholds it until an approval is granted. No intrusive
   Active Testing runs without approval.
5. **Invoke (Phase A).** The tier agent calls the MCP integration layer, which
   invokes the tool, captures stdout / stderr / exit status, and normalises any
   error. The Master Agent itself never calls MCP.
6. **Evidence (Phase C).** Every execution flows through the single Evidence
   collector, producing an immutable `Evidence` object (executed command,
   stdout, stderr, exit status, timestamps, duration, SHA-256 hash) and a
   correlated `Observation`. There is exactly one evidence path.
7. **Report (Phase D).** The Master Agent drives the Reporting pipeline —
   `finding-correlation → risk-analysis → report-generation → evidence-bundle` —
   consuming Findings, Risk, and Evidence by reference only.
8. **Complete.** Execution state is finalised and a `Report` referencing
   canonical objects by identifier is returned.

Canonical objects (`Task`, `AgentResponse`, `Evidence`, `Observation`,
`Finding`) are executable representations of the schemas under
[`schemas/`](../schemas); field names conform to those documents.

---

## Configuration (Phase E)

All configuration lives in one place: a single YAML (or JSON) file, modelled by
[`rpp/config.py`](rpp/config.py). See [`config/rpp.example.yaml`](config/rpp.example.yaml).

It covers: **MCP endpoint**, **authentication**, **execution timeout**, **retry
policy**, **concurrency**, and **custom HTTP headers**.

- **Authentication** is by environment-variable reference only
  (`authentication.token_env`); secrets are never stored in the file or logged.
- **Custom HTTP headers** preserve the previously defined outbound headers:
  `X-RPP-Request-ID` (correlation), `X-RPP-Assessment`, and `X-RPP-Trace`, plus
  `User-Agent: RPP`. These are applied to every outbound MCP request and the
  correlation identifiers are populated per assessment / per request.
- **`dry_run: true`** (default) makes the platform executable without contacting
  any server or running any tool.

The core runtime and the dry-run example use the **standard library only** (a
minimal YAML subset parser is built in). Live operation needs `httpx`
(and optionally `PyYAML`): `pip install -e ".[http,yaml]"`.

---

## Safety (Phase F)

- **Scope / RoE**: `SafetyPolicy.check_scope` rejects excluded targets, targets
  outside the included scope, disallowed hosts, and disallowed protocols.
- **Approval gates**: intrusive capabilities (any `active-testing.*`, anything
  marked intrusive in the registry, or anything listed in
  `RulesOfEngagement.approval_required_capabilities`) are withheld until an
  `Approval` is granted. Defense-in-depth: a tier agent also refuses an intrusive
  invocation that arrives without an approval reference.
- **No hard-coded targets**: the target is always supplied at runtime and
  validated before use.

---

## Validation Steps

From this `runtime/` directory:

```bash
# 1. Smoke tests (standard library only; no network; executes no scans)
python3 -m unittest discover -s tests

# 2. First runnable example in dry-run (replace the target with your own;
#    nothing is executed against it while dry_run is true)
python3 examples/first_run.py \
  --target https://YOUR-APPROVED-TARGET \
  --config config/rpp.example.yaml

# 3. Demonstrate the approval gate releasing an intrusive capability (still dry-run)
python3 examples/first_run.py \
  --target https://YOUR-APPROVED-TARGET \
  --grant active-testing.injection-validation
```

Expected: all tests pass; the example discovers the MCP tool catalogue, plans
across tiers, dispatches non-intrusive work, withholds intrusive Active Testing
for approval, collects evidence through the single path, and prints a report —
without executing any tool.

---

## First Runnable Example

[`examples/first_run.py`](examples/first_run.py) is the end-to-end entry point.
It takes a user-supplied `--target`, builds scope and RoE around it, and runs the
full orchestration in dry-run. It hard-codes no target and executes no scan.

---

## Going Live (later, against approved targets)

1. Set `mcp.endpoint` to your Kali MCP server URL in the config.
2. If the server requires auth, set `authentication.type` and export the token in
   the environment variable named by `authentication.token_env`.
3. Set `dry_run: false`.
4. Install the transport extra: `pip install -e ".[http]"`.
5. Run the example against your **approved** OWASP Juice Shop / DVWA instances.

Until then the platform is fully executable in dry-run and performs no scanning.
