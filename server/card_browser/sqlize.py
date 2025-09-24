from .models import Card, Card_Set, Card_Skill, Faction, Rarity, Skill, Skill_Attributes
import os
import xml.etree.ElementTree as ET

from .parse import parse_cards, parse_card_sets, parse_factions, parse_skills

def delete_old_data():
    # Card (and cascade Card_Skill)
    Card.objects.all().delete()
    Skill.objects.all().delete()
    Card_Set.objects.all().delete()
    Rarity.objects.all().delete()
    Faction.objects.all().delete()

def build_tyrant_db():
    # rarity
    rarities = [
        'Common',
        'Rare',
        'Epic',
        'Legendary',
        'Vindicator',
        'Mythic'
    ]
    for i in range(0, len(rarities)):
        # offset i by 1 for data compatability
        r = Rarity(id=i+1)
        r.name = rarities[i]
        r.save()

    # faction (type)
    factions = parse_factions()
    for key in factions:
        fa = Faction(id=key)
        fa.name = factions[key]
        fa.save()

    # card set
    card_sets = parse_card_sets()
    for key in card_sets:
        cs = Card_Set(id=key)
        cs.name = card_sets[key]
        cs.save()

    # skill + skill attributes
    skills = parse_skills()
    for key in skills:
        skill = Skill(id=key)
        s = skills[key]
        for key in s:
            if key == 'name':
                skill.name = s['name']
            if key == 'desc':
                skill.desc = s['desc']
            if key == 'desc_all':
                skill.desc_all = s['desc_all']
            if key == 'desc_faction':
                skill.desc_faction = s['desc_faction']
            if key == 'desc_all_faction':
                skill.desc_all_faction = s['desc_all_faction']
            if key == 'order':
                skill.order = s['order']
            if key == 'target':
                skill.target = s['target']
            if key == 'upkeep':
                skill.upkeep = s['upkeep']
            if key == 'hidden':
                skill.hidden = s['hidden']
        skill.save()

        if 'attributes' in s:
            attributes = s['attributes']
            
            skill_attr = Skill_Attributes(skill_id=skill)
            for key in attributes:
                if key == 'x':
                    skill_attr.x = attributes['x']
                if key == 'y':
                    skill_attr.y = attributes['y']
                if key == 'all':
                    skill_attr.all = attributes['all']
                if key == 'c':
                    skill_attr.c = attributes['c']
                if key == 's':
                    skill_attr.s = attributes['s']
                if key == 'n':
                    skill_attr.s2 = attributes['n']
            skill_attr.save()

    # card + card_skill
    card_files = []
    for i in range(1, 22):
        card_files.append(f"cards_section_{i}.xml")
    data = parse_cards(card_files)
    for key in data:
        n_card = Card()
        n_card.id = data[key]['id']
        n_card.name = data[key]['name']
        n_card.attack = data[key]['attack']
        n_card.health = data[key]['health']
        n_card.cost = data[key]['cost']
        n_card.rarity = Rarity.objects.get(id=data[key]['rarity'])
        
        if data[key]['set'] is None:
            n_card.card_set = None
        else:
            n_card.card_set = Card_Set.objects.get(id=data[key]['set'])
        n_card.faction = Faction.objects.get(id=data[key]['type'])
        n_card.fusion_level = data[key]['fusion_level']
        n_card.upgrade_id = data[key]['upgrade_id']
        n_card.level = data[key]['level']
        n_card.save()

        for skill in data[key]['skills']:
            n_skill = Card_Skill(owner_id=n_card)
            # skill_id
            skill_id = skill.get('id')
            if skill_id == 'arored':
                skill_id = 'armored'
            elif skill_id == 'Leech':
                skill_id = 'leech'
            n_skill.skill_id = Skill(id=skill_id)
            
            # x
            n_skill.x = skill.get('x', None)
            # y
            n_skill.y = skill.get('y', None)
            # all
            n_skill.all = skill.get('all', None)
            # n
            n_skill.n = skill.get('n', None)
            # c
            n_skill.c = skill.get('c', None)
            # s
            n_skill.s = skill.get('s', None)
            # s2
            n_skill.s2 = skill.get('s2', None)
            # trigger
            n_skill.trigger = skill.get('trigger', None)
            n_skill.card_id = skill.get('card_id', None)
            n_skill.save()