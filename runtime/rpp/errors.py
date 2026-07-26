"""Normalized error model for the RPP runtime.

The MCP integration layer translates every low-level transport, protocol, or
tool failure into one of these canonical categories so that the rest of the
platform never sees MCP implementation details. Categories mirror the
orchestration error categories documented in
``agents/master/error-model.md``.
"""

from __future__ import annotations

from enum import Enum


class ErrorCategory(str, Enum):
    INPUT_INVALID = "input-invalid"
    DELEGATION_TIMEOUT = "delegation-timeout"
    AGENT_UNAVAILABLE = "agent-unavailable"
    AGENT_FAILURE = "agent-failure"
    AGENT_REJECTED = "agent-rejected"
    DEPENDENCY_UNMET = "dependency-unmet"
    SCOPE_VIOLATION = "scope-violation"
    APPROVAL_DENIED = "approval-denied"
    RESOURCE_EXHAUSTED = "resource-exhausted"
    # MCP-transport specific, normalised into orchestration semantics.
    MCP_UNAVAILABLE = "mcp-unavailable"
    MCP_PROTOCOL_ERROR = "mcp-protocol-error"
    TOOL_NOT_FOUND = "tool-not-found"
    TOOL_EXECUTION_ERROR = "tool-execution-error"


# Categories that MAY be retried per the orchestration retry policy.
RETRYABLE = {
    ErrorCategory.DELEGATION_TIMEOUT,
    ErrorCategory.AGENT_FAILURE,
    ErrorCategory.RESOURCE_EXHAUSTED,
    ErrorCategory.MCP_UNAVAILABLE,
}

# Categories that SHALL never be retried.
NON_RETRYABLE = {
    ErrorCategory.SCOPE_VIOLATION,
    ErrorCategory.APPROVAL_DENIED,
    ErrorCategory.AGENT_REJECTED,
    ErrorCategory.INPUT_INVALID,
    ErrorCategory.TOOL_NOT_FOUND,
}


class RPPError(Exception):
    """Base class for all normalized runtime errors."""

    category: ErrorCategory = ErrorCategory.AGENT_FAILURE

    def __init__(self, message: str, *, category: ErrorCategory | None = None,
                 detail: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        if category is not None:
            self.category = category
        self.detail = detail

    @property
    def retryable(self) -> bool:
        return self.category in RETRYABLE

    def to_dict(self) -> dict[str, str | bool | None]:
        return {
            "category": self.category.value,
            "message": self.message,
            "detail": self.detail,
            "retryable": self.retryable,
        }


class ConfigError(RPPError):
    category = ErrorCategory.INPUT_INVALID


class ScopeViolation(RPPError):
    category = ErrorCategory.SCOPE_VIOLATION


class ApprovalDenied(RPPError):
    category = ErrorCategory.APPROVAL_DENIED


class MCPUnavailable(RPPError):
    category = ErrorCategory.MCP_UNAVAILABLE


class MCPProtocolError(RPPError):
    category = ErrorCategory.MCP_PROTOCOL_ERROR


class ToolNotFound(RPPError):
    category = ErrorCategory.TOOL_NOT_FOUND


class ToolExecutionError(RPPError):
    category = ErrorCategory.TOOL_EXECUTION_ERROR
