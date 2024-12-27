from vars import SKILLS, TYPES

# Scoring functions to process card values

# Score a skill's budget
def score_skill(skill):
	id = skill.get('id')
	score = 0
	if id == 'jam' or id == 'flurry': # complex pricing, see below
		s_c = int(skill.get('c'))
		s_n = skill.get('n')
		if s_n: # convert to int for later calculations
			s_n = int(s_n)
		else:
			s_n = 1
		cooldown_decrease = 8-s_c
		score += 10 # estimated 10 for flurry 1 every 8
		# estimated 10 additional per reduced cooldown (c)
		score += cooldown_decrease*10
		# estimated 10 additional per iteration (n)
		score += (s_n - 1) * 10
	elif id == 'allegiance' or id == 'legion' or id == 'coalition' or id == 'scavenge':
		score = int(skill.get('x'))*2 # 2 budget per skill
	elif id == 'revenge' or id == 'inhibt' or id == 'evade':
		score = int(skill.get('x'))*10 # 10 budget per skill
	elif id == 'absorb':
		score = int(skill.get('x'))/2 # 1 budget per 2 skill
	elif id == 'wall':
		score = 10
	elif id == 'overload':
		score = int(skill.get('n'))*15 # 15 budger per skill
	else: # default 1:1 budgeting
		score = skill.get('x')
		if score:
			score = int(score)
	return score

# Convert skill Element to string for display
def skill_to_string(skill) -> str:
	out = "" # string for output
	id = skill.get("id")
	if skill.get("trigger"): # trigger is prefix
		out += "On " + skill.get("trigger") + ": "
	out += id # skill name

	if id == 'jam' or id == 'flurry': # use 'n' and 'c' only. Iterations and Cooldown respectively
		s_n = skill.get('n')
		if s_n == None:
			s_n = 1
		s_c = skill.get('c')
		out += " {} every {}".format(s_n, s_c)
		return out
	elif id == 'summon': # use 'card_id' only. Refers to the card summoned
		s_card_id = skill.get('card_id')
		return out + f'Summon {s_card_id}'
	elif id == 'overload':
		s_n = skill.get('n')
		if s_n == None:
			s_n = 1
		out += " {}".format(s_n)
		return out
	elif id == 'wall': # No addition parameters
		return "Wall"
	else: # standard skill nomenclature
		if skill.get('all'): # affect all elegible targets
			out.join(" all")
		if skill.get('y'): # faction restriction
			out += f" {TYPES[int(skill.get('y'))]}"
		out += " " + skill.get('x') #power
		return out
