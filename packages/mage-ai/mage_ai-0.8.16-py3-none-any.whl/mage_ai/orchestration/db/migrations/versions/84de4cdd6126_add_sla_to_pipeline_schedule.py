"""Add sla to pipeline schedule

Revision ID: 84de4cdd6126
Revises: b01be687e537
Create Date: 2022-10-21 11:13:27.570829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84de4cdd6126'
down_revision = 'b01be687e537'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pipeline_schedule', sa.Column('sla', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pipeline_schedule', 'sla')
    # ### end Alembic commands ###
