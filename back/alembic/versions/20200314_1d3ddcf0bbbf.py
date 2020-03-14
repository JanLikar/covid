"""add_comments

Revision ID: 1d3ddcf0bbbf
Revises: 370c02893a04
Create Date: 2020-03-14 02:05:49.380651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d3ddcf0bbbf'
down_revision = '370c02893a04'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text()),
    sa.Column('email', sa.Text()),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('commented_date', sa.Date(), nullable=False),
    sa.Column('marker_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comments'))
    )

def downgrade():
    op.drop_table('comments')
