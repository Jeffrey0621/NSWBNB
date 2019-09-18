# Run this script from the script directory
# flask server must be running
import csv
import psycopg2
import random
import json
import random
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ.get('PSYCOPG2_DB_CONN_DETAILS'))
cur = conn.cursor()
accid_to_reviews = {}

with open('../data/reviews.csv', mode='r') as csv_file:
    file = csv.DictReader(csv_file)

    for line in file:
        air_id = line['listing_id']
        review_date = line['date']
        reviewer_name = line['reviewer_name']
        review = line['comments']
        
        if air_id not in accid_to_reviews:
            accid_to_reviews[air_id] = []

        accid_to_reviews[air_id].append(dict(review_date=review_date, reviewer_name=reviewer_name, review=review))

with open('./airid_to_nswid.txt', mode='r') as file:
    airid_to_nswid = json.loads(file.read())
    users = {'adam','bob','charlene','dan','eric','fred','greg','hope','ian','jeffrey','kim','loki','meg','nick','owen','paul','quinn','ray','sam','tim','uma','vic','will','xavier','yvonne'}
    resv_review_dates = {}
    # air_id is string, and nsw_id is int
    for air_id, nsw_id in airid_to_nswid.items():
        nsw_id = str(nsw_id)
        print('processing accommodation_id: ' + nsw_id)
        reviews = accid_to_reviews.get(air_id, [])
        count = 0
        for review in reviews:
            # CAP NUM REVIEWS AT 20
            if count == 20:
                break

            try:
                count += 1

                # check if username already exists
                username = review['reviewer_name'].lower().strip().replace(' ', '_')
                if username in users:
                    continue

                # check if review date already exists for accommodation
                if nsw_id not in resv_review_dates:
                    resv_review_dates[nsw_id] = set()

                review_date = review['review_date']
                if review_date in resv_review_dates[nsw_id]:
                    continue

                # record username and dates so we can check for dups later
                users.add(username)
                resv_review_dates[nsw_id].add(review_date)

                email = username + '@gmail.com'
                password_hash = generate_password_hash(username)

                # create user with name of reviewer
                q = """INSERT INTO users (username,email,password_hash)
                            VALUES (%s,%s,%s) RETURNING id"""
                values = (username, email, password_hash)
                cur.execute(q, values)
                new_user_id = cur.fetchone()[0]

                # make reservation
                check_in_date = (datetime.strptime(review_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                q = """INSERT INTO reservation (accommodation_id,guest_id,check_in_date,check_out_date,status)
                            VALUES (%s,%s,%s,%s,%s) RETURNING id"""
                values = (int(nsw_id), new_user_id, check_in_date, review_date, 'checked_out')
                cur.execute(q, values)
                new_res_id = cur.fetchone()[0]

                # create new review
                scores = random.randint(8, 10)
                rating = float(scores)

                q = """INSERT INTO review (reservation_id,guest_id,rating,
                        scores_accuracy,scores_location,scores_communication,scores_check_in,scores_cleanliness,scores_value,
                        is_anonymous,review) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (new_res_id, new_user_id, rating, scores, scores, scores, scores, scores, scores,
                    False, review['review'])
                cur.execute(q, values)

            except Exception as e:
                print('Error: ' + str(e))

        # delete from acc_id to review
        accid_to_reviews.pop(air_id, None)
        # break

conn.commit()
cur.close()
conn.close()
