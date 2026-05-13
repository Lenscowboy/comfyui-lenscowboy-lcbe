"""
LCBE HTTP client — shared by both nodes.

Phase 1 ships the skeleton (this file structure, exception types, token loader).
Phase 2 implements the HTTP methods, retry/backoff, and streaming.
"""

from .errors import (
    LCBEClientError,
    LCBEAuthError,
    LCBETokenRevokedError,
    LCBETierDowngradeError,
    LCBESchemaMismatchError,
    LCBENotFoundError,
    LCBENetworkError,
)

__all__ = [
    "LCBEClientError",
    "LCBEAuthError",
    "LCBETokenRevokedError",
    "LCBETierDowngradeError",
    "LCBESchemaMismatchError",
    "LCBENotFoundError",
    "LCBENetworkError",
]
