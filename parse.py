import xml.etree.ElementTree as ET
import os
import re
import argparse

import scoring as scor

def find_files(file_pattern):
	dir_contents = os.listdir(os.getcwd())
	# regex to match xml files
	pattern = re.compile(file_pattern)
	match_files = [file for file in dir_contents if pattern.fullmatch(file)]
	return match_files

def main(args):
	# file gathering
	files = []
	if args.file != None:
		dir_contents = os.listdir(os.getcwd())
		for file in args.file:
			if file in dir_contents:
				files.append(file)
			else:
				print(f"Failed to find {file}")
	else:
		pattern = "^cards_section_\d*.xml$"
		files = find_files(pattern)
	input(f"{len(files)} files found. Press enter to continue...")
	# load xml
	for file in files:
		print(f"Processing {file}...")
		tree = ET.parse(file)
		root = tree.getroot()
		
		# Iterate over all cards
		for card in root:
			if card == None:
				print("Found empty card, skipping...")
				continue
			# card id
			card_id = card.find('id')
			if card_id != None:
				card_id = card_id.text
			else:
				 card_id = -1
			# card name
			card_name = card.find('name')
			if card_name != None:
				card_name = card_name.text
			# card set + filtering
			card_set = card.find('set')
			if card_set != None:
				card_set = card_set.text
			if card_set != None and args.set != None:
				if int(card_set) == args.set:
					pass
				else:
					continue
			# card rarity filtering
			card_rarity = card.find('rarity')
			if card_rarity != None:
				card_rarity = card_rarity.text
			if card_rarity != None and args.rarity != None:
				if int(card_rarity) == args.rarity:
					pass
				else:
					continue
			# card cost (Commander have no cost)
			card_cost = card.find('cost') # convert for scoring
			if card_cost == None:
				continue # commander analysis will be considered later
			if card_cost.text != None:
				card_cost = int(card_cost.text)
			else:
				print(f"Error: No cost found for {card_id}")
				continue
			# card attack (Structure have no attack)
			card_attack = card.find('attack') # convert attack and health for scoring
			if card_attack == None:
				pass # Structure have no attack tag
			if card_attack != None and card_attack.text != None:
				card_attack = int(card_attack.text)
			# card health
			card_health = card.find('health')
			if card_health != None and card_health.text != None:
				card_health = int(card_health.text)
			else:
				print(f"Error: No health found for {card_id}")
				continue
			# card skills
			card_skills = card.findall('skill') # list of 'skill' Elements
			# iterate and apply upgrades
			for upgrade in card.findall('upgrade'):
				if upgrade.find('card_id') != None:
					card_id = upgrade.find('card_id').text
				if upgrade.find('attack') != None:
					card_attack = int(upgrade.find('attack').text)
				if upgrade.find('health') != None:
					card_health = int(upgrade.find('health').text)
				if upgrade.find('cost') != None:
					if upgrade.find('cost').text == None:
						card_cost = 0
					else:
						card_cost = int(upgrade.find('cost').text)
				if len(upgrade.findall('skill')) != 0:
					# reset skills and refill the list
					card_skills = []
					for skill in upgrade.findall('skill'):
						card_skills.append(skill)
			# score stats
			total_stats = card_health
			if card_attack != None:
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
			card_result = "[{:5}]{} [{:.5}]({}) - [{:.5}]"
			card_result += " {}"*len(card_skills)
			print(card_result.format(card_id, card_name, adjusted_stats, card_cost, avg_skill_score, *final_skills))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--set", help="filter by set", type=int)
	parser.add_argument("--rarity", help="filter by rarity (1-6)", type=int)
	parser.add_argument("-f", "--file", action="extend", nargs="+", help="select file. Load all by default", type=str)
	args = parser.parse_args()
	main(args)
