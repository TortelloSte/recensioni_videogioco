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
