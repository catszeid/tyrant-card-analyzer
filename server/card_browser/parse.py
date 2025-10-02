import xml.etree.ElementTree as ET
import os
import re
from django.conf import settings

# Find files matching the regex pattern
def find_files(file_pattern) -> list:
	dir_contents = os.listdir(settings.STATICFILES_DIR[0])
	pattern = re.compile(file_pattern)
	match_files = [file for file in dir_contents if pattern.fullmatch(file)]
	return match_files

# parse faction data from 'skills_set.xml'
def parse_factions() -> dict:
	tree = ET.parse(os.path.join(settings.STATICFILES_DIR[0], 'skills_set.xml'))
	root = tree.getroot()
	factions = root.findall('unitType')

	results = dict()
	for faction in factions:
		f_id = faction.findtext('id', None)
		f_name = faction.findtext('name', None)
		results[f_id] = f_name
	return results

# parse skill data from 'skills_set.xml'
def parse_skills() -> dict:
	tree = ET.parse(os.path.join(settings.STATICFILES_DIR[0], 'skills_set.xml'))
	root = tree.getroot()

	skills = root.findall('skillType')

	results = dict()
	for skill in skills:
		s = dict()
		s['id'] = skill.findtext('id', None)
		s['name'] = skill.findtext('name', None)
		s['desc'] = skill.findtext('desc', None)
		s['desc_all'] = skill.findtext('desc_all', None)
		s['desc_faction'] = skill.findtext('desc_faction', None)
		s['desc_all_faction'] = skill.findtext('desc_all_faction', None)
		s['order'] = skill.findtext('order', None)
		s['target'] = skill.findtext('sabotage_target', None)
		s['upkeep'] = skill.findtext('enhance_upkeep', None)
		s['hidden'] = skill.findtext('hidden', None)
		# attributes (x, y, all, c, s, s2, n)
		s_attributes = skill.find('attributes', None)
		if s_attributes is not None:
			attrib = dict()
			attrib['x'] = s_attributes.get('x')
			attrib['y'] = s_attributes.get('y')
			attrib['all'] = s_attributes.get('all')
			attrib['c'] = s_attributes.get('c')
			attrib['s'] = s_attributes.get('s')
			attrib['s2'] = s_attributes.get('s2')
			attrib['n'] = s_attributes.get('n')
			s['attributes'] = attrib
		results[s['id']] = s
	return results

def parse_card_sets() -> dict:
	tree = ET.parse(os.path.join(settings.STATICFILES_DIR[0], 'skills_set.xml'))
	root = tree.getroot()

	card_sets = root.findall('cardSet')
	result = dict()
	for set in card_sets:
		s = dict()
		s['id'] = set.findtext('id')
		s['name'] = set.findtext('name')
		result[s['id']] = s
	return result

# parse files for cards with the given arguments
def parse_cards(files: list) -> dict:
	results = {}

	for file in files:
		print(f"Attempting to parse {file}")
		tree = ET.parse(os.path.join(settings.STATICFILES_DIR[0], file))
		root = tree.getroot()
		
		for card in root:
			if card is None:
				continue
			card_id = card.findtext('id', None)
			if card_id is None:
				continue
			card_name = card.findtext('name', None)
			if card_name is None:
				card_name = f"{card_id}"
				continue
			card_set = card.findtext('set', None)
			
			# card rarity
			card_rarity = card.findtext('rarity', None)
			if card_rarity is not None:
				try:
					card_attack = int(card_rarity)
				except:
					card_attack = None
			# card fusion level
			card_fusion_level = card.findtext('fusion_level', None)
			if card_fusion_level is None:
				card_fusion_level = 0
			else:
				try:
					card_fusion_level = int(card_fusion_level)
				except:
					card_fusion_level = 0
			# card cost (Commander have no cost)
			card_cost = card.findtext('cost', None)
			if card_cost is not None:
				try:
					card_cost = int(card_cost)
				except:
					card_cost = None
			# card attack (Structure have no attack)
			card_attack = card.findtext('attack', None)
			if card_attack is not None:
				try:
					card_attack = int(card_attack)
				except:
					card_attack = None
			# card health
			card_health = card.findtext('health', None)
			if card_health is not None:
				try:
					card_health = int(card_health)
				except:
					card_health = None
			# card type (faction)
			card_type = card.findtext('type', None)
			if card_type is not None:
				try:
					card_type = int(card_type)
				except:
					card_type = None
		
			card_level = 1
			
			card_skills = card.findall('skill') # list of 'skill' Elements
			final_skills = card_skills
			card_upgrade_id = None
			upgrades = card.findall('upgrade')
			if upgrades is not None and len(upgrades) > 0:
				card_upgrade_id = upgrades[0].findtext('card_id', None)

			results[card_id] = {'id': card_id, 'name': card_name, 'set': card_set, 'rarity': card_rarity, 
					   'fusion_level': card_fusion_level, 'cost': card_cost, 'attack': card_attack, 
					   'health': card_health, 'level': card_level, 'type': card_type,'skills': final_skills, 'upgrade_id': card_upgrade_id}

			# iterate and apply upgrades
			for i in range(len(upgrades)):
				upgrade = upgrades[i]
				if i+1 < len(upgrades):
					card_upgrade_id = upgrades[i+1].findtext('card_id')
				else:
					card_upgrade_id = None
				# type (faction) and rarity should not change as part of an upgrade
				card_id = upgrade.findtext('card_id', None)
				upgrade_level = upgrade.findtext('level', None)
				if upgrade_level is not None:
					try:
						upgrade_level = int(upgrade_level)
					except:
						upgrade_level = i
					card_level = max(card_level, upgrade_level)
				upgrade_attack = upgrade.findtext('attack', None)
				if upgrade_attack is not None:
					try:
						upgrade_attack = int(upgrade_attack)
					except:
						upgrade_attack = None
					if card_attack is not None and upgrade_attack is not None:
						card_attack = max(card_attack, upgrade_attack)
				upgrade_health = upgrade.findtext('health', None)
				if upgrade_health is not None:
					try:
						upgrade_health = int(upgrade_health)
					except:
						upgrade_health = None
					if card_health is not None and upgrade_health is not None:
						card_health = max(card_health, upgrade_health)
				upgrade_cost = upgrade.findtext('cost', None)
				if upgrade_cost is not None:
					try:
						upgrade_cost = int(upgrade_cost)
					except:
						upgrade_cost = None
					if card_cost is not None and upgrade_cost is not None:
						card_cost = max(card_cost, upgrade_cost)
				if len(upgrade.findall('skill')) != 0:
					# reset skills and refill the list
					card_skills = []
					for skill in upgrade.findall('skill'):
						card_skills.append(skill)
				
				# add each upgrade to database
				final_skills = card_skills
				results[card_id] = {'id': card_id, 'name': card_name, 'set': card_set, 'rarity': card_rarity, 
					   'fusion_level': card_fusion_level, 'cost': card_cost, 'attack': card_attack, 
					   'health': card_health, 'level': card_level, 'type': card_type, 'skills': final_skills, 'upgrade_id': card_upgrade_id}
	return results
