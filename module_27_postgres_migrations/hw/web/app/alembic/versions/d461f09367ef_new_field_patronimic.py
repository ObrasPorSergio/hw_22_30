"""New field patronimic

Revision ID: d461f09367ef
Revises: 643b98bd8a3c
Create Date: 2022-05-03 16:40:16.322039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd461f09367ef'
down_revision = '033a94acd6eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('patronimic', sa.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'patronimic')
    # ### end Alembic commands ###
