import pandas as pd
import psycopg2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


def knnpredict(input_user_id):
    #connect to database and get original accommodation table
    conn = psycopg2.connect("dbname='loki' user='loki' password='00000000' host='project9900-v2-sdyney.clnpnedcibyx.ap-southeast-2.rds.amazonaws.com' port='5433' sslmode='require'")
    cur = conn.cursor()
    cur.execute("SELECT * from public.accommodation")
    rows = cur.fetchall()
    
    #convert data to dataframe
    df = pd.DataFrame(rows)
    df.fillna(0,inplace=True)
    col = ['id','host_id','name','num_guests','num_bedrooms' ,'num_beds','num_bathrooms','description','suburb','city','state','country','price','property_type','amenities','image_urls','rating',
    'num_reviews','scores_accuracy','scores_check_in','scores_cleanliness','scores_communication','scores_location','scores_value','is_deleted']
    df.columns = col
    
    #get useful data
    df = df[['id', 'num_guests', 'num_bedrooms', 'num_beds', 'num_bathrooms', 'price', 'rating', 'num_reviews']]
    
    #if user not login, we recommend four random popular accomendation which rating higher than 9
    if input_user_id==0:
        high_rating = df[df.rating>9]
        #random select data from df
        high_rating = high_rating.sample(frac=0.5)
        return high_rating[0:4].id.tolist()
    
    #connect to database and get original review table
    conn2 = psycopg2.connect("dbname='loki' user='loki' password='00000000' host='project9900-v2-sdyney.clnpnedcibyx.ap-southeast-2.rds.amazonaws.com' port='5433' sslmode='require'")
    cur2 = conn2.cursor()
    cur2.execute("SELECT * from public.review")
    rows2 = cur2.fetchall()
    
    #convert data to dataframe
    df_review = pd.DataFrame(rows2)
    df_review.fillna(0,inplace=True)
    col_review = ['id','guest_id','review_score','review','is_anonymous','reservation_id','scores_accuracy','scores_check_in','scores_cleanliness','scores_commiunication','scores_location','scores_value']
    df_review.columns = col_review

    #get useful data
    df_review = df_review[['id','guest_id','review_score','review']]

    #get users review
    input_user_id = [input_user_id]
    reviews = df_review[df_review.guest_id.isin(input_user_id)]

    #check if user have review history or not
    if len(reviews)<2:
        input_user_id = [input_user_id,27,28]
        reviews = df_review[df_review.guest_id.isin(input_user_id)]
        
    
    #filter user review_score which higher than 80
    reviews = reviews[reviews.review_score>8]
    reviews['review_score'] = 1
    reviews = reviews[['id','review_score']]

    input_accommodation_id = reviews[['id']]

    #get features of accommodations
    col = list(df.columns)
    items_num = df[['id', 'num_guests', 'num_bedrooms', 'num_beds', 'num_bathrooms', 'price', 'rating', 'num_reviews']]

    #clen data
    items_num['id'].astype(int)
    items_num = pd.merge(items_num, reviews, on='id', how='left')
    items_num.fillna(0,inplace = True)


    #create a dataframe with all training data except the target column
    #check that the target variable has been removed
    X = items_num[['id', 'num_guests', 'num_bedrooms', 'num_beds', 'num_bathrooms', 'price', 'rating', 'num_reviews']]

    #separate target values
    y = items_num['review_score'].values
    #view target values
    #y

    """
    #following code is for testing accuracy
    #split dataset into train and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1, stratify=y)


    # Create KNN classifier
    knn = KNeighborsClassifier(n_neighbors = 2)
    # Fit the classifier to the data
    knn.fit(X_train,y_train)
    

    #show first 5 model predictions on the test data
    knn.predict(X_test)
    knn.score(X_test, y_test)
    #create a new KNN model
    knn_cv = KNeighborsClassifier(n_neighbors=2)
    #train model with cv of 5 
    cv_scores = cross_val_score(knn_cv, X, y, cv=5)
    #print each cv score (accuracy) and average them
    print(cv_scores)
    print('cv_scores mean:{}'.format(np.mean(cv_scores)))
    #create new a knn model
    knn2 = KNeighborsClassifier()
    #create a dictionary of all values we want to test for n_neighbors
    param_grid = {'n_neighbors': np.arange(1, 8)}
    #use gridsearch to test all values for n_neighbors
    knn_gscv = GridSearchCV(knn2, param_grid, cv=5)
    #fit model to data
    knn_gscv.fit(X, y)
    #check top performing n_neighbors value
    knn_gscv.best_params_
    p = knn.predict(X)
    """

    #NearestNeighbors
    #n_neighbors=5,defult is 5，find k nearest neighbors
    #algorithm='auto'

    nbrs = KNeighborsClassifier(n_neighbors=5, algorithm="auto").fit(X,y)
    distances, indices = nbrs.kneighbors(X)
    
    #return k nearest neighbors and distance，indices is the index of point
    indices = pd.DataFrame(indices)
    indices.columns = ['self','top1','top2','top3','top4']
    distances = pd.DataFrame(distances)
    distances.columns = ['self2','d1','d2','d3','d4']
    item_with_r = items_num.join(indices, how='outer')
    i3 = item_with_r.join(distances, how='outer')
    result = i3[[ 'top1',
           'top2', 'top3','top4','d1','d2','d3','d4','rating', 'num_reviews', 'review_score' ]]
    
    #get similar array result
    result = result.copy()
    result.loc[:,'id'] = items_num['id']

    input_accommodation_id_list = input_accommodation_id['id'].tolist()
    final_result = result[result.id.isin(input_accommodation_id_list)]
    
    #get top4 similar accommodation
    final_result = final_result[:1][['top1','top2','top3','top4']]

    final_result_list = final_result.to_csv(None, header=False, index=False).split('\n')
    final_result_list = final_result_list[0]
    final_result_list = final_result_list.split(',')
    return final_result_list
    
#knnpredict(0)
