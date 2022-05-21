"""Add column from nikita

Revision ID: 0eee520b247e
Revises: a2d4e9837dc1
Create Date: 2022-01-16 14:30:13.545727

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0eee520b247e'
down_revision = 'a2d4e9837dc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_yoyo_migration')
    op.drop_table('test_table')
    op.drop_table('_yoyo_log')
    op.drop_table('yoyo_lock')
    op.drop_table('_yoyo_version')
    op.add_column('user', sa.Column('surname', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('col_from_nikita_dev', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'col_from_nikita_dev')
    op.drop_column('user', 'surname')
    op.create_table('_yoyo_version',
    sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('installed_at_utc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('version', name='_yoyo_version_pkey')
    )
    op.create_table('yoyo_lock',
    sa.Column('locked', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=False),
    sa.Column('ctime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('pid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('locked', name='yoyo_lock_pkey')
    )
    op.create_table('_yoyo_log',
    sa.Column('id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('migration_hash', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('migration_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('operation', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('hostname', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('comment', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at_utc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='_yoyo_log_pkey')
    )
    op.create_table('test_table',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='test_table_pkey')
    )
    op.create_table('_yoyo_migration',
    sa.Column('migration_hash', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('migration_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('applied_at_utc', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('migration_hash', name='_yoyo_migration_pkey')
    )
    # ### end Alembic commands ###
