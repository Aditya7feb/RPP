"""Smoke tests for the RPP runtime.

These tests execute no scans and require no network. They validate that the
platform is wired correctly: configuration, safety gating, the single evidence
path, the MCP integration boundary (via the mock transport), and the reporting
pipeline.

Run with:  python -m unittest discover -s tests
"""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpp.agents.master import MasterAgent
from rpp.config import RuntimeConfig, _mini_yaml
from rpp.safety.policy import ApprovalStore, SafetyPolicy
from rpp.schemas import RulesOfEngagement, Scope, Target


def _fixture():
    config = RuntimeConfig()  # dry_run=True by default
    scope = Scope(included_targets=["target.test"])
    roe = RulesOfEngagement(allowed_hosts=["target.test"])
    target = Target(value="https://target.test", type="url")
    return config, scope, roe, target


class TestConfig(unittest.TestCase):
    def test_mini_yaml_parses_nested_and_lists(self):
        data = _mini_yaml(
            "mcp:\n  endpoint: http://x\n  timeout_seconds: 30\n"
            "retry:\n  max_attempts: 5\n"
            "custom_headers:\n  User-Agent: RPP\n"
        )
        self.assertEqual(data["mcp"]["endpoint"], "http://x")
        self.assertEqual(data["mcp"]["timeout_seconds"], 30)
        self.assertEqual(data["retry"]["max_attempts"], 5)
        self.assertEqual(data["custom_headers"]["User-Agent"], "RPP")

    def test_outbound_headers_preserve_x_rpp(self):
        config = RuntimeConfig()
        headers = config.outbound_headers("req-1", "asm-1", "trace-1")
        self.assertEqual(headers["X-RPP-Request-ID"], "req-1")
        self.assertEqual(headers["X-RPP-Assessment"], "asm-1")
        self.assertEqual(headers["X-RPP-Trace"], "trace-1")
        self.assertEqual(headers["User-Agent"], "RPP")


class TestSafety(unittest.TestCase):
    def test_scope_violation_out_of_scope(self):
        _, scope, roe, _ = _fixture()
        policy = SafetyPolicy(scope, roe)
        with self.assertRaises(Exception):
            policy.check_scope(Target(value="https://evil.example"))

    def test_in_scope_ok(self):
        _, scope, roe, target = _fixture()
        policy = SafetyPolicy(scope, roe)
        policy.check_scope(target)  # should not raise

    def test_active_testing_requires_approval(self):
        _, scope, roe, target = _fixture()
        policy = SafetyPolicy(scope, roe)
        approvals = ApprovalStore()
        self.assertTrue(policy.requires_approval("active-testing.fuzzing", True))
        with self.assertRaises(Exception):
            policy.enforce_approval("active-testing.fuzzing", target, approvals)
        approvals.grant("active-testing.fuzzing", target.value)
        policy.enforce_approval("active-testing.fuzzing", target, approvals)  # ok


class TestOrchestration(unittest.TestCase):
    def test_dry_run_produces_evidence_without_execution(self):
        config, scope, roe, target = _fixture()
        master = MasterAgent(config, scope, roe)
        result = master.run(target, [
            "discovery.port-discovery",
            "web-security.security-headers",
        ])
        self.assertIsNone(result.scope_error)
        self.assertEqual(len(result.dispatched), 2)
        # Evidence produced through the single path, but marked dry-run.
        self.assertEqual(len(result.store.evidence), 2)
        for ev in result.store.evidence.values():
            self.assertEqual(ev.stdout, "")  # nothing executed
        self.assertIsNotNone(result.report)
        self.assertEqual(result.store.state.phase, "COMPLETED")

    def test_intrusive_capability_withheld_without_approval(self):
        config, scope, roe, target = _fixture()
        master = MasterAgent(config, scope, roe)
        result = master.run(target, ["active-testing.injection-validation"])
        self.assertEqual(len(result.withheld_for_approval), 1)
        self.assertEqual(len(result.dispatched), 0)

    def test_intrusive_capability_dispatched_after_approval(self):
        config, scope, roe, target = _fixture()
        master = MasterAgent(config, scope, roe)
        master.approvals.grant("active-testing.injection-validation", target.value)
        result = master.run(target, ["active-testing.injection-validation"])
        self.assertEqual(len(result.withheld_for_approval), 0)
        self.assertEqual(len(result.dispatched), 1)

    def test_out_of_scope_target_fails_fast(self):
        config, scope, roe, _ = _fixture()
        master = MasterAgent(config, scope, roe)
        result = master.run(Target(value="https://evil.example"),
                            ["discovery.port-discovery"])
        self.assertIsNotNone(result.scope_error)
        self.assertEqual(len(result.dispatched), 0)


if __name__ == "__main__":
    unittest.main()
