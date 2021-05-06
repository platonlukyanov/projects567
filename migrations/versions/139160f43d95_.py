"""empty message

Revision ID: 139160f43d95
Revises: 2d29d8d423fe
Create Date: 2021-05-04 19:27:37.648879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '139160f43d95'
down_revision = '2d29d8d423fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects_users',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('project_id', 'user_id')
    )
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    op.drop_table('projects_users')
    # ### end Alembic commands ###
