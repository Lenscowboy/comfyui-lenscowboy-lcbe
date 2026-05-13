"""
LCBE Load Shot node.

Phase 2 (Read path) ships the full implementation per LCBE_COMFY_MASTER_BRIEF §5.1:
- Authenticates with /v1/auth/check on init (5-min cache, red border on 401)
- Project + shot dropdowns lazy-load from /v1/projects and /v1/projects/{id}/shots
- On execute: GET /v1/shots/{id}?include=layout, GET /v1/media/{shot_id}/{kind}
- Validates LCBE_LAYOUT payload against pinned schema, falls back to {} on failure
- Returns (IMAGE, MASK, LCBE_LAYOUT dict, LCBE_METADATA dict)

This file is a Phase 1 skeleton: class registration is real (so ComfyUI loads it
and INPUT_TYPES/RETURN_TYPES are visible in the node browser), but the execute
method raises NotImplementedError. Phase 2 fills in lcbe_client/* and wires it up.
"""


class LCBELoadShotNode:
    """Phase 2 will implement this. See nodes/load_shot.py for the planned shape."""

    CATEGORY = "LensCowboy/LCBE"
    FUNCTION = "execute"
    RETURN_TYPES = ("IMAGE", "MASK", "LCBE_LAYOUT", "LCBE_METADATA")
    RETURN_NAMES = ("image", "mask", "layout", "metadata")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "project": ("STRING", {"default": "", "tooltip": "Project ID (Phase 2: lazy-loaded dropdown)"}),
                "shot": ("STRING", {"default": "", "tooltip": "Shot ID (Phase 2: lazy-loaded dropdown)"}),
                "version": ("STRING", {"default": "latest", "tooltip": "Version label or 'latest'"}),
                "include_layout": ("BOOLEAN", {"default": True}),
            },
        }

    def execute(self, project: str, shot: str, version: str, include_layout: bool):
        raise NotImplementedError(
            "LCBE Load Shot is a Phase 1 skeleton — full implementation lands in Phase 2 "
            "of the LCBE ComfyUI integration."
        )
