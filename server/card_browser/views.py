from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Card, Card_Skill

from card_browser.tasks import download_files_task, rebuild_card_db_task, test_task

def index(request):
    cards = get_list_or_404(Card)[:10]
    
    return render(request, "card_browser/index.html", {"card_data": cards})

# Initialize the card database from empty
def initialize_database(request):
    rebuild_card_db_task.delay()
    return HttpResponse("Initialized database successfully!")

def download_cards(request):
    # back up data?
    # download
    files = ['skills_set.xml',
             'fusion_recipes_cj2.xml']
    for i in range(1, 22):
        files.append(f"cards_section_{i}.xml")
    download_files_task.delay(files)
    #download_files_task.delay(files)
    return HttpResponse("Downloading card data now...")


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