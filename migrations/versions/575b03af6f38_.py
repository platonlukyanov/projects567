"""empty message

Revision ID: 575b03af6f38
Revises: 47ef6777fd10
Create Date: 2021-05-08 17:23:15.412867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '575b03af6f38'
down_revision = '47ef6777fd10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
