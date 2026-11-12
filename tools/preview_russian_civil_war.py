"""Render a design preview from active HOI4 state/map data and the approved initializer.

This does not modify game files. State ownership is shown as scenario-time transfers;
history/states and map geometry remain unchanged.
"""

from __future__ import annotations

from array import array
from collections import defaultdict
import csv
import json
from pathlib import Path
import re
import struct
import sys
import zlib

from pdx_source import atom, parse, val, vals


MOD = Path(__file__).resolve().parents[1]
GAME = Path(r"E:\SteamLibrary\steamapps\common\Hearts of Iron IV")
OUT = MOD / "DESIGN" / "previews" / "russian_civil_war"

# These are the only randomized state assignments in the initializer.
PROBABILISTIC_OUTCOMES = {
    217: [("DNR", 50), ("AKV", 50)],
    236: [("KAL", 50), ("AKV", 50)],
    237: [("KAL", 50), ("AKV", 50)],
    265: [("DNR", 50), ("DON", 50)],
}

# These southern SOV states form a land-disconnected pocket once the approved
# neighboring Ukrainian, Don, and probabilistic outcomes are applied. The
# owner-directed preview correction assigns the whole pocket to Imperial Russia.
SOUTHERN_SOV_ENCLAVE_TO_CROWN = [220, 221, 240, 254, 255, 257, 258, 260]
# These two states were still blue in the owner's close-up of the Crown's south.
SOUTHERN_SOV_GAP_TO_CROWN = [401, 829]
CROWN_SOUTHWARD_STATES = SOUTHERN_SOV_ENCLAVE_TO_CROWN + SOUTHERN_SOV_GAP_TO_CROWN

# The first group is explicit in the author's handoff. The second group is a
# provisional picture to make unsettled borders reviewable, not an implementation.
ACTORS = {
    "SOV": {"name": "Российская республика", "bloc": "Новая Россия", "color": "648EA9", "anchor": 195},
    "CROWN": {"name": "Российская Империя", "bloc": "Белое движение", "color": "D9C28C", "anchor": 239,
              # Fixed state assignments confirmed by the owner against the current overview.
              "ids": [219, 222, 223, 224, 239, 250, 251, 252, 253] + CROWN_SOUTHWARD_STATES,
              "status": "approved"},
    "DON": {"name": "Область Войска Донского", "bloc": "Белое движение · марионетка ВСЮР", "color": "A78C59", "anchor": 218,
            "ids": [218, 227, 228, 238, 245], "cores": [217, 218, 227, 228, 238, 245, 265],
            "status": "approved"},
    "KUB": {"name": "Кубанская область", "bloc": "Белое движение · марионетка ВСЮР", "color": "B39F6B", "anchor": 234,
            "ids": [233, 234, 235], "status": "approved"},
    "AFSR": {"name": "ВСЮР", "bloc": "Белое движение", "color": "8B754E", "anchor": 137,
             "ids": [137], "status": "approved"},
    "RSB": {"name": "Российское Государство", "bloc": "Нейтральное, вне фракций", "color": "C8B07A", "anchor": 570,
            "ids": [sid for sid in range(561, 581) if sid not in {572, 573}] +
                   [40, 329, 516, 637, 644, 654, 822, 824, 874, 876, 877, 878],
            "status": "approved"},
    "BLR": {"name": "Белорусская Народная Республика", "bloc": "Новая Россия",
            "color": "78A8C8", "anchor": 206,
            "ids": [94, 95, 96, 194, 204, 206, 207, 241], "status": "approved"},
    "RUK": {"name": "Украинская рада", "bloc": "Новая Россия", "color": "4CA9AD", "anchor": 202,
            "ids": [93, 192, 193, 196, 197, 198, 199, 200, 201, 202, 203, 225, 226, 259, 834], "status": "approved"},
    "FER": {"name": "Дальневосточная республика", "bloc": "Новая Россия", "color": "4B9D98", "anchor": 408,
            "ids": [408, 409, 560, 657], "status": "approved"},
    "ABK": {"name": "Абхазия", "bloc": "Новая Россия", "color": "52AFC0", "anchor": 826,
            "ids": [826], "status": "approved"},
    "MNT": {"name": "Горская республика", "bloc": "Новая Россия", "color": "68AEB0", "anchor": 232,
            "ids": [232, 821, 827, 828], "status": "approved"},
    "TCF": {"name": "Закавказская федерация", "bloc": "Новая Россия", "color": "539A91", "anchor": 231,
            "ids": [229, 231], "status": "approved"},
    "ARM": {"name": "Армения", "bloc": "Независимые", "color": "B36D86", "anchor": 230,
            "ids": [230, 800], "status": "approved"},
    "KAL": {"name": "Калмыкия", "bloc": "Возможный исход для каждого региона отдельно", "color": "6EA993",
            "anchor": 237, "status": "probabilistic outcome"},
    "DNR": {"name": "Донская Народная Республика", "legend_name": "Донская Народная Республика",
            "map_name": "ДНР", "bloc": "Новая Россия", "color": "457EA3", "anchor": 217,
            "status": "probabilistic outcome"},
    "AKV": {"name": "Совместная администрация Донской и Астраханских казачьих войск",
            "legend_name": "САДТКВ (AKV)", "map_name": "САДТКВ · AKV",
            "bloc": "марионетка Дона · Российская империя",
            "color": "8A8B55", "anchor": 236, "status": "probabilistic outcome"},
    "TRP": {"name": "Турецкая республика", "bloc": "Внешний участник", "color": "C86D5B", "anchor": 354,
            "ids": [353, 354], "status": "approved"},
    "BLF": {"name": "Балтийская федерация", "bloc": "Независимые", "color": "A07CAF", "anchor": 808,
            "ids": [11, 12, 13, 189, 190, 191, 784, 808, 809, 810, 811, 812, 814, 815], "status": "approved"},
    "BLW": {"name": "Прибалтийский союз рабочих", "bloc": "Новая Россия", "color": "578CBA", "anchor": 813,
            "ids": [813], "status": "approved"},
    "KIR": {"name": "Киргизская народная республика", "bloc": "Новая Россия", "color": "70B7A7", "anchor": 590,
            "ids": [583, 588, 590, 882], "status": "approved"},
    "ALA": {"name": "Алаш-Орда", "bloc": "Независимые", "color": "BA7D9B", "anchor": 881,
            "ids": [402, 404, 406, 407, 586, 587, 589, 881], "status": "approved"},
    "TRK": {"name": "Туркестанское ханство", "bloc": "Независимые", "color": "D19279", "anchor": 405,
            "ids": [405, 584, 585, 732, 742, 823, 830, 831, 832], "status": "approved"},
    "POL": {"name": "Польша", "bloc": "Независимые после освобождения", "color": "A475B4", "anchor": 10},
    "FIN": {"name": "Финляндия", "bloc": "Независимые после освобождения", "color": "AA83BA", "anchor": 146},
    "MON": {"name": "Монголия", "bloc": "Независимое нейтральное государство", "color": "BCA177", "anchor": 330},
    "SIK": {"name": "Синьцзян", "bloc": "Независимое нейтральное государство", "color": "C3A573", "anchor": 617},
    "TUR": {"name": "Османская империя", "bloc": "Внешний участник", "color": "D5AD7C", "anchor": 341},
    "JAP": {"name": "Япония / Северный Сахалин", "bloc": "Внешний участник", "color": "D38F91", "anchor": 655,
            "ids": [655], "status": "approved"},
    "ROM": {"name": "Румыния", "bloc": "Внешняя держава", "color": "B87566", "anchor": 79,
            "ids": [78, 766], "status": "approved"},
}

STATE_STATUS_OVERRIDES = {
    **{sid: "approved by author" for sid in CROWN_SOUTHWARD_STATES},
}

REVIEW_STATES = {
    79: "Уже принадлежит ROM в действующем сценарии; дополнительная передача не требуется",
    572: "Оставлен у SOV в превью: исключён из RSB, чтобы не создавать отдельный двухштатный карман",
    573: "Оставлен у SOV в превью: исключён из RSB, чтобы не создавать отдельный двухштатный карман",
}

STATE_PREVIEW_NOTES = {
    **{sid: "Передан Белорусской Народной Республике по прямому указанию владельца"
       for sid in [94, 95, 96, 194, 204, 206, 207, 241]},
    40: "Фиксированная передача RSB по последней карте владельца",
    217: "Случайный исход при начале войны: 50% DNR / 50% AKV. Бросок независим от других регионов",
    236: "Отдельный бросок для каждого штата: 50% KAL / 50% AKV; возможны разные исходы для 236 и 237",
    237: "Отдельный бросок для каждого штата: 50% KAL / 50% AKV; возможны разные исходы для 236 и 237",
    239: "Фиксированное владение Имперской России (CROWN) по карте владельца",
    **{sid: "Передан Имперской России по просьбе владельца: устранён изолированный южный карман SOV в превью"
       for sid in SOUTHERN_SOV_ENCLAVE_TO_CROWN},
    **{sid: "Добавлен к южному контуру Имперской России по отмеченному владельцем участку; только превью"
       for sid in SOUTHERN_SOV_GAP_TO_CROWN},
    265: "Случайный исход при начале войны: 50% DNR / 50% DON. Бросок независим от других регионов",
    329: "Фиксированная передача RSB по последней карте владельца",
    654: "Фиксированная передача RSB по последней карте владельца",
    742: "Фиксированная передача TRK по последней карте владельца",
    814: "Фиксированная передача BLF по последней карте владельца",
}

VIEWS = {
    "overview": {"ids": [11, 13, 78, 93, 94, 95, 96, 137, 192, 194, 195, 204, 206, 207, 218, 219, 230, 235, 236, 241, 353, 354, 404, 405, 408, 409, 560,
                         570, 583, 590, 655, 657, 766, 800, 821, 826, 830, 834, 881, 882], "pad": (160, 120), "size": (2400, 1160)},
    "europe": {"ids": [11, 13, 78, 79, 93, 94, 95, 96, 137, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 206, 207, 217, 218, 219, 227, 228, 233, 234, 235, 236, 237, 238, 241,
                       245, 250, 251, 252, 253, 259, 265, 766, 784, 808, 813, 834], "pad": (90, 90), "size": (2200, 1300)},
    "caucasus": {"ids": [137, 218, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 245,
                         353, 354, 800, 821, 826, 827, 828], "pad": (75, 75), "size": (2100, 1300)},
    "moldova": {"ids": [78, 79, 80, 89, 91, 192, 197, 198, 199, 203, 766, 834],
                "pad": (65, 65), "size": (1500, 1050)},
    "central_asia": {"ids": [402, 404, 405, 406, 407, 583, 584, 585, 586, 587, 588, 589, 590, 732, 823, 830, 881, 882],
                     "pad": (90, 80), "size": (2100, 1250)},
    "east": {"ids": [408, 409, 560, 561, 564, 570, 574, 580, 637, 644, 655, 657],
             "pad": (105, 100), "size": (2200, 1300)},
}


def color(hex_string):
    return tuple(bytes.fromhex(hex_string))


def load_names():
    paths = [GAME / "localisation/russian/state_names_l_russian.yml",
             MOD / "localisation/replace/nw_state_names_l_russian.yml"]
    names = {}
    pattern = re.compile(r'^\s*STATE_(\d+):\d*\s+"([^"]+)"')
    for path in paths:
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            match = pattern.match(line)
            if match:
                names[int(match[1])] = match[2]
    return names


def load_states():
    result = {}
    province_states = {}
    duplicate_provinces = []
    for path in sorted((MOD / "history/states").glob("*.txt")):
        block = val(parse(path.read_text(encoding="utf-8-sig")), "state")
        sid = int(atom(val(block, "id")))
        history = val(block, "history")
        provinces = [int(atom(node.value)) for node in val(block, "provinces") if node.key is None]
        result[sid] = {
            "file": path.name,
            "owner": atom(val(history, "owner")),
            "controller": atom(val(history, "controller")),
            "cores": [atom(value) for value in vals(history, "add_core_of")],
            "provinces": provinces,
        }
        for province in provinces:
            previous = province_states.setdefault(province, sid)
            if previous != sid:
                duplicate_provinces.append((province, previous, sid))
    return result, province_states, duplicate_provinces


def load_definition(province_states):
    colors = {}
    for line in (GAME / "map/definition.csv").read_text(encoding="utf-8-sig").splitlines():
        fields = line.split(";")
        if len(fields) < 4 or not fields[0].isdigit():
            continue
        province = int(fields[0])
        key = (int(fields[1]) << 16) | (int(fields[2]) << 8) | int(fields[3])
        colors[key] = province_states.get(province, 0)
    return colors


def load_map(province_colors):
    path = GAME / "map/provinces.bmp"
    bmp = path.read_bytes()
    if bmp[:2] != b"BM":
        raise ValueError("provinces.bmp is not BMP")
    offset = struct.unpack_from("<I", bmp, 10)[0]
    width, height = struct.unpack_from("<ii", bmp, 18)
    bpp = struct.unpack_from("<H", bmp, 28)[0]
    compression = struct.unpack_from("<I", bmp, 30)[0]
    if width <= 0 or height <= 0 or bpp != 24 or compression:
        raise ValueError(f"Unexpected province BMP: {width}x{height} {bpp}bpp compression={compression}")
    stride = ((width * 3 + 3) // 4) * 4
    pixels = array("H", [0]) * (width * height)
    bounds = {}
    sums = defaultdict(lambda: [0, 0, 0])
    unknown = 0
    for bottom_row in range(height):
        y = height - bottom_row - 1
        row_start = offset + bottom_row * stride
        out_start = y * width
        for x in range(width):
            i = row_start + x * 3
            sid = province_colors.get((bmp[i + 2] << 16) | (bmp[i + 1] << 8) | bmp[i], 0)
            pixels[out_start + x] = sid
            if sid:
                if sid not in bounds:
                    bounds[sid] = [x, y, x, y]
                else:
                    box = bounds[sid]
                    if x < box[0]: box[0] = x
                    if y < box[1]: box[1] = y
                    if x > box[2]: box[2] = x
                    if y > box[3]: box[3] = y
                entry = sums[sid]
                entry[0] += x
                entry[1] += y
                entry[2] += 1
            else:
                unknown += 1
    centers = {sid: (total[0] / total[2], total[1] / total[2]) for sid, total in sums.items()}
    return pixels, width, height, bounds, centers, unknown


def adjacencies(pixels, width, height):
    touching = set()
    for y in range(height):
        base = y * width
        for x in range(width):
            sid = pixels[base + x]
            if not sid:
                continue
            if x:
                other = pixels[base + x - 1]
                if other and other != sid:
                    touching.add(tuple(sorted((sid, other))))
            if y:
                other = pixels[base + x - width]
                if other and other != sid:
                    touching.add(tuple(sorted((sid, other))))
    return touching


def components(ids, touching):
    remaining = set(ids)
    found = []
    while remaining:
        seed = remaining.pop()
        connected = {seed}
        queue = [seed]
        while queue:
            item = queue.pop()
            for neighbor in tuple(remaining):
                if tuple(sorted((item, neighbor))) in touching:
                    remaining.remove(neighbor)
                    connected.add(neighbor)
                    queue.append(neighbor)
        found.append(sorted(connected))
    return sorted(found, key=lambda part: (-len(part), part))


def assignment(states):
    owners = {sid: info["owner"] for sid, info in states.items()}
    statuses = {}
    collisions = []
    for actor, spec in ACTORS.items():
        for sid in spec.get("ids", []):
            if sid not in states:
                collisions.append(f"{actor}: missing State {sid}")
                continue
            if sid in statuses:
                collisions.append(f"State {sid}: assigned twice ({owners[sid]}, {actor})")
            if states[sid]["owner"] not in {"SOV", actor}:
                collisions.append(f"State {sid}: currently {states[sid]['owner']}, planned {actor}")
            owners[sid] = actor
            statuses[sid] = spec["status"]
    return owners, statuses, collisions


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path, width, height, rgb):
    rows = bytearray()
    stride = width * 3
    for y in range(height):
        rows.append(0)
        rows.extend(rgb[y * stride:(y + 1) * stride])
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(rows, 6)) + chunk(b"IEND", b"")
    path.write_bytes(png)


def view_crop(spec, bounds, width, height):
    boxes = [bounds[sid] for sid in spec["ids"] if sid in bounds]
    if not boxes:
        raise ValueError("View has no mapped states")
    padx, pady = spec["pad"]
    x0 = max(0, min(box[0] for box in boxes) - padx)
    y0 = max(0, min(box[1] for box in boxes) - pady)
    x1 = min(width - 1, max(box[2] for box in boxes) + padx)
    y1 = min(height - 1, max(box[3] for box in boxes) + pady)
    return x0, y0, x1, y1


def render(name, spec, pixels, width, height, bounds, centers, owners, statuses):
    x0, y0, x1, y1 = view_crop(spec, bounds, width, height)
    crop_w, crop_h = x1 - x0 + 1, y1 - y0 + 1
    max_w, max_h = spec["size"]
    scale = min(max_w / crop_w, max_h / crop_h)
    out_w, out_h = max(1, round(crop_w * scale)), max(1, round(crop_h * scale))
    rgb = bytearray(out_w * out_h * 3)
    sid_grid = array("H", [0]) * (out_w * out_h)
    tag_grid = []
    for y in range(out_h):
        src_y = y0 + min(crop_h - 1, int(y / scale))
        for x in range(out_w):
            src_x = x0 + min(crop_w - 1, int(x / scale))
            index = y * out_w + x
            sid = pixels[src_y * width + src_x]
            sid_grid[index] = sid
            tag = owners.get(sid, "SEA") if sid else "SEA"
            is_probabilistic = sid in PROBABILISTIC_OUTCOMES
            # Keep random-color stripes inside one political outline; their
            # actor is selected independently per state, not per pixel.
            tag_grid.append("PROB" if is_probabilistic else tag)
            if is_probabilistic:
                outcomes = PROBABILISTIC_OUTCOMES[sid]
                stripe = ((x + y) // 7) % len(outcomes)
                value = color(ACTORS[outcomes[stripe][0]]["color"])
            elif tag == "SEA":
                value = (190, 213, 218)
            elif tag in ACTORS:
                value = color(ACTORS[tag]["color"])
            elif tag == "SOV":
                value = color(ACTORS["SOV"]["color"])
            else:
                value = (197, 197, 188)
            if sid in statuses and statuses[sid] in {"proposed", "legacy proposal", "range pending review"}:
                if (x + y) % 12 < 3:
                    value = tuple(min(255, part + 29) for part in value)
            rgb[index * 3:index * 3 + 3] = bytes(value)
    for y in range(1, out_h):
        for x in range(1, out_w):
            index = y * out_w + x
            left = index - 1
            above = index - out_w
            if not sid_grid[index]:
                continue
            if tag_grid[index] != tag_grid[left] and sid_grid[left]:
                rgb[index * 3:index * 3 + 3] = b"\x17\x26\x33"
                rgb[left * 3:left * 3 + 3] = b"\x17\x26\x33"
            elif sid_grid[index] != sid_grid[left] and sid_grid[left]:
                rgb[index * 3:index * 3 + 3] = b"\x58\x68\x71"
            if tag_grid[index] != tag_grid[above] and sid_grid[above]:
                rgb[index * 3:index * 3 + 3] = b"\x17\x26\x33"
                rgb[above * 3:above * 3 + 3] = b"\x17\x26\x33"
            elif sid_grid[index] != sid_grid[above] and sid_grid[above]:
                rgb[index * 3:index * 3 + 3] = b"\x58\x68\x71"
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}_base.png"
    write_png(path, out_w, out_h, rgb)
    anchors = {}
    for actor, actor_spec in ACTORS.items():
        sid = actor_spec.get("anchor")
        if sid in centers:
            cx, cy = centers[sid]
            if x0 <= cx <= x1 and y0 <= cy <= y1:
                anchors[actor] = [round((cx - x0) * scale), round((cy - y0) * scale)]
    return {"image": str(path.relative_to(MOD)).replace("\\", "/"), "crop": [x0, y0, x1, y1],
            "size": [out_w, out_h], "scale": scale, "anchors": anchors}


def main():
    names = load_names()
    states, province_states, duplicate_provinces = load_states()
    province_colors = load_definition(province_states)
    pixels, width, height, bounds, centers, unknown = load_map(province_colors)
    touching = adjacencies(pixels, width, height)
    owners, statuses, collisions = assignment(states)
    statuses.update(STATE_STATUS_OVERRIDES)
    for sid, outcomes in PROBABILISTIC_OUTCOMES.items():
        if sum(chance for _, chance in outcomes) != 100:
            raise ValueError(f"State {sid}: probabilistic outcome weights must sum to 100")
        if any(actor not in ACTORS for actor, _ in outcomes):
            raise ValueError(f"State {sid}: outcome references an unknown preview actor")
    requested = sorted({sid for spec in ACTORS.values()
                        for sid in spec.get("ids", []) + spec.get("cores", [])} |
                       set(REVIEW_STATES) | set(PROBABILISTIC_OUTCOMES))
    audit = {
        "source": {"game_map": str(GAME / "map/provinces.bmp"), "mod_states": "history/states",
                   "dimensions": [width, height], "unmapped_or_sea_pixels": unknown,
                   "state_count": len(states), "duplicate_province_claims": duplicate_provinces[:20]},
        "collisions": collisions,
        "probabilistic_outcomes": {
            str(sid): [{"actor": actor, "name": ACTORS[actor]["name"], "chance_percent": chance}
                       for actor, chance in outcomes]
            for sid, outcomes in PROBABILISTIC_OUTCOMES.items()
        },
        "actors": {},
        "states": {},
        "views": {},
    }
    for actor, spec in ACTORS.items():
        ids = spec.get("ids", [])
        audit["actors"][actor] = dict(spec)
        if ids:
            audit["actors"][actor]["land_components"] = components(ids, touching)
    for sid in requested:
        info = states.get(sid, {})
        probabilistic = PROBABILISTIC_OUTCOMES.get(sid)
        core_only = (sid in ACTORS["DON"]["cores"] and sid not in ACTORS["DON"].get("ids", [])
                     and not probabilistic)
        status = ("approved probabilistic outcomes (50/50)" if probabilistic else
                  "approved DON core only" if core_only else
                  REVIEW_STATES.get(sid, STATE_STATUS_OVERRIDES.get(sid, statuses.get(sid))))
        entry = {"name": names.get(sid, "?"), "before": info.get("owner"),
                 "after_preview": ("50/50 outcomes" if probabilistic else owners.get(sid)),
                 "status": status, "note": STATE_PREVIEW_NOTES.get(sid),
                 "file": info.get("file"), "center": centers.get(sid)}
        if probabilistic:
            entry["outcomes"] = [{"actor": actor, "name": ACTORS[actor]["name"], "chance_percent": chance}
                                 for actor, chance in probabilistic]
        audit["states"][str(sid)] = entry
    if "--audit" not in sys.argv:
        for name, spec in VIEWS.items():
            audit["views"][name] = render(name, spec, pixels, width, height, bounds, centers, owners, statuses)
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "preview_data.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        with (OUT / "preview_territories.csv").open("w", encoding="utf-8-sig", newline="") as table:
            writer = csv.writer(table, delimiter=";")
            writer.writerow(["State ID", "Название", "Владелец до войны", "Владелец в превью",
                             "Статус", "Блок / роль", "Вероятностные исходы", "Примечание"])
            for sid in requested:
                entry = audit["states"][str(sid)]
                after = entry["after_preview"]
                bloc = ACTORS.get(after, {}).get("bloc", "Текущий владелец")
                outcomes = entry.get("outcomes", [])
                outcome_text = " / ".join(f"{item['actor']} — {item['chance_percent']}%" for item in outcomes)
                if outcomes:
                    after = "50/50"
                    bloc = "Независимые исходы по State ID"
                if entry["status"] == "approved DON core only":
                    bloc = "Национальный регион Дона; владение не меняется"
                elif sid in REVIEW_STATES:
                    bloc = REVIEW_STATES[sid]
                writer.writerow([sid, entry["name"], entry["before"], after,
                                 entry["status"] or "current owner", bloc, outcome_text, entry["note"] or ""])
        print("Preview data and base PNGs:", OUT)
    else:
        print(json.dumps({"source": audit["source"], "collisions": collisions,
                          "components": {actor: item.get("land_components", []) for actor, item in audit["actors"].items()
                                         if "land_components" in item}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
