from __future__ import annotations

import csv
import os
import re
import struct
import unittest
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "DESIGN" / "previews" / "russian_civil_war" / "preview_territories.csv"
EFFECT = ROOT / "common" / "scripted_effects" / "14_nw_russian_civil_war.txt"
LEGACY_EFFECTS = ROOT / "common" / "scripted_effects" / "14_nw_mechanics.txt"
EVENTS = ROOT / "events" / "14_nw_politics.txt"
SUPEREVENT = ROOT / "events" / "14_nw_russian_civil_war_super_event.txt"
SUPEREVENT_GFX = ROOT / "interface" / "nw14_russian_civil_war.gfx"
SUPEREVENT_ASSET = ROOT / "sound" / "nw14_super_events.asset"
SUPEREVENT_IMAGE = ROOT / "gfx" / "interface" / "nw14_super_events" / "russia_on_fire.png"
SUPEREVENT_MUSIC = ROOT / "sound" / "super_events" / "nw14_russia_on_fire.wav"
SUPEREVENT_GUI = ROOT / "interface" / "nw14_super_events.gui"
SUPEREVENT_SGUI = ROOT / "common" / "scripted_guis" / "nw14_super_events.txt"
LOCALISATION = ROOT / "localisation" / "replace" / "nw14_l_russian.yml"
CAPITULATION = ROOT / "common" / "on_actions" / "14_nw_russian_civil_war_capitulation.txt"
LEADER_GFX = ROOT / "interface" / "nw14_russian_civil_war_leaders.gfx"
PARTY_LOCALISATION = ROOT / "localisation" / "replace" / "nw_parties_l_russian.yml"
COUNTRY_LOCALISATION = ROOT / "localisation" / "replace" / "nw_countries_l_russian.yml"


def approved_state_ids() -> set[int]:
    approved: set[int] = set()
    with PREVIEW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            status = row.get("Статус", "").strip().lower()
            if status in {"approved", "approved by author"}:
                approved.add(int(row["State ID"]))
    # The four states with random outcomes are represented in the CSV as
    # probabilistic rather than fixed assignments.
    approved.update({217, 236, 237, 265})
    # Explicit scenario transfers from the owner's latest direct instruction.
    approved.update({93, 94, 95, 96, 194, 204, 206, 207, 241})
    return approved


def block_for_state(text: str, state_id: int) -> str:
    match = re.search(rf"(?m)^\s*{state_id}\s*=\s*\{{", text)
    if not match:
        return ""
    opening = text.find("{", match.start())
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[match.start() : index + 1]
    return ""


def blocks_for_scope(text: str, key: str) -> list[str]:
    blocks: list[str] = []
    for match in re.finditer(rf"(?m)^\s*{re.escape(key)}\s*=\s*\{{", text):
        opening = text.find("{", match.start())
        depth = 0
        quoted = False
        escaped = False
        comment = False
        for index in range(opening, len(text)):
            character = text[index]
            if comment:
                if character == "\n":
                    comment = False
                continue
            if quoted:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    quoted = False
                continue
            if character == "#":
                comment = True
            elif character == '"':
                quoted = True
            elif character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    blocks.append(text[match.start() : index + 1])
                    break
    return blocks


def brace_errors(text: str) -> list[str]:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        for character in line:
            if comment:
                break
            if quoted:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    quoted = False
                continue
            if character == "#":
                comment = True
            elif character == '"':
                quoted = True
            elif character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth < 0:
                    return [f"extra closing brace on line {line_number}"]
        comment = False
    if quoted:
        return ["unterminated quoted string"]
    if depth:
        return [f"{depth} unclosed brace(s)"]
    return []


def state_data() -> tuple[dict[int, str], dict[int, set[int]]]:
    owners: dict[int, str] = {}
    province_to_state: dict[int, set[int]] = {}
    for path in (ROOT / "history" / "states").glob("*.txt"):
        text = path.read_text(encoding="utf-8-sig")
        state_match = re.search(r"(?m)^\s*id\s*=\s*(\d+)\b", text)
        if not state_match:
            continue
        state_id = int(state_match.group(1))
        owner_match = re.search(r"\bowner\s*=\s*([A-Z]{3})\b", text)
        if owner_match:
            owners[state_id] = owner_match.group(1)
        province_match = re.search(r"(?s)\bprovinces\s*=\s*\{([^}]*)\}", text)
        if province_match:
            for province in map(int, re.findall(r"\b\d+\b", province_match.group(1))):
                province_to_state.setdefault(province, set()).add(state_id)
    return owners, province_to_state


class RussianCivilWarPrealphaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.effect = EFFECT.read_text(encoding="utf-8-sig") if EFFECT.exists() else ""
        cls.legacy = LEGACY_EFFECTS.read_text(encoding="utf-8-sig")
        cls.events = EVENTS.read_text(encoding="utf-8-sig")

    def test_existing_event_routes_into_single_new_initializer(self) -> None:
        self.assertRegex(self.legacy, r"(?s)nw14_rus_fragmentation\s*=\s*\{\s*nw14_rus_civil_war_start\s*=\s*yes\s*\}")
        self.assertIn("nw14_rus_civil_war_start = {", self.effect)
        self.assertIn("has_country_flag = nw_rus_war_started", self.effect)

    def test_only_approved_or_probability_approved_states_are_transferred(self) -> None:
        transferred = {int(state) for state in re.findall(r"\btransfer_state\s*=\s*(\d+)\b", self.effect)}
        civil_war_states = re.search(r"start_civil_war\s*=\s*\{(?P<body>.*?)\n\s*\}", self.effect, re.S)
        self.assertIsNotNone(civil_war_states)
        if civil_war_states:
            listed = re.search(r"\bstates\s*=\s*\{(?P<ids>[^}]*)\}", civil_war_states.group("body"))
            self.assertIsNotNone(listed)
            if listed:
                transferred.update(map(int, re.findall(r"\d+", listed.group("ids"))))
        self.assertTrue(transferred, "no territories were assigned by the civil-war initializer")
        self.assertEqual(transferred, approved_state_ids(), "the initializer must apply the complete approved state set and nothing else")
        self.assertEqual(self.effect.count("transfer_state = 814"), 1)
        self.assertRegex(self.effect, r"(?s)owns_state\s*=\s*93\s*\}\s*RUK\s*=\s*\{\s*transfer_state\s*=\s*93")
        for state in (206, 96, 204, 194, 94, 95, 241, 207):
            with self.subTest(belarus_state=state):
                self.assertRegex(self.effect, rf"(?s)owns_state\s*=\s*{state}\s*\}}\s*BLR\s*=\s*\{{\s*transfer_state\s*=\s*{state}")
        owners, _ = state_data()
        self.assertTrue(transferred <= owners.keys(), "a referenced state ID is missing from history/states")
        self.assertEqual({state: owners[state] for state in transferred if owners[state] != "SOV"}, {}, "the transfer guards currently assume SOV owns every assigned state")

    def test_each_author_approved_probability_is_independent_and_fifty_fifty(self) -> None:
        for state in (217, 236, 237, 265):
            with self.subTest(state=state):
                state_block = block_for_state(self.effect, state)
                self.assertTrue(state_block, f"state {state} has no explicit outcome block")
                self.assertEqual(state_block.count("random_list = {"), 1)
                self.assertEqual(len(re.findall(r"\b50\s*=\s*\{", state_block)), 2)

    def test_russian_state_label_and_old_five_way_don_tag_do_not_run(self) -> None:
        self.assertRegex(self.effect, r"(?s)RSB\s*=\s*\{.*?set_capital\s*=\s*\{\s*state\s*=\s*570")
        self.assertIn("load_oob = NW14_RSB", self.effect)
        for state in (561, 570, 571, 574, 580, 40, 329, 516, 637, 644, 654, 822, 824, 874, 876, 877, 878):
            with self.subTest(state=state):
                self.assertIn(f"transfer_state = {state}", self.effect)
        self.assertNotRegex(self.effect, r"\btransfer_state\s*=\s*(?:572|573)\b")
        self.assertNotRegex(self.effect, r"\bRDN\b")
        self.assertIn("nw14_rus_fragmentation_legacy_disabled = {", self.legacy)
        self.assertNotRegex(self.legacy, r"(?m)^\s*nw14_rus_fragmentation_legacy_disabled\s*=\s*yes")

    def test_only_the_four_author_named_states_are_randomized(self) -> None:
        self.assertEqual(len(re.findall(r"\brandom_list\s*=\s*\{", self.effect)), 4)
        for state in (217, 236, 237, 265):
            self.assertTrue(block_for_state(self.effect, state), f"random outcome missing for State {state}")

    def test_war_start_is_one_shot_and_keeps_player_as_sov(self) -> None:
        self.assertNotIn("change_tag", self.effect)
        self.assertIn("nw_rus_war_started", self.effect)
        self.assertIn("nw_alexei_dead", self.effect)
        option = re.search(r"(?s)id\s*=\s*nw14\.20\b(?P<body>.*?)\n\}", self.events)
        self.assertIsNotNone(option)
        self.assertIn("nw14_rus_fragmentation = yes", self.events)

    def test_new_script_has_balanced_blocks_and_startup_guard_contains_setup(self) -> None:
        self.assertEqual(brace_errors(self.effect), [])
        guard = self.effect.find("if = {\n\t\tlimit = { NOT = { has_country_flag = nw_rus_war_started }")
        civil_war = self.effect.find("start_civil_war = {")
        setup_tail = self.effect.find("country_event = { id = nw14cw.1 hours = 1 }")
        self.assertGreaterEqual(guard, 0)
        self.assertGreater(civil_war, guard)
        self.assertGreater(setup_tail, civil_war)
        self.assertIn("puppet = DON", self.effect)
        self.assertIn("puppet = KUB", self.effect)
        self.assertIn("end_civil_wars = no", self.effect)

    def test_neutral_countries_are_detached_before_the_sov_civil_war(self) -> None:
        detachment = self.effect.find("MON = {")
        civil_war = self.effect.find("start_civil_war = {")
        self.assertGreaterEqual(detachment, 0)
        self.assertGreater(civil_war, detachment)
        self.assertNotRegex(self.effect, r"(?s)MON\s*=\s*\{[^}]*transfer_state")
        self.assertNotRegex(self.effect, r"(?s)SIK\s*=\s*\{[^}]*transfer_state")

    def test_finland_and_poland_are_independent_war_targets_not_territory_transfers(self) -> None:
        civil_war = self.effect.find("start_civil_war = {")
        for tag in ("FIN", "POL"):
            with self.subTest(tag=tag):
                detachment = self.effect.find(f"{tag} = {{")
                self.assertGreaterEqual(detachment, 0)
                self.assertLess(detachment, civil_war)
                self.assertIn(f"target = {tag} type = annex_everything", self.effect)
                self.assertNotRegex(self.effect, rf"\btransfer_state\s*=\s*{tag}\b")

    def test_turkish_republic_fights_both_russian_blocs_turkey_and_armenia(self) -> None:
        trp = re.search(r"(?s)\n\s*TRP\s*=\s*\{\s*if\s*=\s*\{\s*limit\s*=\s*\{\s*event_target:nw14_rus_royal.*?(?P<body>.*?)\n\s*\}", self.effect)
        self.assertIsNotNone(trp)
        if trp:
            for target in ("TUR", "SOV", "ARM"):
                with self.subTest(target=target):
                    self.assertIn(f"target = {target} type = annex_everything", trp.group("body"))
            self.assertIn("target = event_target:nw14_rus_royal type = annex_everything", trp.group("body"))

    def test_approved_southern_leadership_and_cossack_parties_are_configured(self) -> None:
        for expected in (
            'name = "Антон Деникин"',
            'name = "Алексей Каледин"',
            'name = "Сергей Георгиевич Улагай"',
            "nw14_cw_don_party_long",
            "nw14_cw_kub_party_long",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.effect)
        self.assertNotIn('create_country_leader = { name = "Лука Быч"', self.effect)
        loc = LOCALISATION.read_text(encoding="utf-8-sig")
        for key in ("nw14_cw_don_party", "nw14_cw_don_party_long", "nw14_cw_kub_party", "nw14_cw_kub_party_long"):
            with self.subTest(key=key):
                self.assertRegex(loc, rf"(?m)^\s{{1,2}}{re.escape(key)}:")

    def test_russian_state_is_neutral_with_kolchak_and_new_historical_leaders(self) -> None:
        rsb = next((b for b in blocks_for_scope(self.effect, "RSB") if "set_capital = { state = 570 }" in b), "")
        self.assertIn("set_politics = { ruling_party = neutrality elections_allowed = no }", rsb)
        self.assertIn('name = "Адмирал Александр Колчак"', rsb)
        self.assertIn("picture = GFX_NW14_CW_Kolchak_Leader", rsb)
        for leader, portrait_gfx in (
            ("Кирилл Владимирович", "GFX_NW14_CW_Kyril_Leader"),
            ("Антон Деникин", "GFX_NW14_CW_Denikin_Leader"),
            ("Адмирал Александр Колчак", "GFX_NW14_CW_Kolchak_Leader"),
            ("Алексей Каледин", "GFX_NW14_CW_Kaledin_Leader"),
            ("Сергей Георгиевич Улагай", "GFX_NW14_CW_Ulagay_Leader"),
            ("Сеид Алим-хан", "GFX_NW14_CW_Alim_Khan_Leader"),
            ("Михаил Грушевский", "GFX_NW14_CW_Hrushevsky_Leader"),
            ("Алихан Букейханов", "GFX_NW14_CW_Bukeikhanov_Leader"),
        ):
            with self.subTest(leader=leader):
                self.assertIn(f'name = "{leader}" picture = {portrait_gfx}', self.effect)
                self.assertIn(f"name = {portrait_gfx} ", LEADER_GFX.read_text(encoding="utf-8-sig"))

    def test_all_new_russia_members_are_democratic_at_fragmentation(self) -> None:
        self.assertRegex(self.effect, r"(?s)set_politics\s*=\s*\{\s*ruling_party\s*=\s*democratic.*?set_country_flag\s*=\s*nw14_fragment")
        tags = ("RUK", "FER", "ABK", "NCR", "TCF", "BLW", "BLR", "KIR", "DNR", "KAL")
        for tag in tags:
            with self.subTest(tag=tag):
                blocks = blocks_for_scope(self.effect, tag)
                political_blocks = [block for block in blocks if "set_country_flag = nw14_fragment" in block and "set_politics" in block]
                self.assertTrue(political_blocks, f"{tag} has no explicit civil-war political setup")
                self.assertTrue(any("ruling_party = democratic" in block for block in political_blocks), tag)
                self.assertTrue(any("set_popularities = { democratic = 100 }" in block for block in political_blocks), tag)

    def test_finland_and_poland_become_separate_democratic_republics(self) -> None:
        for tag in ("FIN", "POL"):
            with self.subTest(tag=tag):
                blocks = blocks_for_scope(self.effect, tag)
                setup = next((block for block in blocks if "drop_cosmetic_tag = yes" in block), "")
                self.assertIn("ruling_party = democratic", setup)
                self.assertIn("elections_allowed = yes", setup)
                self.assertIn("set_popularities = { democratic = 100 }", setup)
                self.assertIn(f"NW_{tag}_democratic_party", setup)
        party_loc = PARTY_LOCALISATION.read_text(encoding="utf-8-sig")
        self.assertNotRegex(party_loc, r"(?s)NW_FIN_neutrality_party:0\s+\"Династия Романовых\"|NW_FIN_neutrality_party_long:0\s+\"Династия Романовых\"")
        self.assertNotRegex(party_loc, r"(?s)NW_POL_neutrality_party:0\s+\"Династия Романовых\"|NW_POL_neutrality_party_long:0\s+\"Династия Романовых\"")
        self.assertIn('NW_FIN_democratic_party:0 "Республиканский союз Финляндии"', party_loc)
        self.assertIn('NW_POL_democratic_party:0 "Республиканский союз Польши"', party_loc)
        country_loc = COUNTRY_LOCALISATION.read_text(encoding="utf-8-sig")
        self.assertIn('FIN_democratic:0 "Республика Финляндия"', country_loc)
        self.assertIn('POL_democratic:0 "Польская Республика"', country_loc)

    def test_capitulation_auto_annex_only_when_a_fragment_faction_leader_wins(self) -> None:
        self.assertTrue(CAPITULATION.is_file())
        text = CAPITULATION.read_text(encoding="utf-8-sig")
        self.assertEqual(brace_errors(text), [])
        self.assertIn("has_country_flag = nw14_fragment", text)
        self.assertIn("is_faction_leader = yes", text)
        self.assertIn("has_war_with = ROOT", text)
        self.assertIn("annex_country = {", text)
        self.assertIn("target = ROOT", text)
        self.assertIn("transfer_troops = yes", text)
        self.assertIn("set_country_flag = nw14_cw_capitulation_annexed", text)
        self.assertNotIn("else =", text)

    def test_new_leader_portraits_and_military_gfx_paths_exist(self) -> None:
        gfx = LEADER_GFX.read_text(encoding="utf-8-sig")
        self.assertEqual(brace_errors(gfx), [])
        for path in re.findall(r'texturefile\s*=\s*"([^"]+)"', gfx):
            with self.subTest(asset=path):
                self.assertTrue((ROOT / path).is_file())
        for path in re.findall(r'texturefile\s*=\s*"(gfx/leaders/NW14/[^"]+)"', gfx):
            with self.subTest(asset=path):
                self.assertTrue((ROOT / path).is_file())
        for portrait_gfx in re.findall(r"\bpicture\s*=\s*(GFX_NW14_CW_[A-Za-z0-9_]+)", self.effect):
            with self.subTest(portrait=portrait_gfx):
                self.assertIn(f"name = {portrait_gfx} ", gfx)
        for sprite in re.findall(r'\b(?:gfx|portrait_path)\s*=\s*(GFX_NW14_CW_[A-Za-z0-9_]+)', self.effect):
            with self.subTest(sprite=sprite):
                self.assertIn(f"name = {sprite} ", gfx)

    def test_faction_membership_and_subject_chain_match_the_overview(self) -> None:
        self.assertIn("create_faction = nw14_new_russia_faction", self.effect)
        self.assertIn("create_faction = nw14_white_movement_faction", self.effect)

        def extract_scope(marker: str) -> str:
            start = self.effect.index(marker) + len(marker)
            depth = 1
            for index in range(start, len(self.effect)):
                if self.effect[index] == "{":
                    depth += 1
                elif self.effect[index] == "}":
                    depth -= 1
                    if depth == 0:
                        return self.effect[start:index]
            self.fail(f"Unclosed scripted scope: {marker}")

        new_russia = extract_scope("SOV = {\n\t\t\tset_rule = { can_create_factions = yes can_join_factions = yes }")
        for tag in ("RUK", "FER", "ABK", "NCR", "TCF", "BLW", "KIR"):
            with self.subTest(tag=tag):
                self.assertRegex(new_russia, rf"(?m)^\s*add_to_faction\s*=\s*{tag}\s*$")
        for tag in ("DNR", "KAL"):
            with self.subTest(optional_tag=tag):
                self.assertRegex(new_russia, rf"(?s)limit\s*=\s*\{{\s*{tag}\s*=\s*\{{\s*exists\s*=\s*yes\s*\}}\s*\}}.*?add_to_faction\s*=\s*{tag}")

        white_movement = extract_scope("event_target:nw14_rus_royal = {\n\t\t\tset_rule = { can_create_factions = yes can_join_factions = yes }")
        for tag in ("AFS",):
            with self.subTest(white_member=tag):
                self.assertIn(f"{tag} = {{", white_movement)
                self.assertRegex(white_movement, rf"(?m)^\s*add_to_faction\s*=\s*{tag}\s*$")

        # add_to_faction is executed by the faction leader and takes the member as
        # its target. Running it inside the would-be member silently adds the leader
        # to a nonexistent faction instead.
        self.assertNotRegex(new_russia, r"(?m)^\s*(?:RUK|FER|ABK|NCR|TCF|BLW|KIR|DNR|KAL)\s*=\s*\{[^\n]*add_to_faction\s*=\s*SOV")
        self.assertNotRegex(white_movement, r"(?m)^\s*add_to_faction\s*=\s*PREV\s*$")
        self.assertNotIn("add_to_faction = RSB", white_movement)
        self.assertIn("add_to_faction = BLR", new_russia)
        self.assertRegex(self.effect, r"(?s)RSB\s*=\s*\{.*?set_rule\s*=\s*\{\s*can_join_factions\s*=\s*no\s+can_create_factions\s*=\s*no")
        self.assertRegex(self.effect, r"(?s)DON\s*=\s*\{\s*puppet\s*=\s*AKV")
        self.assertIn("puppet = DON", self.effect)
        self.assertIn("puppet = KUB", self.effect)
        self.assertNotIn("target = AKV type = annex_everything", self.effect)
        loc = LOCALISATION.read_text(encoding="utf-8-sig")
        self.assertRegex(loc, r'(?m)^\s*nw14_white_movement_faction:0\s+"Белое движение"')

    def test_external_wars_use_hidden_delayed_dispatch_and_retry(self) -> None:
        initializer = self.effect.split("nw14_rus_civil_war_start = {", 1)[1].split(
            "\nnw14_rus_civil_war_declare_separatist_wars = {", 1
        )[0]
        self.assertNotIn("nw14_rus_civil_war_declare_external_wars = yes", initializer)
        self.assertIn("country_event = { id = nw14cw.2 days = 30 }", initializer)
        self.assertIn("country_event = { id = nw14cw.3 days = 37 }", initializer)
        self.assertNotIn("nw14_cw_external_fronts_started", self.effect)

        separatists = self.effect.split("nw14_rus_civil_war_declare_separatist_wars = {", 1)[1].split(
            "\nnw14_rus_civil_war_declare_new_russia_wars = {", 1
        )[0]
        for enemy in ("FIN", "POL", "ARM", "BLF", "TRP", "ALA", "TRK"):
            with self.subTest(declared_enemy=enemy):
                self.assertIn(f"target = {enemy} type = annex_everything", separatists)

        targets = self.effect.split("nw14_rus_civil_war_declare_new_russia_wars = {", 1)[1].split(
            "\nnw14_rus_civil_war_declare_external_wars = {", 1
        )[0]
        for enemy in ("event_target:nw14_rus_royal", "AFS", "RSB"):
            with self.subTest(declared_enemy=enemy):
                self.assertIn(f"target = {enemy} type = annex_everything", targets)
        for puppet in ("DON", "KUB", "AKV"):
            with self.subTest(white_puppet=puppet):
                self.assertNotIn(f"target = {puppet} type = annex_everything", targets)
        wrapper = self.effect.split("nw14_rus_civil_war_declare_external_wars = {", 1)[1]
        self.assertIn("every_country = {", wrapper)
        self.assertIn("is_in_faction_with = SOV", wrapper)
        self.assertRegex(
            wrapper,
            r"(?s)RSB\s*=\s*\{\s*nw14_rus_civil_war_declare_separatist_wars\s*=\s*yes.*?target\s*=\s*SOV\s+type\s*=\s*annex_everything.*?\n\s*\}",
        )
        rsb_wars = wrapper.split("RSB = {", 1)[1].split("\n\t\tTRP = {", 1)[0]
        for white_target in ("event_target:nw14_rus_royal", "AFS", "DON", "KUB", "AKV"):
            with self.subTest(rsb_white_target=white_target):
                self.assertNotIn(f"target = {white_target} type = annex_everything", rsb_wars)
        self.assertNotIn("add_to_war =", self.effect)
        self.assertRegex(self.effect, r"(?s)delete_unit\s*=\s*\{\s*disband\s*=\s*no\s*\}.*?start_civil_war\s*=")

        events = SUPEREVENT.read_text(encoding="utf-8-sig")
        self.assertIn("id = nw14cw.1", events)
        for event_id in ("nw14cw.2", "nw14cw.3"):
            with self.subTest(dispatch_event=event_id):
                block = re.search(rf"(?s)country_event\s*=\s*\{{\s*id\s*=\s*{event_id}\b(?P<body>.*?)\n\}}", events)
                self.assertIsNotNone(block)
                body = block.group("body") if block else ""
                self.assertIn("hidden = yes", body)
                self.assertIn("is_triggered_only = yes", body)
                self.assertIn("fire_only_once = yes", body)
                self.assertIn("has_country_flag = nw_rus_war_started", body)
                self.assertIn("nw14_rus_civil_war_declare_external_wars = yes", body)
        loc = LOCALISATION.read_text(encoding="utf-8-sig")
        self.assertIn("nw14cw.1.t", loc)

    def test_fixed_country_names_and_fer_democratic_setup_are_present(self) -> None:
        effect = self.effect
        for key in ("KIR", "ALA", "TRK"):
            with self.subTest(tag=key):
                self.assertIn(f"{key} = {{", effect)
        self.assertRegex(effect, r"(?s)FER\s*=\s*\{\s*set_capital\s*=\s*\{\s*state\s*=\s*408\s*\}\s*set_politics\s*=\s*\{\s*ruling_party\s*=\s*democratic")
        loc = LOCALISATION.read_text(encoding="utf-8-sig")
        for expected in ("Область Войска Донского", "Кубанская область", "Российское Государство", "Киргизская Народная Республика", "Белорусская Народная Республика", "Алаш-Орда", "Туркестанское ханство"):
            with self.subTest(name=expected):
                self.assertIn(f'"{expected}"', loc)
        self.assertIn('nw14_cw_rsb_party:0 "Сибирское национальное правительство"', loc)
        self.assertIn('nw14_cw_rsb_party_long:0 "Правительство Российского Государства в Сибири"', loc)
        game = Path(os.environ.get("HOI4_GAME_PATH", "E:/SteamLibrary/steamapps/common/Hearts of Iron IV"))
        for relative in ("gfx/flags/FER_democratic.tga", "gfx/flags/medium/FER_democratic.tga", "gfx/flags/small/FER_democratic.tga"):
            with self.subTest(flag=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_oob_locations_belong_to_the_approved_starting_states(self) -> None:
        _, province_to_state = state_data()
        allowed = {
            "NW14_SOV_CW.txt": {195},
            "NW14_ROYAL_CW.txt": {239},
            "NW14_AFS.txt": {137},
            "NW14_DON_CW.txt": {218, 227, 228, 238, 245, 265},
            "NW14_KUB_CW.txt": {233, 234, 235},
            "NW14_RUK_CW.txt": {93, 202, 834},
            "NW14_RSB.txt": {570},
            "NW14_FER_CW.txt": {408},
            "NW14_ABK_CW.txt": {826},
            "NW14_NCR_CW.txt": {232},
            "NW14_TCF_CW.txt": {231},
            "NW14_ARM_CW.txt": {230},
            "NW14_TRP_CW.txt": {353},
            "NW14_BLF_CW.txt": {808},
            "NW14_BLW_CW.txt": {813},
            "NW14_BLR_CW.txt": {206},
            "NW14_DNR_217.txt": {217},
            "NW14_DNR_265.txt": {265},
            "NW14_AKV_217.txt": {217},
            "NW14_AKV_236.txt": {236},
            "NW14_AKV_237.txt": {237},
            "NW14_KAL_236.txt": {236},
            "NW14_KAL_237.txt": {237},
            "NW14_KIR_CW.txt": {590},
            "NW14_ALA_CW.txt": {881},
            "NW14_TRK_CW.txt": {405},
        }
        for filename, allowed_states in allowed.items():
            text = (ROOT / "history" / "units" / filename).read_text(encoding="utf-8-sig")
            locations = list(map(int, re.findall(r"\blocation\s*=\s*(\d+)\b", text)))
            self.assertTrue(locations, filename)
            for province in locations:
                with self.subTest(oob=filename, province=province):
                    self.assertTrue(province_to_state.get(province, set()) & allowed_states)
        loaded = set(re.findall(r"\bload_oob\s*=\s*([A-Z0-9_]+)", self.effect))
        required = {Path(name).stem for name in allowed}
        self.assertTrue(required.issubset(loaded), f"OOBs not loaded by the initializer: {sorted(required - loaded)}")

    def test_russian_spirits_are_removed_from_former_subjects(self) -> None:
        expected = {
            "FIN": "nw_fin_imperial_autonomy",
            "POL": "nw_pol_imperial_autonomy",
            "MON": "nw_mon_russian_resident",
            "SIK": "nw_sik_sponsored_independence",
        }
        for tag, idea in expected.items():
            with self.subTest(tag=tag):
                blocks = blocks_for_scope(self.effect, tag)
                detached = next((block for block in blocks if f"remove_ideas = {idea}" in block), "")
                self.assertTrue(detached, f"{tag} does not remove {idea}")

    def test_civil_war_oob_counts_and_explicit_stockpiles_match_tiers(self) -> None:
        oob_counts = {
            "NW14_SOV_CW": 40, "NW14_ROYAL_CW": 40, "NW14_AFS": 40, "NW14_RSB": 40,
            "NW14_RUK_CW": 25,
            "NW14_BLR_CW": 20, "NW14_BLF_CW": 20, "NW14_FER_CW": 20,
            "NW14_ALA_CW": 20, "NW14_TRK_CW": 20,
            "NW14_DON_CW": 5, "NW14_KUB_CW": 5, "NW14_BLW_CW": 5,
            "NW14_ABK_CW": 5, "NW14_NCR_CW": 5, "NW14_TCF_CW": 5,
            "NW14_ARM_CW": 5, "NW14_TRP_CW": 5, "NW14_KIR_CW": 5,
            "NW14_DNR_217": 5, "NW14_DNR_265": 5,
            "NW14_AKV_217": 5, "NW14_AKV_236": 5, "NW14_AKV_237": 5,
            "NW14_KAL_236": 5, "NW14_KAL_237": 5,
        }
        for name, expected in oob_counts.items():
            path = ROOT / "history" / "units" / f"{name}.txt"
            text = path.read_text(encoding="utf-8-sig")
            with self.subTest(oob=name):
                self.assertEqual(len(re.findall(r"\bdivision\s*=\s*\{", text)), expected)
        for tag, manpower, rifles, oob in (
            ("SOV", 264000, 18480, "NW14_SOV_CW"),
            ("event_target:nw14_rus_royal", 229000, 18480, "NW14_ROYAL_CW"),
            ("AFS", 164000, 14800, "NW14_AFS"), ("RSB", 229000, 18480, "NW14_RSB"),
            ("RUK", 130000, 8250, "NW14_RUK_CW"), ("BLR", 132000, 9240, "NW14_BLR_CW"),
            ("BLF", 97000, 9240, "NW14_BLF_CW"), ("FER", 132000, 9240, "NW14_FER_CW"),
            ("ALA", 132000, 9240, "NW14_ALA_CW"), ("TRK", 132000, 9240, "NW14_TRK_CW"),
        ):
            with self.subTest(stockpile_tag=tag):
                line = next((line for line in self.effect.splitlines() if f"{tag} = {{" in line and f"load_oob = {oob}" in line), "")
                self.assertTrue(line, f"missing OOB load line for {tag}")
                self.assertIn(f"add_manpower = {manpower}", line)
                self.assertIn(f"amount = {rifles}", line)

    def test_imperial_flag_variants_exist_for_afs_and_akv(self) -> None:
        for tag in ("AFS", "AKV"):
            for size in ("", "medium/", "small/"):
                for suffix in ("", "_neutrality", "_democratic", "_communism", "_fascism"):
                    with self.subTest(tag=tag, size=size, suffix=suffix):
                        self.assertTrue((ROOT / "gfx" / "flags" / size / f"{tag}{suffix}.tga").is_file())

    def test_super_event_has_existing_resources_and_localisation(self) -> None:
        event = SUPEREVENT.read_text(encoding="utf-8-sig")
        gfx = SUPEREVENT_GFX.read_text(encoding="utf-8-sig")
        asset = SUPEREVENT_ASSET.read_text(encoding="utf-8-sig")
        loc = LOCALISATION.read_text(encoding="utf-8-sig")
        self.assertTrue(SUPEREVENT_IMAGE.is_file())
        self.assertTrue(SUPEREVENT_MUSIC.is_file())
        self.assertIn("hidden = yes", event)
        self.assertIn("fire_only_once = yes", event)
        self.assertNotIn("news_event =", event)
        self.assertNotIn("play_song = nw14_russia_on_fire", self.effect)
        self.assertIn("gfx/interface/nw14_super_events/russia_on_fire.png", gfx)
        self.assertIn('file = "super_events/nw14_russia_on_fire.wav"', asset)
        for key in ("nw14cw.1.t", "nw14cw.1.d", "nw14cw.1.a"):
            self.assertRegex(loc, rf"(?m)^\s{{1,2}}{re.escape(key)}:")

    def test_super_event_gui_binding_broadcast_and_local_close(self) -> None:
        event = SUPEREVENT.read_text(encoding="utf-8-sig")
        gui = SUPEREVENT_GUI.read_text(encoding="utf-8-sig")
        sgui = SUPEREVENT_SGUI.read_text(encoding="utf-8-sig")
        for text in (event, gui, sgui, SUPEREVENT_ASSET.read_text()):
            self.assertEqual(brace_errors(text), [])
            self.assertNotIn("\ufeff", text)
        window = re.search(r'window_name\s*=\s*"([^"]+)"', sgui).group(1)
        self.assertIn(f'name = "{window}"', gui)
        self.assertIn("context_type = player_context", sgui)
        self.assertIn("NOT = { has_global_flag = nw14_cw_super_event_announced }", event)
        self.assertIn("set_global_flag = nw14_cw_super_event_announced", event)
        self.assertIn("every_country =", event)
        self.assertIn("limit = { is_ai = no }", event)
        self.assertIn("set_country_flag = nw14_cw_super_event_visible", event)
        self.assertIn("has_country_flag = nw14_cw_super_event_visible", sgui)
        self.assertIn('name = "nw14_super_event_close"', gui)
        self.assertIn("nw14_super_event_close_click =", sgui)
        self.assertIn("clr_country_flag = nw14_cw_super_event_visible", sgui)
        self.assertNotIn("clr_global_flag", sgui)
        self.assertNotIn("scoped_sound_effect", sgui)  # No playback on visibility ticks.
        self.assertEqual(event.count("scoped_sound_effect = nw14_cw_super_event_sound"), 1)
        loc = ROOT / "localisation/russian/nw14_super_events_l_russian.yml"
        self.assertTrue(loc.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertIn("nw14cw.close:", loc.read_text(encoding="utf-8-sig"))

    def test_super_event_png_and_wav_are_real_engine_resources(self) -> None:
        image = SUPEREVENT_IMAGE.read_bytes()
        self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", image[16:24]), (899, 592))
        with wave.open(str(SUPEREVENT_MUSIC)) as recording:
            self.assertEqual(recording.getframerate(), 44100)
            self.assertEqual(recording.getnchannels(), 2)
            self.assertEqual(recording.getsampwidth(), 2)
            self.assertEqual(recording.getcomptype(), "NONE")
            self.assertAlmostEqual(recording.getnframes() / 44100, 126.329, delta=0.1)
            frames = recording.readframes(recording.getnframes())
            self.assertTrue(any(frames), "recording must not be silent")
        asset = SUPEREVENT_ASSET.read_text()
        self.assertIn('name = "nw14_cw_super_event_sound"', asset)
        self.assertIn('sound = "nw14_cw_super_event_recording"', asset)
        self.assertIn('name = "nw14_cw_super_event_recording"', asset)
        self.assertIn("soundeffects = { nw14_cw_super_event_sound }", asset)
        self.assertFalse((ROOT / "music/nw14_russian_civil_war.asset").exists())

    def test_super_event_registered_fonts_cover_russian_and_fit_text(self) -> None:
        # Inspect the actual language-selected atlas chain, not filenames as names.
        from preview_super_event_fonts import audit
        game = Path(os.environ.get("HOI4_GAME_PATH", "E:/SteamLibrary/steamapps/common/Hearts of Iron IV"))
        if not (game / "interface/core.gfx").is_file():
            self.skipTest("Set HOI4_GAME_PATH to check installed font atlases")
        records = audit(game)
        self.assertEqual({r["element"] for r in records},
                         {"title", "description", "quote_heading", "remark", "quote_author", "nw14_super_event_close"})
        for record in records:
            with self.subTest(element=record["element"]):
                self.assertEqual(record["missing_glyphs"], 0)
                self.assertLessEqual(record["text_height"], record["max_height"])

    def test_all_new_actor_tags_have_definitions_history_and_names(self) -> None:
        tags = ("AFS", "DNR", "AKV", "NCR", "TCF", "TRP", "BLF", "BLW", "KIR", "ALA", "TRK")
        tag_file = (ROOT / "common" / "country_tags" / "14_nw_civilwar.txt").read_text(encoding="utf-8-sig")
        loc = LOCALISATION.read_text(encoding="utf-8-sig")
        for tag in tags:
            with self.subTest(tag=tag):
                self.assertRegex(tag_file, rf"(?m)^{tag}\s*=")
                self.assertTrue((ROOT / "common" / "countries" / f"NW14_{tag}.txt").is_file())
                self.assertTrue((ROOT / "history" / "countries" / f"{tag} - NW14.txt").is_file())
                self.assertRegex(loc, rf"(?m)^\s{{1,2}}{tag}:")


if __name__ == "__main__":
    unittest.main(verbosity=2)
