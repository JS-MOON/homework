"""empty message

Revision ID: 3723f82b8a3
Revises: 18e6418622eb
Create Date: 2014-08-10 02:43:20.725000

"""

# revision identifiers, used by Alembic.
revision = '3723f82b8a3'
down_revision = '18e6418622eb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('password', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'password')
    ### end Alembic commands ###
