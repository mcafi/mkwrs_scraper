# Importa le librerie necessarie
import requests
from bs4 import BeautifulSoup

def web_scraper(url):
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.content

        soup = BeautifulSoup(page_content, 'html.parser')

        return soup
    else:
        print("Unable to access page")
