import pytest
from tests import res_to_json, res_to_token
from datetime import datetime, timedelta

def test_get_accommodation(client):
    bad_id = -1
    res = client.get('/api/accommodation/' + str(bad_id))
    assert res.status_code == 404

    # deleted accommodation should not be retrieved
    deleted_acc_id = 2
    res = client.get('/api/accommodation/' + str(deleted_acc_id))
    msg = res_to_json(res)['msg']
    assert res.status_code == 404
    assert msg == 'Accommodation not found'

    good_id = 1
    res = client.get('/api/accommodation/' + str(good_id))
    msg = eval(res.data.decode('utf-8'))['msg']
    assert res.status_code == 200
    assert msg['id'] == good_id
    assert msg['property_type'] == 'Space ship'

    # tomorrow should be unavailable to book as it is already booked
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    assert msg['unavailable_dates'] == [today, tomorrow]

def test_create_accommodation(client, auth):
    host_id = 4
    num_guests = 1
    num_bedrooms = 1
    num_beds = 1
    num_bathrooms = 1
    description = 'The best house ever'
    city = 'Sydney'
    country = 'Australia'
    price = '99999999'
    property_type = 'space ship'
    amenities = 'wifi,asdf'
    image_urls = 'www.sharksarefriendly.com'
    bad_token = 'bad_token'

    post_data = {
        'host_id': host_id,
        'num_guests': num_guests,
        'num_bedrooms': num_bedrooms,
        'num_beds': num_beds,
        'num_bathrooms': num_bathrooms,
        'description': description,
        'city': city,
        'country': country,
        'price': price,
        'property_type': property_type,
        'amenities': amenities,
        'image_urls': image_urls,
        'token': bad_token
    }

    # user not logged in
    res = client.post('/api/accommodation', data=post_data)
    msg = eval(res.data.decode('utf-8'))['msg']
    assert res.status_code == 401
    assert msg == 'Must be logged in to create accommodation'

    # login and try again
    res = auth.login()
    msg = eval(res.data.decode('utf-8'))['msg']
    assert msg['user_id']
    assert msg['username']
    real_token = msg['token']
    
    # num_guests < 1
    post_data['token'] = real_token
    post_data['num_guests'] = 0
    res = client.post('/api/accommodation', data=post_data)
    msg = eval(res.data.decode('utf-8'))['msg']
    assert res.status_code == 400
    assert msg == 'number of guests must be at least one'

    # happy path
    post_data['num_guests'] = 1
    res = client.post('/api/accommodation', data=post_data)
    msg = eval(res.data.decode('utf-8'))['msg']
    assert res.status_code == 201
    assert msg['amenities'] == amenities.split(',')
    assert msg['image_urls'] == image_urls.split(',')

def test_update_accommodation(client, auth):
    # 400 if no token
    res = client.put('/api/accommodation/1')
    assert res.status_code == 400

    # 401 if not logged in / invalid token
    invalid_token = 'asdf'
    res = client.put('/api/accommodation/1', data={'token': invalid_token})
    msg = res_to_json(res)['msg']
    assert res.status_code == 401
    assert msg == 'You must be logged in to update accommodation details.'

    res = auth.login()
    token = res_to_token(res)

    # 404 if id doesnt exist
    bad_id = 9999999
    res = client.put('/api/accommodation/' + str(bad_id), data={'token': token})
    msg = res_to_json(res)['msg']
    assert res.status_code == 404
    assert msg == 'Accommodation could not be found'

    # happy path
    update_data = dict(
        token=token,
        num_guests=5,
        num_bedrooms=5,
        num_beds=5,
        num_bathrooms=5,
        price=int(1e5),
        description='this accommodation has been updated',
        city='New City',
        country='New Country',
        property_type='new property type',
        name='new name',
        suburb='new suburb',
        state='new state',
        amenities='New amenity 1, New amenity 2',
        image_urls='New url 1, New url 2'
    )

    res = client.put('/api/accommodation/1', data=update_data)
    msg = res_to_json(res)['msg']
    assert res.status_code == 200

    # retrieve and make sure data has actually been updated
    res = client.get('/api/accommodation/1')
    acc = res_to_json(res)['msg']
    assert acc['num_guests'] == 5
    assert acc['num_bedrooms'] == 5
    assert acc['num_beds'] == 5
    assert acc['num_bathrooms'] == 5
    assert acc['price'] == int(1e5)
    assert acc['description'] == 'this accommodation has been updated'
    assert acc['city'] == 'New City'
    assert acc['country'] == 'New Country'
    assert acc['property_type'] == 'new property type'
    assert acc['name'] == 'new name'
    assert acc['suburb'] == 'new suburb'
    assert acc['state'] == 'new state'
    assert acc['amenities'] == ['new amenity 1', 'new amenity 2']
    assert acc['image_urls'] == ['New url 1', 'New url 2']

def test_delete_accommodation(client, auth):
    # 400 if no token
    res = client.delete('/api/accommodation/1')
    assert res.status_code == 400

    # 401 if not logged in / invalid token
    invalid_token = 'asdf'
    res = client.delete('/api/accommodation/1', data={'token': invalid_token})
    msg = res_to_json(res)['msg']
    assert res.status_code == 401
    assert msg == 'You must be logged in to delete accommodation.'

    res = auth.login()
    token = res_to_token(res)

    # 403 if you try to delete acc you do not own
    bad_id = 3
    res = client.delete('/api/accommodation/' + str(bad_id), data={'token': token})
    msg = res_to_json(res)['msg']
    assert res.status_code == 403
    assert msg == 'This user does not have permission to delete this accommodation.'

    # happy path
    res = client.delete('/api/accommodation/1', data={'token': token})
    msg = res_to_json(res)['msg']
    assert res.status_code == 200

    # future reservations for this accommodation should be cancelled
    res = client.get('/api/reservation', data={'token': token, 'filter': 'future'})
    reservations = res_to_json(res)['msg']
    assert len(reservations) == 0