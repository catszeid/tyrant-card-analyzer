import pytest
import xml.etree.ElementTree as ET

import scoring as s

def test_rally_score():
	target = 10
	skill_rally = ET.Element("skill", attrib={"id": "rally", "x": "10"})
	score = s.score_skill(skill_rally)
	assert score == target

def test_wall_score():
	skill = ET.Element("skill", attrib={"id": "wall"})
	target = 10
	score = s.score_skill(skill)
	assert score == target

def test_armored_score():
	target = 10
	skill_counter = ET.Element("skill", attrib={"id": "counter", "x": "10"})
	score = s.score_skill(skill_counter)
	assert score == target

def test_heal_score():
	target = 10
	skill_heal = ET.Element("skill", attrib={"id": "heal", "x": "10"})
	score = s.score_skill(skill_heal)
	assert score == target

def test_strike_score():
	target = 10
	skill_strike = ET.Element("skill", attrib={"id": "strike", "x": "10"})
	score = s.score_skill(skill_strike)
	assert score == target

def test_weaken_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "weaken", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_besiege_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "besiege", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_pierce_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "pierce", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_poison_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "poison", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_leech_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "leech", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_evade_score():
	target = 100
	skill = ET.Element("skill", attrib={"id": "evade", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_berserk_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "berserk", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_enfeeble_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "enfeeble", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_protect_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "protect", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_enhance_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "enhance", "x": "10", "s": "armored"})
	score = s.score_skill(skill)
	assert score == target

def test_jam_score_1():
	target_1_3 = 60
	skill_1_3 = ET.Element("skill", attrib={"id": "jam", "c": "3"})
	score_1_3 = s.score_skill(skill_1_3)
	assert score_1_3 == target_1_3

def test_jam_score_2():
	target_2_3 = 70
	skill_2_3 = ET.Element("skill", attrib={"id": "jam", "n": "2", "c": "3"})
	score_2_3 = s.score_skill(skill_2_3)
	assert score_2_3 == target_2_3

def test_jam_score_play():
	target_play = 90
	skill_play = ET.Element("skill", attrib={"id": "jam", "trigger": "play", "n": "3"})
	score_play = s.score_skill(skill_play)
	assert score_play == target_play

def test_corrosive_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "corrosive", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_inhibit_score():
	target = 100
	skill = ET.Element("skill", attrib={"id": "inhibit", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_flurry_score_1():
	target = 60
	skill = ET.Element("skill", attrib={"id": "flurry", "c": "3"})
	score = s.score_skill(skill)
	assert score == target

def test_flurry_score_2():
	target = 70
	skill = ET.Element("skill", attrib={"id": "flurry", "n": "2", "c": "3"})
	score = s.score_skill(skill)
	assert score == target
def test_valor_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "valor", "x": "10"})
	score = s.score_skill(skill)
	assert score == target
def test_overload_score():
	target = 30
	skill = ET.Element("skill", attrib={"id": "overload", "n": "2"})
	score = s.score_skill(skill)
	assert score == target

def test_overload_score_play():
	target = 30
	skill = ET.Element("skill", attrib={"id": "overload", "trigger": "play"})
	score = s.score_skill(skill)
	assert score == target
def test_legion_score():
	target = 60
	skill = ET.Element("skill", attrib={"id": "legion", "x": "30"})
	score = s.score_skill(skill)
	assert score == target
def test_payback_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "payback", "x": "1"})
	score = s.score_skill(skill)
	assert score == target

def test_avenge_score():
	target = 30
	skill = ET.Element("skill", attrib={"id": "avenge", "x": "30"})
	score = s.score_skill(skill)
	assert score == target

def test_refresh_score():
	target = 50
	skill = ET.Element("skill", attrib={"id": "refresh", "x": "50"})
	score = s.score_skill(skill)
	assert score == target

def test_evolve_score():
	target = 30
	skill = ET.Element("skill", attrib={"id": "evolve", "s": "pierce", "s2": "rupture"})
	score = s.score_skill(skill)
	assert score == target

def test_venom_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "venom", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_mend_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "mend", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_siege_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "siege", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_swipe_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "swipe", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_sunder_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "sunder", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_enrage_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "enrage", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_allegiance_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "allegiance", "x": "5"})
	score = s.score_skill(skill)
	assert score == target

def test_drain_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "drain", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_stasis_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "stasis", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_revenge_score():
	target = 50
	skill = ET.Element("skill", attrib={"id": "revenge", "x": "5"})
	score = s.score_skill(skill)
	assert score == target

def test_mimic_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "mimic", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_coalition_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "coalition", "x": "5"})
	score = s.score_skill(skill)
	assert score == target

def test_sabotage_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "sabotage", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_barrier_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "barrier", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_entrap_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "entrap", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_subdue_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "subdue", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_tribute_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "tribute", "x": "1"})
	score = s.score_skill(skill)
	assert score == target

def test_summon_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "summon", "card_id": "1"})
	score = s.score_skill(skill)
	assert score == target

def test_bravery_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "bravery", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_absorb_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "absorb", "x": "20"})
	score = s.score_skill(skill)
	assert score == target

def test_disease_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "disease", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_mark_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "mark", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_fortify_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "fortify", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_hunt_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "hunt", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_scavenge_score():
	target = 20
	skill = ET.Element("skill", attrib={"id": "scavenge", "x": "10"})
	score = s.score_skill(skill)
	assert score == target

def test_rupture_score():
	target = 10
	skill = ET.Element("skill", attrib={"id": "rupture", "x": "5"})
	score = s.score_skill(skill)
	assert score == target

def test_flying_score():
	target = 69
	skill = ET.Element("skill", attrib={"id": "flying",})
	score = s.score_skill(skill)
	assert score == target

def test_rush_score():
	target = 0
	skill = ET.Element("skill", attrib={"id": "rush"})
	score = s.score_skill(skill)
	assert score == target