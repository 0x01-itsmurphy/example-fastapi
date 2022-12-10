"""add content column in posts table

Revision ID: 46a7ef6853d5
Revises: f9e03b31951e
Create Date: 2022-12-11 00:55:48.210223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46a7ef6853d5'
down_revision = 'f9e03b31951e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
