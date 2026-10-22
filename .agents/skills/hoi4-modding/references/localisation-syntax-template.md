# Localization syntax template

Encoding, key name, color code, dynamic replacement and script localization call. For writing style specifications, see `modding-rules.md` "Localization Writing Standards".

## File location and naming

```
localisation/
  simp_chinese/
    <name>_l_simp_chinese.yml
  english/
    <name>_l_english.yml
```

- The file name must match the language suffix: `_l_simp_chinese.yml`, `_l_english.yml`
- Directory names: `simp_chinese`, `english`, etc. are consistent with the game

## Encoding

- Use **UTF-8 with BOM** (`utf-8-sig`)
- Python reads and writes first `encoding="utf-8-sig"`
- **Forbidden** PowerShell `Set-Content` directly writes Chinese yml (easy to lose BOM/garbled code)
- When the code is garbled, try to diagnose it with `utf-8-sig` / `utf-8` / `gbk`, and then write it back with `utf-8-sig`

## File header

```yaml
l_simp_chinese:
  KEY: "Text"
  KEY2: "Another row"
```

- The first line must be `l_<language>:`
- There is a colon between the key and the text; it is recommended that the text be wrapped in double quotes
- The version number field of `KEY:0 "text"` is common in the vanilla; **The new write key can be written as `KEY: "text"` or `KEY:0 "text"`**, which is consistent with the existing files of the project

## Key name convention

| Content | Key Pattern |
|------|--------|
| National focus name | `FOCUS_ID: "name"` or existing model of the project |
| National focus description | `FOCUS_ID_desc: "Description"` |
| event title | `namespace.1.t` |
| Event description | `namespace.1.d` |
| Event options | `namespace.1.a` / `.b` |
| Idea name | `IDEA_ID` |
| Idea Description | `IDEA_ID_desc` |
| Resolution | Corresponds to decision id |
| Custom tooltip | `TAG_something_tt` |
| Script localization results | The key pointed to by `localization_key` |
The same key in the yml loaded later will overwrite the one loaded first (depending on the mod order).

## Line breaks and formatting

```yaml
  some.event.d: "The first paragraph.\n\nThe second paragraph continues."
```

- `\n` line break; `\n\n` segmentation
- Avoid meaningless long single lines; but do not break them into literary chapters.

## Color code

Use `§` as the starting color and `§!` as the ending color:

| Code | Common Colors |
|----|----------|
| `§Y` | Huang (emphasis added) |
| `§G` | Green (front) |
| `§R` | Red (negative/dangerous) |
| `§B` | Blue |
| `§C` | Green |
| `§L` | Gray |
| `§O` | Orange |
| `§W` | White |
| `§H` | Highlight (commonly used in the original UI) |

```yaml
  example_tt: "Get §YNational Spirit§!: §GXXXX§!"
  example_bad: "§RWarning: Decreased stability§!"
```

Enter `§`: Unicode or Alt sequences are required in some editors; remain consistent with the original yml.

**Note**: Some interfaces/events have different color support; the original text of the same type shall prevail.

## Dynamic country/character key

```yaml
  news.1.d: "[GER.GetNameDef] announced today..."
  news.2.d: "The [GER.GetAdjective] government said..."
  news.3.d: "[GER.GetLeader] gave a speech."
  news.4.d: "[From.GetNameDef] takes action against [Root.GetNameDef]."
```

Common (not complete):

| key | meaning |
|----|------|
| `[TAG.GetName]` | Country name |
| `[TAG.GetNameDef]` | Country name with article/definition (Chinese is often close to GetName) |
| `[TAG.GetAdjective]` | Adjective form |
| `[TAG.GetLeader]` | Leader name |
| `[TAG.GetFlag]` | Flag (part of UI) |
| `[Root.*]` / `[From.*]` / `[This.*]` | Relative scope |
| `[GetDateText]` | Date text |
| `[GetYear]` | Year |
It is customary to use `[TAG.GetNameDef]`, `[TAG.GetLeader]`, etc. in the original Chinese version; **Search the vanilla first and then write**.

## Variable display

```yaml
  TAG_val_tt: "Current value: §Y[?TAG_my_var]§!"
  TAG_val_pct: "Efficiency: [?TAG_my_var|%]"
  TAG_val_root: "[?ROOT.TAG_my_var]"
```

See wiki **Localisation** and `variables-arrays-template.md` for more format codes.

## Script localization

Defined in `common/scripted_localisation/`, see `scripted-triggers-template.md`.

Call:

```yaml
  some_title: "[GET_DYNAMIC_TITLE]"
```

`GET_DYNAMIC_TITLE` corresponds to `defined_text = { name = GET_DYNAMIC_TITLE ... }`.

## special / game text symbols

- `$SOME_KEY$`: Nest another localization key (used extensively in the vanilla)
- `£trigger_no` / icon, pound code, etc.: subject to the vanilla and wiki
- Keep event option names short, like the original button

```yaml
  germany.11.a.tt: "§R During the validity period of the treaty, closed economy trade bills will not be available.§!\n"
```

## Writing style (mandatory)

You must check the vanilla of similar keys before writing:

- News: `news.*` or `germany.*` in `events_l_simp_chinese.yml`, etc.
- National focus: short title + description of telecommunications/policy tone
- Prohibition of mechanical explanations, player monologues, and stereotypes

See `modding-rules.md` for details.

## Minimal example (event)
```yaml
l_simp_chinese:
  RSC_RYH_news.1.t: "Academy of Sciences takes over government"
  RSC_RYH_news.1.d: "According to reliable sources, [RSC.GetNameDef]'s scientific research institute has taken over administrative powers. The previous debate over the direction of the country's development has come to an end."
  RSC_RYH_news.1.a: "Interesting."
  RSC_RYH_news.1.b: "History will remember this day."
```

## Checklist

1. BOM / `l_simp_chinese:` header
2. The key name is consistent with the script id
3. Is the dynamic key tag/scope valid at runtime?
4. Color `§` / `§!` in pairs
5. Same flavor as the original

## Query order

1. `modding-rules.md` style of writing
2. Grammar of this page
3. Ontology `localisation/simp_chinese/` similar keys
4. wiki: **Localisation**
5. Ask the user

## Related documents

- `modding-rules.md` / `event-template.md` / `scripted-triggers-template.md` / `variables-arrays-template.md`
