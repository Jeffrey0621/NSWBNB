from flask_restplus import Resource, reqparse, Namespace
from app import db
from app.models import Accommodation, Reservation,User

from datetime import datetime

#from RecommendSystem import project_recommendation
from RecommendSystem.project_recommendation import predict
from RecommendSystem.knnpredict import knnpredict

api = Namespace('', description='recommendation engine for suggesting accommodations to users')

@api.route('/api/recommendation/<int:id>', strict_slashes=False)
class RetrieverReccomendation(Resource):
    def get(self, id):
        acc = Accommodation.query.filter(
            (Accommodation.id == id) &
            (Accommodation.is_deleted == False)
        ).first()
        if not acc:
            return {'msg': 'Accommodation not found'}, 404

        acc_list = predict(id)
        if len(acc_list)!=4:
        	return {'msg': 'Recommendation failed'}, 404

        result=[]
        for acc_id in acc_list:
            acc = Accommodation.query.filter(Accommodation.id == acc_id).first_or_404()
            acc = acc.to_dict_1()
            result.append(acc)
        
        return {'msg': result}, 200

@api.route('/api/knn_recommendation', strict_slashes=False) 
class RetrieverReccomendationUser(Resource):
    def get(self): #input_user_id
        parser = reqparse.RequestParser()
        parser.add_argument('user_id')
        args = parser.parse_args()
        
        if not args.user_id:
            id = 0
        else:
            user = User.query.filter_by(id =args.user_id).first()
            id = user.id

        acc_list = knnpredict(id)
        if len(acc_list)!=4:
            return {'msg': 'Recommendation failed'}, 404

        result=[]
        for acc_id in acc_list:
            acc = Accommodation.query.filter(Accommodation.id == acc_id).first_or_404()
            acc = acc.to_dict_1()
            result.append(acc)
        
        return {'msg': result}, 200