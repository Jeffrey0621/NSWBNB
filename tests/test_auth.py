import pytest

def test_login(client):
    incorrect_email = 'wrong@wrong.com'
    correct_email = 'test@test.com'
    incorrect_pass = 'asdf'
    correct_pass = 'test'
    
    # 400 if no email/password
    res = client.post('/api/login/')
    assert res.status_code == 400

    res = client.post('/api/login/', data={'email': correct_email})
    assert res.status_code == 400

    res = client.post('/api/login/', data={'password': correct_pass})
    assert res.status_code == 400

    # 401 if email or password incorrect
    res = client.post('/api/login/', data={'email': incorrect_email, 'password': correct_pass})
    assert res.status_code == 401

    res = client.post('/api/login/', data={'email': correct_email, 'password': incorrect_pass})
    assert res.status_code == 401

    res = client.post('/api/login/', data={'email': correct_email, 'password': correct_pass})
    msg = eval(res.data.decode('utf-8'))['msg']
    assert res.status_code == 200
    assert msg['user_id'] == 1
    assert msg['username'] == 'test'
    assert msg['token']

def test_logout(client, auth):
    # 400 if no token
    res = client.post('/api/logout/')
    assert res.status_code == 400

    # 401 if fake token
    fake_token = 'fake_token'
    res = client.post('/api/logout/', data={'token': fake_token})
    assert res.status_code == 401

    # log in and try again
    res = auth.login()
    msg = eval(res.data.decode('utf-8'))['msg']
    token = msg['token']
    res = client.post('/api/logout', data={'token': token})
    assert res.status_code == 200

    # check that token has been revoked
    res = client.post('/api/logout', data={'token': token})
    assert res.status_code == 401