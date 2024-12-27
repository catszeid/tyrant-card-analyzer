# skill xml attributes
#	id - skill name (see SKILLS)
#	all - does this apply to all eligibile assault? 1=true
#	x - skill magnitude. integer
#	y - type (faction) restriction
#	n - amount of times to trigger. integer [Jam and Flurry ONLY]
#	c - cooldown between activations. integer [Jam and Flurry ONLY]
#	trigger - activation override for when to trigger (see TRIGGERS)
#	card_id - id of summoned card. [Summon ONLY]

SKILLS = (
	'none',
	'wall',
	'armored',
	'counter',
	'heal',
	'rally',
	'strike',
	'weaken',
	'besiege',
	'pierce',
	'poison',
	'leech',
	'evade',
	'berserk',
	'enfeeble',
	'protect',
	'enhance',
	'jam',
	'corrosive',
	'inhibit',
	'flurry',
	'valor',
	'overload',
	'payback',
	'avenge',
	'refresh',
	'venom',
	'mend',
	'mortar',
	'swipe',
	'sunder',
	'enrage',
	'allegiance',
	'drain',
	'stasis',
	'revenge',
	'mimic',
	'coalition',
	'subdue',
	'barrier',
	'entrap',
	'subdue',
	'tribute',
	'summon',
	'bravery',
	'absorb',
	'disease',
	'mark',
	'fortify',
	'hunt',
	'scavenge'
)

TYPES = (
	"none",
	"Imperial",
	"Raider",
	"Xeno",
	"Bloodthirsty",
	"Righteous",
	"Progenitor",
)

TRIGGERS = (
	"attacked", # trigger when card attacked
	"death", # trigger on card death
	"play", # trigger on card play
)
