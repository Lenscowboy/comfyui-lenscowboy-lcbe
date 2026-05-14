"""
LCBE Save node.

Phase 3 (Write path) ships the full implementation per LCBE_COMFY_MASTER_BRIEF §5.2:
- Streams IMAGE (PNG or mp4) to POST /v1/shots/{id}/versions (parent present) or
  POST /v1/shots (parent absent → new shot).
- Captures workflow JSON from ComfyUI's /history/{prompt_id} introspection.
- Surfaces server error responses inline in node UI.

This file is a Phase 1 skeleton: class registration is real (so the socket signatures
appear in the node browser), but execute() raises NotImplementedError. Phase 3 fills
in the multipart streaming + workflow capture wiring.
"""


class LCBESaveNode:
    """Phase 3 will implement this. See nodes/save.py for the planned shape."""

    CATEGORY = "Lenscowboy/LCBE"
    FUNCTION = "execute"
    OUTPUT_NODE = True
    RETURN_TYPES = ("LCBE_METADATA", "STRING")
    RETURN_NAMES = ("metadata", "confirmation")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {
                "parent_shot_ref": ("LCBE_METADATA",),
                "project": ("STRING", {"default": "", "tooltip": "Required if no parent_shot_ref"}),
                "shot_name": ("STRING", {"default": "", "tooltip": "Required if no parent_shot_ref"}),
                "notes": ("STRING", {"default": "", "multiline": True}),
                "vendor_metadata": ("STRING", {"default": "{}", "multiline": True, "tooltip": "Optional JSON; augments server-generated tags"}),
                "layout": ("LCBE_LAYOUT",),
            },
        }

    def execute(self, image, parent_shot_ref=None, project: str = "", shot_name: str = "",
                notes: str = "", vendor_metadata: str = "{}", layout=None):
        raise NotImplementedError(
            "LCBE Save is a Phase 1 skeleton — full implementation lands in Phase 3 "
            "of the LCBE ComfyUI integration."
        )
