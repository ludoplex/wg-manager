"""base

Revision ID: 4ac3e58519eb
Revises: 
Create Date: 2021-03-13 20:29:10.062757

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy.exc import OperationalError

revision = '4ac3e58519eb'
down_revision = None
branch_labels = None
depends_on = None


def ignore_duplicate(fn):
    try:
        fn()
    except OperationalError as e:
        pass


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.create_table('api_keys',
                        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                        sa.Column('key', sa.String(), nullable=True),
                        sa.Column('user_id', sa.Integer(), nullable=True),
                        sa.Column('created_date', sa.DateTime(), nullable=True),
                        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_api_key_user_id',
                                                onupdate='CASCADE', ondelete='CASCADE'),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('key')
                        )
    except OperationalError:
        pass

    try:
        op.drop_table('migrate_version')
    except OperationalError:
        pass

    naming_convention = {
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
    with op.batch_alter_table("peer", naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint("fk_peer_server_id_server", type_="foreignkey")

    with op.batch_alter_table('peer', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_peer_server_id_server', 'server', ['server_id'], ['id'], onupdate='CASCADE',
                                    ondelete='CASCADE')

    ignore_duplicate(lambda: op.add_column('peer', sa.Column('configuration', sa.Text(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('peer', sa.Column('keep_alive', sa.Integer(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('peer', sa.Column('read_only', sa.Integer(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('peer', sa.Column('server_id', sa.Integer(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('peer', sa.Column('shared_key', sa.Text(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('peer', sa.Column('v6_address', sa.String(), nullable=True)))

    # op.drop_constraint(None, 'peer', type_='foreignkey')
    #
    # op.drop_column('peer', 'server')

    try:
        with op.batch_alter_table('peer', schema=None) as batch_op:
            batch_op.drop_column("server")
    except KeyError:
        pass

    ignore_duplicate(lambda: op.add_column('server', sa.Column('allowed_ips', sa.String(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('configuration', sa.Text(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('dns', sa.String(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('keep_alive', sa.Integer(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('read_only', sa.Integer(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('subnet', sa.Integer(), nullable=False)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('v6_address', sa.String(), nullable=True)))
    ignore_duplicate(lambda: op.add_column('server', sa.Column('v6_subnet', sa.Integer(), nullable=False)))
    # op.create_unique_constraint(None, 'server', ['v6_address'])

    try:
        with op.batch_alter_table('server', schema=None) as batch_op:
            batch_op.drop_column("shared_key")
    except KeyError:
        pass

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('server', sa.Column('shared_key', sa.VARCHAR(), nullable=True))
    op.drop_constraint(None, 'server', type_='unique')
    op.drop_column('server', 'v6_subnet')
    op.drop_column('server', 'v6_address')
    op.drop_column('server', 'subnet')
    op.drop_column('server', 'read_only')
    op.drop_column('server', 'keep_alive')
    op.drop_column('server', 'dns')
    op.drop_column('server', 'configuration')
    op.drop_column('server', 'allowed_ips')
    op.add_column('peer', sa.Column('server', sa.INTEGER(), nullable=True))
    op.drop_constraint('fk_wg_peer_server_id', 'peer', type_='foreignkey')
    op.create_foreign_key(None, 'peer', 'server', ['server'], ['interface'])
    op.drop_column('peer', 'v6_address')
    op.drop_column('peer', 'shared_key')
    op.drop_column('peer', 'server_id')
    op.drop_column('peer', 'read_only')
    op.drop_column('peer', 'keep_alive')
    op.drop_column('peer', 'configuration')
    op.drop_table('api_keys')
    # ### end Alembic commands ###
