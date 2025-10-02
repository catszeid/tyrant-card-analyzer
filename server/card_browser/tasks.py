from celery import shared_task
from django.conf import settings
import os
import requests
import shutil
import xml.etree.ElementTree as ET

from .models import Card, Card_Set, Card_Skill, Faction, Rarity, Skill, Skill_Attributes
from .parse import find_files, parse_cards, parse_card_sets, parse_factions, parse_skills

@shared_task
def download_files_task(files):
    base_url = "https://mobile.tyrantonline.com/assets/"
    headers = {
        'User-Agent': 'Tyrant-Card-Analyzer/1.0',
        'Accept': 'gzip',
    }

    for file in files:
        with requests.get(base_url + file, stream=True, headers=headers) as response:
            response.raise_for_status()

            response.encoding = 'utf-8'

            with open(os.path.join(settings.STATICFILES_DIR[0], file), 'w', encoding='utf-8') as f:
                f.write(response.text)

@shared_task
def test_task(data):
    print(data)

@shared_task
def rebuild_card_db_task():
    # TODO: Check for relevant data files
    # at least 'skills_set.xml', and 1+ 'cards_section_\d*.xml'
    cards_section_pattern = "^cards_section_\\d+.xml$"
    skills_set_pattern = "^skills_set.xml$"
    skills_set_xml = find_files(skills_set_pattern)
    cards_section_xml = find_files(cards_section_pattern)

    if len(skills_set_xml) < 1:
        print("'skills_set.xml' not found, aborting database build. Try downloading files again.")
        return
    if len(cards_section_xml) < 1:
        print("No card data found. Download data files first.")
        return

    # create backup copy of db. TODO: find better solution
    # file name should be pulled from settings too
    db_file = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    db_backup = os.path.join(settings.BASE_DIR, 'db.sqlite3.bak')
    if os.path.isfile(db_file):
        try:
            shutil.copy(db_file, db_backup)
            print(f"Database backup created successfully!")
        except FileNotFoundError:
            print(f"Error: expected database file '{db_file}' not found")
        except Exception as e:
            print(f"An error occurred: {e}")

    # clear existing tables
    Card.objects.all().delete()
    Skill.objects.all().delete()
    Card_Set.objects.all().delete()
    Rarity.objects.all().delete()
    Faction.objects.all().delete()

    # static rarity values. Maybe put in vars elsewhere
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

    # faction (type) from 'skills_set.xml'
    factions = parse_factions()
    for key in factions:
        fa = Faction(id=key)
        fa.name = factions[key]
        fa.save()

    # card set from 'skills_set.xml'
    card_sets = parse_card_sets()
    for key in card_sets:
        cs = Card_Set(id=key)
        cs.name = card_sets[key]
        cs.save()

    # skill + skill attributes from 'skills_set.xml'
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
            n_skill_y = skill.get('y', None)
            if n_skill_y is not None:
                n_skill.y = Faction.objects.get(id=n_skill_y)
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