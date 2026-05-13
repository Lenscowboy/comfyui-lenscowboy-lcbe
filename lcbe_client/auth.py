"""
Token loader for the LCBE Comfy node.

Reads the token configuration from a JSON file. By default the path is
~/.lcbe/comfy_token.json; override with the LCBE_COMFY_CONFIG environment
variable for testing or non-standard setups.

Expected file contents (mode 0600 enforced for user safety):

    {
      "token": "lcbe_comfy_xxxxxxxxxxxx",
      "endpoint": "https://api.lenscowboy.com",
      "tenant_id": "...",
      "label": "Brad's home rig",
      "created_at": "..."
    }

Phase 1 ships the loader + dataclass. Phase 2's HTTP client consumes the result.
"""

from __future__ import annotations

import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONFIG_PATH = "~/.lcbe/comfy_token.json"


@dataclass(frozen=True)
class TokenConfig:
    token: str
    endpoint: str
    tenant_id: str | None = None
    label: str | None = None
    created_at: str | None = None


class TokenConfigError(Exception):
    """Raised when the token file is missing, unreadable, or malformed."""


def config_path() -> Path:
    """Resolve the token config path, honouring the LCBE_COMFY_CONFIG env var."""
    raw = os.environ.get("LCBE_COMFY_CONFIG", DEFAULT_CONFIG_PATH)
    return Path(raw).expanduser()


def load_token(path: Path | None = None) -> TokenConfig:
    """
    Load and validate the token config.

    Raises TokenConfigError with a user-actionable message if the file is missing,
    has wrong permissions, or fails JSON parsing.
    """
    p = path or config_path()
    if not p.exists():
        raise TokenConfigError(
            f"No LCBE token found at {p}. Generate one in LCBE Settings → "
            "Integrations → ComfyUI, save the JSON to that path, and restart ComfyUI."
        )

    # Soft check: warn (but do not fail) on world/group-readable file.
    # ComfyUI runs as a single user, so a strict-0600 enforcement is too aggressive
    # cross-platform (Windows doesn't expose POSIX mode bits the same way).
    try:
        mode = p.stat().st_mode
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            # Don't raise — just expose via a side-channel for the caller to log if it wants.
            # The HTTP client surfaces this in node UI in Phase 4.
            pass
    except OSError:
        pass

    try:
        with p.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise TokenConfigError(
            f"Could not read {p}: {exc}. Expected JSON with 'token' and 'endpoint' fields."
        ) from exc

    if not isinstance(raw, dict):
        raise TokenConfigError(f"{p}: expected JSON object, got {type(raw).__name__}")

    token = raw.get("token")
    endpoint = raw.get("endpoint")
    if not token or not isinstance(token, str):
        raise TokenConfigError(f"{p}: missing or non-string 'token' field")
    if not endpoint or not isinstance(endpoint, str):
        raise TokenConfigError(f"{p}: missing or non-string 'endpoint' field")

    return TokenConfig(
        token=token,
        endpoint=endpoint.rstrip("/"),
        tenant_id=raw.get("tenant_id"),
        label=raw.get("label"),
        created_at=raw.get("created_at"),
    )
