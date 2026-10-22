# Music and radio templates

## Original structure (concept)

| path | function |
|------|------|
| `music/*.ogg` | Audio resources |
| `music/music.asset` or `.asset` | Register sound name and file |
| `music/_songs.txt`, etc. | Track list, situation weight |

## .asset indication

```
music = {
	name = "TAG_theme_1"
	file = "TAG_theme_1.ogg"
}
```

The actual syntax of the original `music.asset` shall prevail (may include fields such as volume).

## Track list indication

```pdx
music_station = "base_music"

music = {
	song = "TAG_theme_1"
	chance = {
		modifier = {
			factor = 1
		}
	}
}
```

War/peace/camp themes commonly use `modifier` + trigger (war, ideology, etc.). Copy the original `_songs.txt` and then change it in one paragraph for the most stable result.

## Play during effect

```pdx
play_song = TAG_theme_1
```

Super events, news, and national focus celebrations are available; be careful not to conflict with the UI music to the point of harshness.

## Radio

Community Radio = Customized Music Station + Interface + Online Agreement. The library has "Radio Series" tutorials and template zips.  
Summary of steps:

1. Convert audio to **OGG**
2. asset registration
3. songs/station definition
4. Optional scripted_gui radio interface
5. Online: The mods/resources of both parties are consistent

## Specification

- Pay attention to copyright; Steam Workshop distribution requires the right to use the audio
- Control volume and length; super-event BGM uses an independent station to avoid entering the ordinary random pool (see super-event template description)
- Chinese paths are prone to problems, use ASCII for resource names
## Related

- `super-event-template.md` / `scripted-gui-template.md` / `mod-structure-template.md`
