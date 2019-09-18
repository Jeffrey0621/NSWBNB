from flask_restplus import Resource, reqparse, Namespace

from app import db
from app.models import User

api = Namespace('', description='auth functions')

@api.route('/api/login', strict_slashes=False)
class UserLogin(Resource):
    @api.response(200, 'User logged in')
    @api.response(400,'Bad request')
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email', required=True, help='Please enter your email.')
        parser.add_argument('password', required=True, help='Please enter your password.')
        args = parser.parse_args()

        email, password = args['email'], args['password']

        if not (email and password):
            return {'errors': 'Please enter your email and password'}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {'errors': 'Invalid email or unmatched password'}, 401

        token = user.generate_token(expiration=3600)
        db.session.commit()
        data = {
            'user_id': user.id,
            'username':user.username,
            'token': token
        }

        return {'msg': data}, 200
        
@api.route('/api/logout', strict_slashes=False)
class UserLogout(Resource):
    @api.response(200, 'User logged out')
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()
        token = args['token']

        user = User.query.filter_by(token=token).first()
        if not user:
            return {'errors': 'Invalid token'}, 401

        if user.check_token(token) is None:
            return {'errors': 'Invalid token'}, 401

        user.revoke_token()
        db.session.commit()
        return {'msg':'logged out successfully'}, 200