"""add comments status

Revision ID: cb8706fecfd5
Revises: bde5c44da863
Create Date: 2020-03-14 21:29:29.812254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb8706fecfd5'
down_revision = 'bde5c44da863'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('markers',
        sa.Column('status', sa.Integer(), default=0, nullable=False),
    )
    op.add_column('comments',
        sa.Column('status', sa.Integer()),
    )

def downgrade():
    op.drop_column('markers', 'status')
    op.drop_column('comments', 'status')