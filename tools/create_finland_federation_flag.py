#!/usr/bin/env python3
"""Draw the Finland-Sweden federation flag used by the NW cosmetic tag.

The layout is an original redraw inspired by Flag_of_Tough_Love's Reddit
concept for a Sweden/Finland union (r/vexillology, 2015). The Reddit upload
is not bundled because its post does not state a reuse license.
"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS = (
    (ROOT / "gfx/flags", (82, 52)),
    (ROOT / "gfx/flags/medium", (41, 26)),
    (ROOT / "gfx/flags/small", (10, 7)),
)
PREFIXES = ("NW_FINNISH_FEDERATION", "NW_FINNISH_FEDERATION_democratic")
FIELD = (245, 245, 237)
SWEDISH_BLUE = (20, 68, 126)
SWEDISH_GOLD = (246, 190, 0)


def centered_bounds(center, thickness, limit):
    thickness = max(1, min(thickness, limit))
    start = max(0, center - thickness // 2)
    end = min(limit, start + thickness)
    start = max(0, end - thickness)
    return start, end


def render(size):
    width, height = size
    image = Image.new("RGB", size, FIELD)
    draw = ImageDraw.Draw(image)

    vertical_axis = round(width * 0.40)
    horizontal_axis = round(height * 0.50)
    gold_width = max(1, round(height * 0.14))
    outline = max(1, round(gold_width * 0.35))
    blue_width = gold_width + outline * 2

    left, right = centered_bounds(vertical_axis, blue_width, width)
    top, bottom = centered_bounds(horizontal_axis, blue_width, height)
    draw.rectangle((left, 0, right - 1, height - 1), fill=SWEDISH_BLUE)
    draw.rectangle((0, top, width - 1, bottom - 1), fill=SWEDISH_BLUE)

    left, right = centered_bounds(vertical_axis, gold_width, width)
    top, bottom = centered_bounds(horizontal_axis, gold_width, height)
    draw.rectangle((left, 0, right - 1, height - 1), fill=SWEDISH_GOLD)
    draw.rectangle((0, top, width - 1, bottom - 1), fill=SWEDISH_GOLD)
    return image


def main():
    for directory, dimensions in DESTINATIONS:
        directory.mkdir(parents=True, exist_ok=True)
        for prefix in PREFIXES:
            render(dimensions).save(directory / f"{prefix}.tga", format="TGA")

    preview = render((492, 312))
    preview_path = Path("/tmp/nw-fin-pol-task/finland_federation_flag_preview.png")
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview.save(preview_path)
    print(f"Wrote 6 HOI4 TGA files; preview: {preview_path}")


if __name__ == "__main__":
    main()
