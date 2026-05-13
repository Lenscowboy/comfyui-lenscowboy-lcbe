# LCBE Node for ComfyUI

LCBE pipeline integration for ComfyUI by [LensCowboy](https://lenscowboy.com).

Load LCBE shots (with optional PAL spatial layout) into ComfyUI, render any graph you like, save the result back to LCBE as a new version or new shot — with full workflow provenance.

> **Status:** Phase 1 skeleton. Both nodes register and appear in the Comfy node browser, but execution is gated behind `NotImplementedError` until Phase 2 (Read path) and Phase 3 (Write path) ship.

## Nodes

- **LCBE Load Shot** — pulls shot metadata, media, characters, and `LCBE_LAYOUT` from the LCBE backend. Outputs `IMAGE`, `MASK`, `LCBE_LAYOUT`, `LCBE_METADATA`.
- **LCBE Save** — pushes a Comfy output back to LCBE. With `parent_shot_ref` connected, saves as a new version on the parent shot. Without it, creates a new shot in the chosen project. Captures the workflow JSON automatically.

## Custom socket types

| Socket | Carries | Schema |
|---|---|---|
| `LCBE_LAYOUT` | Spatial scene data (cameras, proxies, world) | [lcbe-layout-schema v1.0](https://github.com/Lenscowboy/lcbe-layout-schema) |
| `LCBE_METADATA` | Shot/version metadata (IDs, characters, tags) | Server-normalized dict |
| `LCBE_SHOT_REF` | Reference back into LCBE | Server-normalized dict |

All three are registered as Python `dict` on the node side. Socket colours live in `web/lcbe.js` for visual distinction on the canvas.

## Install

> **Phase 1 note:** the node loads in ComfyUI but does nothing useful yet. If you want to test that registration works, you can install it now; otherwise wait for the Phase 2 release.

### ComfyUI Manager

Will be listed under "LCBE Node" once Phase 4 publishes a tagged release.

### Manual

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Lenscowboy/comfyui-lenscowboy-lcbe.git
cd comfyui-lenscowboy-lcbe
pip install -r requirements.txt
# Restart ComfyUI
```

## Configuration

The node reads its LCBE token from `~/.lcbe/comfy_token.json` (override with the `LCBE_COMFY_CONFIG` env var). Generate the token in LCBE Settings → Integrations → ComfyUI once Phase 1 ships the issuance UI.

Expected file shape:

```json
{
  "token": "lcbe_comfy_xxxxxxxxxxxx",
  "endpoint": "https://api.lenscowboy.com",
  "tenant_id": "...",
  "label": "Brad's home rig",
  "created_at": "..."
}
```

File should be mode `0600` on POSIX hosts.

## Tier eligibility

LCBE ComfyUI integration is available on:

- **Studio** — gated by seat count (1 token per seat). Workflow provenance stored as hash + vendor metadata.
- **LSV** — unlimited tokens. Full workflow JSON stored alongside each rendered version for Article 50 compliance.

Pro, Influencer, and Creator tiers do not include ComfyUI integration. Existing tokens on downgraded tenants enter a 30-day read-only grace window before auto-revocation.

## Schema synchronization

This repo vendors a pinned copy of the `LCBE_LAYOUT` JSON Schema from the canonical [lcbe-layout-schema](https://github.com/Lenscowboy/lcbe-layout-schema) repository.

Files:

- `schemas/PINNED_VERSION` — the semver of the upstream tag this repo is pinned to (e.g. `1.0.0`).
- `schemas/lcbe_layout.schema.json` — vendored copy of the upstream schema at the pinned version.
- `schemas/.sha256` — SHA-256 of the upstream schema, used by CI to detect drift.

A GitHub Actions check (`.github/workflows/schema-check.yml`) runs on every PR and main push and fails if the local schema diverges from the pinned upstream version.

### Bumping the pinned schema version

1. Edit `schemas/PINNED_VERSION` to the new semver.
2. Run `bash scripts/sync-schema.sh` — fetches the upstream schema at the new tag and updates the local copy + `.sha256`.
3. Commit all three files and push.

Never edit `schemas/lcbe_layout.schema.json` directly — the canonical source is upstream.

## Companion repos

- [comfyui-lenscowboy-pal](https://github.com/Lenscowboy/comfyui-lenscowboy-pal) — PAL Layout node. Emits `LCBE_LAYOUT` directly from its 3D viewport (Phase 3.5).
- [lcbe-layout-schema](https://github.com/Lenscowboy/lcbe-layout-schema) — canonical `LCBE_LAYOUT` JSON Schema.

## License

MIT — see [LICENSE](LICENSE).
