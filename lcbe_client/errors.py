"""
Exception types for the LCBE HTTP client.

Mapped to the error surfaces called out in LCBE_COMFY_MASTER_BRIEF §4.1 Polish:
- Token revoked, project deleted, shot deleted, tier downgrade, schema mismatch,
  Drive quota, network exhaustion.

Phase 4 wires each of these to the user-facing node UI message catalogue.
"""


class LCBEClientError(Exception):
    """Base class for all LCBE client errors."""


class LCBEAuthError(LCBEClientError):
    """Token failed /v1/auth/check. Catch-all for 401 responses."""


class LCBETokenRevokedError(LCBEAuthError):
    """Server reports the token has been revoked. User must reissue."""


class LCBETierDowngradeError(LCBEClientError):
    """Tenant tier no longer supports ComfyUI integration. May include grace_window info."""

    def __init__(self, message: str, grace_window_expires_at: str | None = None):
        super().__init__(message)
        self.grace_window_expires_at = grace_window_expires_at


class LCBESchemaMismatchError(LCBEClientError):
    """LCBE_LAYOUT payload schema_version is not supported by this node."""

    def __init__(self, message: str, server_version: str, client_supports: str):
        super().__init__(message)
        self.server_version = server_version
        self.client_supports = client_supports


class LCBENotFoundError(LCBEClientError):
    """Resource (project, shot, version, asset) not found or no access."""


class LCBENetworkError(LCBEClientError):
    """All retries exhausted; server unreachable."""
