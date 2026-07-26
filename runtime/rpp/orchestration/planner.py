"""Planning (Phase B).

The planner converts a list of requested capabilities plus a user-supplied
target into an ordered set of canonical Tasks. It decides WHAT work happens and
in what order; it never executes anything. Discovery is scheduled first;
intrusive Active Testing capabilities are marked as gated so the Master Agent
holds them for approval.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..schemas import Scope, RulesOfEngagement, Target, Task, TaskStatus

# Canonical tier ordering for scheduling.
_TIER_ORDER = {
    "discovery": 0,
    "authentication": 1,
    "web-security": 2,
    "api-security": 2,
    "cloud": 2,
    "active-testing": 3,
    "evidence": 4,
    "reporting": 5,
}


def _tier_of(capability: str) -> str:
    return capability.split(".", 1)[0]


@dataclass
class ExecutionPlan:
    """Canonical execution-plan (see schemas/execution-plan.md)."""

    assessment_id: str
    tasks: list[Task] = field(default_factory=list)
    approval_points: list[str] = field(default_factory=list)


class Planner:
    def __init__(self, scope: Scope, roe: RulesOfEngagement) -> None:
        self._scope = scope
        self._roe = roe

    def build(self, assessment_id: str, target: Target,
              capabilities: list[str]) -> ExecutionPlan:
        ordered = sorted(capabilities, key=lambda c: _TIER_ORDER.get(_tier_of(c), 9))
        plan = ExecutionPlan(assessment_id=assessment_id)
        previous_discovery: list[str] = []
        for capability in ordered:
            tier = _tier_of(capability)
            task = Task(
                capability=capability,
                target=target,
                assessment_id=assessment_id,
                category=tier,
                phase=tier,
                status=TaskStatus.CREATED,
                assigned_agent=f"{tier}-agent",
                scope_ref=self._scope.scope_id,
                roe_ref=self._roe.roe_id,
            )
            # Non-discovery work depends on discovery completing first.
            if tier != "discovery" and previous_discovery:
                task.depends_on = list(previous_discovery)
            if tier == "discovery":
                previous_discovery.append(task.task_id)
            if tier == "active-testing":
                plan.approval_points.append(task.task_id)
            plan.tasks.append(task)
        return plan
