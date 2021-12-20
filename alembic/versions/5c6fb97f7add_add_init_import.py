"""Add init import

Revision ID: 5c6fb97f7add
Revises: ee357e9e500e
Create Date: 2021-12-20 03:08:48.451609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c6fb97f7add'
down_revision = 'ee357e9e500e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('import_batches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('version_id', sa.Integer(), nullable=True),
    sa.Column('ran_at', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['versions.id'], name=op.f('fk_import_batches_version_id_versions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_import_batches'))
    )
    op.create_table('sdvx_apeca_imports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('apeca_id', sa.Integer(), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apeca_id'], ['sdvx_apecas.id'], name=op.f('fk_sdvx_apeca_imports_apeca_id_sdvx_apecas')),
    sa.ForeignKeyConstraint(['batch_id'], ['import_batches.id'], name=op.f('fk_sdvx_apeca_imports_batch_id_import_batches')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sdvx_apeca_imports'))
    )
    op.create_table('sdvx_difficulty_imports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('music_id', sa.Integer(), nullable=True),
    sa.Column('difficulty_name', sa.Enum('NOV', 'ADV', 'EXH', 'MXM', 'INF', 'GRV', 'HVN', 'VVD', name='difficulties'), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['import_batches.id'], name=op.f('fk_sdvx_difficulty_imports_batch_id_import_batches')),
    sa.ForeignKeyConstraint(['difficulty_name'], ['sdvx_difficulties.name'], name=op.f('fk_sdvx_difficulty_imports_difficulty_name_sdvx_difficulties')),
    sa.ForeignKeyConstraint(['music_id'], ['sdvx_difficulties.music_id'], name=op.f('fk_sdvx_difficulty_imports_music_id_sdvx_difficulties')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sdvx_difficulty_imports'))
    )
    with op.batch_alter_table('sdvx_difficulties', schema=None) as batch_op:
        batch_op.add_column(sa.Column('has_internal_jacket', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('external_jacket', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sdvx_difficulties', schema=None) as batch_op:
        batch_op.drop_column('external_jacket')
        batch_op.drop_column('has_internal_jacket')

    op.drop_table('sdvx_difficulty_imports')
    op.drop_table('sdvx_apeca_imports')
    op.drop_table('import_batches')
    # ### end Alembic commands ###
