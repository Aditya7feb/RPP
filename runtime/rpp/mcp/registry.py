"""Capability-to-tool registry.

Maps a canonical capability identifier (for example ``discovery.port-discovery``)
to a concrete MCP tool invocation. This is the only place that knows which MCP
tool implements a capability, keeping tool selection out of the capability
agents and the orchestrator.

Bindings are representative defaults and may be extended or overridden. No
target is ever hard-coded; the target is supplied by the task at resolution
time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from ..schemas import Target


@dataclass
class Invocation:
    """A resolved, ready-to-execute MCP tool call."""

    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)
    intrusive: bool = False


ArgBuilder = Callable[[Target, dict[str, Any]], dict[str, Any]]


@dataclass
class ToolBinding:
    tool: str
    build_args: ArgBuilder
    intrusive: bool = False


def _target_arg(target: Target, _inputs: dict[str, Any]) -> dict[str, Any]:
    return {"target": target.value}


class CapabilityRegistry:
    """Resolves capabilities to MCP invocations."""

    def __init__(self) -> None:
        self._bindings: dict[str, ToolBinding] = {}
        self._install_defaults()

    def register(self, capability: str, binding: ToolBinding) -> None:
        self._bindings[capability] = binding

    def has(self, capability: str) -> bool:
        return capability in self._bindings

    def resolve(self, capability: str, target: Target,
                inputs: dict[str, Any] | None = None) -> Invocation:
        binding = self._bindings.get(capability)
        if binding is None:
            from ..errors import ToolNotFound

            raise ToolNotFound(f"no MCP tool bound to capability '{capability}'")
        arguments = binding.build_args(target, inputs or {})
        return Invocation(tool=binding.tool, arguments=arguments,
                          intrusive=binding.intrusive)

    def capabilities(self) -> list[str]:
        return sorted(self._bindings)

    # -- default bindings --------------------------------------------------

    def _install_defaults(self) -> None:
        # Discovery tier (non-intrusive enumeration).
        self.register("discovery.port-discovery",
                      ToolBinding("nmap", _target_arg))
        self.register("discovery.subdomain-discovery",
                      ToolBinding("subfinder", _target_arg))
        self.register("discovery.fingerprinting",
                      ToolBinding("whatweb", _target_arg))
        self.register("discovery.api-discovery",
                      ToolBinding("httpx", _target_arg))
        self.register("discovery.content-discovery",
                      ToolBinding("httpx", _target_arg))

        # Web security tier (non-intrusive analysis; validation is gated).
        self.register("web-security.security-headers",
                      ToolBinding("httpx", _target_arg))

        # Active testing tier (intrusive; requires approval before dispatch).
        self.register("active-testing.injection-validation",
                      ToolBinding("nuclei", _target_arg, intrusive=True))
        self.register("active-testing.fuzzing",
                      ToolBinding("ffuf", _target_arg, intrusive=True))
