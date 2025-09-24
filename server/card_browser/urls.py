from django.urls import path

from . import views

app_name = "card_browser"
urlpatterns = [
    path("", views.index, name="index"),
    path("init_db", views.initialize_database, name="init_db"),
    path("download_cards", views.download_cards, name="download_data"),
    path("<int:card_id>", views.card_detail, name='detail'),
]