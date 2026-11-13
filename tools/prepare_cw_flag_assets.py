"""Offline conversion of reviewed Commons SVGs; never downloads or runs source code."""
import io
import json
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'DESIGN/source_assets/cw_flags'
CHOICES = {
    'ALA': ('neutrality', 'Alash-Orda', 'regional historical design'),
    'TRK': ('neutrality', 'Bukhara / Said Alim Khan', 'regional historical design'),
    'NCR': ('democratic', 'Mountain Republic', 'historical reconstruction'),
    'TCF': ('democratic', 'Transcaucasian Federation', 'disputed historical attribution'),
    'DNR': ('democratic', 'Don Soviet Republic', 'plain red banner; author option'),
    'KIR': ('democratic', 'Kazakh flag proposal (1911)', 'Kazakh national proposal; reconstructed'),
    'BLF': ('neutrality', 'United Baltic Duchy cross', 'alternative adoption for federation'),
    'BLW': ('democratic', 'Baltic sailors banner', 'Petropavlovsk 1917; alternative adoption'),
}


def main():
    sheet = Image.new('RGB', (880, 5 * 210), '#e8e4d8')
    draw = ImageDraw.Draw(sheet)
    credits = ['# CW flag asset sources', '',
               'Selected on 2026-11-12 for Nothing Wrong. Original SVGs and Commons imageinfo metadata are retained beside this file.',
               'Conversions: SVG rasterization or KIR source PNG, RGB resampling to HOI4 flag sizes 82×52, 41×26, 10×7; no redraw or new emblem generation.',
               'Regional historical designs and fictional project adoptions are distinguished below.', '']
    for index, (tag, (ideology, label, context)) in enumerate(CHOICES.items()):
        svg = (SOURCE / f'{tag}.svg').read_bytes()
        document = ElementTree.fromstring(svg)
        for node in document.iter():
            if node.tag.split('}')[-1] in ('script', 'image', 'foreignObject'):
                raise ValueError(f'{tag}: unexpected active or external SVG element')
            for key, value in node.attrib.items():
                if key.endswith('href') and not value.startswith('#'):
                    raise ValueError(f'{tag}: external reference {value}')
        import cairosvg  # Already installed; no installation/network access here.
        png = cairosvg.svg2png(bytestring=svg, output_width=820)
        image = Image.open(SOURCE / 'KIR_KAZAKH_1911.png').convert('RGBA') if tag == 'KIR' else Image.open(io.BytesIO(png)).convert('RGBA')
        opaque = Image.new('RGBA', image.size, 'white')
        opaque.alpha_composite(image)
        image = opaque.convert('RGB')
        for folder, size in (('', (82, 52)), ('medium', (41, 26)), ('small', (10, 7))):
            for suffix in ('', '_' + ideology):
                output = ROOT / 'gfx/flags' / folder / f'{tag}{suffix}.tga'
                buffer = io.BytesIO()
                image.resize(size, Image.Resampling.LANCZOS).save(buffer, format='TGA', compression=None)
                data = buffer.getvalue()
                if output.exists() and output.read_bytes() != data:
                    raise FileExistsError(f'Refusing to overwrite a changed flag: {output}')
                if not output.exists():
                    output.write_bytes(data)
        x, y = (index % 2) * 440 + 20, (index // 2) * 210 + 10
        sheet.paste(image.resize((246, 156), Image.Resampling.LANCZOS), (x, y))
        draw.text((x, y + 160), f'{tag} - {label}', fill='black')
        draw.text((x, y + 178), context, fill='#703b27')
        info = json.loads((SOURCE / ('KIR_KAZAKH_1911.json' if tag == 'KIR' else f'{tag}.json')).read_text())
        meta = info['extmetadata']
        credits += [f'## {tag} — {label}', '', f'Role: {context}.',
                    f"Source: {info['descriptionurl']}",
                    f"License: {meta.get('LicenseShortName',{}).get('value','UNKNOWN')}; {meta.get('LicenseUrl',{}).get('value','see source page')}.",
                    f"Artist / attribution (Commons metadata HTML): {meta.get('Artist',{}).get('value','see source page')}",
                    'For NCR, the SVG and converted TGA derivatives remain licensed CC BY-SA 4.0; this attribution applies to those assets, not a blanket license of the project.', '']
    # Include the explicitly requested vanilla FIN flag in the review sheet.
    fin = Image.open(ROOT / 'gfx/flags/FIN_democratic.tga').convert('RGB')
    sheet.paste(fin.resize((246, 156)), (20, 850))
    draw.text((20, 1010), 'FIN - plain Finnish national flag', fill='black')
    out = ROOT / 'DESIGN/previews/cw_flags_20261112.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    credits += ['## Vanilla reuse', '',
                'FIN_democratic: byte-for-byte copy of vanilla FIN_neutrality (plain national cross without arms), three sizes. The ideology is not changed.',
                'TRP / TRP_neutrality: copies of vanilla TUR_democratic, three sizes.',
                'Vanilla assets remain game assets; no independent redistribution license is asserted.', '']
    (SOURCE / 'CREDITS.md').write_text('\n'.join(credits))


if __name__ == '__main__':
    main()
