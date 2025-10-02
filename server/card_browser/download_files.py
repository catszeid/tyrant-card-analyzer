import requests
import os

from django.conf import settings

def download_all_card_data_files():
    base_url = "https://mobile.tyrantonline.com/assets/"
    files = ['skills_set.xml',
             'fusion_recipes_cj2.xml']
    headers = {
        'User-Agent': 'Tyrant-Card-Analyzer/1.0',
        'Accept': 'gzip',

    }
    for i in range(1, 22):
        files.append(f"cards_section_{i}.xml")
    for file in files:
        with requests.get(base_url + file, stream=True, headers=headers) as response:
            response.raise_for_status()

            response.encoding = 'utf-8'

            with open(os.path.join(settings.STATICFILES_DIR[0], file), 'w', encoding='utf-8') as f:
                f.write(response.text)
