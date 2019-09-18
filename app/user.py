from flask_restplus import Resource, reqparse, Namespace
from app import db
from app.models import User,Reservation,Accommodation


api = Namespace('', description='user management functions')

@api.route('/api/user', strict_slashes=False)
class ManageUser(Resource):
    #--------------user info retrieved---------------------------
    @api.response(200, 'User info retrieved')
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()

        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to retrieve user details'}, 401

        return {'msg': user.to_dict()}, 200
    #--------------user registeration ---------------------------
    @api.response(201, 'User created')
    @api.response(400,'Bad request')
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', required=True, help='Username cannot be blank.')
        parser.add_argument('email', required=True, help='Email cannot be blank.')
        parser.add_argument('password', required=True, help='Password cannot be blank.')
        parser.add_argument('gender')
        parser.add_argument('phone')
        args = parser.parse_args()

        username = args.username
        email = args.email
        gender = args.gender
        phone = args.phone

        # handle duplicate email/username
        if User.query.filter_by(username=username).first():
            return {'msg': 'username already in use.'}, 400

        if User.query.filter_by(email=email).first():
            return {'msg': 'email address already in use.'}, 400

        new_user = User(
            username=username,
            email=email
        )

        if gender:
            new_user.gender = gender

        if phone:
            new_user.phone = phone

        # hashes input password, and sets password_hash field
        new_user.set_password(args.password)
        db.session.add(new_user)
        db.session.commit()

        return {'msg': 'user successfully created'}, 201
    #--------------user setting ---------------------------
    @api.response(200, 'User info updated')
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('email', required=False)
        parser.add_argument('phone', required=False)
        parser.add_argument('gender', required=False)
        args = parser.parse_args()
        
        user = User.check_token(args.token)
        if not user:
            return {'msg': 'You must be logged in to update user information'}, 401

        email = args['email']
        phone = args['phone']
        gender = args['gender']

        is_phone_dup = False
        # phone number must be unique
        if phone:
            if User.query.filter_by(phone=phone).first():
                is_phone_dup = True
            else:
                user.phone = phone
        if gender:
            user.gender = gender
        if email:
            user.email = email

        db.session.commit()

        return {'msg': user.to_dict(), 'is_phone_dup': is_phone_dup}, 200


@api.route('/api/user/password') #password change 
class ChangePassword(Resource):
    @api.response(200, 'User password updated')
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('old_password', required=True)
        parser.add_argument('new_password', required=True)
        args = parser.parse_args()

        user = User.check_token(args.token)
        if not user:
            return {'msg': 'Must be logged in to change password'}, 401

        if not user.check_password(args.old_password):
            return {'msg': 'Wrong old password'}, 400

        user.set_password(args.new_password)        
        db.session.commit()

        return {'msg':'User password updated'}, 200


@api.route('/api/user/accommodations') #get all the accommodations belongs to the user in a list
class RetrieveUserAccommodation(Resource):
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    @api.response(200,'User accommodations retrieved')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        args = parser.parse_args()

        host = User.check_token(args.token)
        if not host:
            return {'msg': 'You must be logged in to retrieve your accommodations'}, 401

        accommodations = host.listings.filter(Accommodation.is_deleted == False).all()
        accommodations_list = []
        for acc in accommodations:
            acc = acc.to_dict()
            accommodations_list.append(acc)
        return {'msg': accommodations_list}, 200

    
#get the reservations that a host recieved in a list
#filter:'In_Process','Checked_Out','Cancelled'
@api.route('/api/user/reservations') 
class RetrieveUserReservation(Resource):
    @api.response(400,'Bad request')
    @api.response(401,'Unauthorized')
    @api.response(200,'User reservations retrieved')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, help='Token required.')
        parser.add_argument('filter', required=True, help='filter argument required.')
        args = parser.parse_args()

        host = User.check_token(args.token)
        if not host:
            return {'msg': 'Must be logged in to retrieve your reservations'}, 401
         
        accommodations = host.listings.all()

        if not accommodations:
            return {'msg':'no accommodation belongs to you'},400

        in_process = []
        checked_out = []
        cancelled = []

        for acc in accommodations:
            revs = Reservation.query.filter_by(accommodation_id = acc.id).all()
            if not revs:
                continue
            for rev in revs:
                if rev.status == 'booked' or rev.status == 'checked_in':
                    rev1=rev.to_dict()
                    rev1['accommodation_name']=acc.name
                    rev1['suburb']=acc.suburb
                    guest = User.query.filter_by(id = rev.guest_id).first()
                    if not guest:
                        rev1['guest_name']='user does not exsit anymore'
                        rev1['guest_contact']='user does not exsit anymore'
                    rev1['guest_name']= guest.username
                    rev1['guest_contact']=guest.email
                    in_process.append(rev1)
                elif rev.status == 'checked_out':
                    rev1=rev.to_dict()
                    rev1['accommodation_name']=acc.name
                    rev1['suburb']=acc.suburb
                    guest = User.query.filter_by(id = rev.guest_id).first()
                    if not guest:
                        rev1['guest_name']='user does not exsit anymore'
                        rev1['guest_contact']='user does not exsit anymore'
                    rev1['guest_name']= guest.username
                    rev1['guest_contact']=guest.email
                    checked_out.append(rev1)
                elif rev.status == 'cancelled':
                    rev1=rev.to_dict()
                    rev1['accommodation_name']=acc.name
                    rev1['suburb']=acc.suburb
                    guest = User.query.filter_by(id = rev.guest_id).first()
                    if not guest:
                        rev1['guest_name']='user does not exsit anymore'
                        rev1['guest_contact']='user does not exsit anymore'
                    rev1['guest_name']= guest.username
                    rev1['guest_contact']=guest.email
                    cancelled.append(rev1)

        result=[]
        if args.filter == 'In_Process':
            result = in_process
        elif args.filter == 'Checked_Out':
            result = checked_out
        elif args.filter == 'Cancelled':
            result = cancelled
        else:
            return {'msg':'filter should be one of In_Process,Checked_Out,Cancelled'},400

        if len(result) == 0:
            return {'msg':'No reservation found'},200
        result.reverse()
        return {'msg':result},200