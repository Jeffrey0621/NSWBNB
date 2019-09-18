'''from flask_restplus import Resource, reqparse, Namespace
from app import db
from app.models import User,Accommodation,Favourite


api = Namespace('', description='favourite accommodations management')

@api.route('/api/user/favourite', strict_slashes=False)
class ManageFavourite(Resource):
	@api.response(201, 'favourites successfully added')
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('accommodation_id', required=True)
        args = parser.parse_args()
        
        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to update your favourites'}, 401

        acc = Accommodation.query.filter(id = args.accommodation_id).first_or_404()
        if acc.is_deleted :
        	return {'msg': 'accommodation deleted'}, 400

        new_favourite = Favourite(
            user_id = user.id,
            accommodation_id = args.accommodation_id,
            is_valid = True
        )

        db.session.add(new_favourite)
        db.session.commit()

        return {'msg': 'favourites successfully added'}, 201

    
    def get(self):
    	parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()
        
        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to retrieve your favourites'}, 401
        f_list = user.favourites.all_or_404()
        result = []
        for f in f_list:
            acc = Accommodation.query.filter(id = f.accommodation_id).first_or_404()
            r = acc.to_dict_1()
            r['favourite_id'] = f.id
            r['is_valid'] = f.is_valid
            result.append(r)

        return {'msg': result}, 200
        
        	

    
    @api.response(200, 'favourites successfully deleted')
    def delete(self):
    	parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('favourite_id', required=True)
        args = parser.parse_args()
        
        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to delete your favourites'}, 401
        f = Favourite.query.filter_by(id=favourite_id).first_or_404()
        session.delete(f)
		session.commit()
		return {'msg': 'favourites successfully deleted'}, 200

'''


