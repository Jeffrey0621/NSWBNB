import pytest
from tests import res_to_json, res_to_token
from datetime import datetime, timedelta

def test_get_reservation(client, auth):
    # 400 if filter argument missing
    res = client.get('/api/reservation/?token=adsf')
    assert res.status_code == 400

    # 400 if token missing
    res = client.get('/api/reservation?filter=past')
    assert res.status_code == 400

    # 401 if invalid token
    res = client.get('/api/reservation?filter=past&token=invalid_token')
    assert res.status_code == 401

    res = auth.login()
    token = res_to_json(res)['msg']['token']

    # 400 if filter is not in past, future, all
    res = client.get('/api/reservation?filter=invalid_filter&token=' + token)
    assert res.status_code == 400

    now = datetime.now()
    yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    today = now.strftime('%Y-%m-%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')

    # retrieve reservations in the past. should not retrieve cancelled reservation
    res = client.get('/api/reservation?filter=past&token=' + token)
    msg = res_to_json(res)['msg']
    reservation = msg[0]
    assert len(msg) == 1
    assert reservation['check_in'] == yesterday
    assert reservation['status'] == 'checked_out'

    # retrieve current reservations. should not retrieve cancelled reservation
    res = client.get('/api/reservation?filter=current&token=' + token)
    msg = res_to_json(res)['msg']
    reservation = msg[0]
    assert len(msg) == 1
    assert reservation['check_in'] == today
    assert reservation['status'] == 'checked_in'

    # retrieve reservations in the future
    res = client.get('/api/reservation?filter=future&token=' + token)
    msg = res_to_json(res)['msg']
    reservation = msg[0]
    assert len(msg) == 1
    assert reservation['check_in'] == tomorrow

    # retrieve all reservations. should not retrieve cancelled reservation
    res = client.get('/api/reservation?filter=all&token=' + token)
    msg = res_to_json(res)['msg']
    assert len(msg) == 3
    assert msg[0]['status'] == 'checked_out'
    assert msg[1]['status'] == 'checked_in'
    assert msg[2]['status'] == 'booked'
    assert res.status_code == 200

def test_create_reservation(client, auth):
    # 400 if guest_id missing
    res = client.post('/api/reservation/', data={'accommodation_id': 1, 'num_guests':1, 'check_in': '1111-11-11', 'check_out':'1111-11-12', 'token':'asdf'})
    assert res.status_code == 400

    # 400 if accommodation_id missing
    res = client.post('/api/reservation/', data={'guest_id': 1, 'num_guests':1, 'check_in': '1111-11-12', 'check_out':'1111-11-13', 'token':'asdf'})
    assert res.status_code == 400

    # 400 if num_guests missing
    res = client.post('/api/reservation/', data={'accommodation_id': 1, 'guest_id':1, 'check_in': '1111-11-13', 'check_out':'1111-11-14', 'token':'asdf'})
    assert res.status_code == 400

    # 400 if check_in missing
    res = client.post('/api/reservation/', data={'accommodation_id': 1, 'num_guests':1, 'guest_id': 1, 'check_out':'1111-11-12', 'token':'asdf'})
    assert res.status_code == 400

    # 400 if check_out missing
    res = client.post('/api/reservation/', data={'accommodation_id': 1, 'num_guests':1, 'check_in': '1111-11-11', 'guest_id':1, 'token':'asdf'})
    assert res.status_code == 400

    # 400 if token missing
    res = client.post('/api/reservation/', data={'accommodation_id': 1, 'num_guests':1, 'check_in': '1111-11-14', 'check_out':'1111-11-15', 'guest_id':'asdf'})
    assert res.status_code == 400

    # 401 if invalid token
    invalid_token = 'invalid_token'
    res = client.post('/api/reservation/', data={'guest_id': 1, 'accommodation_id': 1, 'num_guests':1, 'check_in': '1111-11-15', 'check_out':'1111-11-16', 'token':invalid_token})
    assert res.status_code == 401

    # log in
    res = auth.login()
    token = res_to_token(res)

    # 404 if accommodation has been deleted
    deleted_acc_id = 2
    res = client.post('/api/reservation/', data={'accommodation_id': deleted_acc_id, 'check_in': '1111-11-11', 'check_out': '1111-11-11', 'guest_id': 1, 'num_guests':1, 'token':token})
    msg = res_to_json(res)['msg']
    assert res.status_code == 404
    assert msg == 'Reservation could not be made as the accommodation does not exist'

    # 400 if check_out is == check_in
    check_in = '1111-11-11'
    check_out = check_in
    res = client.post('/api/reservation/', data={'check_in': check_in, 'check_out': check_out, 'guest_id': 1, 'accommodation_id': 1, 'num_guests':1, 'token':token})
    assert res.status_code == 400

    # 400 if check_out is < check_in
    check_in = '1111-11-11'
    check_out = '1111-10-10'
    res = client.post('/api/reservation/', data={'check_in': check_in, 'check_out': check_out, 'guest_id': 1, 'accommodation_id': 1, 'num_guests':1, 'token':token})
    assert res.status_code == 400

    # 201 if successful
    check_in = '1111-11-11'
    check_out = '1111-12-12'
    res = client.post('/api/reservation/', data={'check_in': check_in, 'check_out': check_out, 'guest_id': 1, 'accommodation_id': 1, 'num_guests':1, 'token':token})
    assert res.status_code == 201

    # 400 if you try to book dates that are already booked
    check_in = '1111-12-11'
    check_out = '1111-12-12'
    res = client.post('/api/reservation/', data={'check_in': check_in, 'check_out': check_out, 'guest_id': 1, 'accommodation_id': 1, 'num_guests':1, 'token':token})
    assert res.status_code == 400
    assert res_to_json(res)['msg'] == 'Reservation not available for these dates'

def test_reservation_cancellation(client, auth):
    # 400 if required params not passed
    res = client.put('/api/reservation/1', data={})
    assert res.status_code == 400

    # 401 if invalid token
    invalid_token = 'asdf'
    res = client.put('/api/reservation/1', data={'status': 'cancelled', 'token': invalid_token})
    msg = res_to_json(res)['msg']
    assert msg == 'You must be logged in to modify a reservation'
    assert res.status_code == 401

    # log in
    res = auth.login()
    token = res_to_token(res)

    # 404 if res id not found
    bad_reservation_id = '99'
    res = client.put('/api/reservation/' + bad_reservation_id, data={'status': 'cancelled', 'token': token})
    msg = res_to_json(res)['msg']
    assert msg == 'This reservation could not be found'
    assert res.status_code == 404

    # 400 if status is invalid
    res = client.put('/api/reservation/2', data={'status': 'asdf', 'token': token})
    msg = res_to_json(res)['msg']
    assert msg == 'You can only change booking status to \'cancelled\' or \'checked_out\''
    assert res.status_code == 400

    # 200 for successful cancellation
    res = client.put('/api/reservation/2', data={'status': 'cancelled', 'token': token})
    assert res.status_code == 200

    # check that the reservation we just cancelled is not retrieved by get reservation
    res = client.get('/api/reservation?filter=future&token=' + token)
    msg = res_to_json(res)['msg']
    assert len(msg) == 0

def test_reservation_check_out(client, auth):
    # log in as user who is not host of reservation
    res = auth.login('other@other.com', 'other')
    token = res_to_token(res)

    # should 403 since this user is not the host of the reservation
    res = client.put('/api/reservation/2', data={'status': 'checked_out', 'token': token})
    msg = res_to_json(res)['msg']
    assert msg == 'Only host can change reservation status to checked_out'
    assert res.status_code == 403

    # log in as host of reservation
    res = auth.login()
    token = res_to_token(res)

    # should successfully change status to checked_out
    res = client.put('/api/reservation/2', data={'status': 'checked_out', 'token': token})
    msg = res_to_json(res)['msg']
    assert msg == 'Reservation successfully updated to checked_out'
    assert res.status_code == 200

    # retrieve reservation and check that status is now checked_out
    res = client.get('/api/reservation?filter=all&token=' + token)
    reservations = res_to_json(res)['msg']

    for resv in reservations:
        print(resv)
        if resv['reservation_id'] == 2:
            assert resv['status'] == 'checked_out'
