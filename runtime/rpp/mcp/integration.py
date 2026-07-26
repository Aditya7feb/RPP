"""MCP integration layer (Phase A boundary).

This is the single seam between the RPP platform and the Kali MCP server. It
exposes tool execution through the canonical ``task -> agent-response`` workflow
and hides every MCP implementation detail from the rest of the repository.

Responsibilities:

* discover available MCP tools
* query capabilities
* resolve a canonical capability to a concrete tool invocation
* invoke tools (with retry) and capture stdout / stderr / exit status
* normalise errors
* honour dry-run mode (plan an invocation without executing anything)
"""

from __future__ import annotations

import time
from typing import Any

from ..config import RuntimeConfig
from ..errors import RPPError, ErrorCategory, RETRYABLE
from ..schemas import Target, utc_now
from .client import ExecutionResult, MCPClient
from .registry import CapabilityRegistry, Invocation
from .transport import ToolDescriptor, build_transport


class MCPIntegration:
    """Facade over transport, client and capability registry."""

    def __init__(self, config: RuntimeConfig, *, assessment_id: str,
                 registry: CapabilityRegistry | None = None) -> None:
        self._config = config
        self._assessment_id = assessment_id
        self._registry = registry or CapabilityRegistry()
        self._client = MCPClient(
            build_transport(config, assessment_id=assessment_id)
        )

    @property
    def registry(self) -> CapabilityRegistry:
        return self._registry

    @property
    def dry_run(self) -> bool:
        return self._config.dry_run

    # -- discovery ---------------------------------------------------------

    def discover(self) -> list[ToolDescriptor]:
        """Discover available MCP tools."""
        return self._client.discover_tools()

    def query(self, tool: str) -> ToolDescriptor | None:
        """Query a single tool's advertised capability."""
        return self._client.query_capability(tool)

    # -- resolution --------------------------------------------------------

    def resolve(self, capability: str, target: Target,
                inputs: dict[str, Any] | None = None) -> Invocation:
        """Resolve a canonical capability to a concrete MCP invocation."""
        return self._registry.resolve(capability, target, inputs)

    # -- execution ---------------------------------------------------------

    def execute(self, invocation: Invocation) -> ExecutionResult:
        """Execute a resolved invocation, honouring dry-run and retry policy."""
        if self._config.dry_run:
            return self._dry_run_result(invocation)
        return self._execute_with_retry(invocation)

    def _dry_run_result(self, invocation: Invocation) -> ExecutionResult:
        now = utc_now()
        return ExecutionResult(
            tool=invocation.tool,
            arguments=invocation.arguments,
            executed_command=f"{invocation.tool} {invocation.arguments}",
            stdout="",
            stderr="",
            exit_status=None,
            started_at=now,
            completed_at=now,
            duration=0.0,
            is_error=False,
            dry_run=True,
            raw={"dry_run": True},
        )

    def _execute_with_retry(self, invocation: Invocation) -> ExecutionResult:
        retry = self._config.retry
        delay = retry.backoff_seconds
        last: ExecutionResult | None = None
        for attempt in range(1, retry.max_attempts + 1):
            result = self._client.invoke(invocation.tool, invocation.arguments)
            if result.succeeded:
                return result
            last = result
            category = None
            if result.error:
                try:
                    category = ErrorCategory(result.error.get("category"))
                except ValueError:
                    category = None
            if category not in RETRYABLE or attempt == retry.max_attempts:
                return result
            time.sleep(min(delay, retry.max_backoff_seconds))
            delay *= retry.backoff_multiplier
        assert last is not None
        return last

    def close(self) -> None:
        self._client.close()
