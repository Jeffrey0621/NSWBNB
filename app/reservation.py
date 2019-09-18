from flask_restplus import Resource, reqparse, Namespace

from app import db
from app.models import Accommodation, Reservation, User
from app.utils import DateType

from datetime import datetime

api = Namespace('', description='reservation related functions')

# TODO: need to change reservation status to checked out after user checks out
@api.route('/api/reservation', strict_slashes=False)
class CreateRetrieveReservation(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filter', required=True, help='filter argument required.')
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()

        # TODO: this should use User.check_token instead
        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to retrieve a reservation.'}, 401
        
        today = datetime.now().strftime('%Y-%m-%d')

        # check out date is in the past
        if args.filter == 'past':
            reservations = user.reservations.filter(
                (Reservation.check_out_date <= today) & 
                (Reservation.status != 'cancelled')
            ).all()
        # check in date is in past and check out date is in future
        elif args.filter == 'current':
            reservations = user.reservations.filter(
                (Reservation.check_in_date <= today) &
                (Reservation.check_out_date > today) & 
                (Reservation.status != 'cancelled')
            ).all()
        # check in date is in future
        elif args.filter == 'future':
            reservations = user.reservations.filter(
                (Reservation.check_in_date > today) &
                (Reservation.status != 'cancelled')
            ).all()
        elif args.filter == 'all':
            reservations = user.reservations.filter(Reservation.status != 'cancelled').all()
        else:
            return {'msg': 'filter must be one of {past, current, future, all}'}, 400
        
        data = []
        for res in reservations:
            d = {
                'reservation_id': res.id,
                'check_in': str(res.check_in_date),
                'check_out': str(res.check_out_date),
                'accommodation_id': res.accommodation.id,
                'accommodation_name': res.accommodation.name,
                'suburb': res.accommodation.suburb,
                'price': res.accommodation.price,
                'status': res.status
            }
            data.append(d)
        return {'msg': data}, 200

    @api.response(201, 'Accommodation successfully booked')
    @api.response(400,'Bad request')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('guest_id', type=int, required=True, help='guest_id cannot be blank.')
        parser.add_argument('accommodation_id', type=int, required=True, help='accommodation_id cannot be blank.')
        parser.add_argument('num_guests', type=int, required=True, help='num_guests cannot be blank.')
        parser.add_argument('check_in', required=True, type=DateType)
        parser.add_argument('check_out', required=True, type=DateType)
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()

        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to create a reservation.'}, 401

        acc = Accommodation.query.filter(
            (Accommodation.id == args.accommodation_id) &
            (Accommodation.is_deleted == False)
        ).first()
        
        if not acc:
            return {'msg': 'Reservation could not be made as the accommodation does not exist'}, 404

        # ensure check out is after check in
        if datetime.strptime(args.check_in, '%Y-%m-%d') >= datetime.strptime(args.check_out, '%Y-%m-%d'):
            return {'msg': 'check in date must be before check out date'}, 400

        # use accommodation_id to find all reservations that conflict with given checkin/out dates
        # TODO: need to consider reservation status as well
        reservations = Reservation.query.filter(
            (Reservation.accommodation_id == args.accommodation_id) &
            ((Reservation.check_in_date < args.check_out) & (Reservation.check_out_date > args.check_in))
        ).all()

        if len(reservations):
            return {'msg': 'Reservation not available for these dates'}, 400

        # check that num_guests is <= acc's num_guests
        acc = Accommodation.query.filter_by(id=args.accommodation_id).first()
        if acc.num_guests < args.num_guests:
            return {'msg': 'num_guests is too many for this accommodation'}, 400

        # create new reservation for given guest_id and dates
        new_res = Reservation(
            accommodation_id=args.accommodation_id,
            guest_id=args.guest_id,
            check_in_date=args.check_in,
            check_out_date=args.check_out,
            status='booked'
        )

        db.session.add(new_res)
        db.session.commit()
        return {'msg': new_res.to_dict()}, 201

@api.route('/api/reservation/<int:id>', strict_slashes=False)
class UpdateReservation(Resource):
    # Currently this route only allows cancelling a reservation. But it could be extended to
    # support extending reservations and other things.
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True)
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()
        token = args.token
        status = args.status

        user = User.check_token(token)
        if not user:
            return {'msg': 'You must be logged in to modify a reservation'}, 401

        res = Reservation.query.filter_by(id=id).first()
        if not res:
            return {'msg': 'This reservation could not be found'}, 404

        if status == 'cancelled':
            if res.guest_id != user.id:
                return {'msg': 'This user does not have permission to modify this reservation.'}, 403
            msg = 'Booking has been cancelled'
        elif status == 'checked_out':
            if user.id != res.accommodation.host_id:
                return {'msg': 'Only host can change reservation status to checked_out'}, 403
            msg = 'Reservation successfully updated to checked_out'
        else:
            return {'msg': 'You can only change booking status to \'cancelled\' or \'checked_out\''}, 400

        res.status = status
        db.session.commit()
        return {'msg': msg}, 200
