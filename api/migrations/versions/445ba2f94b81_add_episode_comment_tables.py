"""Add episode/comment tables

Revision ID: 445ba2f94b81
Revises:
Create Date: 2023-09-02 14:08:36.352399

"""
import sqlalchemy as sa
from alembic import op

revision = "445ba2f94b81"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "episode",
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("season_no", sa.String(), nullable=True),
        sa.Column("episode_no", sa.String(), nullable=True),
        sa.Column("rating", sa.Numeric(), nullable=True),
        sa.Column("imdb_id", sa.String(), nullable=True),
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "comment",
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("episode_id", sa.Uuid(), nullable=True),
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["episode_id"],
            ["episode.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("comment")
    op.drop_table("episode")
