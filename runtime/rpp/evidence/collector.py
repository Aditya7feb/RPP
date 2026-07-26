"""Evidence tier binding (Phase C).

Every MCP execution flows through this single collector, which produces a
canonical :class:`~rpp.schemas.Evidence` object and a correlated
:class:`~rpp.schemas.Observation`. There is exactly one evidence path in the
runtime; no capability introduces its own.

The Evidence object captures the canonical execution metadata required by the
Evidence schema: executed command, stdout, stderr, exit status, timestamps,
duration, and an integrity hash. Evidence is immutable once created.
"""

from __future__ import annotations

import hashlib

from ..mcp.client import ExecutionResult
from ..schemas import Evidence, Observation, Task


class EvidenceCollector:
    """Builds Evidence and Observations from MCP executions."""

    def __init__(self, assessment_id: str) -> None:
        self._assessment_id = assessment_id

    def from_execution(self, task: Task, result: ExecutionResult,
                       agent_name: str) -> tuple[Evidence, Observation]:
        combined = (result.stdout + result.stderr).encode("utf-8", "replace")
        digest = hashlib.sha256(combined).hexdigest()
        preview = (result.stdout or result.executed_command)[:280]

        evidence = Evidence(
            assessment_id=self._assessment_id,
            task_id=task.task_id,
            category="tool-execution",
            type="command-output",
            source="kali-mcp",
            collected_by_agent=agent_name,
            collected_by_tool=result.tool,
            target_host=task.target.value,
            collection_method="mcp-invocation",
            execution_id=None,
            content_type="application/json",
            preview=preview,
            executed_command=result.executed_command,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_status=result.exit_status,
            started_at=result.started_at,
            completed_at=result.completed_at,
            duration=result.duration,
            hash=digest,
            hash_algorithm="SHA-256",
            size=len(combined),
            encoding="utf-8",
        )

        summary = (
            f"dry-run planned {result.tool}" if result.dry_run
            else f"executed {result.tool} (exit={result.exit_status})"
        )
        observation = Observation(
            assessment_id=self._assessment_id,
            task_id=task.task_id,
            type=f"{task.capability}",
            summary=summary,
            data={
                "tool": result.tool,
                "arguments": result.arguments,
                "dry_run": result.dry_run,
                "exit_status": result.exit_status,
                "error": result.error,
            },
            evidence_refs=[evidence.evidence_id],
        )
        evidence.related_observation_refs.append(observation.observation_id)
        return evidence, observation
