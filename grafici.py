import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_voti(df):
    if not os.path.exists("grafici"):
        os.makedirs("grafici")

    voti_validi = df['Voto'].apply(lambda x: pd.to_numeric(x, errors='coerce')).notnull() # controllo che la colonna "Voto" sia effettivamente valida e che non ci siano valori errati
    df = df[voti_validi]  # Filtraggio del DataFrame per i valori validi

    value_counts = df['Voto'].value_counts().sort_index(ascending=False) # faccio il conteggio dei voti

    ax = sns.barplot(x=value_counts.index, y=value_counts.values) # ora vado a creare il grafico con la libreria seaborn
    plt.xlabel('Voto')
    plt.ylabel('Numero di voti')
    plt.title('Distribuzione dei voti')

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom')

    plt.savefig("./grafici/distribuzione_voti.png") # salvo il grafico nella cartella "grafici"
    plt.close()

    # Generazione di un altro grafico che mostra la distribuzione dei voti in base ai giorni della settimana
    voti_df = df.copy()
    voti_df['Data'] = pd.to_datetime(voti_df['Data'], errors='coerce') # controllo che la colonna "Data" sia effettivamente valida e che non ci siano valori errati
    voti_df = voti_df.dropna(subset=['Data']) # elimino le date errate

    voti_df['GiornoSettimana'] = voti_df['Data'].dt.day_name() # estraggo il nome del giorno della settimana dalla colonna "Data"
    voti_per_giorno = voti_df['GiornoSettimana'].value_counts().sort_index() # conteggio dei voti per ogni giorno della settimana

    ax = sns.barplot(x=voti_per_giorno.index, y=voti_per_giorno.values)
    plt.xlabel('Giorno della settimana')
    plt.ylabel('Numero di voti')
    plt.title('Distribuzione dei voti per giorno della settimana')

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom')
    plt.savefig("./grafici/distribuzione_voti_giorni.png") # salvo il grafico nella cartella "grafici"
    plt.close()
    # ora fatto questo grafico possiamo andare a vedere per ogni giorno della settimana la distribuzione percentuale dei voti
    voti_percentuali = {}
    for giorno in voti_df['GiornoSettimana'].unique():
        voti_giorno = voti_df[voti_df['GiornoSettimana'] == giorno]
        divisione_percentuale = voti_giorno['Voto'].value_counts(normalize=True, sort=False) * 100
        voti_percentuali[giorno] = divisione_percentuale

    # creazione del df per dividere i dati percentuali
    divisioni_df = pd.DataFrame(voti_percentuali)
    divisioni_df = divisioni_df.reindex(columns=sorted(divisioni_df.columns, key=lambda x: int(x.split()[0]) if x.split()[0].isdigit() else x))
    divisioni_df.to_csv("./data/analisi_voti_giorno.csv", index=False) # salvo queste analisi dentro un altro csv per andare a lavorarlo da un'altra parte
    # Visualizzazione del DataFrame delle divisioni percentuali dei voti
    # print("voti nella settimana:")
    # print(divisioni_df)

    giorni = divisioni_df.columns.tolist()

    # Creazione di una figura con subplots per i grafici
    fig, axs = plt.subplots(len(giorni), 1, figsize=(6, 4*len(giorni)))
    fig.suptitle('Divisione percentuale dei voti per giorno della settimana')

    # Generazione dei grafici separati per ogni giorno della settimana
    for i, giorno in enumerate(giorni):
        ax = axs[i]
        divisione_percentuale = divisioni_df[giorno]
        y_pos = np.arange(len(divisione_percentuale))
        colors = ['royalblue', 'mediumblue', 'darkblue', 'dodgerblue', 'deepskyblue', 'lightskyblue', 'lightblue', 'powderblue', 'skyblue', 'lightsteelblue', 'steelblue']
        
        ax.barh(y_pos, divisione_percentuale, color=colors)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(divisione_percentuale.index)
        ax.invert_yaxis()
        ax.set_xlabel('Percentuale')
        ax.set_title(f"Giorno: {giorno}")

    # Salvataggio della pagina con i grafici come file PDF
    plt.tight_layout()
    plt.savefig("./grafici/pagina_grafici.pdf", format='pdf')
    plt.close()

    # Filtraggio delle date corrette per grafico solamente con le date
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df = df.dropna(subset=['Data'])

    # Creazione del grafico di distribuzione temporale
    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(x=df['Data'], y=df['Voto'])
    ax.set(xlabel='Data', ylabel='Voto', title='Distribuzione temporale dei voti')
    plt.xticks(rotation=45)

    # Salvataggio del grafico come immagine
    plt.savefig('./grafici/distribuzione_temporale.png')
    plt.close()