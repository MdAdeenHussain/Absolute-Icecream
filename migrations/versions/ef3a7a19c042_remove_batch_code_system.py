"""Remove batch-code verification tables.

Revision ID: ef3a7a19c042
Revises: d31bc28e7f44
"""
from alembic import op
import sqlalchemy as sa


revision = "ef3a7a19c042"
down_revision = "d31bc28e7f44"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("lab_reports")
    op.drop_table("batches")


def downgrade():
    op.create_table(
        "batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_code", sa.String(length=64), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("variant_id", sa.Integer(), nullable=True),
        sa.Column("manufacture_date", sa.Date(), nullable=False),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("lab_report_url", sa.String(length=500), nullable=True),
        sa.Column("lab_report_name", sa.String(length=255), nullable=True),
        sa.Column("lab_report_uploaded_at", sa.DateTime(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["variant_id"], ["product_variants.id"]),
    )
    op.create_index("ix_batches_batch_code", "batches", ["batch_code"], unique=True)
    op.create_table(
        "lab_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("report_number", sa.String(length=150), nullable=False, unique=True),
        sa.Column("laboratory_name", sa.String(length=255), nullable=False),
        sa.Column("laboratory_accreditation", sa.String(length=255), nullable=True),
        sa.Column("report_date", sa.Date(), nullable=True),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column("file_hash", sa.String(length=128), nullable=True),
        sa.Column("report_status", sa.String(length=40), nullable=False),
        sa.Column("verification_status", sa.String(length=40), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("is_demo", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="CASCADE"),
    )
