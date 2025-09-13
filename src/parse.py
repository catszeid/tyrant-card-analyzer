import xml.etree.ElementTree as ET
import os
import re
import argparse

import src.scoring as scor
from src.sqlize import build_tyrant_db

def heapify_by_score(arr, n, i):
	largest = i
	left = 2 * i + 1
	right = 2 * i + 2

	if left < n and arr[left][1] > arr[largest][1]:
		largest = left
	if right < n and arr[right][1] > arr[largest][1]:
		largest = right
	
	if largest != i:
		arr[i], arr[largest] = arr[largest], arr[i]
		heapify_by_score(arr, n, largest)

def heap_sort(arr):
	n = len(arr)

	for i in range(n//2 - 1, -1, -1):
		heapify_by_score(arr, n, i)
	
	for i in range(n - 1, 0, -1):
		arr[i], arr[0] = arr[0], arr[i]
		heapify_by_score(arr, i, 0)

# sort in ascending order
def sort_scored_results(data) -> list:
	sorted = []
	for key in data:
		score = data[key]['score']
		id = key
		sorted.append((id, score))
	heap_sort(sorted)

	return sorted

# Find files matching the regex pattern
def find_files(file_pattern, folder='data') -> list:
	dir_contents = os.listdir(os.path.join(os.getcwd(), folder))
	pattern = re.compile(file_pattern)
	match_files = [file for file in dir_contents if pattern.fullmatch(file)]
	return match_files

# get the list of data files to read for cards
# When files is None, it will search for all files matching the default naming scheme
def get_files(files=None, folder='data') -> list:
	fileList = []
	if files is not None:
		dir_contents = os.listdir(os.path.join(os.getcwd(), folder))
		for file in files:
			if file in dir_contents:
				fileList.append(file)
			else:
				print(f"Failed to find {file}")
	else:
		pattern = "^cards_section_\\d+.xml$"
		fileList = find_files(pattern, folder)

	return fileList

def get_ignored_list(folder='data') -> set:
	# ignore ids Block
	ignored_file = find_files("^ignoredcards.xml$")
	ignored_ids = set()
	if len(ignored_file) > 0:
		file = ignored_file[0]
		tree = ET.parse((os.path.join(os.getcwd(), folder, file)))
		root = tree.getroot()
		for id in root:
			if id is not None and id.text is not None:
				ignored_ids.add(id.text)
	return ignored_ids

def score_by_fields(data, *argv):
	for key in data:
		try:
			score = 0
			for arg in argv:
				score += data[key][arg]
		except:
			print(f"Warning: Error while scoring {key}")
		data[key]['score'] = score

def avg_card_stats(c_health: int | None, c_attack: int | None, c_cost: int) -> float:
	sum = 0
	if c_health is not None:
		sum += c_health
	if c_attack is not None:
		sum += c_attack
	if c_cost is None:
		c_cost = 0
	return sum / (c_cost + 1)

def avg_card_skill(c_skills: list) -> float:
	score = 0
	count = 0
	for skill in c_skills:
		score += scor.score_skill(skill)
		count += 1
	if count > 0:
		score = score / count
	return score
	
def readable_skills(c_skills: list) -> list:
	skill_out = []
	for skill in c_skills:
		skill_out.append(scor.skill_to_string(skill))
	return skill_out

# parse files for cards with the given arguments
def parse_cards(files: list, args, folder='data', ignore=True) -> dict:
	results = {}

	ignored_ids = {}
	if ignore:
		ignored_ids = get_ignored_list()

	for file in files:
		tree = ET.parse(os.path.join(os.getcwd(), folder, file))
		root = tree.getroot()
		
		for card in root:
			if card is None:
				print(f"Found empty card in {file}, skipping...")
				continue
			card_id = card.findtext('id', None)
			if card_id is None:
				print(f"Warning: Card {card_id} in {file} has no card_id")
				continue
			if card_id in ignored_ids:
				continue
			card_name = card.findtext('name', None)
			if card_name is None:
				print(f"Warning: Card {card_id} in {file} has no name")
				continue
			card_set = card.findtext('set', None)
			if args.set is not None and int(card_set) not in args.set:
				continue
			
			# card rarity filtering
			card_rarity = card.findtext('rarity', None)
			if args.rarity is not None and int(card_rarity) not in args.rarity:
				continue
				
			# card fusion level
			card_fusion_level = card.findtext('fusion_level', None)
			if card_fusion_level is None:
				card_fusion_level = 0
			else:
				card_fusion_level = int(card_fusion_level)
			if args.fusion_level is not None and card_fusion_level not in args.fusion_level:
				continue
			# card cost (Commander have no cost)
			card_cost = card.findtext('cost', None)
			if card_cost is not None:
				try:
					card_cost = int(card_cost)
				except:
					card_cost = None
			if args.cost is not None and card_fusion_level not in args.fusion_level:
				continue
			# card attack (Structure have no attack)
			card_attack = card.findtext('attack', None)
			if card_attack is not None:
				card_attack = int(card_attack)
			# card health
			card_health = card.findtext('health', None)
			if card_health is not None:
				card_health = int(card_health)
			# card type (faction)
			card_type = card.findtext('type', None)
			if card_type is not None:
				card_type = int(card_type)
			if args.faction is not None and card_type not in args.faction:
				continue
		
			card_level = 1
			
			card_skills = card.findall('skill') # list of 'skill' Elements
			adjusted_stats = avg_card_stats(card_health, card_attack, card_cost)
			avg_skill_score = avg_card_skill(card_skills)
			final_skills = card_skills
			card_upgrade_id = None
			upgrades = card.findall('upgrade')
			if upgrades is not None:
				try:
					card_upgrade_id = upgrades[0].find('card_id').text
				except:
					pass

			results[card_id] = {'id': card_id, 'name': card_name, 'set': card_set, 'rarity': card_rarity, 
					   'fusion_level': card_fusion_level, 'cost': card_cost, 'attack': card_attack, 
					   'health': card_health, 'level': card_level, 'type': card_type, 'adj_stats': adjusted_stats, 
					   'avg_skill': avg_skill_score, 'skills': final_skills, 'upgrade_id': card_upgrade_id}

			# iterate and apply upgrades
			for i in range(len(upgrades)):
				upgrade = upgrades[i]
				if i+1 < len(upgrades):
					card_upgrade_id = upgrades[i+1].findtext('card_id')
				else:
					card_upgrade_id = None
				# type (faction) and rarity should not change as part of an upgrade
				card_id = upgrade.findtext('card_id', None)
				card_level = upgrade.findtext('level', None)
				if card_level is not None:
					card_level = int(card_level)
				card_attack = upgrade.findtext('attack', None)
				if card_attack is not None:
					try:
						card_attack = int(card_attack)
					except:
						card_attack = None
				card_health = upgrade.findtext('health', None)
				if card_health is not None:
					try:
						card_health = int(card_health)
					except:
						card_health = None
				card_cost = upgrade.findtext('cost', None)
				if card_cost is not None:
					try:
						card_cost = int(card_cost)
					except:
						card_cost = None
				if len(upgrade.findall('skill')) != 0:
					# reset skills and refill the list
					card_skills = []
					for skill in upgrade.findall('skill'):
						card_skills.append(skill)
				
				# add each upgrade to database
				adjusted_stats = avg_card_stats(card_health, card_attack, card_cost)
				avg_skill_score = avg_card_skill(card_skills)
				final_skills = card_skills
				results[card_id] = {'id': card_id, 'name': card_name, 'set': card_set, 'rarity': card_rarity, 
					   'fusion_level': card_fusion_level, 'cost': card_cost, 'attack': card_attack, 
					   'health': card_health, 'level': card_level, 'type': card_type, 'adj_stats': adjusted_stats, 
					   'avg_skill': avg_skill_score, 'skills': final_skills, 'upgrade_id': card_upgrade_id}
	return results

def print_results_paginated(data, pageLength=30):
	# score and sort each card for overall skill and stats
	score_by_fields(data, 'avg_skill', 'adj_stats')
	skill_sorted = sort_scored_results(data)

	# rarity, name, id, adjusted stats, avg skill score
	out_string = "[{}] {} ({}) - {:.1f} / {:.1f}"

	print("Sort by Stats + Skill")
	# pagination to prevent overscroll
	count = 0
	curPage = 1

	for i in range(len(skill_sorted) - 1, -1, -1):
		if count > pageLength * curPage:
			if input(f"Page {curPage}... (Q): Quit (Enter): Next Page :: ") == "q":
				break
			
			curPage += 1
		count += 1
		val = data[skill_sorted[i][0]]
		print(out_string.format(val['rarity'], val['name'], val['id'], val['adj_stats'],val['avg_skill']))

def main(args):
	files = get_files(args.file)

	cards = parse_cards(files, args, ignore=True)
	if 'test.db' not in os.listdir(os.path.join(os.getcwd(), 'data')):
		build_tyrant_db('data/test.db', 'src/tu_tables.sql', cards)
	print(f"{len(cards)} cards found!")

	pageLen = args.page if args.page is not None else 30

	print_results_paginated(cards, pageLen)

def setup_argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument("--set", action="extend", nargs="+", help="Filter by set id. ex: 1000 for base set", type=int)
	parser.add_argument("--rarity", action="extend", nargs="+", help="Filter by rarity (1-6)", type=int)
	parser.add_argument("--file", action="extend", nargs="+", help="Select file from data. Load all by default", type=str)
	parser.add_argument("-fl", "--fusion-level", action="extend", nargs="+", help="Filter by Fusion level (0-2)", type=int)
	parser.add_argument("--faction", action="extend", nargs="+", help="Whitelist faction(s) (1-6)", type=int)
	parser.add_argument("-c", "--cost", action="extend", nargs="+", help="Filter by cost. ex: 0 for all 0 cost", type=int)
	# TODO skill filter
	parser.add_argument("--page", action="extend", nargs=1, help="Output limit per page", type=int)
	return parser

if __name__ == "__main__":
	parser = setup_argparser()
	args = parser.parse_args()
	main(args)
