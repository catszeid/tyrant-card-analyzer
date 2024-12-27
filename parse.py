import xml.etree.ElementTree as ET
import scoring as scor

# load sample xml
tree = ET.parse('cards_section_1.xml')
root = tree.getroot()

# Iterate over all cards
for card in root:
	if card == None:
		print("Found empty card, skipping...")
		continue
	card_name = card.find('name')
	if card_name != None:
		card_name = card_name.text
	
	card_cost = card.find('cost') # convert for scoring
	if card_cost != None and card_cost.text != None:
		card_cost = int(card_cost.text)
	else:
		card_cost = 0
	
	card_attack = card.find('attack') # convert attack and health for scoring
	if card_attack != None and card_attack.text != None:
		card_attack = int(card_attack.text)
	card_health = int(card.find('health').text)
	card_skills = card.findall('skill') # list of 'skill' Elements
	# iterate through all upgrades for final card version
	for upgrade in card.findall('upgrade'):
		if upgrade.find('attack'):
			card_attack = int(upgrade.find('attack').text)
		if upgrade.find('health'):
			card_health = int(upgrade.find('health').text)
		if upgrade.find('cost'):
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
	card_result = "{} [{},{:.5}]({}) - [{:.5}]"
	card_result += " {}"*len(card_skills)
	print(card_result.format(card_name, total_stats, adjusted_stats, card_cost, avg_skill_score, *final_skills))