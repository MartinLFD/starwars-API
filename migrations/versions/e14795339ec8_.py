"""empty message

Revision ID: e14795339ec8
Revises: 5b409a890f4e
Create Date: 2024-10-29 17:42:52.618393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e14795339ec8'
down_revision = '5b409a890f4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_planet', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('user_primary_id')
        batch_op.drop_column('planet_primary_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_primary_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('user_primary_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
