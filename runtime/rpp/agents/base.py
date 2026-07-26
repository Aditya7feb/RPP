"""Specialist tier agents (Phase B).

A specialist tier agent fronts one canonical capability tier. It accepts a Task,
invokes the MCP integration layer when tool execution is required, and returns a
canonical AgentResponse. Agents never execute shell commands directly; all tool
execution flows through the MCP integration layer.
"""

from __future__ import annotations

from ..evidence.collector import EvidenceCollector
from ..mcp.integration import MCPIntegration
from ..orchestration.state import AssessmentStore
from ..schemas import AgentResponse, ResponseStatus, Task, utc_now


class SpecialistTierAgent:
    """Base class for the eight capability-tier agents."""

    tier: str = "generic"

    def __init__(self, integration: MCPIntegration, collector: EvidenceCollector,
                 store: AssessmentStore) -> None:
        self._integration = integration
        self._collector = collector
        self._store = store

    @property
    def name(self) -> str:
        return f"{self.tier}-agent"

    def execute(self, task: Task) -> AgentResponse:
        started = utc_now()
        response = AgentResponse(
            task_id=task.task_id,
            assessment_id=task.assessment_id,
            agent_name=self.name,
            status=ResponseStatus.SKIPPED,
            started_at=started,
        )

        # Resolve the capability to a concrete MCP invocation.
        try:
            invocation = self._integration.resolve(task.capability, task.target,
                                                    task.inputs)
        except Exception as exc:  # normalised RPPError
            return self._fail(response, str(exc))

        # Defense-in-depth: an intrusive invocation must arrive already approved.
        if invocation.intrusive and not task.approval_ref:
            response.status = ResponseStatus.WAITING_FOR_APPROVAL
            response.summary = f"{task.capability} requires approval before execution"
            response.completed_at = utc_now()
            self._store.add_response(response)
            return response

        # Execute through the MCP layer (never a direct shell call).
        result = self._integration.execute(invocation)

        # Every execution flows through the single Evidence path.
        evidence, observation = self._collector.from_execution(task, result, self.name)
        self._store.add_evidence(evidence)
        self._store.add_observation(observation)

        response.evidence.append(evidence.evidence_id)
        response.observations.append(observation.observation_id)
        response.execution_id = evidence.execution_id
        response.completed_at = utc_now()
        response.duration = result.duration

        if result.dry_run:
            response.status = ResponseStatus.SKIPPED
            response.summary = f"dry-run: planned {result.tool} for {task.capability}"
        elif result.succeeded:
            response.status = ResponseStatus.SUCCESS
            response.summary = f"executed {result.tool} for {task.capability}"
        else:
            response.status = ResponseStatus.FAILED
            response.summary = f"{result.tool} failed for {task.capability}"
            response.reason = (result.error or {}).get("message", "execution error")

        self._store.add_response(response)
        return response

    def _fail(self, response: AgentResponse, reason: str) -> AgentResponse:
        response.status = ResponseStatus.FAILED
        response.reason = reason
        response.completed_at = utc_now()
        self._store.add_response(response)
        return response


class DiscoveryAgent(SpecialistTierAgent):
    tier = "discovery"


class AuthenticationAgent(SpecialistTierAgent):
    tier = "authentication"


class WebSecurityAgent(SpecialistTierAgent):
    tier = "web-security"


class APISecurityAgent(SpecialistTierAgent):
    tier = "api-security"


class CloudAgent(SpecialistTierAgent):
    tier = "cloud"


class ActiveTestingAgent(SpecialistTierAgent):
    tier = "active-testing"


class EvidenceAgent(SpecialistTierAgent):
    tier = "evidence"


class ReportingAgent(SpecialistTierAgent):
    tier = "reporting"


def build_tier_agents(integration: MCPIntegration, collector: EvidenceCollector,
                      store: AssessmentStore) -> dict[str, SpecialistTierAgent]:
    """Instantiate one specialist agent per canonical capability tier."""
    classes = [
        DiscoveryAgent, AuthenticationAgent, WebSecurityAgent, APISecurityAgent,
        CloudAgent, ActiveTestingAgent, EvidenceAgent, ReportingAgent,
    ]
    return {cls.tier: cls(integration, collector, store) for cls in classes}
