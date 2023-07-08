import os
import pandas as pd
import scraping
import grafici

csv_path = './data/recensioni.csv'

if not os.path.exists(csv_path):
    scraping.main()

df = pd.read_csv(csv_path)

grafici.plot_voti(df)