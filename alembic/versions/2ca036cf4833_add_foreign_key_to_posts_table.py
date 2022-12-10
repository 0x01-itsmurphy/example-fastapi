"""add foreign-key to posts table

Revision ID: 2ca036cf4833
Revises: b027ba44cffb
Create Date: 2022-12-11 01:21:05.071032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ca036cf4833'
down_revision = 'b027ba44cffb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts',
                          referent_table='users', local_cols=["owner_id"], remote_cols=["id"], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('users', 'owner_id')
    pass
