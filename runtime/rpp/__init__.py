"""RPP runtime: the executable integration between the RPP architecture and a
Kali MCP server.

This package is implementation code that conforms to the authoritative,
documentation-first architecture under ``schemas/``, ``skills/`` and ``agents/``.
It does not modify that architecture.
"""

from .config import RuntimeConfig, load_config
from .schemas import RulesOfEngagement, Scope, Target

__all__ = [
    "RuntimeConfig",
    "load_config",
    "Scope",
    "RulesOfEngagement",
    "Target",
    "__version__",
]

__version__ = "0.1.0"
