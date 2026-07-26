"""Execution state and the assessment store.

The store is the single, authoritative record of orchestration progress and the
canonical objects produced during a run. Findings, Evidence, and Observations
are held here by identifier so the Reporting tier can consume them by reference.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..schemas import AgentResponse, Evidence, Finding, Observation, Task


@dataclass
class ExecutionState:
    """Canonical execution-state summary (see schemas/execution-state.md)."""

    assessment_id: str
    phase: str = "NEW"
    tasks_total: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_waiting_approval: int = 0
    coverage_gaps: list[str] = field(default_factory=list)


class AssessmentStore:
    """In-memory store of everything produced during one assessment."""

    def __init__(self, assessment_id: str) -> None:
        self.assessment_id = assessment_id
        self.state = ExecutionState(assessment_id=assessment_id)
        self.tasks: list[Task] = []
        self.responses: list[AgentResponse] = []
        self.evidence: dict[str, Evidence] = {}
        self.observations: dict[str, Observation] = {}
        self.findings: dict[str, Finding] = {}

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.state.tasks_total = len(self.tasks)

    def add_response(self, response: AgentResponse) -> None:
        self.responses.append(response)

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence[evidence.evidence_id] = evidence

    def add_observation(self, observation: Observation) -> None:
        self.observations[observation.observation_id] = observation

    def add_finding(self, finding: Finding) -> None:
        self.findings[finding.finding_id] = finding

    def finding_ids(self) -> list[str]:
        return list(self.findings)

    def evidence_ids(self) -> list[str]:
        return list(self.evidence)
