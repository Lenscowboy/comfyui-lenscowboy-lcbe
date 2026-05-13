/**
 * LCBE Node for ComfyUI — frontend extension.
 *
 * Phase 1 (this file): registers visual colours for the custom socket types
 * so LCBE_LAYOUT / LCBE_METADATA / LCBE_SHOT_REF connections are visually
 * distinct on the Comfy canvas.
 *
 * Phase 2+ will extend this with: token-status badge on Load Shot, lazy-loaded
 * project/shot dropdowns, schema-mismatch warning UI, save confirmation toast.
 */

import { app } from "../../scripts/app.js";

const EXT_NAME = "LensCowboy.LCBE";

const SOCKET_COLOURS = {
  LCBE_LAYOUT:   "#8b5cf6",   // purple — spatial scene data
  LCBE_METADATA: "#3b82f6",   // blue   — shot/version metadata
  LCBE_SHOT_REF: "#10b981",   // green  — references back into LCBE
};

app.registerExtension({
  name: EXT_NAME,
  init() {
    // LiteGraph reads link_type_colors when drawing connections.
    if (typeof LiteGraph !== "undefined" && LiteGraph.LGraphCanvas) {
      const canvas = LiteGraph.LGraphCanvas;
      canvas.link_type_colors = canvas.link_type_colors || {};
      for (const [type, colour] of Object.entries(SOCKET_COLOURS)) {
        canvas.link_type_colors[type] = colour;
      }
    }
  },
});
