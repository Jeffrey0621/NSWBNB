# Run this script from the script directory
import csv
import os
import psycopg2
import re
import random
import json
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ.get('PSYCOPG2_DB_CONN_DETAILS'))
cur = conn.cursor()
hosts = ['adam','bob','charlene','dan','eric','fred','greg','hope','ian','jeffrey','kim','loki','meg','nick','owen','paul','quinn','ray','sam','tim','uma','vic','will','xavier','yvonne']
airid_to_nswid = {}

# create users
for host in hosts:
    username = host
    email = username + '@gmail.com'
    password_hash = generate_password_hash(username)

    # create user with name of reviewer
    q = """INSERT INTO users (username,email,password_hash)
                VALUES (%s,%s,%s) RETURNING id"""
    values = (username, email, password_hash)
    cur.execute(q, values)

with open('../data/sydney-detailed.csv', mode='r') as csv_file:
    file = csv.DictReader(csv_file)
    line_count = 0
    for line in file:
        if line_count == 2500: # set to 100
            break

        if not line['host_neighbourhood']:
            continue

        if line['host_neighbourhood'] not in ['Bondi Beach', 'North Bondi', 'Manly', 'Darlinghurst', 'Bondi', 'Surry Hills', 'Randwick']:
            continue

        if not line['review_scores_rating']:
            continue
        
        image_filename = '../data/listing-images/sydney/' + line['id']

        try:
            if os.stat(image_filename).st_size != 0:
                with open(image_filename, mode='r') as images:
                    image_urls = []
                    for url in images:
                        image_urls.append(url.strip())

                    price_in_cents = re.sub('[$,.]','',line['price'] or '$99.00')

                    # construct SQL query
                    q = """INSERT INTO accommodation (host_id,name,num_guests,num_bedrooms,num_beds,num_bathrooms,description,
                            suburb,city,state,country,price,property_type,amenities,image_urls,rating,num_reviews,
                            scores_accuracy,scores_cleanliness,scores_check_in,scores_communication,scores_location,scores_value)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""

                    host_id = random.randint(1, len(hosts))
                    
                    values = (
                        host_id,
                        line['name'] or 'Best house ever',
                        line['guests_included'] or 4,
                        line['bedrooms'] or 2,
                        line['beds'] or 2,
                        float(line['bathrooms']) if line['bathrooms'] else 1,
                        line['description'] or 'This is the best holiday home in NSW!',
                        line['host_neighbourhood'],
                        line['city'] or 'Sydney',
                        line['state'] or 'New South Wales',
                        line['country'] or 'Australia',
                        price_in_cents,
                        line['property_type'] or 'Apartment',
                        line['amenities'].lower() or '{}',
                        image_urls,
                        # should not put in default scores as this means they have scores
                        # but no reviews, which doesn't make sense
                        float(line['review_scores_rating']) / 10,
                        line['number_of_reviews'],
                        line['review_scores_accuracy'] or None,
                        line['review_scores_cleanliness'] or None,
                        line['review_scores_checkin'] or None,
                        line['review_scores_communication'] or None,
                        line['review_scores_location'] or None,
                        line['review_scores_value'] or None
                    )
                    cur.execute(q, values)
                    new_acc_id = cur.fetchone()[0]

                    airid = line['id']
                    airid_to_nswid[str(airid)] = new_acc_id
                    line_count += 1
        except FileNotFoundError as fe:
            print(fe)
        except Exception as e:
            print(e)
            print('exception when inserting with id of ' + str(line['id']))

        # line_count += 1

conn.commit()
cur.close()
conn.close()

with open('./airid_to_nswid.txt', 'w') as file:
    file.write(json.dumps(airid_to_nswid))


