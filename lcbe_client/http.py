"""
Shared HTTP client for the LCBE Comfy node.

Phase 1 ships only the skeleton — class structure, retry policy constants,
and the dataclass for endpoint responses. Phase 2 implements:

- GET  /v1/auth/check
- GET  /v1/projects
- GET  /v1/projects/{id}/shots
- GET  /v1/projects/{id}/characters
- GET  /v1/shots/{id}            (?include=media,layout)
- GET  /v1/shots/{id}/layout
- GET  /v1/media/{shot_id}/{kind}             (streaming)
- GET  /v1/media/asset/{asset_id}/{format}    (streaming)

Phase 3 adds:

- POST /v1/shots/{id}/versions   (multipart streaming)
- POST /v1/shots                 (multipart streaming)
- POST /v1/media/asset           (streaming, used by PAL Phase 3.5)
- PATCH /v1/shots/{id}/status

Retry policy per master brief §5.1: 3 retries, exponential backoff, 30s total cap.
"""

from __future__ import annotations

from dataclasses import dataclass

from .auth import TokenConfig

DEFAULT_RETRIES = 3
DEFAULT_BACKOFF_BASE_SECONDS = 0.5
DEFAULT_TOTAL_TIMEOUT_SECONDS = 30.0
USER_AGENT = "comfyui-lenscowboy-lcbe/0.1.0"


@dataclass
class LCBEHttpClient:
    """
    Configured HTTP client bound to a single tenant token.

    Phase 1: skeleton only — instantiating works, but every method raises
    NotImplementedError. Phase 2 wires in `requests` + retry/backoff.
    """

    config: TokenConfig
    retries: int = DEFAULT_RETRIES
    backoff_base: float = DEFAULT_BACKOFF_BASE_SECONDS
    total_timeout: float = DEFAULT_TOTAL_TIMEOUT_SECONDS

    # Phase 2 entry points — all currently placeholders.

    def auth_check(self) -> dict:
        raise NotImplementedError("Phase 2")

    def list_projects(self) -> list[dict]:
        raise NotImplementedError("Phase 2")

    def list_shots(self, project_id: str, **filters) -> dict:
        raise NotImplementedError("Phase 2")

    def list_characters(self, project_id: str) -> list[dict]:
        raise NotImplementedError("Phase 2")

    def get_shot(self, shot_id: str, include: tuple[str, ...] = ()) -> dict:
        raise NotImplementedError("Phase 2")

    def get_layout(self, shot_id: str) -> dict | None:
        raise NotImplementedError("Phase 2")

    def stream_media(self, shot_id: str, kind: str = "latest"):
        raise NotImplementedError("Phase 2")

    def stream_asset(self, asset_id: str, format: str = "glb"):
        raise NotImplementedError("Phase 2")

    # Phase 3 entry points.

    def submit_version(self, shot_id: str, media_stream, *, notes: str = "",
                       vendor_metadata: dict | None = None,
                       workflow_json: dict | None = None,
                       parent_version_id: str | None = None) -> dict:
        raise NotImplementedError("Phase 3")

    def submit_shot(self, project_id: str, name: str, media_stream, *,
                    notes: str = "", vendor_metadata: dict | None = None,
                    workflow_json: dict | None = None) -> dict:
        raise NotImplementedError("Phase 3")

    def upload_asset(self, asset_stream, format: str = "glb") -> dict:
        raise NotImplementedError("Phase 3")

    def patch_status(self, shot_id: str, *, status: str | None = None,
                     notes: str | None = None, tags: list[str] | None = None) -> dict:
        raise NotImplementedError("Phase 3")
