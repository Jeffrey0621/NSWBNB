'''from flask import jsonify, g
from app import db
from app.auth import basic_auth,token_auth

#token retrieval route that clients will invoke when they need a token
@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.generate_token()
    db.session.commit()
    return jsonify({'token': token})

#clients can send a DELETE request to the /tokens URL to invalidate the token
@app.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
'''

# DO NOT USE FOR NOW.  J said he does not need it for now.
# However,it is always good to provide a route that can help the clients to invoke or revoke a token anytime.
# e.g. Admin needs to revoke a token immediately for security issue
# So keep it for future discussion