from textblob import TextBlob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import psycopg2

conn = psycopg2.connect("dbname='loki' user='loki' password='00000000' host='project9900-v2-sdyney.clnpnedcibyx.ap-southeast-2.rds.amazonaws.com' port='5433' sslmode='require'")
cur = conn.cursor()
cur.execute("SELECT * from public.review")
rows = cur.fetchall()
df = pd.DataFrame(rows)
df.fillna(0,inplace=True)
col = ['id','guest_id','rating','review','is_anonymous' ,'reservation_id','scores_accuracy','scores_check_in','scores_cleanliness','scores_communication','scores_location','scores_value']
df.columns = col

def predict(r):
	senti = TextBlob(r)
	rate = senti.sentiment.polarity
	if rate  < -0.5:
		return 1
	elif (rate >= -0.5) and (rate < 0.0):
		return 3
	elif rate >= 0.0 and rate <0.3:
		return 8
	elif rate >= 0.3 and rate <0.5:
		return 9
	elif rate >= 0.5:
		return 10

df['rating'] = df['review'].apply(predict)
#df = df[df.seti_rating.isin([False])]
df.to_csv("reviews.csv")


