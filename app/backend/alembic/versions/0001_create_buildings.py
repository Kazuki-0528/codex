"""create core tables

Revision ID: 0001_create_buildings
Revises:
Create Date: 2026-01-01
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_buildings"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=120), nullable=False),
        sa.Column("gross_area_m2", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("buildings.id"), nullable=False),
        sa.Column("ifc_id", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("usage_type", sa.String(length=30), nullable=False, server_default="office"),
        sa.Column("area_m2", sa.Float(), nullable=False, server_default="30"),
        sa.Column("operating_hours_per_day", sa.Float(), nullable=False, server_default="8"),
    )

    op.create_table(
        "envelope_elements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("buildings.id"), nullable=False),
        sa.Column("ifc_id", sa.String(length=120), nullable=False),
        sa.Column("element_type", sa.String(length=60), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("envelope_elements")
    op.drop_table("rooms")
    op.drop_table("buildings")
