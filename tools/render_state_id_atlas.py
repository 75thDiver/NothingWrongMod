"""Build unannotated state-ID atlas map tiles from the active HOI4 map.

This reads the active mod's history/states and the configured HOI4 province
map. It does not change game files. PowerShell adds readable labels afterward.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from pathlib import Path

import preview_russian_civil_war as source


MAX_STATES_PER_PAGE = 60
BASE_COLUMNS = 4
BASE_ROWS = 2
BASE_LABELS = "ABCD"
SEA = (203, 225, 233)
LAND_LIGHT = (234, 235, 227)
LAND_SHADE = (224, 228, 219)
BORDER = (66, 79, 86)
CANON_NAMES = {
    88: "Краков (Krakow)",
    89: "Станиславов (Stanislavov)",
    90: "Кельце (Kielce)",
    91: "Львов (Lwow)",
}


def split_page(code, box, state_items):
    if len(state_items) <= MAX_STATES_PER_PAGE:
        return [{"code": code, "box": box, "state_ids": [sid for sid, _ in state_items]}]

    x_spread = max(xy[0] for _, xy in state_items) - min(xy[0] for _, xy in state_items)
    y_spread = max(xy[1] for _, xy in state_items) - min(xy[1] for _, xy in state_items)
    axis = 0 if x_spread >= y_spread else 1
    ordered = sorted(state_items, key=lambda item: (item[1][axis], item[0]))
    middle = len(ordered) // 2
    before = ordered[middle - 1][1][axis]
    after = ordered[middle][1][axis]
    cut = (before + after) / 2

    x0, y0, x1, y1 = box
    if axis == 0:
        left_box, right_box = (x0, y0, cut, y1), (cut, y0, x1, y1)
    else:
        left_box, right_box = (x0, y0, x1, cut), (x0, cut, x1, y1)

    return (
        split_page(code + "a", left_box, ordered[:middle])
        + split_page(code + "b", right_box, ordered[middle:])
    )


def make_pages(centers, width, height):
    pages = []
    for row in range(BASE_ROWS):
        for column in range(BASE_COLUMNS):
            box = (
                width * column / BASE_COLUMNS,
                height * row / BASE_ROWS,
                width * (column + 1) / BASE_COLUMNS,
                height * (row + 1) / BASE_ROWS,
            )
            items = [
                (sid, point)
                for sid, point in centers.items()
                if box[0] <= point[0] < box[2] and box[1] <= point[1] < box[3]
            ]
            if items:
                pages.extend(split_page(BASE_LABELS[column] + str(row + 1), box, items))
    return sorted(pages, key=lambda page: page["code"])


def render_crop(pixels, map_width, map_height, box, output_path):
    x0, y0, x1, y1 = box
    crop_width, crop_height = x1 - x0, y1 - y0
    rgb = bytearray(crop_width * crop_height * 3)
    for local_y in range(crop_height):
        y = y0 + local_y
        for local_x in range(crop_width):
            x = x0 + local_x
            sid = pixels[y * map_width + x]
            if not sid:
                color = SEA
            else:
                color = LAND_LIGHT if sid & 1 else LAND_SHADE
                neighbors = []
                if x:
                    neighbors.append(pixels[y * map_width + x - 1])
                if x + 1 < map_width:
                    neighbors.append(pixels[y * map_width + x + 1])
                if y:
                    neighbors.append(pixels[(y - 1) * map_width + x])
                if y + 1 < map_height:
                    neighbors.append(pixels[(y + 1) * map_width + x])
                if any(neighbor != sid for neighbor in neighbors):
                    color = BORDER
            offset = (local_y * crop_width + local_x) * 3
            rgb[offset : offset + 3] = bytes(color)
    source.write_png(output_path, crop_width, crop_height, rgb)


def write_index(out_dir, states, names, centers, page_for_state):
    path = out_dir / "atlas_index.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow(["State ID", "Название", "Текущий владелец", "Файл history/states", "Лист", "X карты", "Y карты"])
        for sid in sorted(states):
            x, y = centers[sid]
            writer.writerow([
                sid,
                names.get(sid, "НАЗВАНИЕ НЕ НАЙДЕНО"),
                states[sid].get("owner") or "",
                states[sid]["file"],
                page_for_state[sid],
                round(x),
                round(y),
            ])
    return path


def write_html(out_dir, pages, state_count):
    figures = "\n".join(
        f'<figure><a href="maps/{html.escape(page["code"])}.png">'
        f'<img loading="lazy" src="maps/{html.escape(page["code"])}.png" '
        f'alt="Карта листа {html.escape(page["code"])} с ID регионов"></a>'
        f'<figcaption>Лист {html.escape(page["code"])} · {len(page["state_ids"])} регионов</figcaption></figure>'
        for page in pages
    )
    page = f"""<!doctype html>
<html lang="ru">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Атлас State ID — Nothing Wrong</title>
<style>
body {{ margin: 24px; color: #182731; background: #f4f6f3; font: 16px Segoe UI, Arial, sans-serif; }}
h1 {{ margin-bottom: 6px; }}
p {{ margin-top: 0; color: #40515a; }}
nav {{ margin: 16px 0 22px; }}
nav a {{ margin-right: 18px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 20px; }}
figure {{ margin: 0; }}
figure img {{ display: block; width: 100%; height: auto; }}
figcaption {{ padding: 6px 0 12px; font-weight: 600; }}
</style>
<h1>Атлас регионов HOI4 по State ID</h1>
<p>Все {state_count} активных регионов отмечены один раз. ID — внутренний номер региона; названия, владельцы и имена файлов — в таблице.</p>
<nav><a href="00_locator.png">Указатель листов</a><a href="atlas_index.csv">Таблица State ID</a></nav>
<div class="grid">{figures}</div>
</html>
"""
    path = out_dir / "index.html"
    path.write_text(page, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    work_dir = args.work_dir.resolve()
    out_dir = args.out_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    base_dir = work_dir / "tiles"
    base_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "maps").mkdir(parents=True, exist_ok=True)

    states, province_states, duplicate_provinces = source.load_states()
    colors = source.load_definition(province_states)
    pixels, width, height, _, centers, unknown = source.load_map(colors)
    names = source.load_names()
    names.update(CANON_NAMES)
    if duplicate_provinces:
        raise RuntimeError(f"Duplicate province claims: {duplicate_provinces[:10]}")
    missing_centers = sorted(set(states) - set(centers))
    if missing_centers:
        raise RuntimeError(f"States without map geometry: {missing_centers[:20]}")

    pages = make_pages(centers, width, height)
    page_for_state = {}
    page_manifest = []
    for page in pages:
        for sid in page["state_ids"]:
            if sid in page_for_state:
                raise RuntimeError(f"State {sid} assigned to more than one atlas page")
            page_for_state[sid] = page["code"]

        x0, y0, x1, y1 = page["box"]
        padding = 18
        render_box = (
            max(0, math.floor(x0) - padding),
            max(0, math.floor(y0) - padding),
            min(width, math.ceil(x1) + padding),
            min(height, math.ceil(y1) + padding),
        )
        base_path = base_dir / f'{page["code"]}.base.png'
        render_crop(pixels, width, height, render_box, base_path)
        entries = []
        for sid in page["state_ids"]:
            state = states[sid]
            entries.append({
                "id": sid,
                "name": names.get(sid, "НАЗВАНИЕ НЕ НАЙДЕНО"),
                "owner": state.get("owner"),
                "file": state["file"],
                "center": [centers[sid][0], centers[sid][1]],
            })
        page_manifest.append({
            "code": page["code"],
            "title": f'Лист {page["code"]} · {len(page["state_ids"])} регионов',
            "subtitle": "Цифры — State ID; названия и владельцы — в atlas_index.csv.",
            "bbox": [round(value, 2) for value in page["box"]],
            "render_bbox": list(render_box),
            "base_image": str(base_path),
            "states": entries,
        })

    if set(page_for_state) != set(states):
        missing = sorted(set(states) - set(page_for_state))
        raise RuntimeError(f"Atlas pages do not cover all states: {missing[:20]}")

    root_grid = []
    for row in range(BASE_ROWS):
        for column in range(BASE_COLUMNS):
            root_grid.append({
                "code": BASE_LABELS[column] + str(row + 1),
                "bbox": [
                    round(width * column / BASE_COLUMNS),
                    round(height * row / BASE_ROWS),
                    round(width * (column + 1) / BASE_COLUMNS),
                    round(height * (row + 1) / BASE_ROWS),
                ],
            })

    locator_width = 1800
    locator_height = round(locator_width * height / width)
    locator_path = work_dir / "locator.base.png"
    small = bytearray(locator_width * locator_height * 3)
    for y in range(locator_height):
        source_y = min(height - 1, round(y * height / locator_height))
        for x in range(locator_width):
            source_x = min(width - 1, round(x * width / locator_width))
            sid = pixels[source_y * width + source_x]
            color = SEA if not sid else (LAND_LIGHT if sid & 1 else LAND_SHADE)
            offset = (y * locator_width + x) * 3
            small[offset : offset + 3] = bytes(color)
    source.write_png(locator_path, locator_width, locator_height, small)

    write_index(out_dir, states, names, centers, page_for_state)
    write_html(out_dir, pages, len(states))
    manifest = {
        "source": {
            "game_map": str(source.GAME / "map/provinces.bmp"),
            "mod_states": "history/states",
            "dimensions": [width, height],
            "active_state_count": len(states),
            "mapped_state_count": len(centers),
            "unknown_or_sea_pixels": unknown,
            "duplicate_province_claims": duplicate_provinces,
        },
        "root_grid": root_grid,
        "locator": {
            "title": "АТЛАС STATE ID — УКАЗАТЕЛЬ ЛИСТОВ",
            "subtitle": "Строки 1–2, столбцы A–D; буквенные суффиксы — дополнительные увеличенные листы плотных областей.",
            "footer": "Границы показывают только геометрию штатов; цвет не обозначает владение или политический статус.",
        },
        "pages": page_manifest,
    }
    manifest_path = work_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "active_states": len(states),
        "mapped_states": len(centers),
        "pages": len(pages),
        "page_counts": {page["code"]: len(page["state_ids"]) for page in pages},
        "out_dir": str(out_dir),
        "manifest": str(manifest_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
