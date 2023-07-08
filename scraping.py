import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

class Recensione:
    def __init__(self, testata_giornalistica, voto, data, recensione, link_review):
        self.testata_giornalistica = testata_giornalistica
        self.voto = voto
        self.data = data
        self.recensione = recensione
        self.link_review = link_review

    def __str__(self):
        return f"{self.testata_giornalistica} - {self.data}\nVoto: {self.voto}\nRecensione: {self.recensione}"

def main():
    base_url = "https://www.metacritic.com/game/switch/the-legend-of-zelda-tears-of-the-kingdom/user-reviews?page="
    page_num = 0
    has_next_page = True

    lista_recensioni = []

    while has_next_page:
        url = f"{base_url}{page_num}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            soup_recensioni = soup.find_all('div', class_='review_content')

            for recensione in soup_recensioni:
                testata_giornalistica = recensione.find('div', class_='source')
                voto = recensione.find('div', class_='metascore_w')
                data = recensione.find('div', class_='date')
                recensione = recensione.find('div', class_='review_body')
                link_review = recensione.find('a', class_='external')

                if link_review is not None:
                    link_review = link_review['href']
                else:
                    link_review = None

                oggetto_recensione = Recensione(testata_giornalistica, voto, data, recensione, link_review)
                lista_recensioni.append(oggetto_recensione)

            next_button = soup.find('span', class_='flipper next')

            if next_button is None:
                has_next_page = False
            else:
                page_num += 1
        else:
            print("La pagina non è raggiungibile")

    if len(lista_recensioni) > 0:
        data = {'Voto': [], 'Data': [], 'Recensione': []}

        for recensione in lista_recensioni:
            if recensione.voto is not None:
                voto = float(recensione.voto.text)
                if voto > 10 or voto < 0:
                    continue

                data['Voto'].append(voto)
                data['Data'].append(recensione.data.text)
                data['Recensione'].append(recensione.recensione.text)

        df = pd.DataFrame(data)

        if not os.path.exists('data'):
            os.makedirs('data')

        df.to_csv('./data/recensioni.csv', index=False)

