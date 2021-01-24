"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np
import pymongo


def dataframe():
    myClient = pymongo.MongoClient("mongodb+srv://ari:Ari%40123456@cluster0.twwwz.mongodb.net/dht11?retryWrites=true&w=majority")
    # myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myClient.dht11
    collection = db.dht_data
    df = pd.DataFrame(list(collection.find()))
    df = df.drop('_id',1)
    df['id'] = df.index
    df = df[['id','suhu','kelembaban','timestamp']]
    return df