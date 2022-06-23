"""empty message

Revision ID: bfbdf70afd1f
Revises: 
Create Date: 2022-05-11 21:47:27.570035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfbdf70afd1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('team', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('handsome', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('mass_kg', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['driver.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car')
    op.drop_table('driver')
    # ### end Alembic commands ###