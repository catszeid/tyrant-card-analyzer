from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from.download_files import download_all_card_data_files
from .models import Card, Card_Skill
from .sqlize import delete_old_data, build_tyrant_db

def index(request):
    cards = get_list_or_404(Card)[:10]
    
    return render(request, "card_browser/index.html", {"card_data": cards})

def initialize_database(request):
    # clear old card data
    delete_old_data()
    # parse and apply new data
    build_tyrant_db()
    return HttpResponse("Initialized database successfully!")

def download_cards(request):
    # back up data?
    # download
    download_all_card_data_files()
    return HttpResponse("Downloading card data...")


def card_detail(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    prev_card = Card.objects.filter(upgrade_id=card_id).values()
    if len(prev_card) > 0:
        prev_card = prev_card[0]
    next_card = Card.objects.filter(id=card.upgrade_id).values()
    if len(next_card) > 0:
        next_card = next_card[0]
    skills = Card_Skill.objects.filter(owner_id=card_id)

    return render(request, "card_browser/card.html", {"card_data": card, "card_skills": skills, "next_card": next_card, "prev_card": prev_card})