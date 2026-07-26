"""Canonical data models for the RPP runtime.

These dataclasses are executable representations of the canonical schemas defined
under ``schemas/`` in the repository. Field names conform to the canonical
schema documents (``task.md``, ``agent-response.md``, ``evidence.md``,
``observation.md``, ``finding.md``). The runtime never invents new canonical
objects; it only serialises the existing ones.

Only the fields required by the first executable integration are modelled. Every
object accepts and preserves unknown optional fields via ``extra`` for forward
compatibility, mirroring the schema rule that unknown optional fields SHALL be
ignored (here: retained) by consumers.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def new_id(prefix: str) -> str:
    """Return a globally unique, human-readable identifier."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Enumerations (values conform to the canonical schema documents)
# ---------------------------------------------------------------------------


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class ResponseStatus(str, Enum):
    SUCCESS = "Success"
    PARTIAL_SUCCESS = "Partial Success"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    SKIPPED = "Skipped"
    WAITING_FOR_APPROVAL = "Waiting For Approval"


class ApprovalState(str, Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


# ---------------------------------------------------------------------------
# Target / Scope / Rules of Engagement
# ---------------------------------------------------------------------------


@dataclass
class Target:
    """A single in-scope target. Never hard-coded; always user-supplied."""

    value: str
    type: str = "host"  # host | ip | url | api | cloud-resource | domain
    scope: str | None = None


@dataclass
class Scope:
    """Canonical scope object (see schemas/scope.md)."""

    scope_id: str = field(default_factory=lambda: new_id("scope"))
    included_targets: list[str] = field(default_factory=list)
    excluded_targets: list[str] = field(default_factory=list)
    schema_version: str = "1.0.0"


@dataclass
class RulesOfEngagement:
    """Canonical rules-of-engagement object (see schemas/rules-of-engagement.md)."""

    roe_id: str = field(default_factory=lambda: new_id("roe"))
    allowed_hosts: list[str] = field(default_factory=list)
    allowed_ports: list[int] = field(default_factory=list)
    allowed_protocols: list[str] = field(default_factory=lambda: ["http", "https"])
    excluded_paths: list[str] = field(default_factory=list)
    max_request_rate: int | None = None
    approval_required_capabilities: list[str] = field(default_factory=list)
    schema_version: str = "1.0.0"


# ---------------------------------------------------------------------------
# Task / Agent Response
# ---------------------------------------------------------------------------


@dataclass
class Task:
    """Canonical task object (see schemas/task.md)."""

    capability: str
    target: Target
    assessment_id: str
    task_id: str = field(default_factory=lambda: new_id("task"))
    category: str | None = None
    phase: str | None = None
    priority: str = "Medium"
    status: TaskStatus = TaskStatus.CREATED
    owner: str = "Master Agent"
    assigned_agent: str | None = None
    created_by: str = "Master Agent"
    scope_ref: str | None = None
    roe_ref: str | None = None
    approval_ref: str | None = None
    depends_on: list[str] = field(default_factory=list)
    inputs: dict[str, Any] = field(default_factory=dict)
    schema_version: str = "1.0.0"


@dataclass
class AgentResponse:
    """Canonical agent-response object (see schemas/agent-response.md)."""

    task_id: str
    assessment_id: str
    agent_name: str
    status: ResponseStatus
    response_id: str = field(default_factory=lambda: new_id("resp"))
    execution_id: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration: float | None = None
    summary: str = ""
    description: str = ""
    findings: list[str] = field(default_factory=list)      # finding_id references
    evidence: list[str] = field(default_factory=list)      # evidence_id references
    observations: list[str] = field(default_factory=list)  # observation_id references
    technologies: list[str] = field(default_factory=list)
    recommended_tasks: list[str] = field(default_factory=list)
    recommended_agents: list[str] = field(default_factory=list)
    reason: str = ""
    schema_version: str = "1.0.0"


# ---------------------------------------------------------------------------
# Observation / Evidence / Finding
# ---------------------------------------------------------------------------


@dataclass
class Observation:
    """Canonical observation object (see schemas/observation.md)."""

    assessment_id: str
    task_id: str
    observation_id: str = field(default_factory=lambda: new_id("observation"))
    type: str = "generic"
    summary: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    observed_at: str = field(default_factory=utc_now)
    schema_version: str = "1.0.0"


@dataclass
class Evidence:
    """Canonical evidence object (see schemas/evidence.md).

    Immutable once created. For an MCP tool execution the executed command,
    stdout, stderr, exit status, and execution metadata are captured here.
    """

    assessment_id: str
    task_id: str
    evidence_id: str = field(default_factory=lambda: new_id("evidence"))
    category: str = "tool-execution"
    type: str = "command-output"
    source: str = "kali-mcp"
    collected_by_agent: str | None = None
    collected_by_tool: str | None = None
    target_host: str | None = None
    collected_at: str = field(default_factory=utc_now)
    collection_method: str = "mcp-invocation"
    execution_id: str | None = None
    content_type: str = "application/json"
    preview: str = ""
    # Tool-execution content (canonical execution metadata).
    executed_command: str | None = None
    stdout: str = ""
    stderr: str = ""
    exit_status: int | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration: float | None = None
    hash: str | None = None
    hash_algorithm: str = "SHA-256"
    size: int | None = None
    encoding: str = "utf-8"
    related_observation_refs: list[str] = field(default_factory=list)
    schema_version: str = "1.0.0"


@dataclass
class Finding:
    """Canonical finding object (see schemas/finding.md).

    The runtime references findings; capability logic that confirms
    vulnerabilities is owned by the capability tiers. This model exists so that
    references flow through the Reporting tier.
    """

    assessment_id: str
    title: str
    finding_id: str = field(default_factory=lambda: new_id("finding"))
    severity: str = "Info"
    confidence: str = "LOW"
    cwe: str | None = None
    owasp: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    observation_refs: list[str] = field(default_factory=list)
    schema_version: str = "1.0.0"


def to_dict(obj: Any) -> dict[str, Any]:
    """Serialise a dataclass model to a plain dict (enums to their values)."""

    def _convert(value: Any) -> Any:
        if isinstance(value, Enum):
            return value.value
        return value

    return {k: _convert(v) for k, v in asdict(obj).items()}
