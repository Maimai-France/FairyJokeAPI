"""game platform release etc

Revision ID: c1a377997522
Revises: 762487108bd9
Create Date: 2021-04-14 23:16:28.659304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1a377997522'
down_revision = '762487108bd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_game')),
    sa.UniqueConstraint('key', name=op.f('uq_game_key'))
    )
    op.create_table('game_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_game_group'))
    )
    op.create_table('platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['platform.id'], name=op.f('fk_platform_parent_id_platform')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_platform'))
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_region')),
    sa.UniqueConstraint('key', name=op.f('uq_region_key'))
    )
    op.create_table('release_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_release_type'))
    )
    op.create_table('version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_version_game_id_game')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_version'))
    )
    op.create_table('release',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.Column('release_type_id', sa.Integer(), nullable=True),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['game_group.id'], name=op.f('fk_release_group_id_game_group')),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], name=op.f('fk_release_platform_id_platform')),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], name=op.f('fk_release_region_id_region')),
    sa.ForeignKeyConstraint(['release_type_id'], ['release_type.id'], name=op.f('fk_release_release_type_id_release_type')),
    sa.ForeignKeyConstraint(['version_id'], ['version.id'], name=op.f('fk_release_version_id_version')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_release'))
    )
    with op.batch_alter_table('song', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_bpm', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('min_bpm', sa.Integer(), nullable=True))
        batch_op.drop_column('low_bpm')
        batch_op.drop_column('high_bpm')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('song', schema=None) as batch_op:
        batch_op.add_column(sa.Column('high_bpm', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('low_bpm', sa.INTEGER(), nullable=True))
        batch_op.drop_column('min_bpm')
        batch_op.drop_column('max_bpm')

    op.drop_table('release')
    op.drop_table('version')
    op.drop_table('release_type')
    op.drop_table('region')
    op.drop_table('platform')
    op.drop_table('game_group')
    op.drop_table('game')
    # ### end Alembic commands ###