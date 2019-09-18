import pytest
import math
from tests import res_to_json
from datetime import datetime, timedelta

# valid values for required args to search
query_params = dict(
    location='Sydney',
    check_in='3019-11-11',
    check_out='3019-11-12',
    num_guests=1
)

# take base dict and returns a new dict with updated properties
def copy_update_params(new_props):
    new_dict = query_params.copy()
    for k, v in new_props.items():
        new_dict[k] = v
    return new_dict

def test_check_out_before_check_in(client):
    # 400 if check_out <= check_in
    params = copy_update_params(dict(check_out='3019-11-11'))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert res.status_code == 400
    assert msg == 'check in date must be before check out date'

    params = copy_update_params(dict(check_out='3019-11-10'))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert res.status_code == 400
    assert msg == 'check in date must be before check out date'

    params = copy_update_params(dict(check_out='3019-11-12'))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert res.status_code == 200
    assert len(msg) == 1

def test_location_filter(client):
    # Test location not found
    params = copy_update_params(dict(location='Canada'))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # Test valid location 
    res = client.get('/api/search', data=query_params)
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

    # should work case insensitively
    params = copy_update_params(dict(location='sYdNeY'))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_num_guests_filter(client):
    # # Test num_guests filter
    params = copy_update_params(dict(num_guests=10))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    res = client.get('/api/search', data=query_params)
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_amenities_filter(client):
    # fake amenity should not return results
    res = client.get('/api/search', data=copy_update_params(dict(amenities=['Fake amenity'])))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # real amenity should work case insensitively
    res = client.get('/api/search', data=copy_update_params(dict(amenities=['KanGaRoo-fRiEndLy', 'tV'])))
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_price_low_filter(client):
    # min price too high
    res = client.get('/api/search', data=copy_update_params(dict(price_low=1000000000000)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # min price OK
    res = client.get('/api/search', data=copy_update_params(dict(price_low=0)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_price_high_filter(client):
    # max price too low
    res = client.get('/api/search', data=copy_update_params(dict(price_high=0)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # max price OK
    res = client.get('/api/search', data=copy_update_params(dict(price_high=100000000000)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_num_bedrooms_filter(client):
    # num_bedrooms too high
    res = client.get('/api/search', data=copy_update_params(dict(num_bedrooms=100)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # num_bedrooms OK
    res = client.get('/api/search', data=copy_update_params(dict(num_bedrooms=1)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_num_beds_filter(client):
    # num beds too high
    res = client.get('/api/search', data=copy_update_params(dict(num_beds=100)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # num beds OK
    res = client.get('/api/search', data=copy_update_params(dict(num_beds=1)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_num_bathrooms_filter(client):
    # num bathrooms too high
    res = client.get('/api/search', data=copy_update_params(dict(num_bathrooms=100)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

    # num bathrooms OK
    res = client.get('/api/search', data=copy_update_params(dict(num_bathrooms=1)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_pass_all_filters(client):
    params = copy_update_params(dict(
        amenities=['wifi', 'tv'],
        num_bedrooms=1,
        num_beds=1,
        num_bathrooms=1,
        price_low=0,
        price_high=100000000
    ))
    res = client.get('/api/search', data=params)
    msg = res_to_json(res)['msg']
    assert len(msg) == 1

def test_dont_return_booked_accommodations(client):
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow_tomorrow = (now + timedelta(days=2)).strftime('%Y-%m-%d')
    res = client.get('/api/search', data=copy_update_params(dict(check_in=tomorrow, check_out=tomorrow_tomorrow)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

def test_dont_return_deleted_accommodations(client):
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    res = client.get('/api/search', data=copy_update_params(dict(check_in=today, check_out=tomorrow)))
    msg = res_to_json(res)['msg']
    assert len(msg) == 0
    