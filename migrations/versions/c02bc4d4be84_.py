"""empty message

Revision ID: c02bc4d4be84
Revises: 8f23ee41f451
Create Date: 2021-05-07 16:13:46.681312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c02bc4d4be84'
down_revision = '8f23ee41f451'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project_suggest', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project_suggest', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
