"""Bounded source-model tests for recipient selection; not a HOI4 emulator."""
import unittest
from pathlib import Path
from pdx_source import atom, parse, val, walk

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / 'common/on_actions/14_nw_russian_civil_war_capitulation.txt'
EVENTS = ROOT / 'events/14_nw_russian_civil_war_super_event.txt'


def has_term(nodes, key, expected=None):
    return any(
        node.key == key and (expected is None or atom(node.value) == expected)
        for node in walk(nodes)
    )


def find_nodes(nodes, key):
    return [node for node in walk(nodes) if node.key == key]


class Model:
    def __init__(self, winner, overlords=None, eligible=(), participant=True, war=True, active=True, loser="LOS", existing=(), factions=None, enemies=()):
        self.winner = winner
        self.loser = loser
        self.existing = set(existing) | {winner, loser} | set(eligible) | set((overlords or {}).keys()) | set((overlords or {}).values())
        self.factions = factions or {}
        self.enemies = {frozenset(pair) for pair in enemies}
        self.overlords = overlords or {}
        self.flags = {loser: ({'nw14_cw_participant', 'nw14_cw_active'} if active else {'nw14_cw_participant'}) if participant else set()}
        for tag in eligible:
            self.flags.setdefault(tag, set()).update({'nw14_cw_annex_victor', 'nw14_cw_active', 'nw14_cw_participant'})
        self.flags.setdefault(winner, set()).add('nw14_cw_active')
        self.war = war
        self.annexed = []

    def scope(self, key, current):
        return {'ROOT': self.loser, 'FROM': self.winner,
                'OVERLORD': self.overlords.get(current)}.get(key, key)

    def conditions(self, nodes, current):
        results = []
        for n in nodes:
            key, value = n.key, n.value
            if key in ('OR', 'AND', 'NOT'):
                bits = [self.conditions([item], current) for item in value]
                results.append(any(bits) if key == 'OR' else not any(bits) if key == 'NOT' else all(bits))
            elif key == 'has_country_flag':
                results.append(value in self.flags.get(current, set()))
            elif key == 'is_faction_leader':
                results.append(False)
            elif key == 'exists':
                results.append(current in self.existing)
            elif key == 'any_enemy_country':
                enemy = self.winner if current == self.loser else self.loser
                results.append(self.war and self.conditions(value, enemy))
            elif key == 'has_war_with':
                other = self.scope(value, current)
                results.append(frozenset((current, other)) in self.enemies or (self.war and other == self.loser and (current == self.winner or current in self.overlords.values())))
            elif key == 'is_subject':
                results.append((current in self.overlords) == (value == 'yes'))
            elif key == 'is_subject_of':
                results.append(self.overlords.get(current) == self.scope(value, current))
            elif key == 'is_in_faction_with':
                other = self.scope(value, current)
                results.append(current in self.factions and self.factions.get(current) == self.factions.get(other))
            elif key == 'tag':
                results.append(current == self.scope(value, current))
            elif isinstance(value, list):
                results.append(self.conditions(value, self.scope(key, current)))
            else:
                raise AssertionError('Unsupported condition: ' + str(key))
        return all(results)

    def effects(self, nodes, current=None):
        if current is None:
            current = self.loser
        taken = False
        for n in nodes:
            if n.key in ('if', 'else_if', 'else'):
                if n.key == 'if':
                    taken = False
                if not taken and (n.key == 'else' or self.conditions(val(n.value, 'limit', []), current)):
                    self.effects([x for x in n.value if x.key != 'limit'], current)
                    taken = True
            elif n.key == 'set_country_flag':
                self.flags.setdefault(current, set()).add(n.value)
            elif n.key == 'clr_country_flag':
                self.flags.setdefault(current, set()).discard(n.value)
            elif n.key == 'annex_country':
                self.annexed.append((current, self.scope(val(n.value, 'target'), current)))
            elif n.key == 'log':
                pass
            elif isinstance(n.value, list):
                self.effects(n.value, self.scope(n.key, current))
            else:
                raise AssertionError('Unsupported effect: ' + str(n.key))

    def run(self):
        hook = val(val(parse(HOOK.read_text()), 'on_actions'), 'on_capitulation')
        self.effects(val(hook, 'effect'))
        return self.annexed


class RecipientTests(unittest.TestCase):
    def test_claimant_on_victor_side_receives_the_entire_defeated_country(self):
        cases = [
            dict(winner='SOV', loser='BLF', existing=('BLW',), factions={'SOV':'NEW', 'BLW':'NEW'}, expected='BLW'),
            dict(winner='SOV', loser='BLW', existing=('BLF',), factions={'SOV':'NEW', 'BLF':'NEW'}, expected='BLF'),
            dict(winner='AFS', loser='DNR', existing=('DON',), overlords={'DON':'AFS'}, expected='DON'),
            dict(winner='ROY', loser='DNR', existing=('DON',), overlords={'DON':'AFS'}, factions={'ROY':'WHITE', 'AFS':'WHITE'}, expected='DON'),
            dict(winner='KUB', loser='DNR', existing=('DON',), overlords={'DON':'AFS', 'KUB':'AFS'}, expected='DON'),
            dict(winner='SOV', loser='DON', existing=('DNR',), factions={'SOV':'NEW', 'DNR':'NEW'}, expected='DNR'),
            dict(winner='ALA', loser='KIR', existing=('ALA',), expected='ALA'),
        ]
        for case in cases:
            expected = case.pop('expected')
            with self.subTest(case=case):
                self.assertEqual(Model(**case).run(), [(expected, case['loser'])])

    def test_absent_or_hostile_claimant_falls_back_to_special_victor(self):
        self.assertEqual(Model('SOV', loser='BLF', eligible=('SOV',)).run(), [('SOV','BLF')])
        self.assertEqual(Model('SOV', loser='BLF', eligible=('SOV',), existing=('BLW',), factions={'SOV':'NEW','BLW':'NEW'}, enemies=(('SOV','BLW'),)).run(), [('SOV','BLF')])
        self.assertEqual(Model('SOV', loser='KIR', eligible=('SOV',), existing=('ALA',), enemies=(('SOV','ALA'),)).run(), [('SOV','KIR')])

    def test_four_independent_victors_without_faction_leadership(self):
        for tag in ('SOV', 'ROY', 'RSB', 'AFS'):
            with self.subTest(tag=tag):
                self.assertEqual(Model(tag, eligible=(tag,)).run(), [(tag, 'LOS')])

    def test_direct_puppet_victory_goes_to_eligible_overlord(self):
        self.assertEqual(Model('DON', {'DON': 'AFS'}, ('AFS',)).run(), [('AFS', 'LOS')])
        self.assertEqual(Model('KUB', {'KUB': 'AFS'}, ('AFS',)).run(), [('AFS', 'LOS')])

    def test_special_regime_that_is_a_subject_does_not_take_land_itself(self):
        self.assertEqual(Model('RSB', {'RSB': 'SOV'}, ('RSB', 'SOV')).run(), [('SOV', 'LOS')])
        self.assertEqual(Model('AFS', {'AFS': 'GER'}, ('AFS',)).run(), [])

    def test_known_akv_don_afs_chain(self):
        self.assertEqual(Model('AKV', {'AKV': 'DON', 'DON': 'AFS'}, ('AFS',)).run(), [('AFS', 'LOS')])

    def test_unrelated_multilevel_chain_does_not_get_special_rule(self):
        self.assertEqual(Model('ABC', {'ABC': 'DON', 'DON': 'AFS'}, ('AFS',)).run(), [])

    def test_unrelated_winner_loser_and_peace_are_ignored(self):
        self.assertEqual(Model('GER', eligible=('SOV',)).run(), [])
        self.assertEqual(Model('SOV', eligible=('SOV',), participant=False).run(), [])
        self.assertEqual(Model('SOV', eligible=('SOV',), war=False).run(), [])
        self.assertEqual(Model('SOV', eligible=('SOV',), active=False).run(), [])

    def test_daily_cleanup_preserves_active_front_and_excludes_later_war(self):
        hook = val(val(parse(HOOK.read_text()), 'on_actions'), 'on_daily')
        model = Model('SOV', eligible=('SOV',))
        model.effects(val(hook, 'effect'))
        self.assertIn('nw14_cw_active', model.flags['LOS'])
        model.war = False
        model.effects(val(hook, 'effect'))
        self.assertNotIn('nw14_cw_active', model.flags['LOS'])
        model.war = True
        self.assertEqual(model.run(), [])

    def test_repeated_callback_is_idempotent(self):
        model = Model('RSB', eligible=('RSB',))
        model.run()
        self.assertEqual(model.run(), [('RSB', 'LOS')])


class PolandFinlandTests(unittest.TestCase):
    def setUp(self):
        self.hook = val(val(parse(HOOK.read_text(encoding='utf-8')), 'on_actions'), 'on_capitulation')
        self.hook_effect = val(self.hook, 'effect')

    def test_poland_and_finland_become_sov_puppets_only_after_new_russia_victory(self):
        for tag, cosmetic in (
            ('POL', 'NW_POLISH_PEOPLES_REPUBLIC'),
            ('FIN', 'NW_FINNISH_FEDERATION'),
        ):
            with self.subTest(tag=tag):
                matching = [
                    node for node in find_nodes(self.hook_effect, 'if') + find_nodes(self.hook_effect, 'else_if')
                    if atom(val(val(node.value, 'limit', []), 'tag')) == tag
                    and has_term(node.value, 'set_cosmetic_tag', cosmetic)
                ]
                self.assertTrue(matching, f'missing narrow {tag} capitulation branch')
                branch = matching[0]
                sov = val(branch.value, 'SOV', [])
                sov_limit = val(val(branch.value, 'limit', []), 'SOV', [])
                self.assertTrue(has_term(sov, 'puppet', 'ROOT'))
                self.assertTrue(has_term(branch.value, 'set_cosmetic_tag', cosmetic))
                self.assertTrue(has_term(sov_limit, 'has_country_flag', 'nw_rus_war_started'))
                self.assertTrue(has_term(val(val(branch.value, 'limit', []), 'FROM', []), 'is_in_faction_with', 'SOV'))
                self.assertFalse(has_term(branch.value, 'annex_country'))

    def test_polish_capitulation_queues_one_offer_for_an_independent_finland(self):
        candidates = [
            node for node in find_nodes(self.hook_effect, 'if')
            if atom(val(val(node.value, 'limit', []), 'tag')) == 'POL'
        ]
        self.assertTrue(candidates, 'missing Poland capitulation dispatch')
        fin_scope = val(candidates[0].value, 'FIN', [])
        self.assertTrue(has_term(fin_scope, 'set_country_flag', 'nw14_fin_white_offer_fired'))
        event_nodes = find_nodes(fin_scope, 'country_event')
        self.assertTrue(any(atom(val(node.value, 'id')) == 'nw14cw.4' for node in event_nodes))

    def test_finland_offer_can_make_white_peace_and_join_white_movement(self):
        events = parse(EVENTS.read_text(encoding='utf-8'))
        event = next(
            node for node in find_nodes(events, 'country_event')
            if atom(val(node.value, 'id')) == 'nw14cw.4'
        )
        options = find_nodes(event.value, 'option')
        self.assertTrue(has_term(event.value, 'is_triggered_only', 'yes'))
        accept = next(node for node in options if atom(val(node.value, 'name')) == 'nw14cw.4.a')
        decline = next(node for node in options if atom(val(node.value, 'name')) == 'nw14cw.4.b')
        self.assertTrue(has_term(accept.value, 'white_peace'))
        self.assertTrue(has_term(accept.value, 'add_to_faction'))
        self.assertFalse(has_term(decline.value, 'white_peace'))
        self.assertFalse(has_term(decline.value, 'add_to_faction'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
