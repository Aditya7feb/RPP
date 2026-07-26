"""The Master Agent orchestrator (Phase B + F).

The Master Agent is a pure orchestrator. It plans, delegates, enforces scope /
Rules of Engagement / approval gates, tracks execution, drives the reporting
pipeline, and decides completion. It never executes a security tool: all tool
execution happens inside specialist tier agents, which call the MCP integration
layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..config import RuntimeConfig
from ..errors import ApprovalDenied, ScopeViolation
from ..evidence.collector import EvidenceCollector
from ..mcp.integration import MCPIntegration
from ..orchestration.planner import ExecutionPlan, Planner
from ..orchestration.state import AssessmentStore
from ..reporting.pipeline import Report, ReportingPipeline
from ..safety.policy import ApprovalStore, SafetyPolicy
from ..schemas import (
    ResponseStatus,
    RulesOfEngagement,
    Scope,
    Target,
    TaskStatus,
    new_id,
)
from .base import build_tier_agents


@dataclass
class AssessmentResult:
    assessment_id: str
    plan: ExecutionPlan
    store: AssessmentStore
    report: Report | None = None
    scope_error: str | None = None
    dispatched: list[str] = field(default_factory=list)
    withheld_for_approval: list[str] = field(default_factory=list)


class MasterAgent:
    """Pure orchestrator that coordinates capability-tier agents."""

    def __init__(self, config: RuntimeConfig, scope: Scope,
                 roe: RulesOfEngagement, *, assessment_id: str | None = None,
                 approvals: ApprovalStore | None = None) -> None:
        self._config = config
        self._scope = scope
        self._roe = roe
        self.assessment_id = assessment_id or new_id("assessment")

        self._safety = SafetyPolicy(scope, roe)
        self._approvals = approvals or ApprovalStore()
        self._planner = Planner(scope, roe)
        self._store = AssessmentStore(self.assessment_id)
        self._integration = MCPIntegration(config, assessment_id=self.assessment_id)
        self._collector = EvidenceCollector(self.assessment_id)
        self._agents = build_tier_agents(self._integration, self._collector, self._store)
        self._reporting = ReportingPipeline()

    @property
    def approvals(self) -> ApprovalStore:
        return self._approvals

    @property
    def integration(self) -> MCPIntegration:
        return self._integration

    def run(self, target: Target, capabilities: list[str]) -> AssessmentResult:
        """Plan, delegate, gate, track, report, and complete."""
        self._store.state.phase = "PLANNING"

        # Validate the user-supplied target against scope and RoE up front.
        try:
            self._safety.check_scope(target)
        except ScopeViolation as exc:
            self._store.state.phase = "FAILED"
            return AssessmentResult(
                assessment_id=self.assessment_id,
                plan=ExecutionPlan(assessment_id=self.assessment_id),
                store=self._store,
                scope_error=exc.message,
            )

        plan = self._planner.build(self.assessment_id, target, capabilities)
        for task in plan.tasks:
            self._store.add_task(task)

        result = AssessmentResult(
            assessment_id=self.assessment_id, plan=plan, store=self._store
        )

        self._store.state.phase = "EXECUTION"
        for task in plan.tasks:
            self._dispatch(task, target, result)

        # Reporting phase (Phase D): drive the pipeline by reference.
        self._store.state.phase = "REPORTING"
        result.report = self._reporting.run(self._store)

        self._store.state.phase = "COMPLETED"
        return result

    # -- delegation --------------------------------------------------------

    def _dispatch(self, task, target: Target, result: AssessmentResult) -> None:
        # Determine intrusiveness without executing anything.
        try:
            invocation = self._integration.resolve(task.capability, target, task.inputs)
            intrusive = invocation.intrusive
        except Exception:
            intrusive = task.capability.startswith("active-testing.")

        # Approval gate (Phase F): withhold intrusive work until approved.
        if self._safety.requires_approval(task.capability, intrusive):
            self._approvals.request(task.capability, target.value,
                                    f"execute {task.capability}")
            try:
                self._safety.enforce_approval(task.capability, target, self._approvals)
            except ApprovalDenied:
                task.status = TaskStatus.WAITING
                self._store.state.tasks_waiting_approval += 1
                self._store.state.coverage_gaps.append(task.capability)
                result.withheld_for_approval.append(task.task_id)
                return
            task.approval_ref = self._approvals.state_for(
                task.capability, target.value
            ).value

        agent = self._agents.get(task.capability.split(".", 1)[0])
        if agent is None:
            task.status = TaskStatus.SKIPPED
            self._store.state.coverage_gaps.append(task.capability)
            return

        task.status = TaskStatus.RUNNING
        response = agent.execute(task)
        result.dispatched.append(task.task_id)

        if response.status in (ResponseStatus.SUCCESS, ResponseStatus.SKIPPED):
            task.status = TaskStatus.COMPLETED
            self._store.state.tasks_completed += 1
        elif response.status == ResponseStatus.WAITING_FOR_APPROVAL:
            task.status = TaskStatus.WAITING
            self._store.state.tasks_waiting_approval += 1
        else:
            task.status = TaskStatus.FAILED
            self._store.state.tasks_failed += 1

    def close(self) -> None:
        self._integration.close()
