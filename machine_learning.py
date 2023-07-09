import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def addestra_modello():
    # Caricamento del dataset
    csv_path = './data/recensioni.csv'
    df = pd.read_csv(csv_path)

    # Feature Engineering: Creazione di nuove feature
    df['Lunghezza_Recensione'] = df['Recensione'].apply(len)

    # Selezione delle feature
    features = ['Lunghezza_Recensione']
    X = df[features]
    y = df['Voto']

    # Divisione del dataset in training set e test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creazione e addestramento dei modelli
    models = [
        ('Linear Regression', LinearRegression()),
        ('Decision Tree', DecisionTreeRegressor()),
        ('Random Forest', RandomForestRegressor())
    ]

    trained_models = []

    for name, model in models:
        model.fit(X_train, y_train)
        trained_models.append((name, model))

        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"{name}: MSE = {mse}")

    return trained_models

def valuta_recensione(model, input_text):
    # Feature Engineering: Creazione di nuove feature per il testo di input
    lunghezza_recensione = len(input_text)

    # Costruzione del vettore di feature
    input_features = pd.DataFrame({'Lunghezza_Recensione': [lunghezza_recensione]})

    # Valutazione dei modelli per il testo di input
    ratings = []

    for name, model in model:
        rating = model.predict(input_features)[0]
        ratings.append((name, rating))

    return ratings

# Addestramento dei modelli
trained_models = addestra_modello()

# Esempio di utilizzo
input_text = input("Scrivi una recensione: ")
predicted_ratings = valuta_recensione(trained_models, input_text)

for name, rating in predicted_ratings:
    print(f"Il testo '{input_text}' viene valutato con il voto {rating} dal modello {name}")
