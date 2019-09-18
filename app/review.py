from flask_restplus import Resource, reqparse, Namespace
from app import db
from app.models import User,Review,Reservation,Accommodation
from textblob import TextBlob

api = Namespace('', description='review related functions')

@api.route('/api/reviews', strict_slashes=False) #leave a review,cannot edit once submit

class WriteReview(Resource):
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    @api.response(403,'Forbidden')
    @api.response(200,'successfully reviewed')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('reservation_id', required=True, help='reservation_id required.')
        parser.add_argument('scores_accuracy', required=True, help='scores_accuracy required.')
        parser.add_argument('scores_location', required=True, help='scores_location required.')
        parser.add_argument('scores_communication', required=True, help='scores_communication required.')
        parser.add_argument('scores_check_in', required=True, help='scores_check_in required.')
        parser.add_argument('scores_cleanliness', required=True, help='scores_cleanliness required.')
        parser.add_argument('scores_value', required=True, help='scores_value required.')
        parser.add_argument('is_anonymous')
        parser.add_argument('review')

        args = parser.parse_args()
        token = args['token']

        user = User.query.filter_by(token=token).first()
        if not user:
            return {'msg': 'Invalid user'}, 400

        if user.check_token(token) is None:
            return {'msg':'Token invalid'},401

        reservation_id = args.reservation_id

        if Review.query.filter_by(reservation_id=reservation_id).first():
            return {'msg': 'You can only write one review for a reservation'}, 400

        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if not reservation:
            return {'msg': 'reservation does not exist'}, 400

        accommodation = Accommodation.query.filter_by(id=reservation.accommodation_id).first()
        if not accommodation:
            return {'msg': 'accommodation does not exist'}, 400

        if reservation.guest_id!=user.id:
            return {'msg': 'Does not have access rights to review,user have never booked this accommodation before'}, 403
        
        status = reservation.status
        if status != 'checked_out':
            return {'msg': 'Only checked_out user can leave a review'}, 403

        is_anonymous = args.is_anonymous
        if is_anonymous is None:
            is_anonymous = False

        review = args.review
        if review is None:
            review =''

        scores_accuracy = int(args.scores_accuracy)
        scores_location=int(args.scores_location)
        scores_communication=int(args.scores_communication)
        scores_check_in=int(args.scores_check_in)
        scores_cleanliness=int(args.scores_cleanliness)
        scores_value=int(args.scores_value)
        rating = (scores_accuracy + scores_location +scores_communication+scores_check_in+scores_cleanliness+scores_value)/6
        rating = int(rating)

        new_review = Review(
            guest_id= user.id,
            reservation_id=reservation_id,
            scores_accuracy=scores_accuracy,
            scores_location=scores_location,
            scores_communication=scores_communication,
            scores_check_in=scores_check_in,
            scores_cleanliness=scores_cleanliness,
            scores_value=scores_value,
            is_anonymous=is_anonymous,
            review=review,
            rating=rating    
        )

        db.session.add(new_review)
        if not accommodation.num_reviews:
            accommodation.num_reviews=0
            
        num_of_reviews=int(accommodation.num_reviews)

        if not accommodation.rating:
            accommodation.rating=0
        if not accommodation.scores_accuracy:
            accommodation.scores_accuracy = 0
        if not accommodation.scores_location:
            accommodation.scores_location = 0
        if not accommodation.scores_communication:
            accommodation.scores_communication = 0
        if not accommodation.scores_cleanliness:
            accommodation.scores_cleanliness = 0
        if not accommodation.scores_value:
            accommodation.scores_value = 0
        if not accommodation.scores_check_in:
            accommodation.scores_check_in = 0 

        accommodation.scores_accuracy = int((accommodation.scores_accuracy * num_of_reviews + scores_accuracy)/(num_of_reviews+1))
        accommodation.scores_location = int((accommodation.scores_location * num_of_reviews + scores_location)/(num_of_reviews+1))
        accommodation.scores_communication = int((accommodation.scores_communication * num_of_reviews + scores_communication)/(num_of_reviews+1))
        accommodation.scores_check_in = int((accommodation.scores_check_in * num_of_reviews + scores_check_in)/(num_of_reviews+1))
        accommodation.scores_cleanliness = int((accommodation.scores_cleanliness * num_of_reviews + scores_cleanliness)/(num_of_reviews+1))
        accommodation.scores_value = int((accommodation.scores_value * num_of_reviews + scores_value)/(num_of_reviews+1))
        accommodation.rating = (accommodation.rating * num_of_reviews + rating)/(num_of_reviews+1)
        num_of_reviews+=1
        accommodation.num_reviews = num_of_reviews
        db.session.commit()

        return {'msg': 'review successfully created'}, 200


#Get all the reviews of one accommodation
@api.route('/api/reviews/<int:id>', strict_slashes='False') #id is the accommodation_id
class GetAllReview(Resource):
    @api.response(200,'successfully retrieved')
    def get(self,id):
        acc = Accommodation.query.get_or_404(id)
        revs = Reservation.query.filter_by(accommodation_id=id).all()
        result = []
        if not revs:
            return {'msg':result},200
        for rev in revs:
            r = Review.query.filter_by(reservation_id=rev.id).first()
            if not r:
                continue
            if r.is_anonymous is True:
                name = "anonymous_user"
            else:
                u = User.query.filter_by(id=r.guest_id).first()
                if not u:
                    name = "former_user"
                name = u.username
            data = {
            'guest_name':name,
            'rating':r.rating,
            'review':r.review
            }

            result.append(data)
        result.reverse()
        return {'msg':result},200

#Get all the good reviews of one accommodation
@api.route('/api/reviews/<int:id>/good', strict_slashes='False') #id is the accommodation_id
class GetGoodReview(Resource):
    @api.response(200,'successfully retrieved')
    def get(self,id):
        acc = Accommodation.query.get_or_404(id)
        revs = Reservation.query.filter_by(accommodation_id=id).all()
        result = []
        if not revs:
            return {'msg':result},200
        for rev in revs:
            r = Review.query.filter_by(reservation_id=rev.id).first()
            if not r:
                continue
            seti_review = TextBlob(r.review)
            if  seti_review.sentiment.polarity < 0 or r.rating < 6:
                continue
            if r.is_anonymous is True:
                name = "anonymous_user"
            else:
                u = User.query.filter_by(id=r.guest_id).first()
                if not u:
                    name = "former_user"
                name = u.username
            data = {
            'guest_name':name,
            'rating':r.rating,
            'review':r.review
            }

            result.append(data)
        result.reverse()
        return {'msg':result},200

#Get all the bad reviews of one accommodation
@api.route('/api/reviews/<int:id>/bad', strict_slashes='False') #id is the accommodation_id
class GetBadReview(Resource):
    @api.response(200,'successfully retrieved')
    def get(self,id):
        acc = Accommodation.query.get_or_404(id)
        revs = Reservation.query.filter_by(accommodation_id=id).all()
        result = []
        if not revs:
            return {'msg':result},200
        for rev in revs:
            r = Review.query.filter_by(reservation_id=rev.id).first()
            if not r:
                continue
            seti_review = TextBlob(r.review)
            if  seti_review.sentiment.polarity>=0 or r.rating >= 6:
                continue
            if r.is_anonymous is True:
                name = "anonymous_user"
            else:
                u = User.query.filter_by(id=r.guest_id).first()
                if not u:
                    name = "former_user"
                name = u.username
            data = {
            'guest_name':name,
            'rating':r.rating,
            'review':r.review
            }

            result.append(data)
        result.reverse()
        return {'msg':result},200


