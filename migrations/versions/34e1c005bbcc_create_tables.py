"""create tables

Revision ID: 34e1c005bbcc
Revises: 
Create Date: 2019-06-14 18:57:04.619702

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '34e1c005bbcc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('is_host', sa.Boolean(), nullable=True),
    sa.Column('token', sa.Text(), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('accommodation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('num_guests', sa.Integer(), nullable=False),
    sa.Column('num_bedrooms', sa.Integer(), nullable=False),
    sa.Column('num_beds', sa.Integer(), nullable=False),
    sa.Column('num_bathrooms', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('suburb', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('state', sa.Text(), nullable=True),
    sa.Column('country', sa.Text(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('property_type', sa.Text(), nullable=False),
    sa.Column('amenities', postgresql.ARRAY(sa.Text()), nullable=True),
    sa.Column('image_urls', postgresql.ARRAY(sa.Text()), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('num_reviews', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accommodation_id', sa.Integer(), nullable=False),
    sa.Column('guest_id', sa.Integer(), nullable=False),
    sa.Column('check_in_date', sa.Date(), nullable=False),
    sa.Column('check_out_date', sa.Date(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['accommodation_id'], ['accommodation.id'], ),
    sa.ForeignKeyConstraint(['guest_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accommodation_id', sa.Integer(), nullable=False),
    sa.Column('guest_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('review', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['accommodation_id'], ['accommodation.id'], ),
    sa.ForeignKeyConstraint(['guest_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('reservation')
    op.drop_table('accommodation')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###