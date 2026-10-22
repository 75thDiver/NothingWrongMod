#Unit model/soldier model entrance template

3D units and building appearances belong to the art pipeline and are not ordinary txt national focus logic. This page provides **file placement and hooking methods**; for modeling software operations, see the library soldier model tutorial.

## Common directories

| path | function |
|------|------|
| `gfx/models/` | Model mesh/animation resource tree |
| `gfx/entities/` | entity definition (tie the mesh into a game entity) |
| `gfx/*.asset` | asset index (partial resources) |
| `interface` / `gfx` related | 2D icons still use normal GFX |

The original land, sea and air unit models are huge; mods usually only replace a small number of entities or add new unit models.

## Logical side hook

1. `sprite = infantry` etc. **sprite/entity name** in `common/units/<unit>.txt`
2. The entity file points the name to mesh/map
3. Technology `enable_subunits` After unlocking the arms, the corresponding entities will be used on the map

Equipment icons are 2D (`GFX_`), separate from the 3D model (`equipment-template.md` / `gfx-registration-template.md`).

## Minimum feasible path (replacement)

1. Find the entity name of a certain unit in the vanilla (reverse check from `sprite =`)
2. Use tools to export/change textures or change mesh (follow tutorial)
3. Cover the corresponding entity/model path in the mod
4. Enter the game to see the map units and production interface

## New unit model

1. Define `sub_units` (`unit-template.md`)
2. Configure sprite/entity name
3. Provide entity + model resources
4. Technology/organization unlocking
5. Localization and 2D Icons
If entity is missing, it will always be pink/invisible/fallback to default.

## Specification

- Don't "fake" entity paths without knowing the model
- Pay attention to the size and loading time of the Steam Workshop for large resources
- Animation, binding, and LOD are subject to the soldier model tutorial
- Do not insert experimental models into the main project before the design is confirmed

## Related

- `unit-template.md` / `equipment-template.md` / `gfx-registration-template.md`
