from flask_restplus import Resource, reqparse, Namespace
from app import db
from app.models import Accommodation, Reservation, User
from datetime import datetime, timedelta

api = Namespace('', description='accommodation related functions')

# return value is list that includes day1, excludes day2
def get_dates_between(day1, day2):
    dates_between = []
    curr_day = day1
    while curr_day != day2:
        dates_between.append(str(curr_day))
        curr_day = curr_day + timedelta(days=1)
    return dates_between

def get_unavailable_dates(reservations):
    unavailable_dates = []
    for resv in reservations:
        dates = get_dates_between(resv.check_in_date, resv.check_out_date)
        unavailable_dates.extend(dates)
    return unavailable_dates

# TODO: add error handling
@api.route('/api/accommodation/<int:id>', strict_slashes=False)
class RetrieveAccommodation(Resource):
    def get(self, id):
        acc = Accommodation.query.filter(
            (Accommodation.id == id) &
            (Accommodation.is_deleted == False)
        ).first()
        if not acc:
            return {'msg': 'Accommodation not found'}, 404
        result = acc.to_dict()

        # find all resv for acc where checkin date is >= today or checkout date is > today
        today = datetime.now().strftime('%Y-%m-%d')
        reservations = Reservation.query.filter(
            (Reservation.accommodation_id == id) &
            ((Reservation.check_in_date >= today) | (Reservation.check_out_date > today))
        ).order_by(Reservation.check_in_date.asc()).all()

        result['unavailable_dates'] = get_unavailable_dates(reservations)
        return {'msg': result}, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('num_guests', type=int)
        parser.add_argument('num_bedrooms', type=int)
        parser.add_argument('num_beds', type=int)
        parser.add_argument('num_bathrooms', type=int)
        parser.add_argument('price', type=int)
        parser.add_argument('description')
        parser.add_argument('city')
        parser.add_argument('country')
        parser.add_argument('property_type')
        parser.add_argument('name')
        parser.add_argument('suburb')
        parser.add_argument('state')
        parser.add_argument('amenities')
        parser.add_argument('image_urls')
        args = parser.parse_args()
        
        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to update accommodation details.'}, 401

        acc = Accommodation.query.filter(
            (Accommodation.id == id) &
            (Accommodation.is_deleted == False)
        ).first()

        if not acc:
            return {'msg': 'Accommodation could not be found'}, 404

        if args.amenities:
            args.amenities = [a.strip() for a in args.amenities.lower().split(',')]

        if args.image_urls:
            args.image_urls = [url.strip() for url in args.image_urls.split(',')]

        update_data = {}
        for arg in args:
            if arg != 'token' and args[arg]:
                update_data[arg] = args[arg]

        # only run update if there are things to update as update() results in an error if dict is empty
        if update_data:
            acc.update_with_dict(update_data)
            db.session.commit()

            return {'msg': 'Accommodation successfully updated'}, 200
        
        return {'msg': 'There was nothing to update'}, 200


    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()

        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to delete accommodation.'}, 401

        # check that user owns accommodation
        acc = user.listings.filter_by(id=id).first()
        if not acc:
            return {'msg': 'This user does not have permission to delete this accommodation.'}, 403

        acc.is_deleted = True

        # should also cancel future reservations for this accommodation
        acc.reservations.filter_by(status='booked').update(dict(status='cancelled'))
        #should set is_valid in Favourite to False for records related to this accommodation
        #acc.favourites.filter_by(accommodation_id = id).update(dict(is_valid= False))
        
        db.session.commit()

        return {'msg': 'Accommodation successfully deleted'}, 200


@api.route('/api/accommodation', strict_slashes=False) #create accommodation
class CreateAccommodation(Resource):
    @api.response(201, 'Accommodation created')
    @api.response(400,'Invalid input')
    @api.response(401,'Unauthorized')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('num_guests', required=True, type=int)
        parser.add_argument('num_bedrooms', required=True, type=int)
        parser.add_argument('num_beds', required=True, type=int)
        parser.add_argument('num_bathrooms', required=True, type=int)
        parser.add_argument('description', required=True)
        parser.add_argument('city', required=True)
        parser.add_argument('country', required=True)
        parser.add_argument('price', required=True, type=int)
        parser.add_argument('property_type', required=True)
        parser.add_argument('name', default=None)
        parser.add_argument('suburb', default=None)
        parser.add_argument('state', default=None)
        parser.add_argument('amenities', default=[])
        parser.add_argument('image_urls', default=[])
        args = parser.parse_args()
        token = args['token']

        # TODO: this should use User.check_token instead
        user = User.query.filter_by(token=token).first()
        if not user:
            return {'msg': 'Must be logged in to create accommodation'}, 401

        if not user.check_token(token):
            return {'msg':'Token expired'}, 401

        if args.amenities:
            args.amenities = [a.strip() for a in args.amenities.lower().split(',')]

        if args.image_urls:
            args.image_urls = [url.strip() for url in args.image_urls.split(',')]

        if args.num_guests < 1:
            return {'msg': 'number of guests must be at least one'}, 400

        new_accommodation = Accommodation(
            host_id=user.id,
            num_guests=args.num_guests,
            num_bedrooms=args.num_bedrooms,
            num_beds=args.num_beds,
            num_bathrooms=args.num_bathrooms,
            description=args.description,
            city=args.city,
            country=args.country,
            price=args.price,
            property_type=args.property_type,
            name=args.name,
            suburb=args.suburb,
            state=args.state,
            amenities=args.amenities,
            image_urls=args.image_urls,
            num_reviews=0,
            rating=0.0,
            scores_accuracy=0,
            scores_location=0,
            scores_communication=0,
            scores_check_in=0,
            scores_cleanliness=0,
            scores_value=0,
            is_deleted=False
        )

        db.session.add(new_accommodation)
        db.session.commit()

        return {'msg': new_accommodation.to_dict()}, 201