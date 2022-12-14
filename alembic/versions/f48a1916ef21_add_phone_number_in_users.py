"""add phone number in users

Revision ID: f48a1916ef21
Revises: 9ec59fe4c512
Create Date: 2022-12-11 02:04:32.290350

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f48a1916ef21'
down_revision = '9ec59fe4c512'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('users', sa.Column(
        'phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')

    # ### end Alembic commands ###
