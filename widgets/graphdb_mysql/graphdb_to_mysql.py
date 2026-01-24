from dotenv import get_key, set_key, load_dotenv, find_dotenv
import requests
from urllib.parse import quote
import csv
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from PyQt5.QtWidgets import *

def GraphDBToMySQL():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    GRAPHDB_URL = get_key(dotenv_path, "GRAPHDB_URL")
    if GRAPHDB_URL.endswith("/"): GRAPHDB_URL = GRAPHDB_URL[:-1]
    GRAPHDB_REPOSITORY = get_key(dotenv_path, "GRAPHDB_REPOSITORY")

    headers = {
        'Accept': 'application/sparql-results+json'
    }

    spql = """
        PREFIX imdb: <http://academy.ontotext.com/imdb/>
        PREFIX schema: <http://schema.org/>

        SELECT * { 
            ?movie a imdb:ColorMovie ;
                schema:name ?movieName ;
                schema:commentCount ?commentCount .
        } ORDER BY DESC(?commentCount)
    """

    response = requests.get(f"{GRAPHDB_URL}/repositories/{GRAPHDB_REPOSITORY}?query={quote(spql)}", headers=headers)
    films = response.json()["results"]["bindings"]
    films_data = []


    for film in films:
        movie = film["movie"]["value"]
        movie_name = film["movieName"]["value"]
        comment_count = film["commentCount"]["value"]
        films_data.append([movie, movie_name, comment_count])

    # Create a DataFrame for one-hot encoding
    df = pd.DataFrame(films_data, columns=["movie", "movieName", "commentCount"])
    # Initialize label encoder
    label_encoder = LabelEncoder()

    # Fit label encoder and transform movie names to numerical labels
    df['movie'] = label_encoder.fit_transform(df['movie'])
    df["movieName"] = label_encoder.fit_transform(df["movieName"])

    #df.to_csv("data/movies.csv", index=False)    

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Successfully converted")
    msg.setWindowTitle("GraphDB to MySQL")
    msg.exec_()