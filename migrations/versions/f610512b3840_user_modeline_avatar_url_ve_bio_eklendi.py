"""User modeline avatar_url ve bio eklendi

Revision ID: f610512b3840
Revises: 9cc4cdb4e036
Create Date: 2026-05-30 20:52:26.522507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f610512b3840'
down_revision = '9cc4cdb4e036'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_url', sa.String(length=512), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.String(length=256), nullable=True))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('avatar_url')