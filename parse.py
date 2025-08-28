import xml.etree.ElementTree as ET
import os
import re
import argparse

import scoring as scor

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
def find_files(file_pattern) -> list:
	dir_contents = os.listdir(os.path.join(os.getcwd(), 'data'))
	pattern = re.compile(file_pattern)
	match_files = [file for file in dir_contents if pattern.fullmatch(file)]
	return match_files

# get the list of data files to read for cards
# When files is None, it will search for all files matching the default naming scheme
def get_files(files=None) -> list:
	fileList = []
	if files is not None:
		dir_contents = os.listdir(os.path.join(os.getcwd(), 'data'))
		for file in files:
			if file in dir_contents:
				fileList.append(file)
			else:
				print(f"Failed to find {file}")
	else:
		pattern = "^cards_section_\\d+.xml$"
		fileList = find_files(pattern)

	return fileList

def get_ignored_list() -> set:
	# ignore ids Block
	ignored_file = find_files("^ignoredcards.xml$")
	ignored_ids = set()
	if len(ignored_file) > 0:
		file = ignored_file[0]
		tree = ET.parse((os.path.join(os.getcwd(), 'data', file)))
		root = tree.getroot()
		for id in root:
			if id is not None and id.text is not None:
				ignored_ids.add(id.text)
	return ignored_ids

def score_by_fields(data, *argv):
	for key in data:
		score = 0
		for arg in argv:
			score += data[key][arg]
		data[key]['score'] = score

# parse files for cards with the given arguments
def parse_cards(files: list, args) -> dict:
	results = {}

	ignored_ids = get_ignored_list()

	for file in files:
		tree = ET.parse(os.path.join(os.getcwd(), 'data', file))
		root = tree.getroot()
		
		for card in root:
			if card is None:
				print("Found empty card in {file}, skipping...")
				continue
			card_id = card.find('id')
			if card_id is not None:
				# id ignore, note the id should target base card, not upgrade
				if card_id.text in ignored_ids:
					continue
				card_id = card_id.text
			else:
				print(f"Warning: Card {card_id} in {file} has no card_id")
				continue
			card_name = card.find('name')
			if card_name is not None and card_name.text is not None:
				card_name = card_name.text
			else:
				print(f"Warning: Card {card_id} in {file} has no name")
				continue
			card_set = card.find('set')
			if card_set is not None and card_set.text is not None:
				card_set = card_set.text
			else:
				print(f"Warning: Card {card_id} in {file} does not have a set")
				continue
			if args.set is not None and int(card_set) not in args.set:
				continue
			
			# card rarity filtering
			card_rarity = card.find('rarity')
			if card_rarity is not None:
				if card_rarity.text is not None:
					card_rarity = card_rarity.text
				else:
					print(f"Warning: Card {card_id} in {file} has no rarity")
					continue
				if args.rarity is not None and int(card_rarity) not in args.rarity:
					continue
				
			# card fusion level
			card_fusion_level = card.find('fusion_level')
			if card_fusion_level is not None and card_fusion_level.text is not None:
				card_fusion_level = int(card_fusion_level.text)
			else:
				card_fusion_level = 0
			if args.fusion_level is not None and int(card_fusion_level) not in args.fusion_level:
				continue
			# card cost (Commander have no cost)
			card_cost = card.find('cost')
			if card_cost is None:
				continue # commander analysis will be considered later
			if card_cost.text is not None:
				if args.cost is not None and int(card_cost.text) not in args.cost:
					continue
				card_cost = int(card_cost.text)
			else:
				print(f"Warning: Card {card_id} in {file} has no cost")
				continue
			# card attack (Structure have no attack)
			card_attack = card.find('attack')
			if card_attack is not None and card_attack.text is not None:
				card_attack = int(card_attack.text)
			# card health
			card_health = card.find('health')
			if card_health is not None and card_health.text is not None:
				card_health = int(card_health.text)
			else:
				print(f"Warning: Card {card_id} in {file} has no health")
				continue
			# card type (faction)
			card_type = card.find('type')
			if card_type is not None and card_type.text is not None:
				card_type = int(card_type.text)
			else:
				print(f"Warning: Card {card_id} in {file} has no type")
				continue
			if args.faction is not None and card_type not in args.faction:
				continue
			
			card_skills = card.findall('skill') # list of 'skill' Elements
			# iterate and apply upgrades
			for upgrade in card.findall('upgrade'):
				if upgrade.find('card_id') is not None:
					card_id = upgrade.find('card_id').text
				if upgrade.find('attack') is not None:
					if upgrade.find('attack').text is None: # 47055 has 'attack' with no text
						print(f"Warning: Empty attack tag in card {card_id} in {file}")
					else:
						card_attack = int(upgrade.find('attack').text)
				if upgrade.find('health') is not None:
					card_health = int(upgrade.find('health').text)
				if upgrade.find('cost') is not None:
					if upgrade.find('cost').text is None:
						print(f"Warning: Card {card_id} in {file} has empty cost field")
					else:
						card_cost = int(upgrade.find('cost').text)
				if len(upgrade.findall('skill')) != 0:
					# reset skills and refill the list
					card_skills = []
					for skill in upgrade.findall('skill'):
						card_skills.append(skill)
			# filter skill here TODO
			# score stats
			total_stats = card_health
			if card_attack is not None:
				total_stats += card_attack
			adjusted_stats = (total_stats) / (card_cost + 1)
			# score skills
			skill_score = 0
			avg_skill_score = 0.0
			# convert skills from Element to readable string
			final_skills = []
			for skill in card_skills:
				skill_score += scor.score_skill(skill)
				final_skills.append(scor.skill_to_string(skill))
			if len(final_skills) > 0:
				avg_skill_score = skill_score / len(final_skills)

			# dictionary holding name, rarity, cost, adjusted stats, avg skill score
			results[card_id] = {'id': card_id, 'name': card_name, 'rarity': card_rarity, 'adj_stats': adjusted_stats, 'avg_skill': avg_skill_score, 'skills': final_skills}
	return results

def print_results_paginated(data, pageLength=30):
	# score and sort each card for overall skill and stats
	score_by_fields(data, 'avg_skill', 'adj_stats')
	skill_sorted = sort_scored_results(data)

	# rarity, name, id, adjusted stats, avg skill score
	out_string = "[{}] {} ({}) - {:.5} / {:.5}"

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

	cards = parse_cards(files, args)
	print(f"{len(cards)} cards found!")

	pageLen = 30
	if args.page is not None:
		pageLen = args.page

	print_results_paginated(cards, pageLen)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--set", action="extend", nargs="+", help="Filter by set id. ex: 1000 for base set", type=int)
	parser.add_argument("--rarity", action="extend", nargs="+", help="Filter by rarity (1-6)", type=int)
	parser.add_argument("--file", action="extend", nargs="+", help="Select file from data. Load all by default", type=str)
	parser.add_argument("-fl", "--fusion-level", action="extend", nargs="+", help="Filter by Fusion level (0-2)", type=int)
	parser.add_argument("--faction", action="extend", nargs="+", help="Whitelist faction(s) (1-6)", type=int)
	parser.add_argument("-c", "--cost", action="extend", nargs="+", help="Filter by cost. ex: 0 for all 0 cost", type=int)
	# TODO skill filter
	parser.add_argument("--page", action="extend", nargs=1, help="Output limit per page", type=int)
	args = parser.parse_args()
	main(args)
