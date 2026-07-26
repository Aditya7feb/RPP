"""Single configuration location for the RPP runtime (Phase E).

This module centralises all runtime configuration:

* MCP endpoint and transport
* authentication (by environment-variable reference, never inline secrets)
* execution timeout
* retry policy
* concurrency
* custom HTTP headers (the ``X-RPP-*`` outbound headers are preserved)

A dependency-free YAML subset loader is included so the platform is executable
with the standard library alone. JSON configuration files are also supported. If
PyYAML is installed it is used automatically for full YAML support.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from .errors import ConfigError

# The custom outbound headers previously defined for the platform
# (see skills/shared/http-client/configuration.md and examples.md). These are
# preserved verbatim and applied to every outbound MCP request.
DEFAULT_CUSTOM_HEADERS: dict[str, str] = {
    "User-Agent": "RPP",
    "X-RPP-Assessment": "",  # populated per-assessment at runtime
    "X-RPP-Trace": "",       # populated per-request at runtime
}
DEFAULT_REQUEST_ID_HEADER = "X-RPP-Request-ID"


@dataclass
class AuthConfig:
    """Authentication for the MCP endpoint.

    Secrets are never stored in the config file. ``token_env`` names an
    environment variable that holds the credential; it is resolved only when a
    connection is opened and is never logged.
    """

    type: str = "none"            # none | bearer | header
    header_name: str = "Authorization"
    token_env: str | None = None
    token_prefix: str = "Bearer "

    def resolve_header(self) -> dict[str, str]:
        if self.type == "none" or not self.token_env:
            return {}
        token = os.environ.get(self.token_env)
        if not token:
            raise ConfigError(
                f"authentication requires environment variable '{self.token_env}' to be set"
            )
        if self.type == "bearer":
            return {"Authorization": f"{self.token_prefix}{token}"}
        return {self.header_name: token}


@dataclass
class RetryConfig:
    max_attempts: int = 3
    backoff_seconds: float = 1.0
    backoff_multiplier: float = 2.0
    max_backoff_seconds: float = 30.0


@dataclass
class ConcurrencyConfig:
    max_parallel_tasks: int = 4


@dataclass
class MCPConfig:
    endpoint: str = ""
    transport: str = "streamable-http"  # streamable-http | sse | stdio
    timeout_seconds: float = 60.0
    verify_tls: bool = True
    auth: AuthConfig = field(default_factory=AuthConfig)


@dataclass
class RuntimeConfig:
    mcp: MCPConfig = field(default_factory=MCPConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    custom_headers: dict[str, str] = field(
        default_factory=lambda: dict(DEFAULT_CUSTOM_HEADERS)
    )
    request_id_header: str = DEFAULT_REQUEST_ID_HEADER
    # When true, the runtime plans and resolves invocations but never contacts
    # the MCP server or executes any tool. Used to make the platform executable
    # without running scans.
    dry_run: bool = True

    def outbound_headers(self, request_id: str, assessment_id: str,
                         trace_id: str) -> dict[str, str]:
        """Return the full set of outbound headers for one MCP request.

        The ``X-RPP-*`` custom headers are always included and populated with the
        current correlation identifiers.
        """
        headers = dict(self.custom_headers)
        headers[self.request_id_header] = request_id
        headers["X-RPP-Assessment"] = assessment_id
        headers["X-RPP-Trace"] = trace_id
        headers.update(self.mcp.auth.resolve_header())
        return headers


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def load_config(path: str) -> RuntimeConfig:
    """Load a :class:`RuntimeConfig` from a YAML or JSON file."""
    if not os.path.exists(path):
        raise ConfigError(f"configuration file not found: {path}")
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    data = _parse_document(text, path)
    if not isinstance(data, dict):
        raise ConfigError("configuration root must be a mapping")
    return _build_config(data)


def _parse_document(text: str, path: str) -> Any:
    if path.endswith(".json"):
        return json.loads(text)
    try:  # Prefer PyYAML when available for full YAML support.
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ModuleNotFoundError:
        return _mini_yaml(text)


def _build_config(data: dict[str, Any]) -> RuntimeConfig:
    cfg = RuntimeConfig()

    mcp = data.get("mcp", {}) or {}
    cfg.mcp.endpoint = str(mcp.get("endpoint", cfg.mcp.endpoint))
    cfg.mcp.transport = str(mcp.get("transport", cfg.mcp.transport))
    cfg.mcp.timeout_seconds = float(mcp.get("timeout_seconds", cfg.mcp.timeout_seconds))
    cfg.mcp.verify_tls = bool(mcp.get("verify_tls", cfg.mcp.verify_tls))

    auth = mcp.get("authentication", {}) or {}
    cfg.mcp.auth = AuthConfig(
        type=str(auth.get("type", "none")),
        header_name=str(auth.get("header_name", "Authorization")),
        token_env=(str(auth["token_env"]) if auth.get("token_env") else None),
        token_prefix=str(auth.get("token_prefix", "Bearer ")),
    )

    retry = data.get("retry", {}) or {}
    cfg.retry = RetryConfig(
        max_attempts=int(retry.get("max_attempts", cfg.retry.max_attempts)),
        backoff_seconds=float(retry.get("backoff_seconds", cfg.retry.backoff_seconds)),
        backoff_multiplier=float(
            retry.get("backoff_multiplier", cfg.retry.backoff_multiplier)
        ),
        max_backoff_seconds=float(
            retry.get("max_backoff_seconds", cfg.retry.max_backoff_seconds)
        ),
    )

    concurrency = data.get("concurrency", {}) or {}
    cfg.concurrency = ConcurrencyConfig(
        max_parallel_tasks=int(
            concurrency.get("max_parallel_tasks", cfg.concurrency.max_parallel_tasks)
        )
    )

    headers = data.get("custom_headers", None)
    if isinstance(headers, dict):
        merged = dict(DEFAULT_CUSTOM_HEADERS)
        merged.update({str(k): str(v) for k, v in headers.items()})
        cfg.custom_headers = merged
    cfg.request_id_header = str(data.get("request_id_header", cfg.request_id_header))

    if "dry_run" in data:
        cfg.dry_run = bool(data["dry_run"])
    return cfg


# ---------------------------------------------------------------------------
# Minimal dependency-free YAML subset parser
# ---------------------------------------------------------------------------


def _mini_yaml(text: str) -> Any:
    """Parse the small YAML subset used by the runtime configuration.

    Supported: nested mappings (2-space indentation), scalar values, inline flow
    lists ``[a, b]``, block scalar lists ``- item``, quoted strings, booleans,
    integers, floats and null. This is deliberately minimal; install PyYAML for
    full YAML support.
    """
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        stripped = raw.rstrip()
        if not stripped.strip() or stripped.strip().startswith("#"):
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = _strip_inline_comment(stripped.strip())
        if content:
            lines.append((indent, content))
    value, _ = _parse_block(lines, 0, 0)
    return value


def _strip_inline_comment(value: str) -> str:
    if value.startswith(("'", '"')):
        return value
    idx = value.find(" #")
    return value[:idx].rstrip() if idx != -1 else value


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int):
    if index >= len(lines):
        return {}, index
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_map(lines, index, indent)


def _parse_map(lines: list[tuple[int, str]], index: int, indent: int):
    result: dict[str, Any] = {}
    while index < len(lines):
        cur_indent, content = lines[index]
        if cur_indent < indent:
            break
        if cur_indent > indent:
            raise ConfigError(f"unexpected indentation in configuration: {content!r}")
        if ":" not in content:
            raise ConfigError(f"invalid configuration line: {content!r}")
        key, _, rest = content.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest:
            result[key] = _scalar(rest)
            index += 1
        else:
            child, index = _parse_block(lines, index + 1,
                                        lines[index + 1][0] if index + 1 < len(lines) else indent)
            result[key] = child
    return result, index


def _parse_list(lines: list[tuple[int, str]], index: int, indent: int):
    result: list[Any] = []
    while index < len(lines):
        cur_indent, content = lines[index]
        if cur_indent < indent or not content.startswith("- "):
            break
        result.append(_scalar(content[2:].strip()))
        index += 1
    return result, index


def _scalar(token: str) -> Any:
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part.strip()) for part in inner.split(",")]
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "'\"":
        return token[1:-1]
    low = token.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~", ""):
        return None
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token
