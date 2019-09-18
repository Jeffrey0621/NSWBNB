import pytest
from tests import res_to_json, res_to_token

def test_get_user(client, auth):
    # 400 if no token
    res = client.get('/api/user/')
    assert res.status_code == 400

    # 401 if invalid token
    invalid_token = 'asdf'
    res = client.get('/api/user?token=' + invalid_token)
    msg = res_to_json(res)['msg']
    assert res.status_code == 401
    assert msg == 'You must be logged in to retrieve user details'

    # happy path
    res = auth.login()
    token = res_to_token(res)
    res = client.get('/api/user?token=' + token)
    user = res_to_json(res)['msg']
    assert res.status_code == 200
    assert user['id'] == 1
    assert user['username'] == 'test'
    assert user['email'] == 'test@test.com'
    assert user['gender'] == 'male'
    assert user['phone'] == '123123123'

def test_create_user(client, auth):
    # 400 if no username
    res = client.post('/api/user/', data={'email': 'test@test.com', 'password': 'test'})
    assert res.status_code == 400

    # 400 if no email
    res = client.post('/api/user/', data={'username': 'test', 'password': 'test'})
    assert res.status_code == 400

    # 400 if no password
    res = client.post('/api/user/', data={'username': 'test', 'email': 'test@test.com'})
    assert res.status_code == 400

    # 400 if duplicate username
    dup_username = 'test'
    res = client.post('/api/user/', data={'username': dup_username, 'email': 'test@test.com', 'password': 'test'})
    msg = res_to_json(res)['msg']
    assert res.status_code == 400
    assert msg == 'username already in use.'

    # 400 if duplicate email
    dup_email = 'test@test.com'
    res = client.post('/api/user/', data={'email': dup_email, 'username': 'not_test', 'password': 'test'})
    msg = res_to_json(res)['msg']
    assert res.status_code == 400
    assert msg == 'email address already in use.'

    # happy path w/o gender + phone
    data = {
        'email': 'valid@email.com',
        'username': 'blahblahblah',
        'password': 'asdf'
    }

    res = client.post('/api/user/', data=data)
    msg = res_to_json(res)['msg']
    assert res.status_code == 201

    # log in with new user
    res = auth.login(data['email'], data['password'])
    token = res_to_token(res)

    # retrieve user and check details
    res = client.get('/api/user?token=' + token)
    user = res_to_json(res)['msg']
    assert user['username'] == data['username']
    assert user['email'] == data['email']
    assert 'gender' not in user
    assert 'phone' not in user

    # happy path w/ gender + phone
    data = {
        'email': 'another@email.com',
        'username': 'new_username',
        'password': 'asdf',
        'gender': 'male',
        'phone': '11111111111'
    }

    res = client.post('/api/user/', data=data)
    msg = res_to_json(res)['msg']
    assert res.status_code == 201

    # log in with new user
    res = auth.login(data['email'], data['password'])
    token = res_to_token(res)

    # retrieve user and check details
    res = client.get('/api/user?token=' + token)
    user = res_to_json(res)['msg']
    assert user['username'] == data['username']
    assert user['email'] == data['email']
    assert user['gender'] == data['gender']
    assert user['phone'] == data['phone']

def test_update_user(client, auth):
    # 400 if no token
    res = client.put('/api/user/')
    assert res.status_code == 400

    # 401 if invalid token
    invalid_token = 'asdf'
    res = client.put('/api/user/', data={'token': invalid_token})
    assert res.status_code == 401

    res = auth.login()
    token = res_to_token(res)

    # update with non-dup phone
    data = {
        'email': 'new@email.com',
        'gender': 'female',
        'phone': '222-222-222',
        'token': token
    }

    res = client.put('/api/user/', data=data)
    res_json = res_to_json(res)
    updated_user = res_json['msg']
    is_phone_dup = res_json['is_phone_dup']
    assert res.status_code == 200
    assert updated_user['email'] == data['email']
    assert updated_user['gender'] == data['gender']
    assert updated_user['phone'] == data['phone']
    assert is_phone_dup == False

    # update with dup phone
    new_data = {
        'phone': '222-222-222',
        'token': token
    }

    res = client.put('/api/user/', data=new_data)
    res_json = res_to_json(res)
    updated_user = res_json['msg']
    is_phone_dup = res_json['is_phone_dup']
    assert res.status_code == 200

    # all data should remain unchanged since phone was a dup, and other properties were not updated
    assert updated_user['phone'] == data['phone']
    assert updated_user['email'] == data['email']
    assert updated_user['gender'] == data['gender']
    assert is_phone_dup == True

def test_update_password(client, auth):
    # 400 if token/new_password/old_password is missing
    res = client.put('/api/user/password', data={'token': 'asdf', 'new_password': 'asdf'})
    assert res.status_code == 400

    res = client.put('/api/user/password', data={'old_password': 'qwer', 'new_password': 'asdf'})
    assert res.status_code == 400

    res = client.put('/api/user/password', data={'old_password': 'qwer', 'token': 'asdf'})
    assert res.status_code == 400

    # 401 if not logged in
    invalid_token = 'asdf'
    res = client.put('/api/user/password', data={'token': invalid_token, 'old_password': 'qwer', 'new_password': 'zxcv'})
    assert res.status_code == 401

    res = auth.login()
    token = res_to_token(res)

    # 400 if old password is incorrect
    res = client.put('/api/user/password', data={'token': token, 'old_password': 'qwer', 'new_password': 'zxcv'})
    msg = res_to_json(res)['msg']
    assert res.status_code == 400
    assert msg == 'Wrong old password'

    # check that password is updated properly
    correct_old_pass = 'test'
    new_pass = 'newpass'
    res = client.put('/api/user/password', data={'token': token, 'old_password': 'test', 'new_password': new_pass})
    msg = res_to_json(res)['msg']
    assert res.status_code == 200

    # try logging in with new password to confirm update was successful
    res = auth.login('test@test.com', new_pass)
    assert res.status_code == 200

    # login with old pass should fail
    res = auth.login('test@test.com', correct_old_pass)
    assert res.status_code == 401

def test_retrieve_user_accommodations(client, auth):
    # 400 if no token
    res = client.get('/api/user/accommodations')
    assert res.status_code == 400

    # 401 if not logged in
    res = client.get('/api/user/accommodations', data={'token': 'invalid_token'})
    msg = res_to_json(res)['msg']
    assert res.status_code == 401
    assert msg == 'You must be logged in to retrieve your accommodations'

    res = auth.login()
    token = res_to_token(res)

    # happy path, should not return deleted accommodations
    res = client.get('/api/user/accommodations', data={'token': token})
    accs = res_to_json(res)['msg']
    assert res.status_code == 200
    assert len(accs) == 1 # if deleted acc was returned, there would be 2 accs

