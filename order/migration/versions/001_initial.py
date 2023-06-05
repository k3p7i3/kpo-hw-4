"""'initial'
Revision ID: 001
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'dish',
        sa.Column('dish_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(precision=2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('is_available', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('dish_id'),
    )
    op.create_table(
        'order',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column(
            'status',
            sa.Enum('waiting', 'in_process', 'cancelled', 'executed', name='orderstatus'),
            nullable=False,
        ),
        sa.Column('special_requests', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('order_id'),
    )
    op.create_table(
        'order_dish',
        sa.Column('order_dish_id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('dish_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(precision=2), nullable=False),
        sa.ForeignKeyConstraint(['dish_id'], ['dish.dish_id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
        sa.PrimaryKeyConstraint('order_dish_id'),
    )


def downgrade() -> None:
    op.drop_table('order_dish')
    op.drop_table('order')
    op.drop_table('dish')
