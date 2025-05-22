"""empty message

Revision ID: bf589912f3f0
Revises: 2676eae410c5
Create Date: 2025-05-22 09:17:35.650886

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bf589912f3f0"
down_revision: Union[str, None] = "2676eae410c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Добавить новый столбец id (nullable=True)
    op.add_column("profiles", sa.Column("id", sa.BigInteger(), nullable=True))
    # 2. Скопировать значения id -> id
    op.execute("UPDATE profiles SET id = id")
    # 3. Сделать id NOT NULL
    op.alter_column("profiles", "id", nullable=False)
    # 4. Удалить старый внешний ключ
    op.drop_constraint("profiles_user_id_fkey", "profiles", type_="foreignkey")
    # 5. Создать новый внешний ключ
    op.create_foreign_key(None, "profiles", "users", ["id"], ["id"], ondelete="CASCADE")
    # 6. Удалить старый столбец
    op.drop_column("profiles", "id")


def downgrade() -> None:
    op.add_column("profiles", sa.Column("id", sa.BIGINT(), autoincrement=False, nullable=True))
    op.execute("UPDATE profiles SET id = id")
    op.alter_column("profiles", "id", nullable=False)
    op.drop_constraint(None, "profiles", type_="foreignkey")
    op.create_foreign_key(
        "profiles_user_id_fkey", "profiles", "users", ["id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("profiles", "id")
