#!/usr/bin/env python3
"""First runnable example for the RPP + Kali MCP integration.

This makes the platform *executable* without running any scan. With the default
configuration (``dry_run: true``) it:

* loads the single configuration file
* builds scope and Rules of Engagement around a USER-SUPPLIED target
* discovers the MCP tool catalogue (no network in dry-run)
* plans an assessment across several capability tiers
* delegates through the Master Agent -> tier agents -> MCP integration layer
* produces Evidence through the single Evidence path
* drives the Reporting pipeline
* demonstrates the approval gate holding intrusive Active Testing

No target is hard-coded. Provide one with ``--target``. Nothing is executed
against it while ``dry_run`` is true.

Usage:
    python examples/first_run.py --target https://your-approved-target.example \
        --config config/rpp.example.yaml

    # Demonstrate an approved intrusive capability (still dry-run, no execution):
    python examples/first_run.py --target https://your-approved-target.example \
        --grant active-testing.injection-validation
"""

from __future__ import annotations

import argparse
import os
import sys
from urllib.parse import urlparse

# Allow running directly from the runtime/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpp.agents.master import MasterAgent          # noqa: E402
from rpp.config import RuntimeConfig, load_config   # noqa: E402
from rpp.schemas import RulesOfEngagement, Scope, Target  # noqa: E402


DEFAULT_CAPABILITIES = [
    "discovery.port-discovery",
    "discovery.fingerprinting",
    "web-security.security-headers",
    "active-testing.injection-validation",   # intrusive -> gated by approval
]


def _host_of(value: str) -> str:
    if "://" in value:
        return (urlparse(value).hostname or "").lower()
    return value.split("/")[0].split(":")[0].lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="RPP + Kali MCP first run (dry-run).")
    parser.add_argument("--target", required=True,
                        help="User-supplied target (host or URL) within approved scope.")
    parser.add_argument("--config", default=None,
                        help="Path to the runtime configuration file.")
    parser.add_argument("--capability", action="append", dest="capabilities",
                        help="Capability to include (repeatable). Defaults to a sample set.")
    parser.add_argument("--grant", action="append", dest="grants", default=[],
                        help="Capability to pre-approve for the target (repeatable).")
    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
    else:
        config = RuntimeConfig()  # safe defaults, dry_run=True

    host = _host_of(args.target)
    if not host:
        print(f"error: could not derive a host from target {args.target!r}", file=sys.stderr)
        return 2

    # Scope and RoE are built around the user-supplied target only.
    scope = Scope(included_targets=[host])
    roe = RulesOfEngagement(allowed_hosts=[host], allowed_protocols=["http", "https"])
    target = Target(value=args.target,
                    type="url" if "://" in args.target else "host")

    capabilities = args.capabilities or list(DEFAULT_CAPABILITIES)

    master = MasterAgent(config, scope, roe)

    # Optionally pre-approve intrusive capabilities to demonstrate the gate.
    for capability in args.grants:
        master.approvals.grant(capability, target.value)

    print(f"== RPP first run (dry_run={config.dry_run}) ==")
    print(f"assessment: {master.assessment_id}")
    print(f"target:     {target.value}  (host={host})")

    tools = master.integration.discover()
    print(f"MCP tools discovered: {[t.name for t in tools]}")

    result = master.run(target, capabilities)

    if result.scope_error:
        print(f"scope error: {result.scope_error}")
        return 1

    print("\n-- plan --")
    for task in result.plan.tasks:
        print(f"  {task.capability:38s} -> {task.assigned_agent}  [{task.status.value}]")

    print("\n-- outcome --")
    print(f"  dispatched:            {len(result.dispatched)}")
    print(f"  withheld for approval: {len(result.withheld_for_approval)}")
    print(f"  evidence collected:    {len(result.store.evidence)}")
    print(f"  observations:          {len(result.store.observations)}")
    print(f"  phase:                 {result.store.state.phase}")

    if result.report:
        print("\n-- report --")
        print(f"  {result.report.executive_summary}")
        print(f"  {result.report.technical_summary}")

    print("\nNo tools were executed (dry-run). Set dry_run: false and configure an "
          "MCP endpoint to run live against approved targets.")
    master.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
