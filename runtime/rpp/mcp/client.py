"""MCP client and execution result.

The :class:`MCPClient` wraps a transport and provides the four responsibilities
of the integration layer's execution half:

* discover available MCP tools
* query tool capabilities
* invoke tools
* capture stdout / stderr / exit status

All failures are normalised into :class:`~rpp.errors.RPPError` subclasses so
callers never see raw transport exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..errors import RPPError, ToolExecutionError
from ..schemas import utc_now
from .transport import ToolDescriptor, ToolResult, Transport


@dataclass
class ExecutionResult:
    """Normalised outcome of a single MCP tool invocation."""

    tool: str
    arguments: dict[str, Any]
    executed_command: str = ""
    stdout: str = ""
    stderr: str = ""
    exit_status: int | None = None
    started_at: str = ""
    completed_at: str = ""
    duration: float = 0.0
    is_error: bool = False
    dry_run: bool = False
    raw: dict[str, Any] = field(default_factory=dict)
    error: dict[str, Any] | None = None

    @property
    def succeeded(self) -> bool:
        return not self.is_error and self.error is None


class MCPClient:
    """A thin, normalised client over an MCP transport."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport
        self._initialized = False
        self._tools: dict[str, ToolDescriptor] | None = None

    def connect(self) -> None:
        if not self._initialized:
            self._transport.initialize()
            self._initialized = True

    def discover_tools(self, *, refresh: bool = False) -> list[ToolDescriptor]:
        self.connect()
        if self._tools is None or refresh:
            self._tools = {t.name: t for t in self._transport.list_tools()}
        return list(self._tools.values())

    def query_capability(self, tool: str) -> ToolDescriptor | None:
        self.discover_tools()
        assert self._tools is not None
        return self._tools.get(tool)

    def invoke(self, tool: str, arguments: dict[str, Any]) -> ExecutionResult:
        """Invoke a tool and capture its output as an :class:`ExecutionResult`."""
        self.connect()
        started = utc_now()
        import time

        clock = time.monotonic()
        try:
            result = self._transport.call_tool(tool, arguments)
        except RPPError as exc:
            completed = utc_now()
            return ExecutionResult(
                tool=tool,
                arguments=arguments,
                started_at=started,
                completed_at=completed,
                duration=time.monotonic() - clock,
                is_error=True,
                error=exc.to_dict(),
            )
        completed = utc_now()
        return self._normalise(tool, arguments, result, started, completed,
                               time.monotonic() - clock)

    def close(self) -> None:
        self._transport.close()
        self._initialized = False

    # -- normalisation -----------------------------------------------------

    @staticmethod
    def _normalise(tool: str, arguments: dict[str, Any], result: ToolResult,
                   started: str, completed: str, duration: float) -> ExecutionResult:
        """Best-effort extraction of command / stdout / stderr / exit code.

        Kali MCP tools commonly return structured content with these fields;
        when absent, the text content is treated as stdout.
        """
        structured = result.structured or {}
        stdout = str(structured.get("stdout", "") or "")
        stderr = str(structured.get("stderr", "") or "")
        command = str(structured.get("command", "") or "")
        exit_status = structured.get("exit_code", structured.get("exit_status"))
        if not stdout and not command:
            stdout = result.content_text
        if not command:
            command = f"{tool} {arguments}"
        try:
            exit_int = int(exit_status) if exit_status is not None else None
        except (TypeError, ValueError):
            exit_int = None
        return ExecutionResult(
            tool=tool,
            arguments=arguments,
            executed_command=command,
            stdout=stdout,
            stderr=stderr,
            exit_status=exit_int,
            started_at=started,
            completed_at=completed,
            duration=duration,
            is_error=result.is_error,
            raw=result.raw,
            error=({"category": ToolExecutionError.category.value,
                    "message": "tool reported an error"} if result.is_error else None),
        )
