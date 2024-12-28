from vars import SKILLS, TYPES

# Scoring functions to process card values

# Score a skill's budget
def score_skill(skill) -> int:
	id = skill.get('id')
	score = 0
	if id == 'jam' or id == 'flurry': # complex pricing, see below
		s_n = skill.get('n')
		if s_n: # convert to int for later calculations
			s_n = int(s_n)
		else:
			s_n = 1
		# trigger + count "On trigger: Jam n"
		if skill.get('trigger'):
			score += 30 * s_n
		else: # "Jam/Flurry n every c"
			if skill.get('c'):
				s_c = int(skill.get('c'))
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
		if skill.get('n'):
			score = int(skill.get('n'))*15 # 15 budget per skill
		else:
			score += 15
	elif id == 'summon':
		score = 10 # todo calculate summon value
	elif id == 'flying':
		score = 69 # nice
	elif id == 'evolve': # n, s (base skill), s2 (upgrade)
		s_n = skill.get('n')
		if s_n:
			s_n = int(s_n)
		else:
			s_n = 1
		s_s = skill.get('s')
		s_s2 = skill.get('s2')
		score += s_n * 30
	elif id == 'enhance': # x, s (skill)
		s_x = skill.get('x')
		if s_x:
			s_x = int(s_x)
		else:
			s_x = 1
		score += s_x * 15 # check rate
	else: # default 1:1 budgeting
		score = skill.get('x')
	return int(score)

# Convert skill Element to string for display
def skill_to_string(skill) -> str:
	out = ""
	id = skill.get("id")
	if skill.get("trigger"): # trigger is prefix
		out += "On " + skill.get("trigger") + ": "
	s_all = skill.get('all')

	if id == 'jam' or id == 'flurry': # use 'n' and 'c' only. Iterations and Cooldown respectively
		out += id
		s_n = skill.get('n')
		if s_n == None:
			s_n = 1
		if skill.get('trigger'):
			out += f" {s_n}"
		else:
			s_c = skill.get('c')
			out += " {} every {}".format(s_n, s_c)
	elif id == 'summon': # use 'card_id' only. Refers to the card summoned
		out += id
		s_card_id = skill.get('card_id')
		out += f' {s_card_id}'
	elif id == 'overload':
		out += id
		s_y = skill.get('y')
		if s_y:
			out += f" {TYPES[int(skill.get('y'))]}"
		s_n = skill.get('n')
		if s_n == None:
			s_n = 1
		out += " {}".format(s_n)

	elif id == 'enhance':
		out += id
		if s_all:
			out += " All"
		# check if n is ever used
		s_x = skill.get('x')
		s_s = skill.get('s')
		out += f" {s_s} {s_x}"
	elif id == 'evolve':
		out += id
		s_s = skill.get('s')
		s_s2 = skill.get('s2')
		if s_all:
			out += " All"
		else:
			s_n = skill.get('n')
			if s_n == None:
				s_n = 1
			out += f" {s_n}"

		out += f" {s_s} to {s_s2}"
	elif id == 'wall': # No addition parameters
		out += id
	elif id == 'flying':
		out += id
	else: # standard skill nomenclature
		out += id
		if skill.get('all'): # affect all elegible targets
			out += " all"
		if skill.get('y'): # faction restriction
			out += f" {TYPES[int(skill.get('y'))]}"
		out += f" {skill.get('x')}" # power
	return out
