"""add activity_start_time and activity_end_time to Post table'


Revision ID: 72695a013b
Revises: 1a559f9fbc0
Create Date: 2016-07-22 16:44:34.740331

"""

# revision identifiers, used by Alembic.
revision = '72695a013b'
down_revision = '1a559f9fbc0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('activity_end_time', sa.TIMESTAMP(), nullable=True))
    op.add_column('posts', sa.Column('activity_start_time', sa.TIMESTAMP(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'activity_start_time')
    op.drop_column('posts', 'activity_end_time')
    ### end Alembic commands ###
