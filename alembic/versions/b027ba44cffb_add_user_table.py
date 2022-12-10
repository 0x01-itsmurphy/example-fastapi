"""add user table

Revision ID: b027ba44cffb
Revises: 46a7ef6853d5
Create Date: 2022-12-11 01:05:06.524174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b027ba44cffb'
down_revision = '46a7ef6853d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
