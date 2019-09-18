# coding: utf-8
#Use our Recommendation system to return the best recommend accommodation id

#import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import psycopg2
from sklearn.metrics.pairwise import cosine_similarity



#Item Based Similarity recommendation system

def predict(accommodation_id):
    #import data from database
    conn = psycopg2.connect("dbname='loki' user='loki' password='00000000' host='project9900-v2-sdyney.clnpnedcibyx.ap-southeast-2.rds.amazonaws.com' port='5433' sslmode='require'")
    cur = conn.cursor()
    #cur.execute("INSERT INTO public.user (user_id, email) VALUES (%s, %s)",(1, "001@gmail.com"))
    cur.execute("SELECT * from public.accommodation")
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    df.fillna(0,inplace=True)
    
    #Data clean
    col = ['id','host_id','name','num_guests','num_bedrooms' ,'num_beds','num_bathrooms','description','suburb','city','state','country','price','property_type','amenities','image_urls','rating',
    'num_reviews','scores_accuracy','scores_check_in','scores_cleanliness','scores_communication','scores_location','scores_value','is_deleted']
    df.columns = col
    df = df[df.is_deleted.isin([False])]
    df = df[['id', 'num_guests', 'num_bedrooms', 'num_beds', 'num_bathrooms', 'price', 'rating', 'num_reviews']]

    #Getting useful features
    items_num = df
    items_num_norm = items_num[['num_guests', 'num_bedrooms', 'num_beds', 'num_bathrooms', 'price', 'rating', 'num_reviews']]

    #Use standard_scaler and standard_matrix to normalize data
    standard_scaler = preprocessing.StandardScaler()
    standard_matrix = standard_scaler.fit_transform(items_num)

    #Compute the cosine similarity matrix using the dummy ratings matrix
    cosine_sim = cosine_similarity(standard_matrix)

    #cosine_sim
    #Convert into pandas dataframe 
    ac_id = np.array(items_num['id']).tolist()

    cosine_sim = pd.DataFrame(cosine_sim, index=ac_id, columns=ac_id)

    #Get similarity list based in cosine matrix
    similarity_list = cosine_sim[accommodation_id][1:].sort_values(ascending=False)
    recommend_accommodation_id = similarity_list[0:20]
    list_of_recommend_accommodation_id = recommend_accommodation_id.index.tolist()
    
    #set rating threshold
    #recommended accommodation rating must larger than 8
    for i in list_of_recommend_accommodation_id:
        if items_num.loc[items_num[(items_num.id==i)].index.tolist()[0],'rating']>8:
            continue
        else:
            list_of_recommend_accommodation_id.remove(i)
    return list_of_recommend_accommodation_id[1:5]

#predict(accommodation_id)

