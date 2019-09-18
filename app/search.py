from flask import Blueprint
from flask_restplus import Resource, reqparse, Namespace

from app import db
from app.models import Accommodation, Reservation
from app.utils import DateType
from sqlalchemy import text

import math
from datetime import datetime

api = Namespace('', description='search for accommodations')

# TODO: only send ~10 results at a time.
# Search is a bit complicated. We want to find all accommodations that meet user criteria
# and that are available in the reservation table. If that was it, it would be fairly simple.
# However, we also want to include accommodations that are not in the reservation table at all,
# as this represents accommodations that have never been booked. I am not sure how to do all of
# this with just one SQL query so I split them up.
@api.route('/api/search', strict_slashes=False)
class Search(Resource):
    # @api.response(200, 'Search successful')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location', required=True, help='location is required')
        parser.add_argument('check_in', required=True, type=DateType)
        parser.add_argument('check_out', required=True, type=DateType)
        parser.add_argument('num_guests', required=True, type=int, help='num_guests is required')
        parser.add_argument('price_low', type=int, default=0)
        parser.add_argument('price_high', type=int, default=math.inf)
        parser.add_argument('num_bedrooms', type=int, default=0)
        parser.add_argument('num_beds', type=int, default=0)
        parser.add_argument('num_bathrooms', type=float, default=0)
        parser.add_argument('amenities', default=[])
        args = parser.parse_args()

        # TODO:
        # validate amenities format. should be 'a,b,c,etc.'
        if args.amenities:
            args.amenities = [a.strip() for a in args.amenities.lower().split(',')]

        # ensure check out is after check in
        if datetime.strptime(args.check_in, '%Y-%m-%d') >= datetime.strptime(args.check_out, '%Y-%m-%d'):
            return {'msg': 'check in date must be before check out date'}, 400
        
        # First, find all accommodations that meet user submitted criteria
        accs = db.session.query(Accommodation.id).filter(
                    ((Accommodation.suburb.ilike(args.location)) | (Accommodation.city.ilike(args.location)) | (Accommodation.state.ilike(args.location))) &
                    (Accommodation.num_guests >= args.num_guests) &
                    (Accommodation.amenities.contains(args.amenities)) &
                    (Accommodation.price >= args.price_low) &
                    (Accommodation.price <= args.price_high) &
                    (Accommodation.num_bedrooms >= args.num_bedrooms) &
                    (Accommodation.num_beds >= args.num_beds) &
                    (Accommodation.num_bathrooms >= args.num_bathrooms) &
                    (Accommodation.is_deleted == False)
                ).all()
        all_acc_ids = [acc.id for acc in accs]

        # Then, find all reservations corresponding to the above accommodations that are NOT available
        reservations = db.session.query(Reservation.accommodation_id).filter(
            Reservation.accommodation_id.in_(all_acc_ids) &
            ((Reservation.check_in_date < args.check_out) & (Reservation.check_out_date > args.check_in)) &
            (Reservation.status != 'checked_out')
        ).all()
        unavailable_acc_ids = [res.accommodation_id for res in reservations]

        # Find accommodations that are left over after removing the unavailable reservations
        available_acc_ids = [acc_id for acc_id in all_acc_ids if acc_id not in unavailable_acc_ids]
        available_accs = db.session.query(Accommodation, db.func.count(Reservation.id).label('total')) \
            .filter((Accommodation.id.in_(available_acc_ids))) \
            .join(Reservation) \
            .group_by(Accommodation.id) \
            .order_by(text('total desc')) \
            .all()

        result = [acc[0].to_dict() for acc in available_accs]
        return {'msg': result}, 200