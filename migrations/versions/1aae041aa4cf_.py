"""empty message

Revision ID: 1aae041aa4cf
Revises: 
Create Date: 2021-04-18 12:36:08.627512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aae041aa4cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###
