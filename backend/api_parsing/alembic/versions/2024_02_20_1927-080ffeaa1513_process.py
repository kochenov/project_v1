"""process

Revision ID: 080ffeaa1513
Revises: 7dd50087253b
Create Date: 2024-02-20 19:27:38.447374

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "080ffeaa1513"
down_revision: Union[str, None] = "7dd50087253b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "process",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("iterate", sa.Integer(), nullable=True),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("error", sa.Boolean(), nullable=True),
        sa.Column("created_ad", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("process")
    # ### end Alembic commands ###
