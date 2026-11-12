"""DISABLED historical generator. Active art was replaced by the author.

Requires Pillow (available in the bundled Codex Python runtime). No KX art is copied.
The historical photograph is fitted without cropping or stretching.
"""
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'DESIGN/previews/russian_civil_war/source_petrograd_1917.jpeg'
TARGET = ROOT / 'gfx/interface/nw14_super_events/russia_on_fire.png'


def build():
    raise SystemExit('Historical artwork generator disabled: preserve the author PNG. Use tools/preview_super_event_fonts.py instead.')
    panel = Image.new('RGBA', (899, 592), (28, 25, 22, 255))
    draw = ImageDraw.Draw(panel)
    draw.rectangle((8, 8, 890, 583), fill=(199, 192, 172), outline=(112, 100, 78), width=3)
    draw.rectangle((20, 20, 878, 85), fill=(56, 45, 39))
    draw.line((25, 96, 873, 96), fill=(124, 108, 83), width=2)
    draw.line((391, 105, 391, 557), fill=(142, 125, 98), width=1)
    draw.rectangle((401, 100, 870, 444), fill=(161, 152, 130), outline=(92, 83, 65), width=2)
    photo = ImageOps.contain(Image.open(SOURCE).convert('RGB'), (457, 328), Image.Resampling.LANCZOS)
    x = 407 + (457 - photo.width) // 2
    y = 108 + (328 - photo.height) // 2
    panel.paste(photo, (x, y))
    draw.line((421, 458, 850, 458), fill=(124, 108, 83), width=1)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    panel.save(TARGET)
    print(f'{TARGET}: {panel.size}, PNG RGBA; photo {photo.size}, no crop')
    # Approximate layout preview, not an HOI4 screenshot. Game text stays localised.
    preview = panel.copy()
    canvas = ImageDraw.Draw(preview)
    loc = (ROOT / 'localisation/replace/nw14_l_russian.yml').read_text(encoding='utf-8-sig')
    def text(key):
        return re.search(r'^\s*' + re.escape(key) + r':\d+ "(.*)"', loc, re.M).group(1)
    title_font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 32)
    body_font = ImageFont.truetype('C:/Windows/Fonts/cour.ttf', 22)
    canvas.text((449, 33), text('nw14cw.1.t'), font=title_font, fill='white', anchor='mt')
    def wrapped(value, width):
        lines = []
        line = ''
        for word in value.split():
            candidate = (line + ' ' + word).strip()
            if line and canvas.textlength(candidate, font=body_font) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        return lines + [line]
    lines = wrapped(text('nw14cw.1.d'), 330)
    if len(lines) * 25 > 370:
        raise ValueError('Description exceeds GUI height')
    canvas.multiline_text((38, 116), '\n'.join(lines), font=body_font, fill=(30, 27, 22), spacing=3)
    canvas.multiline_text((421, 472), '\n'.join(wrapped(text('nw14cw.1.a'), 429)), font=body_font, fill=(30, 27, 22), spacing=3)
    canvas.rectangle((38, 518, 368, 558), outline=(90, 79, 60), width=1)
    canvas.text((203, 525), 'Продолжить', font=body_font, fill=(30, 27, 22), anchor='mt')
    preview.save(ROOT / 'DESIGN/previews/russian_civil_war/super_event_preview.png')


if __name__ == '__main__':
    build()
