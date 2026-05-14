"""
LCBE Node for ComfyUI — Lenscowboy backend integration.

Two nodes:
- LCBE Load Shot — pulls shot media, PAL layout, character refs from LCBE.
- LCBE Save — pushes Comfy outputs back to LCBE as new versions or new shots,
              with full workflow provenance (LSV tier) or hash + vendor tag (Studio).

Custom typed sockets (all registered as Python `dict` on the node side; socket
colours are registered in web/lcbe.js):
- LCBE_LAYOUT   — spatial scene data conforming to lcbe-layout-schema v1.0
- LCBE_METADATA — shot/version metadata dict (shot ID, version ID, characters, tags)
- LCBE_SHOT_REF — reference to a saved LCBE shot, used for round-trip chaining
"""

from .nodes.load_shot import LCBELoadShotNode
from .nodes.save import LCBESaveNode

NODE_CLASS_MAPPINGS = {
    "LCBELoadShotNode": LCBELoadShotNode,
    "LCBESaveNode": LCBESaveNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LCBELoadShotNode": "LCBE Load Shot (Lenscowboy)",
    "LCBESaveNode": "LCBE Save (Lenscowboy)",
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
