# Shader / HLSL entry template

Path: `gfx/FX/` (`.shader` / `.fxh` / `.lua` button state, etc.).
Used for map rendering, special blending, and custom UI effects. Belongs to the category of **graphics programs**.

## When is it needed?

- Changed map coloring, water, and seasonal performance
- Customize progress/button effects
- Community advanced UI (curves, special masks)

Ordinary national focuses/events/ideas do not need to write shaders.

## How to work (concept)

1. Copy FX files that are close to the original
2. Change parameters or minimum segment HLSL
3. Reference in `.gfx`’s `effectFile = "gfx/FX/....lua"`
4. Enter the game and check the performance; a bad shader may cause pink images, blurry screens, and crashes.

## Learning path

1. Library: HLSL basic syntax, `.fxh` header file tutorial
2. Original `gfx/FX` read-only comparison
3. Small mod single effect test
4. Then access the official interface

## Specification

- It is forbidden to overwrite the original main map shader for release without understanding the binding.
- Changes should be kept to a minimum diff, and the meaning of parameters should be commented out.
- FX is prone to failure after version upgrade and is included in the migration test (`version-migration-template.md`)

## Related

- `gfx-registration-template.md` / `map-modding-template.md` / `scripted-gui-template.md`
