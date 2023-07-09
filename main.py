import os
import pandas as pd
import scraping
import grafici
import machine_learning

csv_path = './data/recensioni.csv'

if not os.path.exists(csv_path):
    scraping.main()

df = pd.read_csv(csv_path)

grafici.plot_voti(df)

# qui applico il modello di machine learning

model, vectorizer = machine_learning.addestra_modello()
input_text = input("Scrivi una recensione: ")
predicted_rating = machine_learning.valuta_recensione(model, vectorizer, input_text)

print(f"Il testo '{input_text}' viene valutato con il voto: {predicted_rating}")

# dopo diversi tentativi, non funziona il modello, in mancaza di dati troppo negatizi, visto che ci sono troppi dati troppo positivi
# quindi ora faccio dei tentativi differenti

'''
migliorare il codice cosi da estrarre ogni singolo gioco, creare una nuova lista con tutti i giochi presenti
poi prendere i dati totali, metterli nel dataset aggiungendo altre colonne: ossia nome_videogioco...
devo fare diversi tentativi modificando il main, per far eseguire solo il codice di scraping e controllare poi le dimensioni del dataframe e i valori unici della colonna
'nome_videogioco'
'''