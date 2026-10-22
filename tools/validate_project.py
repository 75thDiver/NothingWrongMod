"""Portable, read-only source checks. Does not emulate or launch HOI4."""

from pathlib import Path
import json
import re

from pdx_source import atom, parse, val, vals


MOD = Path(__file__).resolve().parents[1]
checks = []
warnings = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def load(path):
    return parse(path.read_text(encoding="utf-8-sig"))


focuses = {}
trees = {}
for path in sorted((MOD / "common/national_focus").glob("*.txt")):
    for tree in vals(load(path), "focus_tree"):
        tree_id = atom(val(tree, "id"))
        check("unique tree " + tree_id, tree_id not in trees)
        trees[tree_id] = tree
        for focus in vals(tree, "focus"):
            focus_id = atom(val(focus, "id"))
            check("unique focus " + focus_id, focus_id not in focuses)
            focuses[focus_id] = focus

for focus_id, focus in focuses.items():
    for prerequisite in vals(focus, "prerequisite"):
        references = [atom(item) for item in vals(prerequisite, "focus")]
        check(focus_id + ": prerequisites exist", all(reference in focuses for reference in references))
        if len(references) > 1:
            warnings.append(
                {"focus": focus_id, "kind": "OR prerequisite, review only", "members": references}
            )
    for reference in vals(focus, "relative_position_id"):
        check(focus_id + ": relative parent exists", atom(reference) in focuses)

positions = {}
pending = set()


def position(focus_id):
    if focus_id in positions:
        return positions[focus_id]
    check(focus_id + ": no relative-position cycle", focus_id not in pending)
    pending.add(focus_id)
    focus = focuses[focus_id]
    x = float(val(focus, "x", "0"))
    y = float(val(focus, "y", "0"))
    parent = atom(val(focus, "relative_position_id"))
    if parent:
        parent_x, parent_y = position(parent)
        x += parent_x
        y += parent_y
    positions[focus_id] = (x, y)
    pending.remove(focus_id)
    return x, y


for focus_id in focuses:
    position(focus_id)

for tree_id, tree in trees.items():
    occupied = {}
    for focus in vals(tree, "focus"):
        focus_id = atom(val(focus, "id"))
        coordinates = positions[focus_id]
        if coordinates in occupied:
            warnings.append(
                {
                    "tree": tree_id,
                    "kind": "same resolved position",
                    "focuses": [occupied[coordinates], focus_id],
                    "position": coordinates,
                }
            )
        occupied[coordinates] = focus_id

check("generic_focus restored", "generic_focus" in trees and "liberty_ethos" in focuses)
check(
    "only NW generic is default",
    [tree_id for tree_id, tree in trees.items() if val(tree, "default") == "yes"]
    == ["NW_generic_development"],
)

protected = {
    "NW14_SOV_succession_memorandum": "NW14_SOV_medical_council",
    "NW14_SOV_russian_crossroads": "NW14_SOV_succession_memorandum",
    "NW14_SOV_mobilisation_depots": "NW14_SOV_eastern_audit",
}
protected.update(
    {
        "NW14_SOV_" + branch + "_long_final": "NW14_SOV_" + branch + "_long_17"
        for branch in ("kirill", "sr", "menshevik", "bolshevik", "black")
    }
)
for focus_id, expected in protected.items():
    actual = [vals(block, "focus") for block in vals(focuses[focus_id], "prerequisite")]
    check(focus_id + ": approved prerequisite retained", actual == [[expected]])

states = list((MOD / "history/states").glob("*.txt"))
check("1081 state files present", len(states) == 1081)

for folder, width, height in [("", 82, 52), ("medium", 41, 26), ("small", 10, 7)]:
    for name in ("NW_POLISH_KINGDOM", "NW_FINNISH_DUCHY", "FIN_democratic"):
        path = MOD / "gfx/flags" / folder / (name + ".tga")
        header = path.read_bytes()[:18]
        check(
            (folder or "large") + "/" + name + ": uncompressed truecolor TGA and size",
            header[2] == 2
            and int.from_bytes(header[12:14], "little") == width
            and int.from_bytes(header[14:16], "little") == height,
        )

localisation_files = sorted((MOD / "localisation").rglob("*.yml"))
localisation_keys = {}
key_pattern = re.compile(r"^\s{1,2}([^\s:#]+):\d*\s")
for path in localisation_files:
    raw = path.read_bytes()
    check(path.relative_to(MOD).as_posix() + ": UTF-8 BOM", raw.startswith(b"\xef\xbb\xbf"))
    text = raw.decode("utf-8-sig")
    check(path.relative_to(MOD).as_posix() + ": russian header", text.startswith("l_russian:"))
    for line_number, line in enumerate(text.splitlines(), 1):
        match = key_pattern.match(line)
        if not match:
            continue
        key = match.group(1)
        if key in localisation_keys:
            warnings.append(
                {
                    "kind": "duplicate localisation key",
                    "key": key,
                    "first": localisation_keys[key],
                    "again": f"{path.relative_to(MOD).as_posix()}:{line_number}",
                }
            )
        else:
            localisation_keys[key] = f"{path.relative_to(MOD).as_posix()}:{line_number}"

print(
    json.dumps(
        {
            "game_executed": False,
            "passed_checks": len(checks),
            "focus_count": len(focuses),
            "trees": {tree_id: len(vals(tree, "focus")) for tree_id, tree in trees.items()},
            "state_count": len(states),
            "localisation_files": len(localisation_files),
            "localisation_keys": len(localisation_keys),
            "warnings": warnings,
            "limitations": [
                "Static source check only; this is not a rendered HOI4 view or engine run.",
                "DLC equipment behavior still requires a clean in-game matrix test.",
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
)

