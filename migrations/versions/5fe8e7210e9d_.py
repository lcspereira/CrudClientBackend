"""empty message

Revision ID: 5fe8e7210e9d
Revises: 
Create Date: 2023-02-05 03:34:08.722553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fe8e7210e9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=128), nullable=True),
    sa.Column('cpf', sa.String(length=11), nullable=True),
    sa.Column('data_nasc', sa.DateTime(), nullable=True),
    sa.Column('endereco', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('itens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=128), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('itens')
    op.drop_table('clientes')
    # ### end Alembic commands ###
