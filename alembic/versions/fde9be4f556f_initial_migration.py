"""Initial migration

Revision ID: fde9be4f556f
Revises: db1f53fce50e
Create Date: 2023-12-26 19:48:05.211157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fde9be4f556f'
down_revision: Union[str, None] = 'db1f53fce50e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'category')
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.drop_column('users', 'firt_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('firt_name', sa.VARCHAR(), nullable=True))
    op.drop_column('users', 'first_name')
    op.add_column('tasks', sa.Column('category', sa.VARCHAR(length=9), nullable=True))
    # ### end Alembic commands ###
