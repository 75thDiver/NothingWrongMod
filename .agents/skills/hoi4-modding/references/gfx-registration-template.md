# GFX Registration Template

`.gfx` registers the image on the disk as `GFX_*` name for reference by idea/national focus/event/interface.

## Common locations

| Purpose | Image Catalog | Registration Document (Conventional) |
|------|----------|------------------|
| National focus icon | `gfx/interface/goals/` | `interface/goals.gfx` + `goals_shine.gfx` |
| ethos/bill icon | `gfx/interface/ideas/` | `interface/ideas.gfx` |
| Event graph | `gfx/event_pictures/` | `interface/eventpictures.gfx` |
| News Picture | Same as above | Same as above, the name often contains `news_event` |
| General/leader avatar | `gfx/leaders/<TAG>/` | Part direct path, part `interface` portrait gfx |
| Flags | `gfx/flags/` | The engine loads according to tag convention, generally **not** use spriteType |

You can build your own `interface/TAG_goals.gfx` etc. in the mod, as long as it is loaded.

## spriteType basics

```pdx
spriteTypes = {
	spriteType = {
		name = "GFX_idea_TAG_my_spirit"
		texturefile = "gfx/interface/ideas/TAG_my_spirit.dds"
	}

	spriteType = {
		name = "GFX_goal_TAG_my_focus"
		texturefile = "gfx/interface/goals/TAG_my_focus.dds"
	}
spriteType = {
		name = "GFX_news_event_TAG_foo"
		texturefile = "gfx/event_pictures/news_event_TAG_foo.dds"
	}
}
```

| Field | Description |
|------|------|
| `name` | Script reference name, usually prefixed with `GFX_` |
| `texturefile` | Path relative to the game/mod root |
| `noOfFrames` | Number of frames |
| `effectFile` | Shader (button/progress bar, etc.) |
| `allwaystransparent` | Whether the transparent area is clickable |
| `legacy_lazy_load` | Lazy loading |

Excessive size of a single dds file may cause problems; follow the original resource specifications.

## National focus icon and shine

National focus `icon = GFX_goal_TAG_my_focus` (or the project is written without a prefix, **subject to the project and original citation method**).

Shine in `goals_shine.gfx`:

```pdx
spriteType = {
	name = "GFX_goal_TAG_my_focus_shine"
	texturefile = "gfx/interface/goals/TAG_my_focus.dds"
	effectFile = "gfx/FX/buttonstate.lua"
	animation = {
		animationmaskfile = "gfx/interface/goals/TAG_my_focus.dds"
		animationtexturefile = "gfx/interface/goals/shine_overlay.dds"
		animationrotation = -90.0
		animationlooping=no
		animationtime = 0.75
		animationdelay = 0
		animationblendmode = "add"
		animationtype = "scrolling"
		animationrotationoffset = { x = 0.0 y = 0.0 }
		animationtexturescale = { x = 1.0 y = 1.0 }
	}
	legacy_lazy_load = no
}
```
Copy one of the original shine and then change it to `name`/`texturefile`/`animationmaskfile` for the most stability.

## Idea icon

In the definition:

```pdx
TAG_my_spirit = {
	picture = TAG_my_spirit # or the picture field writing method specified by the project
	modifier = { }
}
```

The corresponding gfx name is mostly `GFX_idea_TAG_my_spirit`, and `texturefile` points to `gfx/interface/ideas/...`.
Project specifications: If the user does not provide an icon, `picture =` can be left blank and let the user fill it in (`modding-rules.md`).

## Events/News Pictures

```pdx
picture = GFX_news_event_generic_read_write
picture = GFX_report_event_generic_funeral
```

Register at `eventpictures.gfx`. You can directly reuse the original `GFX_news_event_*` / `GFX_report_event_*`.

## General portrait

Common character files:

```pdx
portraits = {
	army = {
		large = "gfx/leaders/RYH/Portrait_RYH_x.dds"
		small = "gfx/interface/ideas/RYH_x_small.dds"
	}
}
```

Or refer to an existing `GFX_LEADER_*` (if the project/pre-mod is registered). **Don't make up GFX names that don't exist**; search for the project and body first.

## flag

```
gfx/flags/TAG.tga
gfx/flags/medium/TAG.tga
gfx/flags/small/TAG.tga
```
Ideological flags: `TAG_communism.tga` etc. The cosmetic tag may need a corresponding file name.

## frameAnimatedSpriteType / progress bar

```pdx
frameAnimatedSpriteType = {
	name = "GFX_TAG_anim"
	texturefile = "gfx/interface/TAG_anim.dds"
	noOfFrames = 8
	animation_rate_fps = 15
	looping=yes
	play_on_show = yes
}
```

For progress bars, etc., see the library's "commonly used gfx registration templates" and the original `interface/*.gfx`.

## Specification

- First search the original/front-end mod to see if there is already a picture with the same name, and give priority to reuse.
- Naming: `GFX_<type>_<TAG>_<meaning>`
- Global search for old `GFX_` references after name change
- Do not write compatible code; missing resources will cause pink pictures/pink frames

## Query order

1. This page
2. Ontology `interface/goals.gfx`, `ideas.gfx`, `eventpictures.gfx`
3. The current mod already has `interface/`
4. wiki: **Graphical asset**/Interface
5. Ask the user for a picture or confirm which original picture to reuse.

## Related

- `focus-template.md` / `idea-template.md` / `event-template.md` / `character-template.md`
