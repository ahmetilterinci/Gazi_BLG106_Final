"""Add avatar_url and bio columns (idempotent fix)

Revision ID: a1b2c3d4e5f6
Revises: f610512b3840
Create Date: 2026-05-30 21:25:00.000000

Bu migration IF NOT EXISTS kullanır — kolon zaten varsa hata vermez.
Render'da alembic_version f610512b3840 olarak stamp'lanmış olsa da
bu yeni revision'ı HEAD yapar ve gerçek ALTER TABLE çalıştırır.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'f610512b3840'
branch_labels = None
depends_on = None


def upgrade():
    # IF NOT EXISTS: kolon zaten eklenmişse hata vermez (idempotent)
    op.execute(
        'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(512)'
    )
    op.execute(
        'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS bio VARCHAR(256)'
    )


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('avatar_url')
