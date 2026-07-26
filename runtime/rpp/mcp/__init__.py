"""MCP integration layer: the single seam between RPP and the Kali MCP server."""

from .client import ExecutionResult, MCPClient
from .integration import MCPIntegration
from .registry import CapabilityRegistry, Invocation, ToolBinding
from .transport import (
    MockTransport,
    StreamableHttpTransport,
    ToolDescriptor,
    Transport,
    build_transport,
)

__all__ = [
    "MCPIntegration",
    "MCPClient",
    "ExecutionResult",
    "CapabilityRegistry",
    "Invocation",
    "ToolBinding",
    "Transport",
    "MockTransport",
    "StreamableHttpTransport",
    "ToolDescriptor",
    "build_transport",
]
