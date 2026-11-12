"""Check Russian font chains/glyphs and preview active PNG; never write game art.

Uses actual HOI4 bitmap-font metrics/atlases, not substitute Windows fonts.
Source preview only: does not reproduce the complete engine text renderer.
--check-only works without Pillow. --game-root selects the installed HOI4.
"""
import argparse
import json
from pathlib import Path
import re
from pdx_source import atom, parse, val, vals

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'gfx/interface/nw14_super_events/russia_on_fire.png'
PREVIEW = ROOT / 'DESIGN/previews/russian_civil_war/super_event_preview.png'


def font_registration(name, game):
    # Prefer this feature's isolated registrations; fall back to the actual
    # game's core.gfx for the same logical font IDs used by Kaiserredux.
    paths = (ROOT / 'interface/nw14_super_event_fonts.gfx', game / 'interface/core.gfx')
    for path in paths:
        if not path.is_file():
            continue
        root = parse(path.read_text(encoding='utf-8-sig'))
        definitions = val(root, 'spriteTypes', [])
        fonts = vals(definitions, 'bitmapfont')
        overrides_source = definitions
        if path.name == 'core.gfx':
            # Vanilla and KX keep bitmapfont nodes in a separate root block.
            font_block = val(root, 'bitmapfonts', [])
            fonts = vals(font_block, 'bitmapfont')
            overrides_source = font_block
        matches = [f for f in fonts if atom(val(f, 'name')) == name]
        if len(matches) > 1:
            raise ValueError(f'Duplicate GUI font registration in {path}: {name}')
        if not matches:
            continue
        selected = matches[0]
        overrides = [f for f in vals(overrides_source, 'bitmapfont_override')
                     if atom(val(f, 'name')) == name
                     and 'l_russian' in [atom(n.value) for n in val(f, 'languages', [])]]
        override_chains = {
            tuple(atom(n.value) for n in val(item, 'fontfiles'))
            for item in overrides
        }
        if len(override_chains) > 1:
            raise ValueError(f'Conflicting Russian overrides in {path}: {name}')
        files = val(overrides[0] if overrides else selected, 'fontfiles')
        return [atom(n.value) for n in files], int(val(selected, 'color'), 16)
    raise ValueError(f'Unregistered GUI font in feature and game: {name}')


class BitmapFont:
    def __init__(self, game, resources, colour):
        self.glyphs, self.kernings, self.line_height = {}, {}, 0
        self.colour = ((colour >> 16) & 255, (colour >> 8) & 255, colour & 255, 255)
        for resource in resources:
            stem = game / resource
            fnt, dds = stem.with_suffix('.fnt'), stem.with_suffix('.dds')
            if not fnt.is_file() or not dds.is_file():
                raise ValueError(f'Missing descriptor/atlas: {stem}')
            text = fnt.read_text(encoding='utf-8-sig')
            self.line_height = max(self.line_height, int(re.search(r'\blineHeight=(\d+)', text)[1]))
            for line in text.splitlines():
                numbers = {k: int(v) for k, v in re.findall(r'(\w+)=\s*(-?\d+)', line)}
                if line.startswith('char '):
                    self.glyphs.setdefault(numbers['id'], (dds, numbers))
                elif line.startswith('kerning '):
                    self.kernings.setdefault((numbers['first'], numbers['second']), numbers['amount'])

    def width(self, text):
        width, previous = 0, None
        for character in text:
            code = ord(character)
            if code not in self.glyphs:
                raise ValueError(f'Missing glyph U+{code:04X} {character!r}')
            width += self.kernings.get((previous, code), 0) + self.glyphs[code][1]['xadvance']
            previous = code
        return width

    def wrap(self, text, width):
        result = []
        for paragraph in text.split('\n'):
            line = ''
            for word in paragraph.split():
                candidate = f'{line} {word}'.strip()
                if self.width(candidate) > width and line:
                    result.append(line)
                    line = word
                else:
                    line = candidate
                if self.width(line) > width:
                    raise ValueError(f'Unbreakable word exceeds width: {word}')
            result.append(line)
        return result

    def draw(self, panel, line, x, y):
        from PIL import Image
        previous, atlases = None, {}
        for character in line:
            code = ord(character)
            path, g = self.glyphs[code]
            if path not in atlases:
                atlases[path] = Image.open(path).convert('RGBA')
            x += self.kernings.get((previous, code), 0)
            if g['width'] and g['height']:
                box = (g['x'], g['y'], g['x'] + g['width'], g['y'] + g['height'])
                mask = atlases[path].crop(box).getchannel('A')
                ink = Image.new('RGBA', mask.size, self.colour)
                ink.putalpha(mask)
                panel.alpha_composite(ink, (x + g['xoffset'], y + g['yoffset']))
            x += g['xadvance']
            previous = code


def audit(game, render=False):
    localisation = {}
    for file in (ROOT / 'localisation').rglob('*_l_russian.yml'):
        pairs = re.findall(r'^\s*([\w.]+):\d*\s+"(.*)"', file.read_text(encoding='utf-8-sig'), re.M)
        localisation.update((key, value.replace('\\n', '\n')) for key, value in pairs)
    gui = ROOT / 'interface/nw14_super_events.gui'
    window = val(val(parse(gui.read_text(encoding='utf-8-sig')), 'guiTypes'), 'containerWindowType')
    panel = None
    if render:
        from PIL import Image
        panel = Image.open(ART).convert('RGBA')
    records = []
    elements = [(e, False) for e in vals(window, 'instantTextBoxType')]
    elements += [(e, True) for e in vals(window, 'buttonType')]
    for element, button in elements:
        name = atom(val(element, 'name'))
        font_name = atom(val(element, 'buttonFont' if button else 'font'))
        key = atom(val(element, 'buttonText' if button else 'text'))
        if key not in localisation:
            raise ValueError(f'Unresolved localisation: {key}')
        resources, colour = font_registration(font_name, game)
        font = BitmapFont(game, resources, colour)
        value = localisation[key]
        # Check actual strings plus all 66 Russian upper/lowercase letters.
        required = set(value.replace('\n', '') + 'Ёё' + ''.join(map(chr, range(1040, 1104))))
        font.width(''.join(required))
        width, height = int(val(element, 'maxWidth', '352')), int(val(element, 'maxHeight', '48'))
        lines = font.wrap(value, width)
        if len(lines) * font.line_height > height:
            raise ValueError(f'{name}: {len(lines) * font.line_height}px text exceeds {height}px')
        position = val(element, 'position')
        x, y = int(val(position, 'x')), int(val(position, 'y'))
        if x < 0 or y < 0 or x + width > 899 or y + height > 592:
            raise ValueError(f'{name}: text block exceeds panel')
        records.append(dict(element=name, font=font_name, fontfiles=resources,
                            required_glyphs=len(required), missing_glyphs=0,
                            text_height=len(lines) * font.line_height, max_height=height))
        if render:
            if button:
                panel.alpha_composite(Image.open(game / 'gfx/interface/event_option_entry.dds').convert('RGBA'), (x, y))
                y += (height - font.line_height) // 2
            for line in lines:
                align = 'center' if button else atom(val(element, 'format', 'left'))
                dx = (width - font.width(line)) // 2 if align == 'center' else 0
                font.draw(panel, line, x + dx, y)
                y += font.line_height
    if render:
        PREVIEW.parent.mkdir(parents=True, exist_ok=True)
        panel.save(PREVIEW)
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root', type=Path, default=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV'))
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    print(json.dumps(dict(runtime=False, blocks=audit(args.game_root, not args.check_only)), ensure_ascii=False, indent=2))
