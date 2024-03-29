"""Delete has_sale

Revision ID: 05ed47850774
Revises: 033a94acd6eb
Create Date: 2022-05-03 16:16:37.812360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ed47850774'
down_revision = '033a94acd6eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'has_sale')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('has_sale', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
