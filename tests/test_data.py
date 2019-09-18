from app import db
from app.models import Accommodation, Reservation, User
from datetime import datetime, timedelta

def insert_data(app):
    with app.app_context():
        # insert test user
        new_user = User(
            id=1,
            username='test',
            email='test@test.com',
            gender='male',
            phone='123123123'
        )
        new_user.set_password('test')

        other_user = User(
            id=2,
            username='other',
            email='other@other.com',
            gender='female',
            phone='234234234'
        )
        other_user.set_password('other')

        # insert test accommodation
        new_acc = Accommodation(
            id=1,
            host_id=new_user.id,
            num_guests=2,
            num_bedrooms=2,
            num_beds=2,
            num_bathrooms=2,
            description='Such a good house',
            city='Sydney',
            country='Australia',
            price=99999,
            property_type='Space ship',
            num_reviews=999,
            amenities=['wifi', 'tv', 'kangaroo-friendly'],
            is_deleted=False
        )

        # insert deleted test accommodation
        deleted_acc = Accommodation(
            id=2,
            host_id=new_user.id,
            num_guests=2,
            num_bedrooms=2,
            num_beds=2,
            num_bathrooms=2,
            description='This house is deleted',
            city='Sydney',
            country='Australia',
            price=99999,
            property_type='Space ship',
            num_reviews=999,
            amenities=['wifi', 'tv', 'kangaroo-friendly'],
            is_deleted=True
        )

        now = datetime.now()
        yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
        today = now.strftime('%Y-%m-%d')
        tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
        tomorrow_tomorrow = (now + timedelta(days=2)).strftime('%Y-%m-%d')

        # insert reservation with check in date in the past
        past_reservation = Reservation(
            id=1,
            accommodation_id=new_acc.id,
            guest_id=new_user.id,
            check_in_date=yesterday,
            check_out_date=today,
            status='checked_out'
        )

        # insert reservation with check in date in the past and check out date in future
        current_reservation = Reservation(
            id=4,
            accommodation_id=new_acc.id,
            guest_id=new_user.id,
            check_in_date=today,
            check_out_date=tomorrow,
            status='checked_in'
        )

        # insert reservation with check in date in the future
        future_reservation = Reservation(
            id=2,
            accommodation_id=new_acc.id,
            guest_id=new_user.id,
            check_in_date=tomorrow,
            check_out_date=tomorrow_tomorrow,
            status='booked'
        )

        cancelled_reservation = Reservation(
            id=3,
            accommodation_id=new_acc.id,
            guest_id=new_user.id,
            check_in_date=yesterday,
            check_out_date=today,
            status='cancelled'
        )

        db.session.add(new_user)
        db.session.add(other_user)
        db.session.add(new_acc)
        db.session.add(deleted_acc)
        db.session.add(past_reservation)
        db.session.add(current_reservation)
        db.session.add(future_reservation)
        db.session.add(cancelled_reservation)
        db.session.commit()

def cleanup(app):
    with app.app_context():
        db.session.query(Reservation).delete()
        db.session.query(Accommodation).delete()
        db.session.query(User).delete()
        db.session.commit()