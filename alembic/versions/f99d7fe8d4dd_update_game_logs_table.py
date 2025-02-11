"""update game logs table

Revision ID: f99d7fe8d4dd
Revises: 4fb07bae5535
Create Date: 2025-02-10 16:12:50.327148

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f99d7fe8d4dd"
down_revision: Union[str, None] = "4fb07bae5535"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "game_logs",
        "team_abbrev",
        existing_type=sa.CHAR(length=3),
        type_=sa.VARCHAR(length=3),
        existing_nullable=False,
    )
    op.alter_column(
        "game_logs",
        "opponent_abbrev",
        existing_type=sa.CHAR(length=3),
        type_=sa.VARCHAR(length=3),
        existing_nullable=False,
    )
    op.alter_column(
        "game_logs",
        "plus_minus",
        existing_type=sa.INTEGER(),
        type_=sa.Numeric(precision=5, scale=1),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "game_logs",
        "plus_minus",
        existing_type=sa.Numeric(precision=5, scale=1),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "game_logs",
        "opponent_abbrev",
        existing_type=sa.VARCHAR(length=3),
        type_=sa.CHAR(length=3),
        existing_nullable=False,
    )
    op.alter_column(
        "game_logs",
        "team_abbrev",
        existing_type=sa.VARCHAR(length=3),
        type_=sa.CHAR(length=3),
        existing_nullable=False,
    )
    op.create_table(
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("date", sa.DATE(), autoincrement=False, nullable=True),
        sa.Column("team", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("location", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("opponent", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("outcome", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("active", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("seconds_played", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("made_field_goals", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "attempted_field_goals", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "made_three_point_field_goals",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "attempted_three_point_field_goals",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("made_free_throws", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "attempted_free_throws", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "offensive_rebounds", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "defensive_rebounds", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column("assists", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("steals", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("blocks", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("turnovers", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("personal_fouls", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("points_scored", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "game_score",
            sa.NUMERIC(precision=10, scale=1),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("plus_minus", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("player_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("player_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("is_home", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("is_win", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "minutes_played",
            sa.NUMERIC(precision=10, scale=3),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
