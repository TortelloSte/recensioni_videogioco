import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression

def addestra_modello():
    csv_path = './data/recensioni.csv'
    df = pd.read_csv(csv_path)

    vectorizer = TfidfVectorizer()
    X_transformed = vectorizer.fit_transform(df['Recensione'])
    y = df['Voto']

    model = LinearRegression()
    model.fit(X_transformed, y)

    return model, vectorizer

def valuta_recensione(model, vectorizer, input_text):
    input_text_transformed = vectorizer.transform([input_text])
    predicted_rating = model.predict(input_text_transformed)[0]

    return predicted_rating
