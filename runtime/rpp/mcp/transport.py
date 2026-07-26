"""MCP transports.

A transport speaks the wire protocol to the Kali MCP server. The rest of the
runtime depends only on the :class:`Transport` protocol, never on a concrete
transport, so MCP implementation details never leak upward.

Two transports are provided:

* :class:`MockTransport` -- dependency-free, executes nothing, used for dry runs
  and tests.
* :class:`StreamableHttpTransport` -- a minimal MCP JSON-RPC client over
  Streamable HTTP / SSE, using ``httpx`` when available.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Protocol

from ..config import RuntimeConfig
from ..errors import MCPProtocolError, MCPUnavailable


@dataclass
class ToolDescriptor:
    name: str
    description: str = ""
    input_schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    """Raw result of a single MCP ``tools/call``."""

    content_text: str = ""
    is_error: bool = False
    structured: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


class Transport(Protocol):
    """The wire contract the rest of the runtime depends on."""

    def initialize(self) -> None: ...

    def list_tools(self) -> list[ToolDescriptor]: ...

    def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult: ...

    def close(self) -> None: ...


# ---------------------------------------------------------------------------
# Mock transport (no network, executes nothing)
# ---------------------------------------------------------------------------


class MockTransport:
    """A transport that performs no I/O.

    It advertises a small, representative tool catalogue and returns a
    deterministic "not executed" result. This makes the platform executable and
    testable without contacting any server or running any scan.
    """

    CATALOGUE = [
        ToolDescriptor("nmap", "Network and port scanning"),
        ToolDescriptor("httpx", "HTTP probing and fingerprinting"),
        ToolDescriptor("whatweb", "Web technology fingerprinting"),
        ToolDescriptor("nuclei", "Template-based vulnerability scanning"),
        ToolDescriptor("ffuf", "Content and parameter fuzzing"),
        ToolDescriptor("subfinder", "Passive subdomain discovery"),
    ]

    def __init__(self) -> None:
        self._initialized = False

    def initialize(self) -> None:
        self._initialized = True

    def list_tools(self) -> list[ToolDescriptor]:
        return list(self.CATALOGUE)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        payload = {
            "command": f"{name} {json.dumps(arguments)}",
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "note": "mock transport: no execution performed",
        }
        return ToolResult(
            content_text=payload["note"],
            is_error=False,
            structured=payload,
            raw={"mock": True, "tool": name, "arguments": arguments},
        )

    def close(self) -> None:
        self._initialized = False


# ---------------------------------------------------------------------------
# Streamable HTTP transport (minimal MCP JSON-RPC client)
# ---------------------------------------------------------------------------


class StreamableHttpTransport:
    """Minimal MCP JSON-RPC 2.0 client over Streamable HTTP / SSE.

    This transport is intentionally small and dependency-guarded. It performs
    the MCP handshake (``initialize``), tool discovery (``tools/list``) and tool
    invocation (``tools/call``). Full validation happens against a live server;
    until then the transport is importable without ``httpx`` installed.
    """

    PROTOCOL_VERSION = "2025-06-18"

    def __init__(self, config: RuntimeConfig, *, assessment_id: str) -> None:
        self._config = config
        self._assessment_id = assessment_id
        self._session_id: str | None = None
        self._rpc_id = 0
        self._client: Any = None

    # -- lifecycle ---------------------------------------------------------

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            import httpx  # type: ignore
        except ModuleNotFoundError as exc:  # pragma: no cover - env dependent
            raise MCPUnavailable(
                "httpx is required for the Streamable HTTP transport",
                detail="install with: pip install httpx",
            ) from exc
        if not self._config.mcp.endpoint:
            raise MCPUnavailable("no MCP endpoint configured")
        self._client = httpx.Client(
            timeout=self._config.mcp.timeout_seconds,
            verify=self._config.mcp.verify_tls,
        )
        return self._client

    def initialize(self) -> None:
        result = self._request(
            "initialize",
            {
                "protocolVersion": self.PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "rpp-runtime", "version": "0.1.0"},
            },
            expect_session=True,
        )
        if "protocolVersion" not in result:
            raise MCPProtocolError("MCP initialize returned no protocolVersion")
        # Notify the server the client is initialized (best-effort).
        try:
            self._notify("notifications/initialized", {})
        except MCPProtocolError:
            pass

    def list_tools(self) -> list[ToolDescriptor]:
        result = self._request("tools/list", {})
        tools = []
        for item in result.get("tools", []):
            tools.append(
                ToolDescriptor(
                    name=item.get("name", ""),
                    description=item.get("description", ""),
                    input_schema=item.get("inputSchema", {}) or {},
                )
            )
        return tools

    def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        result = self._request(
            "tools/call", {"name": name, "arguments": arguments}
        )
        content = result.get("content", [])
        text_parts = [c.get("text", "") for c in content if c.get("type") == "text"]
        structured = result.get("structuredContent", {}) or {}
        return ToolResult(
            content_text="\n".join(text_parts),
            is_error=bool(result.get("isError", False)),
            structured=structured,
            raw=result,
        )

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    # -- JSON-RPC plumbing -------------------------------------------------

    def _next_id(self) -> int:
        self._rpc_id += 1
        return self._rpc_id

    def _headers(self) -> dict[str, str]:
        import uuid

        headers = self._config.outbound_headers(
            request_id=str(uuid.uuid4()),
            assessment_id=self._assessment_id,
            trace_id=str(uuid.uuid4()),
        )
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json, text/event-stream"
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id
        return headers

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        client = self._ensure_client()
        body = {"jsonrpc": "2.0", "method": method, "params": params}
        try:
            client.post(self._config.mcp.endpoint, json=body, headers=self._headers())
        except Exception as exc:  # pragma: no cover - network dependent
            raise MCPProtocolError("MCP notification failed", detail=str(exc)) from exc

    def _request(self, method: str, params: dict[str, Any], *,
                 expect_session: bool = False) -> dict[str, Any]:
        client = self._ensure_client()
        body = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params,
        }
        try:
            response = client.post(
                self._config.mcp.endpoint, json=body, headers=self._headers()
            )
        except Exception as exc:  # pragma: no cover - network dependent
            raise MCPUnavailable("MCP request failed", detail=str(exc)) from exc

        if expect_session:
            session = response.headers.get("Mcp-Session-Id")
            if session:
                self._session_id = session

        message = self._decode(response)
        if "error" in message:
            err = message["error"]
            raise MCPProtocolError(
                f"MCP error {err.get('code')}: {err.get('message')}",
                detail=json.dumps(err),
            )
        return message.get("result", {})

    @staticmethod
    def _decode(response: Any) -> dict[str, Any]:
        content_type = response.headers.get("Content-Type", "")
        text = response.text
        if "text/event-stream" in content_type:
            # Take the last complete ``data:`` JSON payload from the SSE stream.
            payload = None
            for line in text.splitlines():
                if line.startswith("data:"):
                    payload = line[len("data:"):].strip()
            if payload is None:
                raise MCPProtocolError("empty SSE response from MCP server")
            return json.loads(payload)
        try:
            return response.json()
        except Exception as exc:
            raise MCPProtocolError("invalid JSON from MCP server", detail=text[:200]) from exc


def build_transport(config: RuntimeConfig, *, assessment_id: str) -> Transport:
    """Construct the transport selected by configuration."""
    if config.dry_run:
        return MockTransport()
    transport = config.mcp.transport
    if transport in ("streamable-http", "sse", "http"):
        return StreamableHttpTransport(config, assessment_id=assessment_id)
    raise MCPUnavailable(f"unsupported MCP transport: {transport}")
