"""initial tables

Revision ID: 20250724_abcde
Revises: 
Create Date: 2025-07-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import JSON

# revision identifiers, used by Alembic.
revision = '20250724_abcde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Seller Table
    op.create_table(
        'sellers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('official_name', sa.String(100)),
        sa.Column('kyc', sa.String(255)),
        sa.Column('rating', sa.Float, default=0.0),
        sa.Column('since_active', sa.String(50)),
        sa.Column('address', sa.String(255)),
    )

    # Product Table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_name', sa.String(100), nullable=False),
        sa.Column('product_code', sa.String(50), unique=True, nullable=False),
        sa.Column('product_summary', sa.String(255)),
        sa.Column('product_description', sa.Text),
        sa.Column('product_details', JSON),

        sa.Column('product_type', sa.String(50), nullable=False),
        sa.Column('product_category', sa.String(50), nullable=False),
        sa.Column('product_sub_category', sa.String(50)),
        sa.Column('brand', sa.String(50), nullable=False),
        sa.Column('gender', sa.String(20)),
        sa.Column('age_group', sa.String(20)),

        sa.Column('sizes_available', JSON),
        sa.Column('colors_available', JSON),

        sa.Column('material', sa.String(50)),
        sa.Column('pattern', sa.String(50)),
        sa.Column('fit_type', sa.String(50)),
        sa.Column('occasion', sa.String(50)),
        sa.Column('fabric_care', sa.String(100)),

        sa.Column('mrp', sa.Float, nullable=False),
        sa.Column('selling_price', sa.Float, nullable=False),
        sa.Column('discount', sa.Float, default=0.0),
        sa.Column('offers', JSON),

        sa.Column('stock_quantity', sa.Integer, nullable=False),
        sa.Column('low_stock_threshold', sa.Integer, default=5),

        sa.Column('main_image_url', sa.String(255)),
        sa.Column('additional_image_urls', JSON),
        sa.Column('video_url', sa.String(255)),

        sa.Column('delivery_charge', sa.Float, default=0.0),
        sa.Column('cod_available', sa.Boolean, default=True),
        sa.Column('dispatch_time', sa.Integer, default=2),
        sa.Column('max_delivery_days', sa.Integer, default=5),

        sa.Column('returnable', sa.Boolean, default=True),
        sa.Column('return_days', sa.Integer, default=15),
        sa.Column('exchange_available', sa.Boolean, default=True),
        sa.Column('warranty', sa.String(100)),

        sa.Column('meta_title', sa.String(255)),
        sa.Column('meta_description', sa.String(255)),
        sa.Column('search_tags', JSON),

        sa.Column('hsn_code', sa.String(20)),
        sa.Column('gst_percentage', sa.Float),
        sa.Column('country_of_origin', sa.String(50)),

        sa.Column('seller_id', sa.Integer, sa.ForeignKey('sellers.id', ondelete="CASCADE"))
    )

    # Order Table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('buyer_id', sa.Integer),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id', ondelete="CASCADE")),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('order_status', sa.String(50), default="Pending"),
        sa.Column('payment_status', sa.String(50), default="Unpaid"),
        sa.Column('order_date', sa.DateTime, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('sellers')
