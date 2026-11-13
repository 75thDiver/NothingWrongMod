"""Read-only inventory of declared CW effects, not an interpreter of HOI4."""

import hashlib
import json
import re
from pathlib import Path

from pdx_source import atom, parse, val, vals, walk

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'common/scripted_effects/14_nw_russian_civil_war.txt'
ROYAL = 'event_target:nw14_rus_royal'


def inventory(root=ROOT):
    source = root / SOURCE.relative_to(ROOT)
    text = source.read_text(encoding='utf-8-sig')
    actors = {}

    def actor(tag):
        return actors.setdefault(tag, {'scope': tag, 'statements': []})

    def visit(nodes, scope='SOV'):
        for node in nodes:
            key = node.key or ''
            if key == 'limit':
                continue  # Conditions are not executed effects.
            if re.fullmatch(r'[A-Z]{3}', key) or key == ROYAL:
                visit(node.value, key)
            elif key == 'start_civil_war':
                actor(ROYAL)['split_states'] = [int(n.value) for n in val(node.value, 'states', [])]
            elif key in {'transfer_state', 'set_capital', 'load_oob', 'add_ideas',
                         'remove_ideas', 'create_faction', 'add_to_faction', 'puppet'}:
                value = node.value
                if key == 'set_capital':
                    value = val(value, 'state')
                if isinstance(value, list):
                    value = [atom(n.value) for n in value]
                actor(scope)['statements'].append({
                    'key': key, 'value': atom(value),
                    'line': text.count('\n', 0, node.begin) + 1,
                })
            elif isinstance(node.value, list):
                visit(node.value, scope)

    visit(val(parse(text), 'nw14_rus_civil_war_start'))
    # FIN/POL already exist, keep their history OOB; other detached neutrals
    # MON/SIK and territorial recipients ROM/JAP are recorded but not CW armies.
    for tag in ('FIN', 'POL'):
        actor(tag)
    province_states = {}
    for path in (root / 'history/states').glob('*.txt'):
        state = val(parse(path.read_text(encoding='utf-8-sig')), 'state')
        state_id = int(val(state, 'id'))
        for province in val(state, 'provinces', []):
            province_states.setdefault(int(province.value), []).append(state_id)

    for tag, record in actors.items():
        histories = sorted((root / 'history/countries').glob(f'{tag} - *.txt'))
        history = parse(histories[0].read_text(encoding='utf-8-sig')) if histories else []
        record['history'] = [p.relative_to(root).as_posix() for p in histories]
        record['history_ideas'] = [atom(n.value) for b in vals(history, 'add_ideas')
                                   for n in (b if isinstance(b, list) else [])]
        record['history_oob'] = [atom(v) for v in vals(history, 'oob')]
        record['history_capital'] = val(history, 'capital')
        names = [s['value'] for s in record['statements'] if s['key'] == 'load_oob']
        if tag in ('FIN', 'POL'):
            names += record['history_oob']
        record['oobs'] = []
        for name in sorted(set(names)):
            path = root / 'history/units' / f'{name}.txt'
            info = {'name': name, 'exists': path.is_file()}
            if path.is_file():
                nodes = parse(path.read_text(encoding='utf-8-sig'))
                templates = [atom(val(b, 'name')) for b in vals(nodes, 'division_template')]
                divisions = [n.value for n in walk(nodes) if n.key == 'division']
                references = [atom(val(b, 'division_template')) for b in divisions]
                info.update(division_count=len(divisions), templates=templates,
                            missing_templates=sorted(set(references) - set(templates)),
                            location_states={str(val(b, 'location')):
                                             province_states.get(int(val(b, 'location')), [])
                                             for b in divisions})
            record['oobs'].append(info)
    return {'game_executed': False,
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'limitations': ['Declared statements only; conditions/random branches are not simulated.',
                            'History ideas exclude later focus/event effects and engine inheritance.',
                            'No claim of runtime army counts, war membership or spirit assignment.'],
            'actors': list(actors.values())}


if __name__ == '__main__':
    print(json.dumps(inventory(), ensure_ascii=False, indent=2))
