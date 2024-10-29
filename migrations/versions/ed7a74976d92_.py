"""empty message

Revision ID: ed7a74976d92
Revises: e14795339ec8
Create Date: 2024-10-29 17:48:13.712368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed7a74976d92'
down_revision = 'e14795339ec8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_character', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('user_primary_id')
        batch_op.drop_column('character_primary_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('character_primary_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('user_primary_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
