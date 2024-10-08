"""Initial migration.

Revision ID: bcc0aba22770
Revises: 1e6f96280287
Create Date: 2024-10-08 11:39:27.500208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcc0aba22770'
down_revision = '1e6f96280287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.drop_column('image_filename')

    with op.batch_alter_table('property_image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=100), nullable=False))
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property_image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('image_file')

    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.VARCHAR(length=100), nullable=True))

    # ### end Alembic commands ###
